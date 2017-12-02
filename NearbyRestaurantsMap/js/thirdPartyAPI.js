ZOMATO_API_KEY = 'PASTE_ZOMATO_KEY';
ZOMATO_BASE_URI = "https://developers.zomato.com/api/v2.1/search";
DEFAULT_QUERY_PARAM = {count: 20, sort: "real_distance", order: "asc"};//, sort: "real_distance", order: "asc"};
var xhrCap;
var errorCap;
var tpData;
function fetchRestaurantsInCircle(lat, lng, radius, callbackFn){
  console.log("lat:"+lat+", lng:"+lng+", radius:"+radius)
  //create copy of DEFAULT_QUERY_PARAM
  var queryParam = Object.assign({},DEFAULT_QUERY_PARAM);
  queryParam.radius = encodeURIComponent(radius);
  queryParam.lat = encodeURIComponent(lat);
  queryParam.lon = encodeURIComponent(lng);
  $.ajax({
    type: 'GET',
    url: ZOMATO_BASE_URI,
    headers: {"user-key": ZOMATO_API_KEY},
    data: queryParam,
    beforeSend: displayLoading,
}).done(wrapData).fail(handleAjaxError);

  function displayLoading(){
    console.log('loading data...');
  }

  function wrapData(data){
    tpData = data;
    console.log('wrapData');
    data.isError = false;
    callbackFn(data);
  }

  function handleAjaxError(xhr, status, error) {
    // var err = eval("(" + xhr.responseText + ")");
    // console.log('status:'+status);
    // console.log('err:'+err);
    // console.log('xhr.responseText:'+xhr.responseText);
    // infowindow.setContent("Error!");
    console.log('handleAjaxError');
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

    var data = {isError: true, errorMsg: errorMsg};
    callbackFn(data);
    // infowindow.setContent('<div class="error">'+errorMsg+'</div>');
    // xhrCap = xhr;
    // errorCap = error;
  }

}
