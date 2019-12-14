"use strict";

import Timeline from "/static/arbre/js/timeline.js";

var svg = d3.select("svg"),
    x_padding = 100,
    width = window.innerWidth,
    height = window.innerHeight;


var timeline = Timeline(svg);
timeline.init("/get_json/1/2");
