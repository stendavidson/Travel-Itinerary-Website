import logging
from flask import Flask, Response, request, redirect, render_template
from json import dumps
from os.path import exists

from flaskr.model.Itinerary import Itinerary
from flaskr.model.data_access_layer.GeocodeAPIConnector import GeocodeApiConnector
from flaskr.model.data_access_layer.ItineraryConnector import ItineraryConnector
from flaskr.model.data_access_layer.WeatherAPIConnector import WeatherAPIConnector
from flaskr.model.exceptions.ItineraryRequestException import ItineraryRequestException
from flaskr.model.exceptions.RepeatLocationException import RepeatLocationException
from flaskr.model.exceptions.LocationKeyException import LocationKeyException
from flaskr.model.exceptions.WeatherRequestException import WeatherRequestException
from flaskr.model.exceptions.InvalidUnitException import InvalidUnitException
from flaskr.model.exceptions.GeocodeRequestException import GeocodeRequestException
from flaskr.model.exceptions.InvalidLocationException import InvalidLocationException
from flaskr.controller.utils import error_response



##################################################################################
############################# Retrieve API Keys ##################################
##################################################################################



# The API Keys are loaded from a text file.
KEYS_FILE = "./keys.txt"

keys = []


# The file is verified
if not exists(KEYS_FILE) :

    print("The \"./keys.txt\" file cannot be found in the root folder.")
    
    # Exit using error code 2 in Windows indicates that a file cannot be found.
    exit(2)


# The file is read into an array line by line
with open(KEYS_FILE, mode="r") as file:
    
    keys = file.readlines()


# If the API Keys cannot be found in the file exit.
if len(keys) != 2:

    print("No API keys found, please provide the Google and OpenWeather API " \
          + "keys in a text file (one per line)")
    
    # Exit using error code 13 in Windows indicates that the data is invalid
    exit(13)
    

# Google API Key
GOOGLE_KEY = keys[0].strip().replace("\n", "")
OPEN_WEATHER_KEY = keys[1].strip().replace("\n", "")



##################################################################################
############################# Create Flask App ##################################
##################################################################################



# The flask app is added and configured.
app = Flask(__name__)
app.static_folder = "../view/static"
app.template_folder = "../view/templates"



##################################################################################
################################## Exceptions ####################################
##################################################################################


# The following function handles exceptions thrown by the itinerary connector
@app.errorhandler(ItineraryRequestException)
def itinerary_request_handler(e : ItineraryRequestException) -> Response:

    """
    This function handles exceptions thrown when itinerary data cannot be accessed
    or stored because an unanticipated exception was thrown.

    Parameters:
        e (ItineraryRequestException): Custom exception class.

    Returns: 
        Response: a json encoded HTTP 500 response containing an error message.
    """

    return error_response(e.__str__(), 500)



@app.errorhandler(LocationKeyException)
def location_key_handler(e : LocationKeyException) -> Response:

    """
    This function handles exceptions thrown by the Itinerary class when an
    invalid location key is used to retrieve a location entry.

    Parameters:
        e (LocationKeyException): Custom exception class.

    Returns: 
        Response: a json encoded HTTP 500 response containing an error message.
    """

    return error_response(e.__str__(), 500)



@app.errorhandler(RepeatLocationException)
def repeat_location_handler(e : RepeatLocationException) -> Response:

    """
    This function handles exceptions thrown by the Itinerary class when a
    duplicate location name is added to the itinerary.

    Parameters:
        e (InvalidLocationException): Custom exception class.

    Returns: 
        Response: a json encoded HTTP response containing an error message.
    """

    # If the request corresponding to the error was a POST request then
    # the request was in error.
    http_code = 500
    
    if request.method == "POST" :

        http_code = 400

    return error_response(e.__str__(), http_code)



@app.errorhandler(InvalidLocationException)
def invalid_location_handler(e : InvalidLocationException) -> Response:

    """
    This function handles exceptions thrown by the Itinerary class when a
    location outside of the UK is added to the itinerary.

    Parameters:
        e (InvalidLocationException): Custom exception class.

    Returns: 
        Response: a json encoded HTTP 400 response containing an error message.
    """

    return error_response(e.__str__(), 400)



@app.errorhandler(InvalidUnitException)
def weather_request_handler(e : InvalidUnitException) -> Response:

    """
    This function handles exceptions thrown when an inalid unit type is
    submitted.

    Parameters:
        e (InvalidUnitException): Custom exception class.

    Returns: 
        Response: a json encoded HTTP 400 response containing an error message.
    """

    return error_response(e.__str__(), 400)



@app.errorhandler(WeatherRequestException)
def weather_request_handler(e : WeatherRequestException) -> Response:

    """
    This function handles exceptions thrown when the OpenWeather API returns 
    an unexpected response or the connector class is in error.

    Parameters:
        e (WeatherRequestException): Custom exception class.

    Returns: 
        Response: a json encoded HTTP 500 response containing an error message.
    """

    return error_response(e.__str__(), 500)




