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
    .distanceMin(0)
    .distanceMax(100);

var initForces = function(chart){
    const [R, Cx, Cy] = [chart.radius, chart.center.x, chart.center.y];

    let _dateToR = function(date_str){
        if (date_str === null)
            return null;
        let scaling = chart.dateUtils.converter(date_str);
        return R * scaling;
    }

    let _distance = function(d){
        let source_r = _dateToR(d.source.birth_date),
            target_r = _dateToR(d.target.birth_date),
            delta_r = Math.abs(source_r - target_r);
        return (source_r === null || target_r === null) ? 30 : delta_r;
    }

    var simulation = d3.forceSimulation()
        .force("radial", d3.forceRadial(d => _dateToR(d.birth_date), Cx, Cy)
            .strength(d => d.birth_date === null ? 0 : 1))
        .force("link", d3.forceLink().id(d => d.id).distance(_distance).strength(1))
        .force("repelForce", repelForce);

    return simulation;
}


export default initForces;