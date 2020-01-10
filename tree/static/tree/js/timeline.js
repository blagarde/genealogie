"use strict";

import initForces from "/static/tree/js/forces.js";
import Voronoi from "/static/tree/js/voronoi.js";


// Using the pattern described at https://bost.ocks.org/mike/chart/
var Chart = function(svg){

    var self = function() {
    }

    self.x_margin = 100,
    self.width = window.innerWidth - 2 * self.x_margin,
    self.height = window.innerHeight,
    self.voronoi = Voronoi(self.width, self.height, "g.nodes");

    self.init = function(url) {
        d3.json(url, function(error, data) {
            if (error) throw error;
            self.data = data;
            self.simulation = initForces(self);
            self._initSVG();
            self._initListeners();
            // FIXME: Figure out how to move this back into forces.js:
            self.simulation.force("link").links(data.links);
        });
        return self;
    }

    self._initSVG = function(){
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

    self._initListeners = function(){
        self.voronoi.initListeners()
        self.simulation.nodes(self.data.nodes).on("tick", tick);
    }

    function tick() {
        self.simulation.updateForces();
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

    return self;
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


export default Chart;