"use strict";

import initForces from "/static/tree/js/radial_forces.js";
import getPolarConverter from "/static/tree/js/polar_utils.js";
import Voronoi from "/static/tree/js/voronoi.js";
import getDateUtils from "/static/tree/js/date_utils.js";


var RadialTree = function(svg){

    var my = function() {
    }
    const margin = 40;
    my.width = window.innerWidth,
    my.height = window.innerHeight,
    my.radius = Math.min(my.height, my.width) / 2 - margin,
    my.center = {x: my.width / 2, y: my.height / 2},
    my.converter = getPolarConverter(my.center.x, my.center.y),
    my.voronoi = Voronoi(my.width, my.height, "g.nodes");

    my.init = function(url) {
        d3.json(url, function(error, data) {
            if (error) throw error;
            my.data = data;
            my.dateUtils = getDateUtils(data, url.startsWith("/get_ancestors/"));
            my.simulation = initForces(my);
            my._initSVG();
            my._initListeners();
            // FIXME: Figure out how to move this back into radial_forces.js:
            my.simulation.force("link").links(data.links);
        });
        return my;
    }

    my._initSVG = function(){
        my._drawCircles();
        my.link = svg.append("g")
            .attr("class", "links")
            .selectAll("path")
            .data(my.data.links)
            .enter().append("path")
            .attr("class", "link");

        my.node_container = svg.append("g").attr("class", "nodes");

        my.nodes = my.node_container.selectAll("g.node")
            .data(my.data.nodes)
            .enter()
            .append("g").attr("class", "node");


        my.voronoi.initSVG(my);

        my.nodes.append("circle")
            .attr("r", (d => d.type === "couple" ?  0 : 3));

        my.nodes.append("text")
            .attr("dx", 0)
            .attr("dy", 12)
            .attr("text-anchor","middle")
            .text(function(d) { return d.first_name; });

    }

    my._drawCircles = function(){
        // Draw concentric circles, one every 25 years.
        const interval_years = 25;
        var ticks_arr = my.dateUtils.getTicks(interval_years);
        ticks_arr.forEach(function(i){
            let r = i.value * my.radius;
            if (r<=0)
                return;
            svg.append("circle")
                .attr("class", "year")
                .attr("r", r)
                .attr("cx", my.center.x)
                .attr("cy", my.center.y);
            svg.append("text")
                .attr("class", "year")
                .attr("x", my.center.x - r)
                .attr("y", my.height / 2)
                .text(i.year);
        });
    }

    my._initListeners = function(){
        my.voronoi.initListeners();
        my.simulation.nodes(my.data.nodes).on("tick", tick);
    }

    function tick() {
        _updateLinks(my.link);
        _updateNodes(my.nodes);
        my.voronoi.redraw();
    }

    my.dragstarted = function(d) {
        if (!d3.event.active) my.simulation.alphaTarget(1).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    my.dragged = function(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
    }

    my.dragended = function(d) {
        if (!d3.event.active) my.simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }
    
    var _getControlPoints = function(x1, y1, x2, y2){
        // Return the 2 points that are on the same respective radiuses as the two
        // points provided and on the circle that is equidistant from them.
        let X1 = my.converter.toPolar(x1, y1),
            X2 = my.converter.toPolar(x2, y2),
            R = (X1.r + X2.r) / 2;
            // If the link source is too close to the center (<50px), draw a straight
            // line by placing its control point on the target's radius.
            let P1 = X1.r < 50 ? my.converter.toCartesian(R, X2.radians): my.converter.toCartesian(R, X1.radians);
        return [P1, my.converter.toCartesian(R, X2.radians)];
    }

    var _updateLinks = function(link){
        link.attr("d", function(d) {
            let x1 = d.source.x, y1 = d.source.y,
                x2 = d.target.x, y2 = d.target.y;

            let [P1, P2] = _getControlPoints(x1, y1, x2, y2);
            return `M ${x1} ${y1} C ${P1.x} ${P1.y} ${P2.x} ${P2.y} ${x2} ${y2}`;
        });
    }

    return my;
}

var _updateNodes = function(nodes){
    nodes.attr("transform", function(d){
        return "translate(" + d.x + "," + d.y + ")"
    });
}


export default RadialTree;