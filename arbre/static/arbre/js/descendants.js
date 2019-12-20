"use strict";

import RadialTree from "/static/arbre/js/radial_tree.js";

var svg = d3.select("svg");


var tree = RadialTree(svg);
tree.init("/get_descendants/4/4");
