"use strict";

  const average = function(arr){
    // Returns the average of an array of numeric values, ignoring any `undefined`.
    let filtered = arr.filter(x => (x !== undefined));
    return filtered.reduce( ( p, c ) => p + c, 0 ) / filtered.length;
  }

//set the repel force - may need to be tweaked for multiple data
//the lower the strength the more they will repel away from each other
//the larger the distance, the more apart they will be
var repelForce = d3.forceManyBody()
    .strength(-200)
    .distanceMin(85)
    .distanceMax(100);


var initForces = function(timeline){
    const [w, h, x_margin] = [timeline.width, timeline.height, timeline.x_margin],
        birth_dates = timeline.data.nodes.map((p) => p.birth_date)
                                            .filter(Boolean)
                                            .map(p => new Date(p)),
        earliest_date = new Date(Math.min(...birth_dates)),
        latest_date = new Date(Math.max(...birth_dates)),
        range = (latest_date - earliest_date);

    let _dateToX = function(date_str){
        let date = new Date(date_str);
        return w * (date - earliest_date) / range + x_margin;
    }

    let _getXstrength = function(d){
        let relative_x = (d.x - _dateToX(d.birth_date)) / w;
        let strength = Math.pow(Math.abs(relative_x), .5);
        return (d.birth_date === null)? 0: strength;
    }


    var _getYanchor = function(d){
      let y_arr = timeline.link.data().map(function(l){
        if (l.target.id === d.id)
          return l.source.y;
        if (l.source.id === d.id)
          return l.target.y;
      });
      // y_arr.push(d.y);
      return average(y_arr);
    }
    var _getYstrength = function(d){
      return (_getYanchor(d) === d.y) ? 0: .5;
    };


    var simulation = d3.forceSimulation()
        .force("xAxis", d3.forceX(d => _dateToX(d.birth_date)).strength(_getXstrength))
        .force("yAxis", d3.forceY(h / 2)  // Center vertically.
            .strength(d =>  ((h / 2) - d.y) / (100 * h))
          )
        .force("link", d3.forceLink().id(d => d.id).strength(0.2))
        .force("repelForce", repelForce);

    simulation.updateForces = function(){
        // Callback intended to be used inside `tick()`.
        simulation.force("yAffinity", d3.forceY(_getYanchor).strength(_getYstrength));
    }
    return simulation;
}


export default initForces;