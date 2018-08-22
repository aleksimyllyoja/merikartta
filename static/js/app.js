var url = "https://julkinen.liikennevirasto.fi/rasteripalvelu/wmts";

var layers = [
  "liikennevirasto:Merikarttasarja A public",
  "liikennevirasto:Merikarttasarja A erikoiskartat public",
  /*"liikennevirasto:Merikarttasarja B",
  "liikennevirasto:Merikarttasarja C public",
  "liikennevirasto:Merikarttasarja D",
  "liikennevirasto:Merikarttasarja E",
  "liikennevirasto:Merikarttasarja F public",
  "liikennevirasto:Merikarttasarja G public",
  "liikennevirasto:Merikarttasarja G erikoiskartat public",
  "liikennevirasto:Merikarttasarja J",
  "liikennevirasto:Merikarttasarja K",
  "liikennevirasto:Merikarttasarja L",
  "liikennevirasto:Merikarttasarja M",
  "liikennevirasto:Merikarttasarja N",
  "liikennevirasto:Merikarttasarja O",
  "liikennevirasto:Merikarttasarja P",
  "liikennevirasto:Merikarttasarja R",
  "liikennevirasto:Merikarttasarja T",
  "liikennevirasto:Merikarttasarja V",
  "liikennevirasto:Rannikkokartat public",
  "liikennevirasto:Rannikkokarttojen erikoiskartat public",
  "liikennevirasto:Satamakartat",
  "liikennevirasto:Sisavesikartat public",
  "liikennevirasto:Yleiskartat public",
  "liikennevirasto:Merikarttasarjat public",
  "liikennevirasto:Merikarttasarjojen erikoiskartat public",*/
]

var map = L.map('map', {
  maxZoom: 15,
}).setView([60.116374, 24.956884], 15);

L.control.scale({
  'position': 'bottomleft',
  'metric': true,
  'imperial': false
}).addTo(map);

var cache_layer = L.tileLayer('http://localhost:5000/get/{z}/{x}/{y}');

var osm = L.tileLayer('http://{s}.tiles.wmflabs.org/bw-mapnik/{z}/{x}/{y}.png', {
	maxZoom: 18,
	attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
});

function add_staf_layer(layer, map) {
  var staf_layer = new L.TileLayer.WMTS("https://julkinen.liikennevirasto.fi/rasteripalvelu/wmts", {
     style: "normal",
     layer: layer,
     tilematrixSet: "WGS84_Pseudo-Mercator",
     format: "image/png",
  });
  map.addLayer(staf_layer);
}

map.addLayer(osm);

for(var i=0;i<layers.length;i++) add_staf_layer(layers[i], map);

//map.addLayer(cache_layer);
//

$.getJSON('http://localhost:7000/latest', function (data) {

	var velocityLayer = L.velocityLayer({
		displayValues: true,
		displayOptions: {
			velocityType: 'Global Wind',
			displayPosition: 'bottomleft',
			displayEmptyString: 'No wind data'
		},
		data: data,
		maxVelocity: 15,
    velocityScale: 0.002,
    colorScale: ['rgba(0, 0, 255, 0.2)', 'rgba(0, 0, 255, 0.3)', 'rgba(0, 0, 255, 0.4)', 'rgba(0, 0, 255, 0.5)']
	});

  map.addLayer(velocityLayer);
});
