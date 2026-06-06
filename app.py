import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------
# Page Configuration
# ----------------------------------
st.set_page_config(
    page_title="Industrial By-Product Matching",
    page_icon="♻️",
    layout="wide"
)

# ----------------------------------
# Load Dataset
# ----------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("industrial_waste_images_csv.zip")

df = load_data()

# ----------------------------------
# Title
# ----------------------------------
st.title("♻️ Industrial By-Product B2B Matching Dashboard")

st.markdown("""
This dashboard helps industries identify reusable waste materials
and potential business matching opportunities.
""")

# ----------------------------------
# Dataset Preview
# ----------------------------------
st.subheader("Dataset Preview")
st.dataframe(df.head())

# ----------------------------------
# KPIs
# ----------------------------------
col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Records",
    len(df)
)

col2.metric(
    "Waste Categories",
    df["waste_type"].nunique()
    if "waste_type" in df.columns else "-"
)

col3.metric(
    "Industries",
    df["industry"].nunique()
    if "industry" in df.columns else "-"
)

st.divider()

# ----------------------------------
# Waste Distribution
# ----------------------------------
if "waste_type" in df.columns:

    st.subheader("Waste Type Distribution")

    waste_count = (
        df["waste_type"]
        .value_counts()
        .reset_index()
    )

    waste_count.columns = ["Waste Type", "Count"]

    fig = px.bar(
        waste_count,
        x="Waste Type",
        y="Count",
        color="Count"
    )

    st.plotly_chart(fig, use_container_width=True)

# ----------------------------------
# Industry Distribution
# ----------------------------------
if "industry" in df.columns:

    st.subheader("Industry Distribution")

    fig2 = px.pie(
        df,
        names="industry",
        title="Industry Share"
    )

    st.plotly_chart(fig2, use_container_width=True)

# ----------------------------------
# Simple B2B Matching
# ----------------------------------
st.subheader("Find Matching Industries")

if "waste_type" in df.columns:

    selected_waste = st.selectbox(
        "Select Waste Type",
        sorted(df["waste_type"].dropna().unique())
    )

    matches = df[
        df["waste_type"] == selected_waste
    ]

    st.write("Potential Buyers / Sellers")

    st.dataframe(matches)

# ----------------------------------
# Statistics
# ----------------------------------
st.subheader("Summary Statistics")
st.write(df.describe(include="all"))
