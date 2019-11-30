"use strict";

var svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height");


d3.json("/static/arbre/data/mini_tree.json", function(error, graph) {
    if (error) throw error;

    const birth_dates = graph.nodes.map((p) => new Date(p.birth_date)),
          earliest_date = new Date(Math.min(...birth_dates)),
          latest_date = new Date(Math.max(...birth_dates)),
          range = (latest_date - earliest_date);

//set the repel force - may need to be tweaked for multiple data
//the lower the strength the more they will repel away from each other
//the larger the distance, the more apart they will be
var repelForce = d3.forceManyBody()
    .strength(-3000)
    .distanceMin(85)
    .distanceMax(450);


var simulation = d3.forceSimulation()
    .force("xAxis",
        d3.forceX(0).strength(function(d){
            let birth_date = new Date(d.birth_date);
            return (birth_date - earliest_date) / range;
        })
    )
    .force("xAxis",
        d3.forceX(width).strength(function(d){
            let birth_date = new Date(d.birth_date);
            return (latest_date - birth_date) / range;
        })
    )
    .force("link", d3.forceLink().id(function(d) { return d.id; }))
    .force("repelForce", repelForce)
    .force("center", d3.forceCenter(width / 2, height / 2));

  
var link = svg.append("g")
    .attr("class", "links")
    .selectAll("line")
    .data(graph.links)
    .enter().append("line");

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
    .attr("r", 5);

nodes.append("text")
        .style("fill", "black")
        .attr("dx", 0)
        .attr("dy", 50)
        .attr("text-anchor","middle")
        .text(function(d) { return d.first_name; });


simulation
  .nodes(graph.nodes)
  .on("tick", tick);

simulation.force("link")
  .links(graph.links);

function tick() {
  link
    .attr("x1", function(d) { return d.source.x; })
    .attr("y1", function(d) { return d.source.y; })
    .attr("x2", function(d) { return d.target.x; })
    .attr("y2", function(d) { return d.target.y; });

  nodes.attr("transform", function(d){
        return "translate(" + d.x + "," + d.y + ")"
    });
}

function dragstarted(d) {
  if (!d3.event.active) simulation.alphaTarget(0.3).restart();
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