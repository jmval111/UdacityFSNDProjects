"""Fetches upcoming and top rated movies from TMDB,
    to generate and open webpages.
"""

import custom_fresh_tomatoes
import movie_helper


# fetch upcoming and top rated movies from TMDB
upcomingMovies = movie_helper.get_movies("upcoming")
topRatedMovies = movie_helper.get_movies("top_rated")

# Print movie titles for debugging
print("Upcoming movies titles")
for movie in upcomingMovies:
    print(movie.title)

print
print("Upcoming movies titles")
for movie in topRatedMovies:
    print(movie.title)

# Generate webpages and open a webpage
custom_fresh_tomatoes.open_movies_page(upcomingMovies, topRatedMovies)
