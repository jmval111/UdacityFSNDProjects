
function loadData() {

    var $body = $('body');
    var $wikiElem = $('#wikipedia-links');
    var $nytHeaderElem = $('#nytimes-header');
    var $nytElem = $('#nytimes-articles');
    var $greeting = $('#greeting');
	var $street = $("#street").val();
	var $city = $("#city").val();
	var $address = $street +","+$city;
    // clear out old data before new request
    $wikiElem.text("");
    $nytElem.text("");
	
	$greeting.text('So, you want to live at '+$address+'?');

    // load streetview
	$('.bgimg').remove();
    // YOUR CODE GOES HERE!
	$body.append('<img class="bgimg" src="'+encodeURI('http://maps.googleapis.com/maps/api/streetview?size=600x400&location='+$address)+'">');
	console.log('<img class="bgimg" src="'+encodeURI('http://maps.googleapis.com/maps/api/streetview?size=600x400&location='+$address)+'">');
	
	var nytimesUrl = encodeURI('https://api.nytimes.com/svc/search/v2/articlesearch.json?q='+$city+'&sort=newest&api-key=NYT-API_KEY')
	//load articles
	$.getJSON( nytimesUrl, function( data ) {
		//console.log(data.response.docs[0]);
		$.each(data.response.docs, function(){
		$nytElem.append(
		'<li class="article"><a href="'+this.web_url+'">'+this.headline.main+'</a><p>'+this.snippet+'</p></li>'
		)
		})
		
	 }).fail(function(){
		$nytHeaderElem.text('New York Times Articles Could Not Be Loaded');
	 });
	 
	 var wikiUrl='https://en.wikipedia.org/w/api.php?action=opensearch&search='+$city+'&format=json&callback=wikiCallback'
	 
	 $.ajax({
		url: wikiUrl,
		dataType: "jsonp",
		success: function( response ){
			var articleList = response[1];
			
			for(var i=0;i<articleList.length; i++){
				articleStr=articleList[i];
				var url='https://en.wikipedia.org/wiki/'+articleStr;
				$wikiElem.append('<li><a href="'+url+'">'+articleStr+'</li>');
			};
		}
	 }).fail(function(){
		$wikiElem.text('Wikipedia Links Could Not Be Loaded');
	 });;
	 
    return false;
};

$('#form-container').submit(loadData);
