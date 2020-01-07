"use strict";

import initForces from "/static/tree/js/radial_forces.js";
import getPolarConverter from "/static/tree/js/polar_utils.js";
import Voronoi from "/static/tree/js/voronoi.js";
import getDateUtils from "/static/tree/js/date_utils.js";


var Chart = function(svg){

    var self = function() {
    }
    const margin = 40;
    self.width = window.innerWidth,
    self.height = window.innerHeight,
    self.radius = Math.min(self.height, self.width) / 2 - margin,
    self.center = {x: self.width / 2, y: self.height / 2},
    self.converter = getPolarConverter(self.center.x, self.center.y),
    self.voronoi = Voronoi(self.width, self.height, "g.nodes");

    self.init = function(url) {
        d3.json(url, function(error, data) {
            if (error) throw error;
            self.data = data;
            self.dateUtils = getDateUtils(data, url.startsWith("/get_ancestors/"));
            self.simulation = initForces(self);
            self._initSVG();
            self._initListeners();
            // FIXME: Figure out how to move this back into radial_forces.js:
            self.simulation.force("link").links(data.links);
        });
        return self;
    }

    self._initSVG = function(){
        self._drawCircles();
        self.link = svg.append("g")
            .attr("class", "links")
            .selectAll("path")
            .data(self.data.links)
            .enter().append("path")
            .attr("class", "link");

        self.node_container = svg.append("g").attr("class", "nodes");

        self.nodes = self.node_container.selectAll("g.node")
            .data(self.data.nodes)
            .enter()
            .append("g").attr("class", "node");


        self.voronoi.initSVG(self);

        self.nodes.append("circle")
            .attr("r", (d => d.type === "couple" ?  0 : 3));

        self.nodes.append("text")
            .attr("dx", 0)
            .attr("dy", 12)
            .attr("text-anchor","middle")
            .text(function(d) { return d.first_name; });

    }

    self._drawCircles = function(){
        // Draw concentric circles, one every 25 years.
        const interval_years = 25;
        var ticks_arr = self.dateUtils.getTicks(interval_years);
        ticks_arr.forEach(function(i){
            let r = i.value * self.radius;
            if (r<=0)
                return;
            svg.append("circle")
                .attr("class", "year")
                .attr("r", r)
                .attr("cx", self.center.x)
                .attr("cy", self.center.y);
            svg.append("text")
                .attr("class", "year")
                .attr("x", self.center.x - r)
                .attr("y", self.height / 2)
                .text(i.year);
        });
    }

    self._initListeners = function(){
        self.voronoi.initListeners();
        self.simulation.nodes(self.data.nodes).on("tick", tick);
    }

    function tick() {
        _updateLinks(self.link);
        _updateNodes(self.nodes);
        self.voronoi.redraw();
    }

    self.dragstarted = function(d) {
        if (!d3.event.active) self.simulation.alphaTarget(1).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    self.dragged = function(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
    }

    self.dragended = function(d) {
        if (!d3.event.active) self.simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }
    
    var _getControlPoints = function(x1, y1, x2, y2){
        // Return the 2 points that are on the same respective radiuses as the two
        // points provided and on the circle that is equidistant from them.
        let X1 = self.converter.toPolar(x1, y1),
            X2 = self.converter.toPolar(x2, y2),
            R = (X1.r + X2.r) / 2;
            // If the link source is too close to the center (<50px), draw a straight
            // line by placing its control point on the target's radius.
            let P1 = X1.r < 50 ? self.converter.toCartesian(R, X2.radians): self.converter.toCartesian(R, X1.radians);
        return [P1, self.converter.toCartesian(R, X2.radians)];
    }

    var _updateLinks = function(link){
        link.attr("d", function(d) {
            let x1 = d.source.x, y1 = d.source.y,
                x2 = d.target.x, y2 = d.target.y;

            let [P1, P2] = _getControlPoints(x1, y1, x2, y2);
            return `M ${x1} ${y1} C ${P1.x} ${P1.y} ${P2.x} ${P2.y} ${x2} ${y2}`;
        });
    }

    return self;
}

var _updateNodes = function(nodes){
    nodes.attr("transform", function(d){
        return "translate(" + d.x + "," + d.y + ")"
    });
}


export default Chart;