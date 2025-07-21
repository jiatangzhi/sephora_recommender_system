import streamlit as st
import pandas as pd

@st.cache
def load_data():
    products_df = pd.read_csv("/Users/mcarmentz/Desktop/sephora_recommender_system/dataset/product_info.csv")
    reviews_df = pd.read_csv("/Users/mcarmentz/Desktop/sephora_recommender_system/dataset/skincare_products_reviews.csv")
    return products_df, reviews_df
