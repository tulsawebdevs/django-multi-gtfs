explore = {
    mapPoint: function(map_id, x, y, zoom) {
        var map = new OpenLayers.Map(map_id);
        var osm = new OpenLayers.Layer.OSM("OpenStreetMap Map");
        var fromProjection = new OpenLayers.Projection("EPSG:4326");
        var toProjection = new OpenLayers.Projection("EPSG:900913");
        var position = new OpenLayers.LonLat(x, y).transform(fromProjection, toProjection);
        map.addLayer(osm);

        var markers = new OpenLayers.Layer.Markers( "Markers" );
        map.addLayer(markers);
        markers.addMarker(new OpenLayers.Marker(position));

        map.setCenter(position, zoom);
    }
}
