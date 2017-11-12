"""Module provides get_movies(option) to retrieve movies data using TMDB API
    (https://www.themoviedb.org/documentation/api).
    Please set the tmdb.API_KEY value to the API KEY
    obtained from TMDB account.
    """

import tmdbsimple as tmdb

# Set the TMDB API-KEY for service access
tmdb.API_KEY = 'keysample123' # paste API KEY here
YOUTUBE_BASE_URL = "https://youtu.be/"
POSTER_SIZE = "w185"

# Get the base url for images
config = tmdb.Configuration()
response = config.info()
IMAGE_BASE_URL = config.images["secure_base_url"]


def get_movies(options):
    """Fetches data from TMDB service
        and returns a list of tmdb.Movies object

        Args:
            options (str): upcoming or top_rated. Defaults to top_rated/

        Returns:
            tmdb.Movies object list
            """
    
    movies = tmdb.Movies()
    
    if options == "upcoming":
        response = movies.upcoming(page=1)
    elif options == "top_rated":
        response = movies.top_rated(page=1)
    else:
        response = movies.top_rated(page=1)
        
    new_movies = []  # initialize a list to return
    for result in movies.results:
        movie = tmdb.Movies()
        movie._set_attrs_to_values(result)
        movie.videos()  # fetch youtube trailers for a movie

        # set trailer_youtube_url for a movie object
        if movie.results:
            setattr(movie, "trailer_youtube_url", 
                    YOUTUBE_BASE_URL+movie.results[0]["key"])
        else:
            setattr(movie, "trailer_youtube_url", "")

        # set poster_image_url for a movie object
        if movie.poster_path:
            setattr(movie, "poster_image_url", 
                    IMAGE_BASE_URL+POSTER_SIZE+movie.poster_path)
        else:
            setattr(movie, "poster_image_url", None)
        
        new_movies.append(movie)

    return new_movies

