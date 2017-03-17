import pandas as pd
import pickle
import numpy as np
from sklearn.metrics import pairwise_distances

from pymongo import MongoClient
client = MongoClient('ec2-34-198-179-91.compute-1.amazonaws.com', 27017)
db = client.fletcher
dress_col = db.rtr_dresses
df_general = pd.read_csv('../../data/dress_features_norm.csv', index_col=0)
df_body = pd.read_csv('../../data/dress_features_bt.csv', index_col=0)
df_body = df_body.replace(np.nan, 0)
df_comment = pd.read_csv('../../data/comment_search.csv', index_col=0)

num_cols = ['age', 'usually_wears', 'pregnant', 'weight', 'upper_bust', 'under_bust', 'height_in']

cluster_model = pickle.load(open('../../tools/clustering_model.sav', 'rb'))
cluster_mapping = pickle.load(open('../../data/cluster_mapping.pkl', 'rb'))

def cluster(age=None, usually_wears=None, pregnant=None, weight=None, upper_bust=None, under_bust=None, height=None, body_type=None):
    body_info = np.array([age, usually_wears, pregnant, weight, upper_bust, under_bust, height])
    norm_vals = []
    for col, val in zip(num_cols, body_info):
        mapping = cluster_mapping[col]
        if not val:
            normed = 0.5
        else:
            normed = (val - mapping['min'] ) / mapping['col_range']
        if 'weight' in mapping:
            normed = normed * mapping['weight']
        norm_vals.append(normed)

    body_type_array = np.zeros(6)
    if body_type >= 0:
        body_type_array[body_type] = 1
    input = np.append(norm_vals, body_type_array)
    return cluster_model.predict(input)[0]


def get_bad_dresses(cluster):
    df_cluster = df_body[df_body.index==cluster].transpose().sort_values(by=cluster,ascending=False)
    return df_cluster[df_cluster[cluster] > 0.5].index.values


def get_general_df(df, columns):
    cur_df = df.iloc[:, columns]
    if len(columns) > 1:
        cur_df['dist'] = pairwise_distances(cur_df, [1] * len(columns), metric="cosine")
    else:
        cur_df['dist'] = pairwise_distances(cur_df, [1] * len(columns))
    return cur_df


def get_recommendations(columns, n, cluster=None):
    main_df = get_general_df(df_general, columns)
    if cluster:
        bad_dresses = get_bad_dresses(cluster)
        # penalize negatives
        main_df.loc[main_df.index.isin(bad_dresses), 'dist'] -= 0.5

    rec = []
    for url in main_df.sort_values('dist').head(n).index:
        dress = dress_col.find_one({'url': url})
        problems = get_problems(url)
        rec.append((dress['dress_name'], dress['designer_name'],
        dress['img_link'], url, problems))

    return rec

def get_comments(url, columns, n):
    cur_df = df_comment[df_comment.url == url]
    cur_df = cur_df.loc[:, columns]
    cur_df['dist'] = pairwise_distances(cur_df, [1] * len(columns), metric='cosine')
    cur_df = cur_df.sort_values('dist').head(20)
    cur_df = df_comment[df_comment.index.isin(cur_df.index)].sort_values('polarity', ascending=False).head(n)
    return list(cur_df.review.values)

df_problems = pd.read_csv('../../data/dress_problems.csv', index_col=0)
threshold = ["Some customers reported ", "A lot of customers reported "]
problems = ['zipper issues', "dress is too long",
            'that the dress is itchy', "they have trouble with bra selection",
            "dress is too short", "the cut is too low"]
def get_problems(url, bottom_threshold=0.3, high_threshold=0.6):
    problem_list = []
    for i, val in enumerate(df_problems[df_problems.index == url].values[0]):
        if val > high_threshold:
            problem_list.append(threshold[0] + problems[i])
        elif val > bottom_threshold:
            problem_list.append(threshold[1] + problems[i])
    return problem_list
