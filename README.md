# RTR

## Goal
I would like to make a recommendation system for dresses that are in rent the runway through analysis of comments.

1. [Gathering data](scraping/scraping-rtr.ipynb)
2. [Clustering](model/clustering.ipynb)
3. [Topic Modelling](model/topic-modelling.ipynb)

## Tools
1. [Bust size mapping](tools/bust_size_mapping.ipynb)
    - mapping conventional bra sizes (e.g. 34B) to under bust to upper bust measurements.

## Approach
- Select which topics are dress related vs people related.
- Cluster on similar dresses by the dress features, or the cluster of people they attract.
- Rate how much a comment love the dress. If they love the dress, they will love similar dresses too.
- If they input body data, recommend what people with the same body cluster love. 
