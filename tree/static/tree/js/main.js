"use strict";

import Timeline from "/static/tree/js/timeline.js";

var svg = d3.select("svg");


var timeline = Timeline(svg);
timeline.init("/get_json/1/4");
