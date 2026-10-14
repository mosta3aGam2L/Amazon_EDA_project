from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

st.set_page_config(page_title="Amazon India Dashboard", page_icon="📊", layout="wide")

# ---------------------------------------------------------
# Settings
# ---------------------------------------------------------
# Change this path to where your file is.
DEFAULT_FILE = Path(r"F:\Amazon_EDA_project\notebooks\amazon_clean_for_powerbi (1).xlsx")

REQUIRED = [
    "product_id", "product_name", "main_category", "sub_category",
    "discounted_price", "actual_price", "discount_pct", "rating",
    "rating_count",
]
NUMERIC = ["discounted_price", "actual_price", "discount_pct", "rating", "rating_count"]

TEAL, AMBER, CORAL = "#0E7C86", "#E8A317", "#C8404F"


# ---------------------------------------------------------
# Data loading and cleaning
# ---------------------------------------------------------
def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in NUMERIC:
        # Works on raw values like "₹1,099" or "64%" and on already-clean numbers
        df[col] = pd.to_numeric(
            df[col].astype(str).str.replace(r"[₹,%]", "", regex=True),
            errors="coerce",
        )
    df.loc[df["rating"] > 5, "rating"] = float("nan")  # invalid ratings
    df = df.drop_duplicates("product_id")
    return df


def read_file(source) -> pd.DataFrame:
    name = getattr(source, "name", str(source)).lower()
    df = pd.read_csv(source) if name.endswith(".csv") else pd.read_excel(source)
    return df


@st.cache_data
def load_from_path(path: str) -> pd.DataFrame:
    return clean(read_file(path))


try:
    df = load_from_path(str(DEFAULT_FILE))
except Exception as e:  # noqa: BLE001
    st.error(f"Error loading the dataset: {e}")
    st.stop()

missing = [c for c in REQUIRED if c not in df.columns]
if missing:
    st.error(f"Missing columns in the file: {missing}")
    st.stop()

# ---------------------------------------------------------
# Header
# ---------------------------------------------------------
st.title("📊 Amazon Products Dashboard")
st.caption(
    "Prices in $. The dataset has no sales figures, so **rating_count** is used "
    "as a proxy for how much a product is bought."
)

# ---------------------------------------------------------
# Sidebar filters
# ---------------------------------------------------------
st.sidebar.header("🔍 Filters")

cats = sorted(df["main_category"].dropna().unique())
sel_cats = st.sidebar.multiselect("Main category", cats, default=cats)

subs = sorted(df[df["main_category"].isin(sel_cats)]["sub_category"].dropna().unique())
sel_subs = st.sidebar.multiselect("Sub category (empty = all)", subs)

min_rating = st.sidebar.slider("Minimum rating", 0.0, 5.0, 0.0, 0.1)

p_min, p_max = int(df["discounted_price"].min()), int(df["discounted_price"].max())
price_range = st.sidebar.slider("Price range ($)", p_min, p_max, (p_min, p_max))

min_reviews = st.sidebar.number_input("Minimum number of ratings", min_value=0, value=0, step=100)
search = st.sidebar.text_input("Search product name")

mask = df["main_category"].isin(sel_cats)
if sel_subs:
    mask &= df["sub_category"].isin(sel_subs)
if min_rating > 0:
    mask &= df["rating"] >= min_rating
mask &= df["discounted_price"].between(*price_range)
if min_reviews > 0:
    mask &= df["rating_count"] >= min_reviews
if search.strip():
    mask &= df["product_name"].str.contains(search.strip(), case=False, na=False, regex=False)

f = df[mask]

if f.empty:
    st.warning("No products match the current filters.")
    st.stop()

# ---------------------------------------------------------
# KPIs
# ---------------------------------------------------------
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Products", f"{len(f):,}")
k2.metric("Avg discount", f"{f['discount_pct'].mean():.1f}%")
k3.metric("Avg rating", f"{f['rating'].mean():.2f} / 5")
k4.metric("Total ratings", f"{int(f['rating_count'].sum()):,}")
k5.metric("Median price", f"₹{f['discounted_price'].median():,.0f}")

