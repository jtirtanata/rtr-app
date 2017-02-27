import flask
import numpy as np
import pandas as pd
import pickle

# Initialize the app
app = flask.Flask(__name__)
with open('body_data.pkl', 'rb') as f:
    data_list = pickle.load(f)

# Homepage
@app.route("/")
def viz_page():
    """
    Homepage: serve our visualization page, awesome.html
    """
    with open("index.html", 'r') as viz_file:
        return viz_file.read()

# Get an example and return it's score from the predictor model
@app.route("/data", methods=["POST"])
def data():
    """
    When A POST request with json data is made to this uri,
    Read the example from the json, predict probability and
    send it with a response
    """
    # Get decision score for our example that came with the request
    data = flask.request.json
    x = np.matrix(data["cluster_no"])
    # Put the result in a nice dict so we can send it as json
    results = {"data": str(data_list)}
    return flask.jsonify(results)

#--------- RUN WEB APP SERVER ------------#

# Start the app server on port 80
# (The default website port)
# app.run(host='0.0.0.0')
app.run(debug=True)
