var map;
var types = new Set(["all"]);
var viewModel;
var infowindow;
var loc_types_food = [
  "restaurant",
  "cafe",
  "meal_takeaway",
  "meal_delivery"
];

var locationDetails = function(place){
  this.placeID = place.place_id;
  this.name = place.name;
  this.formatted_address = place.formatted_address;
  this.rating = place.rating;
  this.type = place.types[0];
}

var placeIDs = ['ChIJ2dwdG-625zsRpiwnKWf7L6I',
  'ChIJA3oJu-625zsRTn5gf9za28Q',
  'ChIJm8mGy-e25zsRQr3AGJAC3Gg',
  'ChIJy0WY1ui25zsRZp42Q5Y5N5g',
  'ChIJSz7D5Ou25zsRBRtLmjZ3W_U',
  'ChIJmeSKZAG35zsRJHALp7D2q0c'
];

var appViewModel = function(){
  self = this;
  self.places = new Array();
  self.markers = new Array();
  self.availableLocations = ko.observableArray([]);
  self.selectedLocation = ko.observable();
  self.typeFilterOptions = ko.observableArray();
  self.selectedType = ko.observable("all");
  self.filteredLocations = ko.computed(function(){
    return self.availableLocations().filter(function(location){
      return (self.selectedType() === "all" || location.type === self.selectedType());
    });
  });

  self.highlightMarkers = function(){
    if(self.selectedLocation()){
      if(self.selectedLocation()){
        markerSelected(self.selectedLocation());
      }
    }
  };

  self.filteredLocations.subscribe(function(){
      for(var i=0; i<self.markers.length;i++){
        var currMarker = self.markers[i];
        if(self.filteredLocations().some(function(loc){return (loc.placeID === self.markers[i].id);})){
          if(currMarker.getMap() == null){
            currMarker.setMap(map);
          }
        }else{
          currMarker.setMap(null);
        }
      }
    });

}

viewModel = new appViewModel();
ko.applyBindings(viewModel);
// Create a new blank array for all the listing markers.
function initMap() {
  //19.190638, 72.834392
  // Create a map centered in Khandelwal Layout Extension Malad West
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 19.190638, lng: 72.834392},
    zoom: 15
  });

  function calculateCenter() {
    center = map.getCenter();
  }
  google.maps.event.addDomListener(map, 'idle', function() {
    calculateCenter();
  });

  google.maps.event.addDomListener(window, 'resize', function() {
	map.setCenter(center);
  });
  infowindow = new google.maps.InfoWindow();
  var service = new google.maps.places.PlacesService(map);

  //populate places and markers
  for(var i=0; i<placeIDs.length; i++){
    console.log("populating places and markers");
    service.getDetails({
          placeId: placeIDs[i]
        }, function(place, status) {
          if (status === google.maps.places.PlacesServiceStatus.OK) {
            var marker = new google.maps.Marker({
              map: map,
              position: place.geometry.location,
              icon: 'http://maps.google.com/mapfiles/ms/icons/orange-dot.png'
            });
            marker.id = place.place_id;
            var locationItem = new locationDetails(place);
            //locationList.push(locationItem);
            google.maps.event.addListener(marker, 'click', function() {
              markerSelected(locationItem);
            });
            viewModel.markers.push(marker);
            //places.push(place);
            viewModel.places.push(place);
            types.add(place.types[0]);
            viewModel.typeFilterOptions(Array.from(types));
            viewModel.availableLocations.push(locationItem);
          }
        });
  }//populated places and markers

}//ENDED initMap

function toggleSidebar(){
  $('.sidebar').toggleClass('sidebar-active');
  $('.sidebarBtn').toggleClass('sidebarBtn-close');
}

function displayFilters(){
  $('#filters-list').toggleClass("display-filters");
}

function markerSelected(selectedLocn){
  for(var i=0; i<viewModel.markers.length;i++){
    viewModel.markers[i].setIcon('http://maps.google.com/mapfiles/ms/icons/orange-dot.png');
  }
  var markersArr = $.grep(viewModel.markers, function(m){ return m.id === selectedLocn.placeID; })
  if(markersArr.length>0){
    var marker = markersArr[0];
    marker.setIcon('http://maps.google.com/mapfiles/ms/icons/yellow-dot.png');
    marker.setAnimation(google.maps.Animation.BOUNCE);
    window.setTimeout(function(){marker.setAnimation(null);},700);

    infowindow.open(map, marker);
    viewModel.selectedLocation(selectedLocn);
    if(loc_types_food.indexOf(selectedLocn.type)>-1){
      getZomatoDetails(selectedLocn.name, marker.position.lat(), marker.position.lng(), infowindow);

  }else{
    infowindow.setContent('<div><strong>' + selectedLocn.name + '</strong><br>' +
      'Place ID: ' + selectedLocn.placeID + '<br>' +
      selectedLocn.formatted_address + '</div>');
  }
 }
}
