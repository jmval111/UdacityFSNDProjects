"""The module provides open_movies_page(tmdb.Movies list,tmdb.Movies list)
    method. open_movies_page generates webpages from the movies lists:
    TopRatedMovies.html and UpcomingMovies.html and opens UpcomingMovies.html
    in a browser.
    """

import webbrowser
import os
import re


# Styles and scripting for the page
main_page_head = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Fresh Tomatoes!</title>
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    <link rel="stylesheet" type="text/css" href="css/mystyle.css">
    <script type="text/javascript" charset="utf-8">
        // Pause the video when the modal is closed
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
            // Remove the src so the player itself gets removed, as this is the only
            // reliable way to ensure the video stops playing in IE
            $("#trailer-video-container").empty();
        });
        // Start playing the video whenever the trailer modal is opened
        $(document).on('click', '.youtube-play-image', function (event) {
            var trailerYouTubeId = $(this).attr('data-trailer-youtube-id')
            var sourceUrl = 'http://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';
            $("#trailer-video-container").empty().append($("<iframe></iframe>", {
              'id': 'trailer-video',
              'type': 'text-html',
              'src': sourceUrl,
              'frameborder': 0
            }));
        });
        // Animate in the movies when the page loads
        $(document).ready(function () {
          $('.movie-card').hide().first().show("fast", function showNext() {
            $(this).next("div").show("fast", showNext);
          });
        });
    </script>
</head>
'''


# The main page layout and title bar
main_page_content = '''
  <body>
    <!-- Trailer Video Modal -->
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          </div>
        </div>
      </div>
    </div>

    <!-- Main Page Content -->

    <!-- logo text and navigation list -->
    <div class="header-container">
	<div class="logo"><span>MOVIES</span></div>
            <div class="custom-navigation">
	    	<ul>
                    <li><a {upcomingClass} href="UpcomingMovies.html">Upcoming</a></li>
                    <li><a {topratedClass} href="TopRatedMovies.html">Top Rated</a></li>
		</ul>
	    </div>
    </div>
    <div class="movie-container">
      {movie_tiles}
    </div>
    <!-- fixed footer -->
    <div id="about">
		<span>Developed by Viraj Bhosle. </span><span>Information courtesy of <a href="https://www.themoviedb.org">TMDB</a></span>
    </div>
  </body>
</html>
'''


# A single movie entry html template
movie_tile_content = '''
    <div class="movie-card">
		<div class="movie-poster">
			<img class="poster-image" src="{poster_image_url}" />
		</div>
		<div class="movie-info">
			<h2>{movie_title}</h2>
			<img class="youtube-play-image" src="icons/play.png" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer"/>
			<div class="rating"><span><strong>{vote_average}</strong></span></div>
			<h4>Overview</h4>
			<p class="overview-para">{overview}</p>
			<strong>Release Date: </strong><span class="genre-span">{release_date}</span><br/><br/>
		</div>
		
    </div>
'''


def create_movie_tiles_content(movies):
    """Generates HTML movie card layout for the list of movies.
        Args:
            movies (:obj:'list' of :obj:'tmdb.Movies'): list of tmdb.Movies

        Returns:
            formatted HTML content.
    """
    # The HTML content for this section of the page
    content = ''
    for movie in movies:
        # Extract the youtube ID from the url
        youtube_id_match = re.search(
            r'(?<=v=)[^&#]+', movie.trailer_youtube_url)
        youtube_id_match = youtube_id_match or re.search(
            r'(?<=be/)[^&#]+', movie.trailer_youtube_url)
        trailer_youtube_id = (youtube_id_match.group(0) if youtube_id_match
                              else None)

        # Append the tile for the movie with its content filled in
        content += movie_tile_content.format(
            movie_title=movie.title,
            poster_image_url=movie.poster_image_url,
            trailer_youtube_id=trailer_youtube_id,
            vote_average=movie.vote_average,
            release_date=movie.release_date,
            overview=movie.overview.encode("utf-8")
        )
    return content


def open_movies_page(upcomingMovies, topRatedMoives):
    """Generates webpages from the movies lists:
        TopRatedMovies.html and UpcomingMovies.html and opens UpcomingMovies.html
        in a browser.

        Args:
            upcomingMovies (:obj:'list' of :obj:'tmdb.Movies'): Upcoming movies
            topRatedMoives (:obj:'list' of :obj:'tmdb.Movies'): Top rated movies

        Returns: None. Generates webpages, TopRatedMovies.html and UpcomingMovies.html and opens UpcomingMovies.html
        in a browser.
    """
    
    # Create or overwrite the output file
    output_file = open('TopRatedMovies.html', 'w')

    # Replace the movie tiles placeholder generated content
    rendered_content = main_page_content.format(
        movie_tiles=create_movie_tiles_content(topRatedMoives),
        upcomingClass='',
        topratedClass='class="active"')

    # Output the file
    output_file.write(main_page_head + rendered_content)
    output_file.close()

    # Create or overwrite the output file
    output_file = open('UpcomingMovies.html', 'w')

    # Replace the movie tiles placeholder generated content
    rendered_content = main_page_content.format(
        movie_tiles=create_movie_tiles_content(upcomingMovies),
        upcomingClass='class="active"',
        topratedClass='')

    # Output the file
    output_file.write(main_page_head + rendered_content)
    output_file.close()

    # open the output file in the browser (in a new tab, if possible)
    url = os.path.abspath(output_file.name)
    webbrowser.open('file://' + url, new=2)