@app.errorhandler(GeocodeRequestException)
def geocode_request_handler(e : GeocodeRequestException) -> Response:

    """
    This function handles exceptions thrown when the Google Geocode API returns 
    an unexpected response or the connector class is in error.

    Parameters:
        e (GeocodeRequestException): Custom exception class.

    Returns: 
        Response: a json encoded HTTP 400 response containing an error message.
    """

    return error_response(e.__str__(), 500)



@app.errorhandler(TypeError)
def parameter_handler(e : TypeError) -> Response:

    """
    This function handles TypeErrors thrown  when invalid data types are passed 
    to various model methods.

    Parameters:
        e (TypeError): The error being caught.

    Returns: 
        Response: a json encoded HTTP 400 response containing an error message.
    """

    return error_response(e.__str__(), 400)



@app.errorhandler(ValueError)
def parameter_handler(e : ValueError) -> Response:

    """
    This function handles ValueErrors thrown when the correct argument type is
    passed but the value is incorrect.

    Parameters:
        e (ValueError): The error being caught.

    Returns: 
        Response: a json encoded HTTP 400 response containing an error message.
    """

    return error_response(e.__str__(), 400)



@app.errorhandler(404)
def error_404_handler(e : int) -> Response:

    """
    This function handles HTTP 404 Resource Not Found Errors. Since this is can be
    raised in the context of both the web app and the API an appropriate response
    is returned depending on the url resource being accessed.

    Parameters:
        e (int): The HTTP error code.

    Returns: 
        Response: a json error or html error page.
    """

    # By default a "page not found" page is displayed
    response = Response(render_template("errors/error-404.html"), 404)

    # Conditional handles non-existent api endpoints
    if request.base_url[:20] == "http://localhost/api" :

        response = error_response("This API endpoint does not exist", 404)

    return response



@app.errorhandler(Exception)
def generic_error_handler(e : Exception) -> Response:

    """
    This function handles the most generic Exception possible, since this may be
    raised outside the context of an API request, the response is a html page.

    Parameters:
        e (Exception): The exception being caught.

    Returns: 
        Response: a generic html error page.
    """

    print(str(e))

    return Response(render_template("errors/error-500.html"), 500)



##################################################################################
################################# API Endpoints ##################################
##################################################################################



@app.route("/api/geocode/<location>", methods=["GET"])
def get_coordinates(location : str)  -> Response:

    """
    API HTTP GET endpoint handler - retrieves the coordinates corresponding to
    the input location name.

    URL Parameters:
        location (str): The plain text location name, description or address.

    Returns:
        Response: A json encoded HTTP 200 response containing a list of valid
        itinerary names.
    """

    response = None

    # Request validation
    if location == None or location == "" :
        
        response = error_response("Invalid request, the location parameter was missing", 400)

    else :

        # Coordinates are retrieved from google geocoding api
        connector = GeocodeApiConnector(GOOGLE_KEY)

        coordinates = connector.request_coordinates(location)

        response = Response(dumps({"coordinates" : coordinates}), 200)

    response.access_control_allow_origin = "*"
    response.content_language = "en"
    response.content_type = "application/json"

    return response



@app.route("/api/itineraries", methods=["GET"])
def get_itinerary_names()  -> Response:

    """
    API HTTP GET endpoint handler - retrieves a list of valid itinerary names.

    Returns:
        Response: A json encoded HTTP 200 response containing a list of valid
        itinerary names.
    """

    # The itinerary names are retrieved.
    connector = ItineraryConnector("./itineraries")

    itinerary_names = connector.get_names()

    response = Response(dumps({"itineraries" : itinerary_names}), 200)

    # Set the response headers
    response.access_control_allow_origin = "*"
    response.content_language = "en"
    response.content_type = "application/json"

    return response



@app.route("/api/itineraries/<name>", methods=["GET"])
def get_itinerary(name : str)  -> Response:

    """
    API HTTP GET endpoint handler - retrieves the itinerary data for a specific
    itinerary.

    URL Parameters: 
        name (str): The name of the itinerary.

    Returns:
        Response: A json encoded HTTP 200 response containing itinerary data.
    """

    response = None

    # Request validation
    if name == None or name == "":
        
        response = error_response("Invalid request, the name parameter was missing", 400)

    else :

        # The itinary data is retrieved from a file
        connector = ItineraryConnector("./itineraries")

        itinerary = connector.read(name)

        response = Response(dumps({
            "center" : itinerary.center, 
            "coordinates" : itinerary.coordinates
            }), 200)

    # Set the response headers
    response.access_control_allow_origin = "*"
    response.content_language = "en"
    response.content_type = "application/json"

    return response



