"use strict";

  const average = function(arr){
    // Returns the average of an array of numeric values, ignoring any `undefined`.
    let filtered = arr.filter(x => (x !== undefined));
    return filtered.reduce( ( p, c ) => p + c, 0 ) / filtered.length;
  }

// Set the repel force - may need to be tweaked for multiple data
// the lower the strength the more they will repel away from each other
// the larger the distance, the more apart they will be.
var repelForce = d3.forceManyBody()
    .strength(-200)
    .distanceMin(85)
    .distanceMax(500);


var initForces = function(chart){
    const [R, Cx, Cy] = [chart.radius, chart.center.x, chart.center.y];

    let _dateToR = function(date_str){
        let scaling = chart.dateUtils.converter(date_str);
        return R * scaling;
    }

    let _getRstrength = function(d){
        let polar_coords = chart.converter.toPolar(d.x, d.y),
            delta_r = (polar_coords.r - _dateToR(d.birth_date)) / R,
            strength = Math.pow(Math.abs(delta_r), .5);
        return (d.birth_date === null)? 0: strength;
    }

    var simulation = d3.forceSimulation()
        .force("radial", d3.forceRadial(d => _dateToR(d.birth_date), Cx, Cy).strength(_getRstrength))
        .force("link", d3.forceLink().id(d => d.id).strength(0.05))
        .force("repelForce", repelForce);

    return simulation;
}


export default initForces;