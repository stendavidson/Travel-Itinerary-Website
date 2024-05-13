from flask import Flask, Response

from ..model.exceptions.ItineraryRequestException import ItineraryRequestException
from ..model.exceptions.RepeatLocationException import RepeatLocationException
from ..model.exceptions.WeatherRequestException import WeatherRequestException
from utils import error_response



app = Flask(__name__)


@app.errorhandler(ItineraryRequestException)
def itinerary_exception_handler(e : ItineraryRequestException)  -> Response:

    return error_response(e.__str__(), 500)
    


@app.errorhandler(RepeatLocationException)
def itinerary_exception_handler(e : RepeatLocationException)  -> Response:

    return error_response(e.__str__(), 400)



@app.errorhandler(WeatherRequestException)
def itinerary_exception_handler(e : WeatherRequestException)  -> Response:

    return error_response(e.__str__(), 500)






# Response for custom HTTP codes, mimetypes and presumably other headers too.