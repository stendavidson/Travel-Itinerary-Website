from flask import Response, make_response


def error_response(message : str, status : int) -> Response :

    # Create error response body
    body = {"error" : {"message" : message}}

    # Create response object
    response = make_response(body)

    # Headers
    response.status = status
    response.access_control_allow_origin = "*"
    response.content_language = "en"
    response.content_type = "application/json"

    return response