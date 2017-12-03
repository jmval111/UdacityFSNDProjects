var map;
//set won't keep duplicates :)
var allCuisines = new Set([]);
var drawingManager;
var restoViewModel;
// This global circle variable is to ensure only ONE circle is rendered.
var circle = null;
var infowindow;

//preprocess restaurant data from json
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
  self.isSearchMode = ko.observable(true);
  self.availableRestaurants = ko.observableArray([]);
  self.selectedRestaurant = ko.observable();
  self.availableCuisines = ko.observableArray();
  self.selectedCuisine = ko.observable("all");
  //for later use in cost filter
  self.availableMinCost = ko.observable();
  self.availableMaxCost = ko.observable();
  self.selectedMinCost = ko.observable();
  self.selectedMaxCost = ko.observable();
  self.filteredRestaurants = ko.computed(function(){
    return self.availableRestaurants().filter(function(restaurant){
      return ( (self.selectedCuisine() === "all") || (restaurant.cuisines.indexOf(self.selectedCuisine())>-1) );
    });
  });

  self.highlightMarkers = function(){
    if(self.selectedRestaurant()){
      if(self.selectedRestaurant()){
        markerSelected(self.selectedRestaurant());
      }
    }
  };

  //filter markers
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

  //restaurants list independent controls
  self.zoom_in_text = ko.observable();

  // This function takes the input value in the find nearby area text input
  // locates it, and then zooms into that area. This is so that the user can
  // show all listings, then decide to focus on one area of the map.
  self.zoomToArea = function() {
    // Initialize the geocoder.
    var geocoder = new google.maps.Geocoder();
    // Get the address or place that the user entered.
    var address = self.zoom_in_text();
    console.log('Zoom Text:'+address);
    // Make sure the address isn't blank.
    if (address == '') {
      //TODO put this is closable alert div
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
            //TODO put this in closable alert div
            window.alert('We could not find that location - try entering a more' +
                ' specific place.');
          }
        });
    }
  };

  // This shows and hides (respectively) the drawing options.
  self.toggleDrawing = function() {
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
  };

  // This function hides all markers outside the circle,
  // and shows only the ones within it. This is so that the
  // user can specify an exact area of search.
  self.searchWithinCircle=function() {
    //hides search button to prevent overlapping searches
     self.isSearchMode(false);

     if(circle!=null){
       fetchRestaurantsInCircle(circle.getCenter().lat(),circle.getCenter().lng(),circle.getRadius(),displayRestaurants);
     }
     else{
       //TODO put msg in closable alert div
       console.log('please draw circle first');
       //don't hide search button on error
       self.isSearchMode(true);
     }
  };

  self.clearSearch = function(){
    clearMarkers();
    clearViewModel();
    //remove circle if any
    if(circle!=null){
      circle.setMap(null);
      circle = null;
    }
  };

  //to control filters control panel
  self.showFilters = ko.observable(false);
  self.toggleShowFilters = function(){
    self.showFilters(!self.showFilters());
  };

  //to control top right corner panel
  self.showOptions = ko.observable(false);
  self.toggleShowOptions = function(){
    self.showOptions(!self.showOptions());
  };

  //to control left sidebar panel
  self.showSidebar = ko.observable(false);
  self.toggleSidebar = function(){
    self.showSidebar(!self.showSidebar());
  }
}

restoViewModel = new RestaurantViewModel();
ko.applyBindings(restoViewModel);

//google calls initMap when map is loaded
function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    //TODO create a CONSTANT for lat lng
    center: {lat: 19.190638, lng: 72.834392},
    zoom: 15
  });

  infowindow = new google.maps.InfoWindow();
  // Initialize the drawing manager.
  drawingManager = new google.maps.drawing.DrawingManager({
    drawingMode: google.maps.drawing.OverlayType.CIRCLE,
    drawingControl: true,
    drawingControlOptions: {
      position: google.maps.ControlPosition.TOP_LEFT,
      drawingModes: [
        google.maps.drawing.OverlayType.CIRCLE
      ]
    }
  });



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

//Animate selected marker and show details of restaurant
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


function clearMarkers(){
  var total_markers = restoViewModel.availableRestaurants().length;
  console.log('clearMarkers:'+total_markers);
  for(var i=0;i<total_markers;i++){
    restoViewModel.markers[i].setMap(null);
  }
}

function clearViewModel(){
  console.log('clearViewModel');
  restoViewModel.showFilters(false);
  restoViewModel.isSearchMode(true);
  restoViewModel.markers.length = 0;
  restoViewModel.availableRestaurants.removeAll();
  restoViewModel.availableCuisines.removeAll();
  allCuisines.clear();

  // restoViewModel.showSidebar = restoViewModel.showSidebar(false);
}

//remove this debug var
var cbData;

//callback function when ajax request returns data
function displayRestaurants(data){
  //TODO for debug, remove later
  cbData=data;
  if(data.results_found>0){
    console.log("Restaurants found:"+data.results_found);
    //TODO filter out of circle places
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

      //add restaurants cuisines to the set
      for(var c=0;c<currRestaurant.cuisines.length;c++){
          allCuisines.add(currRestaurant.cuisines[c]);
      }

      restoViewModel.availableRestaurants.push(currRestaurant);

    }//populated places and markers

    var sortedCuisines = Array.from(allCuisines).sort();
    //first cuisine option should be "all"
    sortedCuisines.unshift("all");
    restoViewModel.availableCuisines(sortedCuisines);
  }
  else{
    console.log('Error:'+data.errorMsg);
    clearMarkers();
    clearViewModel();
  }
}
