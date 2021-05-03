
var mapPos = [
  parseFloat($('#longitude').val()),
  parseFloat($('#latitude').val())
];

var attribution = new ol.control.Attribution({
  collapsible: true
});

ol.Map.prototype.addMarker = function(lonlat, icon) {
  var marker = new ol.Feature({
    geometry: new ol.geom.Point(ol.proj.fromLonLat(lonlat))
  });
  marker.setStyle(
    new ol.style.Style({
      image: new ol.style.Icon({
        crossOrigin: 'anonymous',
        src: icon
      })
    })
  );
  var layer = new ol.layer.Vector({
    source: new ol.source.Vector({
      features: [marker]
    })
  });
  this.addLayer(layer);
  return marker;
}

var map = new ol.Map({
  controls: ol.control.defaults({attribution: false}).extend([attribution]),
  interactions: ol.interaction.defaults({dragPan: false, mouseWheelZoom: false}).extend([
    new ol.interaction.DragPan({
      condition: function (event) {
        return (this.getPointerCount() === 2 ||
                  ol.events.condition.platformModifierKeyOnly(event));
      }
    }),
    new ol.interaction.MouseWheelZoom({
      condition: ol.events.condition.platformModifierKeyOnly,
    })
  ]),
  layers: [
    new ol.layer.Tile({
      source: new ol.source.OSM()
    }),
  ],
  target: 'map',
  view: new ol.View({
    center: ol.proj.fromLonLat(mapPos),
    zoom: 17
  })
});
map.addMarker(mapPos, '/static/img/pin.svg');