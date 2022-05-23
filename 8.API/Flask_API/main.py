from logging.config import dictConfig
from flask import Flask, request, jsonify

app = Flask(__name__)
dictConfig({
    "version": 1,
    "formatters": {"default": {
        "format": '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    }},
    "handlers": {
        "wsgi": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "default",
        }
    },
    "root": {
      "level": "DEBUG",
      "handlers": ['wsgi']
    }
})

COURSES = {}


@app.route("/")
def hello_world():
    return "Hello world\n"


# string/int/float/path/uuid
@app.route("/course/<course_name>", methods=["GET", "DELETE"])
def show_course_by_name(course_name):
    if request.method == "GET":
        app.logger.info(request.args)
        app.logger.info(request.headers)
        app.logger.info(request.cookies)
        return COURSES[course_name]
    if request.method == "DELETE":
        del COURSES[course_name]
        return jsonify({"status": "ok"})


@app.route("/course", methods=["PUT"])
def create_course():
    app.logger.info(request.get_data())
    app.logger.info(request.is_json)
    payload = request.json
    app.logger.info(type(payload))
    COURSES[payload["name"]] = payload["desc"]
    return jsonify({"status": "ok"})
