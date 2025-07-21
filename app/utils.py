from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# Compute similarity between product names using TF-IDF and cosine similarity
def get_tfidf_similarity(products_df):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(products_df['product_name'].fillna(""))
    return cosine_similarity(tfidf_matrix)

# Filter products by category and skin type
def filter_products(products_df, category=None, skin_type=None):
    filtered = products_df.copy()
    
    if category:
        filtered = filtered[filtered['primary_category'] == category]
    
    if skin_type and 'skin_type_compatibility' in filtered.columns:
        filtered = filtered[filtered['skin_type_compatibility'].str.contains(skin_type, na=False, case=False)]
    
    return filtered
