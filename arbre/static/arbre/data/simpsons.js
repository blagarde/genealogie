"use strict";

// Each person needs a node
// AND each family needs a node

var nodes = [

  // Homer and Marge's Family
  {"type":'family',"id":'f1',"name":'', "image":""},
  {"type":'person',"id":'p1',"name":'Marge Simpson',"age": 39, "profession": "housewife","sex":'f',"image": "/static/arbre/img/marge.png"},
  {"type":'person',"id":'p2',"name":'Homer Simpson',"age": 36, "profession": "safety inspector","sex":'m',"image": "/static/arbre/img/homer.png"},
  {"type":'person',"id":'p3',"name":'Bart Simpson',"age": 10 ,"sex":'m',"image": "/static/arbre/img/bart.png"},
  {"type":'person',"id":'p4',"name":'Lisa Simpson',"age": 8 ,"sex":'f',"image": "/static/arbre/img/lisa.png"},
  {"type":'person',"id":'p5',"name":'Maggie Simpson',"age": 1,"sex":'f',"image": "/static/arbre/img/maggie.png"},
  {"type":'person',"id":'p6',"name":"Santa's Little Helper","age": 2,"sex":'m',"image": "/static/arbre/img/santa.png"},

  // Abraham and Mona's Family
  {"type":'family',"id":'f3',"name":'', "image":""},
  {"type":'person',"id":'p8',"name":'Abraham Simpson',"age": 83, "profession": "retired farmer","sex":'m',"image": "/static/arbre/img/grampa.png"},
  {"type":'person',"id":'p9',"name":'Mona Simpson',"age": 81, "profession": "activist","sex":'f',"image": "/static/arbre/img/mona.png"},
  {"type":'person',"id":'p7',"name":'Herb Simpson',"age": 44, "profession": "car salesman","sex":'m',"image": "/static/arbre/img/herb.png"},

  // Bouviers: Clancy and Jacqueline's Family
  {"type":'family',"id":'f4',"name":'', "image":""},
  {"type":'person',"id":'p10',"name":'Clancy Bouvier',"age": 75, "profession": "air steward","sex":'m',"image": "/static/arbre/img/dad.png"},
  {"type":'person',"id":'p11',"name":'Jacqueline Bouvier',"age": 71, "profession": "housewife","sex":'f',"image": "/static/arbre/img/mum.png"},
  {"type":'person',"id":'p13',"name":'Patty Bouvier',"age": 41, "profession": "receptionist","sex":'f',"image": "/static/arbre/img/selma.png"},

  // Selma's Family
  {"type":'family',"id":'f5',"name":'', "image":""},
  {"type":'person',"id":'p12',"name":'Selma Bouvier',"age": 41, "profession": "secretary","sex":'f',"image": "/static/arbre/img/patty.png"},
  {"type":'person',"id":'p14',"name":'Ling Bouvier',"age": 3,"sex":'f',"image": "/static/arbre/img/ling.png"}

];

//currently there are four types of links
//family - family id is always the source
//married - link between two person ids
//adopted and divorced - behave like family but
//dotted line for divorced, gold line for adopted

var edges = [
  // FAMILY 1 - Simpsons
  {id:1,source:'f1',target:'p1',type:'divorced'},
  {id:2,source:'f1',target:'p2',type:'divorced'},
  {id:3,source:'f1',target:'p3',type:'child'},
  {id:4,source:'f1',target:'p4',type:'child'},
  {id:5,source:'f1',target:'p5',type:'child'},
  {id:6,source:'f1',target:'p6',type:'child'},


  // FAMILY 2 - Abraham
  {id:8,source:'f3',target:'p8',type:'married'},
  {id:9,source:'f3',target:'p9',type:'married'},
  {id:10,source:'f3',target:'p2',type:'child'},
  {id:11,source:'f3',target:'p7',type:'child'},

  // FAMILY 3 - Bouviers
  {id:8,source:'f4',target:'p10',type:'married'},
  {id:9,source:'f4',target:'p11',type:'married'},
  {id:10,source:'f4',target:'p1',type:'child'},
  {id:10,source:'f4',target:'p12',type:'child'},
  {id:10,source:'f4',target:'p13',type:'child'},

  // FAMILY 4 - Selma
  {id:8,source:'f5',target:'p12',type:'married'},
  {id:10,source:'f5',target:'p14',type:'child'}

];

export {nodes, edges};
