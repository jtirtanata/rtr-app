import flask
import numpy as np
import pandas as pd
import pickle

# Initialize the app
app = flask.Flask(__name__)
imgs = ['https://pc-ap.renttherunway.com/productimages/nomodel/1080x/a8/BM347.jpg',
 'https://pc-ap.renttherunway.com/productimages/nomodel/1080x/42/JS84.jpg',
 'https://pc-ap.renttherunway.com/productimages/front/1080x/f4/SW112.jpg',
 'https://pc-ap.renttherunway.com/productimages/nomodel/1080x/4a/BM53.jpg']
# Homepage
@app.route("/")
def viz_page():
    """
    Homepage: serve our visualization page, awesome.html
    """
    with open("index.html", 'r') as viz_file:
        return viz_file.read()

@app.route("/rec", methods=["POST"])
def rec():
    """
    When A POST request with json data is made to this uri,
    Read the example from the json, predict dress that is best suited.
    """
    data = flask.request.json
    inputs = [int(x) for x in data["inputs"].split(',')]
    print(inputs)
    for i, val in enumerate(inputs):
        if val == 1:
            print(i)
    results = {"imgs": imgs}
    return flask.jsonify(results)

@app.route("/labels", methods=["GET"])
def labels():
    """
    When A POST request with json data is made to this uri,
    Read the example from the json, predict dress that is best suited.
    """
    data = ['Nothing itchy, please!', 'I like it sparkly',
     'No bra issues', 'Beautiful back design', 'Comfortable'];
    return flask.jsonify(data)

#--------- RUN WEB APP SERVER ------------#

# Start the app server on port 80
# (The default website port)
app.run(host='0.0.0.0')
