import random
import time
from flask import Flask
import requests

app = Flask(__name__)


def metric_generator(endpoint, return_message):
    start = time.time()
    time.sleep(random.randint(0, 6))
    code = random.choice([200, 201, 202, 404, 503, 400])
    payload = {"time": time.time() - start, "status": code, "endpoint": endpoint}
    try:
        requests.post("http://localhost:5000/metric-receiver", json=payload)
    except:
        app.logger.error("Can't push metrics")
    return return_message, code


@app.route("/show-analytics")
def show_analytics():
    return metric_generator("/show-analytics", {"result": "some analytical data"})


@app.route("/process-finances")
def process_finances():
    return metric_generator("/process-finances", {"result": "some finance data"})
