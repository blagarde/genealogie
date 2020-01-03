// https://bl.ocks.org/d3indepth/ee5a4b110b9841cc55dbba0716343143
// create a Voronoi diagram based on the data and the scales

import tooltip from "/static/tree/js/tooltip.js";


function Voronoi(width, height, container_selector){
    var self = function(){
    }
    self.hovered = null;

    var voronoi = d3.voronoi()
        .x(d => d.x)
        .y(d => d.y)
        .extent([[0, 0], [width, height]]);


    self.initSVG = function(chart){
        self.data = chart.data;
        self.chart = chart;
        self.container = d3.select(container_selector);
        self.container.append("circle").attr("r", 7).attr("class", "halo");
        self.container.selectAll("path")
            .data(self.data.nodes)
            .enter()
            .append('path')
            .attr('class', 'voronoi');
    }

    self.initListeners = function(){
        self.container.selectAll(".voronoi").call(d3.drag()
            .on("start", self.chart.dragstarted)
            .on("drag", self.chart.dragged)
            .on("end", self.chart.dragended))
            .on('mouseover', function(d) {
                self.hovered = d;
                self._updateHalo();
                tooltip.draw(d);
            })
            .on('mouseout', function(d) {
                self.hovered = null;
                self._updateHalo();
                tooltip.mouseout();
            })
            .on('mousemove', tooltip.mousemove);
    }

    self.redraw = function() {
        var polygons = voronoi(self.data.nodes).polygons();

        // merge polygons into points
        self.data.nodes = self.data.nodes.map(function(d, i) {
            d.polygon = polygons[i];
            return d;
        });
        self.container.selectAll("path")
            .attr('d', d => _polygon(d.polygon));
        self._updateHalo();
    }

    self._updateHalo = function() {

        d3.select('.halo')
            .style('opacity', self.hovered === null ? 0 : 1);

        if(self.hovered === null)
            return;

        d3.select('.halo')
            .attr('cx', self.hovered.x)
            .attr('cy', self.hovered.y);
    }

    return self;
}

function _polygon(d) {
  // Build the SVG parameter of a polygon array like [[x1, y1], ...].
  if (d !== undefined)
    return 'M' + d.join('L') + 'Z';
  // The voronoi().polygons() function returns a sparse array for
  // any polygons that are outside of the canvas (I think).
  // For `undefined` values, we return a valid empty path.
  return 'M0,0';
}


export default Voronoi;