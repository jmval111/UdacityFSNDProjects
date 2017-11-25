var map;
var types = new Set(["all"]);
var viewModel;

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
  'ChIJSz7D5Ou25zsRBRtLmjZ3W_U'
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
      //console.log(this.selectedType());
      return (self.selectedType() === "all" || location.type === self.selectedType());
    });
  });

  self.highlightMarkers = function(){
    //console.log("highlighting marker for "+Object.keys(self.selectedLocation()));
    for(var i=0; i<self.markers.length;i++){
      self.markers[i].setIcon('http://maps.google.com/mapfiles/ms/icons/orange-dot.png');
    }
    if(self.selectedLocation()){
      var selectedMarker = $.grep(self.markers, function(m){ return m.id === self.selectedLocation().placeID; })
      selectedMarker[0].setIcon('http://maps.google.com/mapfiles/ms/icons/yellow-dot.png');
      selectedMarker[0].setAnimation(google.maps.Animation.BOUNCE);
      window.setTimeout(function(){selectedMarker[0].setAnimation(null);},700);
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
  var infowindow = new google.maps.InfoWindow();
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
              infowindow.setContent('<div><strong>' + place.name + '</strong><br>' +
                'Place ID: ' + place.place_id + '<br>' +
                place.formatted_address + '</div>');
              infowindow.open(map, this);
            });
            viewModel.markers.push(marker);
            //places.push(place);
            viewModel.places.push(place);
            types.add(place.types[0]);
            viewModel.typeFilterOptions(Array.from(types));
            //viewModel.availableLocations(locationList);
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
// Cinemax Malad
// ChIJ2dwdG-625zsRpiwnKWf7L6I
//
// Movie Time Cinemax
// ChIJA3oJu-625zsRTn5gf9za28Q
//
// Orchids The International school
// ChIJm8mGy-e25zsRQr3AGJAC3Gg
//
// Silver Oaks
// ChIJy0WY1ui25zsRZp42Q5Y5N5g
//
// Ryan International school
// ChIJ0SmyQFTP5zsRjIdkzrwnMXE
//
// Axis bank
// ChIJQSK0tuK25zsRcyOalRc9YI8
//
// Landmark Veg restaurant
// ChIJV3Odaem25zsRlc1R4TvdfRo
//
// Cinemax
// ChIJ2dwdG-625zsRpiwnKWf7L6I
//
// KG Mittal Institute of Management
// ChIJQzph2O-25zsRDEC4mibd6XE
//
// DMart Malad
// ChIJnUd5au625zsR4G6PeNn1YBw
//
// Joey's Pizza
// ChIJQVuEsfa25zsRhrWdU-l8WeE
//
// PVR Milap Cinemas
// ChIJRYoTluC25zsRyfRBwb62I0M
