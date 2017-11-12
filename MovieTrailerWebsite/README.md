# Movie Trailer Website [First Udacity Project]
This project is part of the **Udacity Full Stack Developer Nanodegree Program**. It fetches movies data from [TMDB API](https://www.themoviedb.org/documentation/api) and **generates web pages to display the movies data like title, overview, poster image, vote rating, trailer**.

# Prerequisite
Python 2.7.9 or higher installed.

# Step 1: Install tmdb API
`pip install tmdbsimple`
Refer to [a python wrapper for TMDB](https://pypi.python.org/pypi/tmdbsimple) for more details.

# Step 2: Get the TMDB API KEY
1. Signup on for TMDB developer account here, [TMDB](https://www.themoviedb.org).
2. Go to **Account Settings>API>Register for API KEY>Developer**.

# Step 3: Add TMDB API KEY to *movie_helper.py* file
 Edit **movie_helper.py**, set `tmdb.API_KEY = \*PASTE API KEY HERE*\`, save.

# Step 4: Execute *web_page_generator.py*
 1. Open file **web_page_generator.py** in **IDLE** editor.
 2. Then go to **Run>Run Module(F5)**.

# Output
Two webpages are generated **TopRatedMovies.html** and **UpcomingMovies.html** and UpcomingMovies.html is opened in a web browser.
Sample output pages are available under **sampleoutput** directory

# Note
In the Internet Explorer you may get a warning at the bottom of the page that **Internet Explorer restricted this webpage from running scripts**. In that case click **Allow blocked content** to be able to play movie trailers.
