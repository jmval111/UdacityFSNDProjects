var map;
var allCuisines = new Set(["all"]);
var restoViewModel;
// This global circle variable is to ensure only ONE circle is rendered.
var circle = null;
var infowindow;

var Restaurant = function(restaurant_data){
  this.id = restaurant_data.id;
  this.name = restaurant_data.name;
  this.average_cost_for_two = restaurant_data.average_cost_for_two;
  //convert cuisines to array and trim spaces.
  this.cuisines = restaurant_data.cuisines.split(",").map(function (str) {
    return str.trim();
  });
  this.currency = restaurant_data.currency;
  //TODO Set default image
  this.featured_image = restaurant_data.featured_image;
  this.has_online_delivery = restaurant_data.has_online_delivery;
  this.has_table_booking = restaurant_data.has_table_booking;
  this.address = restaurant_data.location.address;
  this.lat = parseFloat(restaurant_data.location.latitude);
  this.lng = parseFloat(restaurant_data.location.longitude);
  this.menu_url = restaurant_data.menu_url;
  this.photos_url = restaurant_data.photos_url;
  this.url = restaurant_data.url;
  this.user_rating = restaurant_data.user_rating;
}

var RestaurantViewModel = function(){
  self = this;
  self.markers = new Array();
  self.availableRestaurants = ko.observableArray([]);
  self.selectedRestaurant = ko.observable();
  self.availableCuisuines = ko.observableArray();
  self.selectedCuisine = ko.observable("all");
  self.availableMinCost = ko.observable();
  self.availableMaxCost = ko.observable();
  self.selectedMinCost = ko.observable();
  self.selectedMaxCost = ko.observable();
  self.filteredRestaurants = ko.computed(function(){
    return self.availableRestaurants().filter(function(restaurant){
      return ( (self.selectedCuisine() === "all") || (self.availableCuisuinesself().indexOf(self.selectedCuisine())>-1) );
    });
  });

  self.highlightMarkers = function(){
    if(self.selectedRestaurant()){
      if(self.selectedRestaurant()){
        markerSelected(self.selectedRestaurant());
      }
    }
  };

  self.filteredRestaurants.subscribe(function(){
      for(var i=0; i<self.markers.length;i++){
        var currMarker = self.markers[i];
        if(self.filteredRestaurants().some(function(resto){return (resto.id === self.markers[i].id);})){
          if(currMarker.getMap() == null){
            currMarker.setMap(map);
          }
        }else{
          currMarker.setMap(null);
        }
      }
    });

}

restoViewModel = new RestaurantViewModel();
ko.applyBindings(restoViewModel);
// Create a new blank array for all the listing markers.
function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    //TODO create a CONSTANT for lat lng
    center: {lat: 19.190638, lng: 72.834392},
    zoom: 15
  });

  infowindow = new google.maps.InfoWindow();
  // Initialize the drawing manager.
  var drawingManager = new google.maps.drawing.DrawingManager({
    drawingMode: google.maps.drawing.OverlayType.CIRCLE,
    drawingControl: true,
    drawingControlOptions: {
      position: google.maps.ControlPosition.TOP_LEFT,
      drawingModes: [
        google.maps.drawing.OverlayType.CIRCLE
      ]
    }
  });

  $('#toggle-drawing').on('click',function() {
          toggleDrawing(drawingManager);
        });
        
  $('#searchZomatoBtn').on('click',searchWithinCircle);

  drawingManager.addListener('overlaycomplete', function(event) {
  // First, check if there is an existing circle.
  // If there is, get rid of it and remove the markers
  if (circle) {
    circle.setMap(null);
  }
  // Switching the drawing mode to the HAND (i.e., no longer drawing).
  drawingManager.setDrawingMode(null);
  // Creating a new editable circle from the overlay.
  circle = event.overlay;
  circle.setEditable(true);
 });

}//ENDED initMap

function toggleSidebar(){
  $('.sidebar').toggleClass('sidebar-active');
  $('.sidebarBtn').toggleClass('sidebarBtn-close');
}

$('#fixed-header').on('click',function(){
  $('.options-box').toggleClass("toggle-visible");
});

function displayFilters(){
  $('#filters-list').toggleClass("display-filters");
}

