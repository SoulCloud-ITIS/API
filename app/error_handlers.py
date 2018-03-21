from app import app
from app.models import Response


@app.errorhandler(404)
def method_not_found(e):
    return Response("Method not found. Please, see documentation", False, 404).to_json(), 404


@app.errorhandler(400)
def bad_request(e):
    return Response("Bad request", False, 400).to_json(), 400


@app.errorhandler(500)
def internal_error(e):
    return Response("Houston, we have a problem. Please contact with API developers.", False, 500).to_json(), 500


@app.errorhandler(405)
def method_not_allowed(e):
    return Response("Method not allowed. Check for correct request type (GET, POST, PUT, DELETE)", False, 405)\
               .to_json(), 405
