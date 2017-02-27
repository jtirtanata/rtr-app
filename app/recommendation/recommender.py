import flask
import numpy as np
import pandas as pd
import pickle
import bust_size

# Initialize the app
app = flask.Flask(__name__)

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
    # find which cluster
    # find dataframe

    print(data)
    cup = bust_size.get_cup_letter(data["bra"])
    band_size = bust_size.get_band_size(data["bra"])
    upper_bust = None
    under_bust = None
    if cup and band_size:
        upper_bust = bust_size.get_upper_bust(cup, band_size)
        under_bust = bust_size.get_under_bust(band_size)
    body_type = [0] * 6
    bt_no = int(data["body-type"])
    if bt_no >= 0:
        body_type[bt_no] = 1
    cluster_X = [int(data["age"]), int(data["usually-wears"]), 0, int(data["weight"]),
                upper_bust, under_bust, int(data["height"])] + body_type

    norm_vals = []
    for col, val in zip(CLUSTER_COLUMNS, cluster_X):
        mapping = cluster_mapping[col]
        if not val:
            normed = 0.5
        else:
            normed = (val - mapping['min'] ) / mapping['col_range']
        if 'weight' in mapping:
            normed = normed * mapping['weight']
        norm_vals.append(normed)

    cluster_no = clustering_model.predict(norm_vals)
    print(norm_vals)
    print(cluster_no)
    # inputs = [int(x) for x in data["preferences"].split(',')]
    # print(inputs)
    # for i, val in enumerate(inputs):
    #     if val == 1:
    #         print(i)

    # results = {"imgs": imgs}
    return flask.jsonify(cluster_X)

@app.route("/labels", methods=["GET"])
def labels():
    """
    When A POST request with json data is made to this uri,
    Read the example from the json, predict dress that is best suited.
    """
    data = ['Nothing itchy, please!', 'I like it sparkly',
     'No bra issues', 'Beautiful back design', 'Comfortable'];
    return flask.jsonify(data)

@app.route("/body_types", methods=["GET"])
def body_types():
    data = [('Athletic', 0),
             ('Full Bust', 1),
             ('Hour Glass', 2),
             ('Pear', 3),
             ('Petite', 4),
             ('Straight & Narros', 5),
             ('Apple', -1)];
    return flask.jsonify(data)

#--------- RUN WEB APP SERVER ------------#

# Start the app server on port 80
# (The default website port)
app.run(host='0.0.0.0')