function markerSelected(selectedLocn){
  for(var i=0; i<restoViewModel.markers.length;i++){
    restoViewModel.markers[i].setIcon('http://maps.google.com/mapfiles/ms/icons/orange-dot.png');
  }
  var markersArr = $.grep(restoViewModel.markers, function(m){ return m.id === selectedLocn.id; })
  if(markersArr.length>0){
    var marker = markersArr[0];
    marker.setIcon('http://maps.google.com/mapfiles/ms/icons/yellow-dot.png');
    marker.setAnimation(google.maps.Animation.BOUNCE);
    window.setTimeout(function(){marker.setAnimation(null);},700);

    infowindow.open(map, marker);
    restoViewModel.selectedRestaurant(selectedLocn);
    infowindow.setContent('<div><strong>' + selectedLocn.name + '</strong><br>' +
      'Cost for two: ' + selectedLocn.average_cost_for_two + '<br>' +
      selectedLocn.user_rating.aggregate_rating + '</div>');
 }
}

// This function takes the input value in the find nearby area text input
// locates it, and then zooms into that area. This is so that the user can
// show all listings, then decide to focus on one area of the map.
function zoomToArea() {
  // Initialize the geocoder.
  var geocoder = new google.maps.Geocoder();
  // Get the address or place that the user entered.
  var address = $('#zoom-to-area-text').val();
  console.log('Zoom Text:'+address);
  // Make sure the address isn't blank.
  if (address == '') {
    window.alert('You must enter an area, or address.');
  } else {
    // Geocode the address/area entered to get the center. Then, center the map
    // on it and zoom in
    geocoder.geocode(
      { address: address,
        componentRestrictions: {country:'IN', locality: 'Mumbai'}
      }, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
          map.setCenter(results[0].geometry.location);
          map.setZoom(15);
        } else {
          window.alert('We could not find that location - try entering a more' +
              ' specific place.');
        }
      });
  }
}

// This shows and hides (respectively) the drawing options.
function toggleDrawing(drawingManager) {
  console.log('toggleDrawing');
  if (drawingManager.map) {
    drawingManager.setMap(null);
    // In case the user drew anything, get rid of the circle
    if (circle !== null) {
      circle.setMap(null);
    }
  } else {
    drawingManager.setMap(map);
  }
}

// This function hides all markers outside the circle,
// and shows only the ones within it. This is so that the
// user can specify an exact area of search.
function searchWithinCircle() {
   //console.log('Circle changed:'+circle.getCenter().lat());
   //TODO: hide Filter sidebar
   //TODO: clear all markers if any
   clearMarkers();
   //TODO: clear restoViewModel data
   clearViewModel();

   if(circle!=null){
     fetchRestaurantsInCircle(circle.getCenter().lat(),circle.getCenter().lng(),circle.getRadius(),displayRestaurants);
   }
   else{
     console.log('please draw circle first');
   }
}

function clearMarkers(){
  var total_markers = restoViewModel.availableRestaurants().length;
  console.log('clearMarkers:'+total_markers);
  for(var i=0;i<total_markers;i++){
    restoViewModel.markers[i].setMap(null);
  }
}

function clearViewModel(){
  console.log('clearViewModel');
}
var cbData;
function displayRestaurants(data){
  cbData=data;
  if(data.results_found>0){
    console.log("Restaurants found:"+data.results_found);
    //populate places and markers

    for(var i=0; i<data.results_shown; i++){
      console.log("populating viewModel and markers");
      var currRestaurant = new Restaurant(data.restaurants[i].restaurant);
      console.log(currRestaurant);
      var marker = new google.maps.Marker({
        map: map,
        position: {lat: currRestaurant.lat, lng: currRestaurant.lng},
        icon: 'http://maps.google.com/mapfiles/ms/icons/orange-dot.png'
      });
      marker.id = currRestaurant.id;
      //locationList.push(locationItem);
      google.maps.event.addListener(marker, 'click', function() {
        return markerSelected(this);
      }.bind(currRestaurant));
      restoViewModel.markers.push(marker);
      for(var c=0;c<currRestaurant.cuisines.length;c++){
          allCuisines.add(currRestaurant.cuisines);
      }
      restoViewModel.availableCuisuines(Array.from(allCuisines));
      restoViewModel.availableRestaurants.push(currRestaurant);

    }//populated places and markers

  }
  else{
    console.log('Error:'+data.errorMsg);
  }
}