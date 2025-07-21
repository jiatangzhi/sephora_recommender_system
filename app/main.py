import streamlit as st
from recommender import get_hybrid_recommendations
from data_loader import load_data

# Page config
st.set_page_config(page_title="Sephora Recommender", layout="centered")

# Inject girly aesthetic CSS
st.markdown("""
    <style>
    /* Background & font */
    body, .stApp {
        background-color: #1e1b2e;
        font-family: 'Helvetica Neue', sans-serif;
        color: #f4d5e0;
    }

    /* Headers */
    h1 {
        color: #d896d8; /* Rosa bebé profundo para títulos principales */
    }
    h2 {
        color: #caa9e0; /* Lila suave para subtítulos */
    }
    h3 {
        color: #f4d5e0; /* Rosa claro pastel para secciones pequeñas */
    }


    /* Product containers */
    .product-container {
        background-color: #2c2340;
        border-radius: 15px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 12px rgba(218, 182, 252, 0.15);
    }

    /* Buttons */
    button[kind="secondary"], button[kind="primary"] {
        background-color: #d896d8;
        color: #1e1b2e;
        border-radius: 10px;
        border: none;
        font-weight: bold;
    }
    button:hover {
        background-color: #bf7fbf !important;
        color: white !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: light-green;
        border-right: 1px solid #6e4b8f;
    }

    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(to right, #f4d5e0, #6e4b8f, #f4d5e0);
    }

    /* Markdown / text tweaks */
    .markdown-text-container {
        font-size: 15px;
        line-height: 1.6;
    }

    </style>
""", unsafe_allow_html=True)

def caption_white(text):
    st.markdown(f"<span style='color: white;'>{text}</span>", unsafe_allow_html=True)

# Init session state
if 'comment_page' not in st.session_state:
    st.session_state.comment_page = 0

# Load data
products_df, reviews_df = load_data()

# Main view (Recommendation List)
if 'selected_product_id' not in st.session_state:
    st.title("💄 Sephora Recommender System")

    # Filters
    skin_types = reviews_df['skin_type'].dropna().unique().tolist()
    primary_categories = products_df['primary_category'].dropna().unique().tolist()

    with st.sidebar:
        st.header("🔍 Filter Products")
        selected_category = st.selectbox("Select Product Category", sorted(primary_categories))
        selected_skin_type = st.selectbox("Select Your Skin Type", sorted(skin_types))

    # Recommendations
    recommendations = get_hybrid_recommendations(products_df, reviews_df, selected_category, selected_skin_type)

    st.subheader("🔥 Recommended Products")

    if not recommendations.empty:
        for _, row in recommendations.iterrows():
            st.markdown(f"### {row['product_name']}")
            caption_white(f"⭐️ Rating: {row['rating']:.2f} | ❤️ Likes: {row['loves_count']}")
            if st.button(f"View details for {row['product_name']}", key=row['product_id']):
                st.session_state.selected_product_id = row['product_id']
                st.experimental_rerun()
            st.markdown("---")
    else:
        st.warning("No recommendations found for the selected filters.")

# Detail view
else:
    product_id = st.session_state.selected_product_id
    product = products_df[products_df['product_id'] == product_id].iloc[0]
    product_reviews = reviews_df[reviews_df['product_id'] == product_id]

    st.title(product['product_name'])
    caption_white(f"Brand: {product['brand_name']}")
    caption_white(f"⭐️ Avg Rating: {product['rating']:.2f} | ❤️ Likes: {product['loves_count']}")

    # Reviews
    st.subheader("💬 Customer Reviews")
    comments_per_page = 5
    start = st.session_state.comment_page * comments_per_page
    end = start + comments_per_page

    # Show reviews
    if not product_reviews.empty:
        for _, row in product_reviews.iloc[start:end].iterrows():
            st.markdown(f"**👤 {row['author_id']}** says:")
            st.write(f"*“{row['review_text'].strip()}”*")
            st.markdown("---")
    else:
        st.info("No reviews available for this product.")

    # Pagination
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅️ Previous") and st.session_state.comment_page > 0:
            st.session_state.comment_page -= 1
            st.experimental_rerun()
    with col2:
        if st.button("Next ➡️") and end < len(product_reviews):
            st.session_state.comment_page += 1
            st.experimental_rerun()

    # Suggested Products
    st.subheader("🛍️ You might also like")
    similar_products = get_hybrid_recommendations(
        products_df, reviews_df, product['primary_category'], None
    )

    for _, rec in similar_products.head(5).iterrows():
        st.markdown(f"**{rec['product_name']}** — *{rec['brand_name']}* ⭐️ {rec['rating']:.2f}")

    # Back button
    if st.button("🔙 Back to Recommendations"):
        del st.session_state['selected_product_id']
        st.session_state.comment_page = 0
        st.experimental_rerun()
