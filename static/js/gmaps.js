var map = (function() {

	var locale = new google.maps.LatLng(30,0);
	var mapOptions = {
		center: locale,
		zoom: 2,
		mapTypeId: google.maps.MapTypeId.SATELLITE // TERRAIN, SATELLITE, HYBRID, ROADMAP
	};
	console.log(mapOptions.mapTypeId);
	var map = new google.maps.Map(document.getElementById('map'), mapOptions);
/*
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
*/
	// for holding old kml layer:
	var old = undefined;
	return {
		addKmlLayer: function(url, options) {
			options = options || {};
			options['map'] = map;
			if (old) {
				old.setMap(null);
			}
			var kmlLayer = new google.maps.KmlLayer(url, options);
			console.log(kmlLayer);
			old = kmlLayer;
		}
	}
}());

// function to hightlight selected item,
// remove any previous selection's highlight:
var selectItem = (function() {
	// for holding the select element:
	var selected = undefined;
	var oldBackground = undefined;

	var func = function(item) {
		if (selected) {
			selected.style.backgroundColor = oldBackground;
		}
		oldBackground = item.style.backgroundColor;
		item.style.backgroundColor = "#FFA500";
		selected = item;
	}	
	return func;
}());
