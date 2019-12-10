"use strict";

var svg = d3.select("svg"),
    x_padding = 100,
    width = window.innerWidth,
    height = window.innerHeight;


d3.json("/get_json/1/2", function(error, graph) {
    if (error) throw error;

    const birth_dates = graph.nodes.map((p) => p.birth_date).filter(Boolean).map(p => new Date(p)),
          earliest_date = new Date(Math.min(...birth_dates)),
          latest_date = new Date(Math.max(...birth_dates)),
          range = (latest_date - earliest_date);

//set the repel force - may need to be tweaked for multiple data
//the lower the strength the more they will repel away from each other
//the larger the distance, the more apart they will be
var repelForce = d3.forceManyBody()
    .strength(-500)
    .distanceMin(85)
    .distanceMax(100);


var get_Xanchor = function (d){
    let birth_date = new Date(d.birth_date);
    let x_anchor = (width - x_padding) * (birth_date - earliest_date) / range + x_padding / 2;
    return x_anchor;
}

var get_Xstrength = function(d){
    let relative_x = (d.x  + x_padding / 2 - get_Xanchor(d)) / (width - x_padding);
    let strength = Math.pow(Math.abs(relative_x), .5);
    return (d.birth_date === null)? 0: strength;
}

var simulation = d3.forceSimulation()
    .force("xAxis", d3.forceX(get_Xanchor).strength(get_Xstrength))
    .force("yAxis", d3.forceY(height / 2)  // Center vertically.
        .strength(d =>  ((height / 2) - d.y) / (100 * height))
      )
    .force("link", d3.forceLink().id(d => d.id).strength(0.2))
    .force("repelForce", repelForce);

  
var link = svg.append("g")
    .attr("class", "links")
    .selectAll("path")
    .data(graph.links)
    .enter().append("path");

var nodes = svg.append("g").attr("class", "nodes")
    .selectAll("g.node")
    .data(graph.nodes)
    .enter()
    .append("g").attr("class", "node")
        .call(d3.drag()
              .on("start", dragstarted)
              .on("drag", dragged)
              .on("end", dragended));

nodes.append("circle")
    .attr("r", function(d){
        return (d.type === "couple") ?  0 : 3;
      });

nodes.append("text")
    .attr("dx", 0)
    .attr("dy", 12)
    .attr("text-anchor","middle")
    .text(function(d) { return d.first_name; });


simulation
  .nodes(graph.nodes)
  .on("tick", tick);

simulation.force("link")
  .links(graph.links);


var getYanchor = function(d){
  const average = function(arr){
    let filtered = arr.filter(x => (x !== undefined));
    return filtered.reduce( ( p, c ) => p + c, 0 ) / filtered.length;
  }

  let y_arr = link.data().map(function(l){
    if (l.target.id === d.id)
      return l.source.y;
    if (l.source.id === d.id)
      return l.target.y;
  });
  // y_arr.push(d.y);
  return average(y_arr);
}
var getYstrength = function(d){
  return (getYanchor(d) === d.y) ? 0: .5;
};


function tick() {

  simulation.force("yAffinity", d3.forceY(getYanchor).strength(getYstrength));

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

  nodes.attr("transform", function(d){
        return "translate(" + d.x + "," + d.y + ")"
    });

}

function dragstarted(d) {
  if (!d3.event.active) simulation.alphaTarget(1).restart();
  d.fx = d.x;
  d.fy = d.y;
}

function dragged(d) {
  d.fx = d3.event.x;
  d.fy = d3.event.y;
}

function dragended(d) {
  if (!d3.event.active) simulation.alphaTarget(0);
  d.fx = null;
  d.fy = null;
}

});