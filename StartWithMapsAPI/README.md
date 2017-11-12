**Note: This project is more of a follow along and quizzes to add new functionality, individual project on the same lines will be done in a Nov-Dec 2017 **
# Google Maps API mini project
This project present a web page displays map of New York, USA and allows following actions
1. Show listings: puts markers on predefined locations
2. Hide listings: hide all the markers
3. Drawing tools: Allows to draw a closed polygon and displays markers within the area, if any
4. Zoom: Zooms in to the entered location (only within map)
5. In The last section, provided expected time of travel, travel mode and location within the map;
Distance and time from predefined markers is calculated and the route can be viewed by clicking **view route** button on the marker info box.

All the page updates are done asynchronously using AJAX request

# Get Google Maps API Key
Sign in to https://console.developers.google.com/
Goto API & Services>credentials>Create credentials>API KEY
And put it in **maps.html**, at **API_KEY**

**Note: Map is restricted to New York area.**