st.markdown("---")

# ---------------------------------------------------------
# Charts
# ---------------------------------------------------------
c1, c2 = st.columns(2)

with c1:
    st.subheader("Top sub-categories")
    sub = f["sub_category"].value_counts().head(10).reset_index()
    sub.columns = ["sub_category", "Products"]
    fig = px.bar(sub, x="Products", y="sub_category", orientation="h",
                 color_discrete_sequence=[TEAL], text="Products")
    fig.update_layout(yaxis={"categoryorder": "total ascending", "title": ""},
                      margin=dict(l=0, r=0, t=10, b=0), height=380)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("Rating distribution")
    fig = px.histogram(f.dropna(subset=["rating"]), x="rating", nbins=30,
                       color_discrete_sequence=[AMBER])
    fig.update_layout(xaxis_title="Rating", yaxis_title="Products",
                      margin=dict(l=0, r=0, t=10, b=0), height=380, bargap=0.05)
    st.plotly_chart(fig, use_container_width=True)

c3, c4 = st.columns(2)

with c3:
    st.subheader("Price bands vs average discount")
    bins = [0, 200, 500, 1000, 2000, 5000, float("inf")]
    labels = ["<200", "200–499", "500–999", "1K–2K", "2K–5K", "5K+"]
    band = (
        f.assign(band=pd.cut(f["discounted_price"], bins=bins, labels=labels, right=False))
        .groupby("band", observed=False)
        .agg(Products=("product_id", "count"), AvgDiscount=("discount_pct", "mean"))
        .reset_index()
    )
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_bar(x=band["band"], y=band["Products"], name="Products", marker_color=TEAL)
    fig.add_trace(
        go.Scatter(x=band["band"], y=band["AvgDiscount"], name="Avg discount %",
                   mode="lines+markers", line=dict(color=CORAL)),
        secondary_y=True,
    )
    fig.update_yaxes(title_text="Products", secondary_y=False)
    fig.update_yaxes(title_text="Avg discount %", range=[0, 100], secondary_y=True)
    fig.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=380,
                      legend=dict(orientation="h", y=1.12))
    st.plotly_chart(fig, use_container_width=True)

with c4:
    st.subheader("Most rated products (≈ best sellers)")
    # Variants of the same product share the same rating count, so keep one of each
    top = (
        f.dropna(subset=["rating_count"])
        .sort_values("rating_count", ascending=False)
        .drop_duplicates("rating_count")
        .head(10)
        .copy()
    )
    top["short_name"] = top["product_name"].str.slice(0, 38) + "…"
    fig = px.bar(top, x="rating_count", y="short_name", orientation="h",
                 color_discrete_sequence=[AMBER], hover_name="product_name",
                 hover_data={"short_name": False, "rating": True})
    fig.update_layout(yaxis={"categoryorder": "total ascending", "title": ""},
                      xaxis_title="Number of ratings",
                      margin=dict(l=0, r=0, t=10, b=0), height=380)
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Discount vs rating")
fig = px.scatter(
    f.dropna(subset=["rating"]), x="discount_pct", y="rating", color="main_category",
    hover_name="product_name", opacity=0.5,
    labels={"discount_pct": "Discount %", "rating": "Rating"},
)
fig.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=380)
st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------
# Table + download
# ---------------------------------------------------------
st.markdown("---")
st.subheader("Products table")

cols = ["product_name", "main_category", "sub_category", "discounted_price",
        "actual_price", "discount_pct", "rating", "rating_count"]

st.dataframe(
    f.sort_values("rating_count", ascending=False)[cols],
    use_container_width=True,
    hide_index=True,
    column_config={
        "discounted_price": st.column_config.NumberColumn("Price ₹", format="₹%d"),
        "actual_price": st.column_config.NumberColumn("Original ₹", format="₹%d"),
        "discount_pct": st.column_config.ProgressColumn(
            "Discount", min_value=0, max_value=100, format="%d%%"),
        "rating": st.column_config.NumberColumn("Rating", format="%.1f"),
        "rating_count": st.column_config.NumberColumn("Ratings", format="%d"),
    },
)