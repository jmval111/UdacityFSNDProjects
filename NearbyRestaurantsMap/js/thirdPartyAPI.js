const ZOMATO_API_KEY = 'ZOMATO_API_KEY';
const ZOMATO_BASE_URI = "https://developers.zomato.com/api/v2.1/search";
const DEFAULT_QUERY_PARAM = {count: 20, sort: "real_distance", order: "asc"};

function fetchRestaurantsInCircle(lat, lng, radius, callbackFn, statusChangeHandlerFn){

  console.log("lat:"+lat+", lng:"+lng+", radius:"+radius)
  //create copy of DEFAULT_QUERY_PARAM
  let queryParam = Object.assign({},DEFAULT_QUERY_PARAM);
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

  function displayLoading(xhr,setting){
    console.log('loading data...'+xhr.status);
    console.log(xhr);
    statusChangeHandlerFn(xhr, null);
    //setAlertMessage('Loading restaurants..','PROGRESS');
  }

  function wrapData(data, textStatus, xhr){
    console.log('wrapData');
    data.isError = false;
    callbackFn(data);
    statusChangeHandlerFn(xhr, null);
  }

  function handleAjaxError(xhr, textStatus, error) {
    statusChangeHandlerFn(xhr, error);
  }

}
