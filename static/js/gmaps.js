var map = (function() {

	var locale = new google.maps.LatLng(30,0);
	var mapOptions = {
		center: locale,
		zoom: 2,
	};
	var map = new google.maps.Map(document.getElementById('map'), mapOptions);

	// the following removes the annoying equator and date lines:
	var mapStyle = [
	      {
		 featureType: "administrative",
		 elementType: "geometry.fill",
		 stylers: [
		    { visibility: "off" }
		 ]
	       }
	];
	var styledMap = new google.maps.StyledMapType(mapStyle);
	map.mapTypes.set('myCustomMap', styledMap);
	map.setMapTypeId('myCustomMap');
	// end part that removes equator and date lines here 
	return {
		addKmlLayer: function(url, options) {
			options = options || {};
			options['map'] = map;
			var kmlLayer = new google.maps.KmlLayer(url, options);
			kmlLayer.setMap(map);
			console.log(kmlLayer);
		}
	}
}());

/*
	var kmlUrl = '/kml';
	var kmlOptions = {
	  suppressInfoWindows: true,
	  preserveViewport: false,
	  map: map
*/
	
