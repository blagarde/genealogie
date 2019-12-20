"use strict";

import Timeline from "/static/arbre/js/timeline.js";

var svg = d3.select("svg");


var timeline = Timeline(svg);
timeline.init("/get_json/1/2");
