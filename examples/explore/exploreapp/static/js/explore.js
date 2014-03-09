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
    },
    mapLine: function(map_id, line_wkt) {
        var map = new OpenLayers.Map(map_id);
        var osm = new OpenLayers.Layer.OSM("OpenStreetMap Map");
        var fromProjection = new OpenLayers.Projection("EPSG:4326");
        var toProjection = new OpenLayers.Projection("EPSG:900913");
        map.addLayer(osm);

        var style = OpenLayers.Util.extend({}, OpenLayers.Feature.Vector.style['default']);
        style.strokeColor = "red";
        style.strokeColor = "red";
        style.fillColor = "red";
        style.pointRadius = 10;
        style.strokeWidth = 3;
        style.rotation = 45;
        style.strokeLinecap = "butt";
        var vectorLayer = new OpenLayers.Layer.Vector("Line", {'style': style});
        var wkt = new OpenLayers.Format.WKT({
            'internalProjection': toProjection,
            'externalProjection': fromProjection,
            'style': style });
        var lineVector = wkt.read(line_wkt);
        var bounds = lineVector.geometry.getBounds();

        map.addLayer(vectorLayer);
        vectorLayer.addFeatures([lineVector]);

        map.zoomToExtent(bounds);
    }
}
