# England's Trails and Tales - A Travel Itinerary Website

## Author
Sten Healey

## Description
This python application is light weight web framework that enables a user to easily retrieve 
existing travel itineraries, retrieve the weather at each location of a itinerary, create 
(save) new itineraries and access geocoding services. 

In addition to implementing a file-store, the web framework wraps a number of external APIs
and re-serves them via a simplified API endpoint.

## Pre-requisites
Please ensure you have Python installed and added to your PATH, here's an article that shows
you [How To Add Python To Path](https://www.mygreatlearning.com/blog/add-python-to-path/#steps-for-adding-python-to-path-in-windows)

API Keys:
1. Please create a Google API Key via the Google Cloud Console. The Key needs access to the Geocoding, Maps and Directions services.
2. Please create an OpenWeather API Key
3. Store these keys in the given order, in a text file named keys.txt
4. Store keys.txt in the root of this project directory "C:\\..\\..\\ETAT"


## How to Run
Navigated to root directory of this project "C:\\..\\..\\ETAT" and please execute the following commands via the terminal:

1. Install Pre-requisite Modules:

```console
pip install -r requirements.txt
```

2. Start Application:

```console
python -m flaskr.controller.app
```


