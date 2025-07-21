import pandas as pd
from utils import get_tfidf_similarity, filter_products
from sklearn.neighbors import NearestNeighbors

def get_content_based(products_df, category=None, skin_type=None):
    filtered = filter_products(products_df, category, skin_type)
    return filtered.sort_values(by='rating', ascending=False).head(10)


def get_collaborative(products_df, reviews_df):
    pivot = reviews_df.pivot_table(index='author_id', columns='product_id', values='rating')
    pivot.fillna(0, inplace=True)
    
    model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
    model_knn.fit(pivot)
    
    sample_user = pivot.sample(1)
    distances, indices = model_knn.kneighbors(sample_user, n_neighbors=6)

    similar_users = pivot.iloc[indices.flatten()[1:]]
    similar_ratings = similar_users.mean().sort_values(ascending=False).head(10)
    top_ids = similar_ratings.index.tolist()
    
    return products_df[products_df['product_id'].isin(top_ids)]

def get_hybrid_recommendations(products_df, reviews_df, category=None, skin_type=None):
    content_df = get_content_based(products_df, category, skin_type)
    collab_df = get_collaborative(products_df, reviews_df)
    hybrid = pd.concat([content_df, collab_df]).drop_duplicates('product_id')
    return hybrid.sort_values(by='rating', ascending=False).head(10)
