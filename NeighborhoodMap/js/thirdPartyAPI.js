ZOMATO_API_KEY = 'PASTE_ZOMATO_KEY';
ZOMATO_SEARCH_RADIUS = 100; //meters
ZOMATO_BASE_URI = "https://developers.zomato.com/api/v2.1/search";
DEFAULT_QUERY_PARAM = {count: 1, radius: 50};//, sort: "real_distance", order: "asc"};
var xhrCap;
var errorCap;
function getZomatoDetails(restaurant_name, lat, lng, infowindow){
  //var request_uri= ZOMATO_BASE_URI+"&q="+encodeURIComponent(restaurant_name)+"&lat="+encodeURIComponent(lat)+"&lon="+encodeURIComponent(lon);
  var queryParam = Object.assign({},DEFAULT_QUERY_PARAM);
  queryParam.q = encodeURIComponent(restaurant_name);
  queryParam.lat = encodeURIComponent(lat);
  queryParam.lon = encodeURIComponent(lng);
  $.ajax({
    type: 'GET',
    url: ZOMATO_BASE_URI,
    headers: {"user-key": ZOMATO_API_KEY},
    data: queryParam,
    beforeSend: displayLoading,
}).done(displayData).fail(handleAjaxError);

  function displayLoading(){
    infowindow.setContent("sending zomato req..");
  }

  function displayData(data){
    if(data.results_found >0){
      var restaurant = data.restaurants[0].restaurant;
      var zomatoLat= parseFloat(restaurant.location.latitude);
      var zomatoLng= parseFloat(restaurant.location.longitude);
      console.log("Restaurant name:"+restaurant.name);
      console.log("Restaurant lat diff:"+(lat-zomatoLat));
      console.log("Restaurant lng diff:"+(lng-zomatoLng));
      if(Math.abs(lat-zomatoLat)<0.2 && Math.abs(lng-zomatoLng)<0.2){
        infowindow.setContent("<h3>"+restaurant.name+"</h3><strong>Cost for two:</strong>"+restaurant.average_cost_for_two
        );
      }
      else{
        infowindow.setContent('<div>Not found on zomato<strong>' + selectedLocn.name + '</strong><br>' +
          'Place ID: ' + selectedLocn.placeID + '<br>' +
          selectedLocn.formatted_address + '</div>');
      }
    }
  }

  function handleAjaxError(xhr, status, error) {
    // var err = eval("(" + xhr.responseText + ")");
    // console.log('status:'+status);
    // console.log('err:'+err);
    // console.log('xhr.responseText:'+xhr.responseText);
    // infowindow.setContent("Error!");
    var errorMsg;
    if(xhr.readyState === 0){
      errorMsg = "Network Error";
    }
    else if(xhr.status && xhr.status === 403){
      errorMsg = "Invalid API KEY";
    }
    else{
      errorMsg = "Error";
    }
    infowindow.setContent('<div class="error">'+errorMsg+'</div>');
    xhrCap = xhr;
    errorCap = error;
  }

}
