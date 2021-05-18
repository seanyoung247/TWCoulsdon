// Set's the attribution information to collapsible
var attribution = new ol.control.Attribution({
  collapsible: true
});

// Generates a map position marker
ol.Map.prototype.addMarker = function(lonlat, icon) {
  // Create a marker at the given location
  var marker = new ol.Feature({
    geometry: new ol.geom.Point(ol.proj.fromLonLat(lonlat))
  });
  // Set the marker to the icon given
  marker.setStyle(
    new ol.style.Style({
      image: new ol.style.Icon({
        crossOrigin: 'anonymous',
        src: icon
      })
    })
  );
  // Append the marker to it's own map layer
  var layer = new ol.layer.Vector({
    source: new ol.source.Vector({
      features: [marker]
    })
  });
  // Attach the marker layer to the map
  this.addLayer(layer);
  return marker;
}

// Creates the openlayers map object
var map = new ol.Map({
  // Attach custom attribution control
  controls: ol.control.defaults({attribution: false}).extend([attribution]),
  // Makes the map mobile friendly by only panning when using two fingers
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
  // Name of the DOM element that will contain the map
  target: 'map',
  // Sets the map view to be centered on the position given
  view: new ol.View({
    center: ol.proj.fromLonLat(mapPos),
    zoom: 17
  })
});
// Creates a custom pin
map.addMarker(mapPos, mapPin);