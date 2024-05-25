from flask import Response
from json import dumps


# This function constructs a basic json error response
def error_response(message : str, status : int) -> Response :

    """
    This function constructs simple json HTTP error responses.

    Parameters:
        message (str): an error message.
        status (int): a HTTP error code

    Returns: 
        Response: a json encoded HTTP response containing an error message.
    """

    # Create response object
    response = Response(dumps({"error" : message}), status)

    # Headers
    response.access_control_allow_origin = "*"
    response.content_language = "en"
    response.content_type = "application/json"

    return response


