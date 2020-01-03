"use strict";

import initForces from "/static/tree/js/forces.js";
import Voronoi from "/static/tree/js/voronoi.js";


// Using the pattern described at https://bost.ocks.org/mike/chart/
var Timeline = function(svg){

    var my = function() {
    }

    my.x_margin = 100,
    my.width = window.innerWidth - 2 * my.x_margin,
    my.height = window.innerHeight,
    my.voronoi = Voronoi(my.width, my.height, "g.nodes");

    my.init = function(url) {
        d3.json(url, function(error, data) {
            if (error) throw error;
            my.data = data;
            my.simulation = initForces(my);
            my._initSVG();
            my._initListeners();
            // FIXME: Figure out how to move this back into forces.js:
            my.simulation.force("link").links(data.links);
        });
        return my;
    }

    my._initSVG = function(){
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

    my._initListeners = function(){
        my.voronoi.initListeners()
        my.simulation.nodes(my.data.nodes).on("tick", tick);
    }

    function tick() {
        my.simulation.updateForces();
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

    return my;
}


var _updateNodes = function(nodes){
    nodes.attr("transform", function(d){
        return "translate(" + d.x + "," + d.y + ")"
    });
}

var _updateLinks = function(link){
    link.attr("d", function(d) {
        let x1 = d.source.x, y1 = d.source.y,
            x2 = d.target.x, y2 = d.target.y;
        if (d.type === "child") {
            let c1x = (d.source.x * 3 + d.target.x) / 4,
                c2x = (d.source.x + d.target.x * 3) / 4,
                c1y = d.source.y, c2y = d.target.y;
            return `M ${x1} ${y1} C ${c1x} ${c1y} ${c2x} ${c2y} ${x2} ${y2}`;
        }
        if (d.type === "couple") {
            let c1x = (d.source.x + d.target.x) / 2,
                c1y = d.source.y,
                c2x = d.target.x,
                c2y = (d.source.y + d.target.y) / 2;
            return `M ${x1} ${y1} C ${c1x} ${c1y} ${c2x} ${c2y} ${x2} ${y2}`;
        }
    });
}


export default Timeline;