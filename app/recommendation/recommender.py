import flask
import numpy as np
import pandas as pd
import pickle
import bust_size
import recmodel

# Initialize the app
app = flask.Flask(__name__, static_url_path='')

# @app.route('/js/<path:path>')
# def send_js(path):
#     return flask.send_from_directory('js', path)

# clustering model
clustering_model = pickle.load(open('../../tools/clustering_model.sav', 'rb'))
cluster_mapping = pickle.load(open('../../data/cluster_mapping.pkl', 'rb'))
imgs = ['https://pc-ap.renttherunway.com/productimages/nomodel/1080x/a8/BM347.jpg',
 'https://pc-ap.renttherunway.com/productimages/nomodel/1080x/42/JS84.jpg',
 'https://pc-ap.renttherunway.com/productimages/front/1080x/f4/SW112.jpg',
 'https://pc-ap.renttherunway.com/productimages/nomodel/1080x/4a/BM53.jpg']
CLUSTER_COLUMNS = ['age', 'usually_wears', 'pregnant', 'weight', 'upper_bust',
       'under_bust', 'height_in', 'body_type[T.Athletic]',
       'body_type[T.Full Bust]', 'body_type[T.Hourglass]', 'body_type[T.Pear]',
       'body_type[T.Petite]', 'body_type[T.Straight & narrow]']

name_dict = ['back', 'bra', 'color', 'material', 'sequins', 'sequins',
 'wedding', 'pockets']
column_names = []

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
    print(data)
    cluster_no = None
    # if int(data["body-info"]) == 1:
    #     # find which cluster
    #     # find dataframe
    #     cup = bust_size.get_cup_letter(data["bra"])
    #     band_size = bust_size.get_band_size(data["bra"])
    #     upper_bust = None
    #     under_bust = None
    #     if cup and band_size:
    #         upper_bust = bust_size.get_upper_bust(cup, band_size)
    #         under_bust = bust_size.get_under_bust(band_size)
    #
    #     cluster_no = recmodel.cluster(age=int(data["age"]),
    #         usually_wears=int(data["usually-wears"]), pregnant=0,
    #         weight=int(data["weight"]), upper_bust=upper_bust,
    #         under_bust=under_bust, height=int(data["height"]),
    #         body_type=int(data["body-type"]))
    columns = [i for i, x in enumerate(data["preferences"].split(',')) if int(x) == 1]
    print(columns)
    dresses = recmodel.get_recommendations(columns, 4, None)
    results = {"dresses": dresses}
    print(results)
    return flask.jsonify(results)

@app.route("/labels", methods=["GET"])
def labels():
    """
    When A POST request with json data is made to this uri,
    Read the example from the json, predict dress that is best suited.
    """
    data = ['cool back', 'no bra issues', 'eye-popping color',
    'comfort is key', 'nothing itchy, please!', 'i like it sparkly',
      'wedding material', 'pockets wanted'];
    return flask.jsonify(data)

@app.route("/body_types", methods=["GET"])
def body_types():
    data = [('Athletic', 0),
             ('Full Bust', 1),
             ('Hour Glass', 2),
             ('Pear', 3),
             ('Petite', 4),
             ('Straight & Narrow', 5),
             ('Apple', -1)];
    return flask.jsonify(data)

@app.route("/comments", methods=["POST"])
def comments():
    data = flask.request.json
    columns = [i for i, x in enumerate(data["columns"].split(',')) if int(x) == 1]
    column_names = set([name_dict[i] for i in columns])
    reviews = recmodel.get_comments(data["url"], column_names, 5)
    return flask.jsonify(reviews)

#--------- RUN WEB APP SERVER ------------#

# Start the app server on port 80
# (The default website port)
app.run(host='0.0.0.0')