@app.route("/api/itineraries", methods=["POST"])
def create_itinerary()  -> Response:

    """
    API HTTP POST endpoint handler - creates and saves a new itinerary to a save
    file.

    Request Body: 
        name (str): The name of the itinerary.
        coordinates (list[tuple[str, float, float]]): A list of location names and
        their corresponding coordinates.

    Returns:
        Response: A body-less HTTP response either 404, 204.
    """

    # Request body retrieved
    data = request.json

    # Request validation
    if ("name" not in data) or ("coordinates" not in data):
        
        response = error_response("""Invalid request, the name (string) and itinerary (list) 
                                  components are both required.""", 400)

    else :

        itinerary = Itinerary()

        # The locations in the interary are added to the data structure
        for location in data["coordinates"] :

            itinerary[location[0]] = (location[1], location[2])

        
        # The itinary object is saved to a file
        connector = ItineraryConnector("./itineraries")

        connector.write(data["name"], itinerary)

        response = Response(status=204)

    # Set the response headers
    response.access_control_allow_origin = "*"

    return response



@app.route("/api/itineraries/<name>", methods=["DELETE"])
def delete_itinerary(name : str)  -> Response:
    
    """
    API HTTP DELETE endpoint handler - deletes a single itinerary.

    URL Parameters:
        name (str): The name of the itinerary to be deleted.

    Returns:
        Response: A body-less HTTP response either 404, 204.
    """

    response = None

    # Request validation
    if name == None or name == "" :
        
        response = error_response("Invalid request, the name parameter was missing", 400)

    else :

        # The itinary save file is deleted
        connector = ItineraryConnector("./itineraries")

        connector.delete(name)

        response = Response(status=204)

    # Set the response headers
    response.access_control_allow_origin = "*"
    response.content_language = "en"

    return response



# The following function handles api GET requests for current weather data
# it can handle one or more simultaneous requests
@app.route("/api/weather", methods=["GET"])
def get_weather()  -> Response:
    """
    API HTTP GET endpoint handler - simultaneously retrieves the weather data
    for any number of requested coordinates.

    URL Parameters:
        lat (float): The latitudes of the desired location encoded as url parameters.
        lng (float): The longitudes of the desired location encoded as url parameters.
        units (str): Optional parameter specifying the units to be used.

    Returns:
        Response: json encoded weather data in HTTP 200 response.
    """


    # GET request's url paramters are retrieved
    latitudes = request.args.getlist("lat")
    longitudes = request.args.getlist("lng")
    units = request.args.get("units", "metric")

    response = None

    # Request validation
    if latitudes == None or len(latitudes) == 0 or len(longitudes) == 0:
        
        response = error_response("Invalid request, the requests " + \
                                   "must have one or more coordinate pairs.", 400)
        
    else :

        # Weather data is retrieved from the OpenWeather API
        connector = WeatherAPIConnector(OPEN_WEATHER_KEY)

        # The input parameters are safely cast to float values
        try:

            latitudes = [float(i) for i in latitudes]
            longitudes = [float(i) for i in longitudes]

        except ValueError as e :

            raise TypeError("The latitudes and longitudes must be valid numerical values (floats).")
            

        # Threaded bulk request is used when more than coordinate is requested
        if len(latitudes) > 1 or len(longitudes) > 1 :
            
            response = Response(dumps({"weather-data" : [i.__dict__ for i in connector.bulk_weather(latitudes, longitudes, units)]}), 200)
            
        else :

            response = Response(dumps({"weather-data" : [connector.current_weather(latitudes[0], longitudes[0], units).__dict__]}), 200)

    # Set the response headers
    response.access_control_allow_origin = "*"
    response.content_language = "en"
    response.content_type = "application/json"

    return response


##################################################################################
################################## Page Routes ###################################
##################################################################################



@app.route("/", methods=["GET", "POST"])
def domain_router() -> Response:

    """
    This function routes the base "domain" to the homepage. This is commmon practice
    when configuring a website's routing.

    Returns: 
        Response: a redirect response.
    """

    return redirect("/index")


# This function routes the user to the main / home page of the website.
@app.route("/index", methods=["GET", "POST"])
def homepage_router() -> str:

    """
    This function displays the homepage of the website when this url is requested.

    Returns: 
        str: a html page to be rendered.
    """

    return render_template("index.html", api_key=GOOGLE_KEY)


# This function routes the user to the main / home page of the website.
@app.route("/create-itinerary", methods=["GET", "POST"])
def itinerary_router() -> str:

    """
    This function displays the "Create Itinerary" page of the website when this url
    is requested.

    Returns: 
        str: a html page to be rendered.
    """

    return render_template("create-itinerary.html")


##################################################################################
################################# Application Start ##############################
##################################################################################


# Conditionally start Flask application
if __name__ == "__main__" :

    import logging
    app.logger.setLevel(logging.INFO)

    app.run(host="localhost", port=80, debug=True)
