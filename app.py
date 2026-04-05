import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from pathlib import Path

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="FoodExpress Analytics Dashboard",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown("""
<style>
    :root {
        --bg-main: #07111f;
        --bg-shell: radial-gradient(circle at top, rgba(34, 211, 238, 0.14), transparent 26%), linear-gradient(180deg, #07111f 0%, #09182a 46%, #050c17 100%);
        --panel-bg: linear-gradient(180deg, rgba(14, 25, 44, 0.92) 0%, rgba(9, 17, 31, 0.88) 100%);
        --panel-border: rgba(96, 165, 250, 0.18);
        --panel-glow: 0 18px 44px rgba(2, 6, 23, 0.46);
        --text-main: #e5eefc;
        --text-soft: #9fb3d1;
        --text-muted: #7d93b4;
        --cyan: #22d3ee;
        --blue: #3b82f6;
        --violet: #8b5cf6;
        --amber: #f59e0b;
        --emerald: #34d399;
    }

    .stApp {
        background: var(--bg-shell);
        color: var(--text-main);
    }

    .main {
        background: transparent;
    }

    .block-container {
        padding-top: 1.4rem;
        padding-bottom: 2.4rem;
        max-width: 1440px;
    }

    h1, h2, h3, label, p, li, span, div {
        color: inherit;
    }

    .hero-box {
        position: relative;
        overflow: hidden;
        background:
            radial-gradient(circle at top right, rgba(34, 211, 238, 0.24), transparent 26%),
            radial-gradient(circle at left center, rgba(139, 92, 246, 0.2), transparent 20%),
            linear-gradient(135deg, rgba(13, 25, 46, 0.98) 0%, rgba(9, 19, 34, 0.94) 52%, rgba(8, 16, 28, 0.94) 100%);
        padding: 42px 40px;
        border-radius: 28px;
        color: white;
        margin-bottom: 22px;
        width: 100%;
        display: block;
        border: 1px solid rgba(96, 165, 250, 0.22);
        box-shadow: 0 24px 64px rgba(2, 6, 23, 0.48);
        text-align: center;
    }

    .hero-box::before {
        content: "";
        position: absolute;
        inset: 0;
        background: linear-gradient(90deg, rgba(59, 130, 246, 0.18), rgba(139, 92, 246, 0.12), rgba(34, 211, 238, 0.18));
        opacity: 0.8;
        pointer-events: none;
    }

    .hero-box::after {
        content: "";
        position: absolute;
        inset: 14px;
        border-radius: 22px;
        border: 1px solid rgba(191, 219, 254, 0.08);
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.05);
        pointer-events: none;
    }

    .hero-kicker,
    .hero-title,
    .hero-subtitle {
        position: relative;
        z-index: 1;
    }

    .hero-kicker {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        padding: 8px 16px;
        margin-bottom: 14px;
        border-radius: 999px;
        background: rgba(11, 22, 40, 0.62);
        border: 1px solid rgba(96, 165, 250, 0.2);
        color: #b8d6ff;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.24em;
        text-transform: uppercase;
        box-shadow: 0 0 22px rgba(59, 130, 246, 0.14);
    }

    .hero-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 12px;
        letter-spacing: 0.01em;
        line-height: 1.08;
        text-shadow: 0 0 30px rgba(96, 165, 250, 0.34);
    }

    .hero-subtitle {
        font-size: 15px;
        color: #cfe0ff;
        line-height: 1.8;
        max-width: 840px;
        margin: 0 auto;
    }

    .section-title {
        font-size: 22px;
        font-weight: 700;
        color: var(--text-main);
        margin-top: 12px;
        margin-bottom: 14px;
        letter-spacing: 0.04em;
    }

    .metric-card,
    .insight-box,
    div[data-testid="stPlotlyChart"],
    div[data-testid="stDataFrame"],
    div[data-testid="stAlert"] {
        background: var(--panel-bg);
        border: 1px solid var(--panel-border);
        box-shadow: var(--panel-glow);
        backdrop-filter: blur(16px);
    }

    .metric-card {
        padding: 18px 18px;
        border-radius: 22px;
        margin-bottom: 12px;
        position: relative;
        overflow: hidden;
    }

    .metric-card::before {
        content: "";
        position: absolute;
        inset: 0 auto auto 0;
        width: 100%;
        height: 3px;
        background: linear-gradient(90deg, var(--blue), var(--violet), var(--cyan));
        opacity: 0.95;
    }

    .metric-label {
        font-size: 12px;
        color: var(--text-soft);
        margin-bottom: 8px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.18em;
    }

    .metric-value {
        font-size: 30px;
        font-weight: 800;
        color: #f8fbff;
        line-height: 1.1;
        text-shadow: 0 0 16px rgba(59, 130, 246, 0.22);
    }

    .metric-delta {
        font-size: 12px;
        color: var(--emerald);
        margin-top: 7px;
        font-weight: 600;
        letter-spacing: 0.04em;
    }

    .insight-box {
        border-radius: 18px;
        padding: 18px 20px;
        margin-bottom: 14px;
        border-left: 1px solid rgba(139, 92, 246, 0.3);
        position: relative;
        overflow: hidden;
    }

    .insight-box::before {
        content: "";
        position: absolute;
        left: 0;
        top: 16px;
        bottom: 16px;
        width: 4px;
        border-radius: 999px;
        background: linear-gradient(180deg, var(--cyan), var(--violet));
        box-shadow: 0 0 18px rgba(34, 211, 238, 0.35);
    }

    .insight-title {
        font-size: 15px;
        font-weight: 700;
        color: #f3f7ff;
        margin-bottom: 7px;
        padding-left: 8px;
    }

    .insight-text {
        font-size: 14px;
        color: var(--text-soft);
        line-height: 1.7;
        padding-left: 8px;
    }

    div[data-testid="stSidebar"] {
        background:
            radial-gradient(circle at top, rgba(34, 211, 238, 0.16), transparent 30%),
            linear-gradient(180deg, #0b1324 0%, #101c33 100%);
        border-right: 1px solid rgba(96, 165, 250, 0.14);
    }

    div[data-testid="stSidebar"] * {
        color: #e5eefc !important;
    }

    .sidebar-brand {
        background:
            radial-gradient(circle at top right, rgba(45,212,191,0.12), transparent 34%),
            linear-gradient(180deg, rgba(35, 72, 89, 0.96) 0%, rgba(26, 49, 76, 0.98) 100%);
        border: 1px solid rgba(96,165,250,0.16);
        border-radius: 20px;
        padding: 18px 16px 16px 16px;
        margin-bottom: 16px;
        box-shadow: 0 20px 36px rgba(2, 6, 23, 0.32);
    }

    .sidebar-brand-logo {
        font-size: 28px;
        line-height: 1;
        margin-bottom: 10px;
        display: block;
    }

    .sidebar-brand-title {
        font-size: 15px;
        font-weight: 800;
        color: #f8fafc !important;
        margin-bottom: 6px;
    }

    .sidebar-brand-tag {
        display: inline-block;
        font-size: 9px;
        text-transform: uppercase;
        letter-spacing: 0.16em;
        color: #78f0d9 !important;
        background: rgba(45,212,191,0.12);
        border: 1px solid rgba(45,212,191,0.18);
        padding: 3px 8px;
        border-radius: 999px;
        font-weight: 800;
        margin-bottom: 10px;
    }

    .sidebar-brand-subtitle {
        font-size: 11px;
        line-height: 1.65;
        color: #c3d6ee !important;
    }

    .sidebar-filter-title {
        font-size: 13px;
        font-weight: 800;
        color: #f8fafc !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-top: 4px;
        margin-bottom: 2px;
    }

    .sidebar-filter-subtitle {
        font-size: 11px;
        color: #7f93b2 !important;
        margin-bottom: 10px;
    }

    .sidebar-filter-label {
        font-size: 11px;
        font-weight: 800;
        color: #93a4be !important;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-bottom: 8px;
        margin-top: 14px;
    }

    .toggle-btn.active {
        background: linear-gradient(135deg, #0f766e 0%, #0d9488 100%);
        border-color: #14b8a6;
        color: #ffffff !important;
        box-shadow: 0 3px 10px rgba(14,165,136,0.35);
    }

    div[data-testid="stSidebar"] div[data-testid="stButton"] > button {
        min-height: 40px;
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.06);
        background: #0a0f18;
        color: #cbd5e1 !important;
        font-weight: 700;
        font-size: 12px;
        letter-spacing: 0.02em;
        box-shadow: none;
        transition: all 0.18s ease;
    }

    div[data-testid="stSidebar"] div[data-testid="stButton"] > button:hover {
        border-color: rgba(255,255,255,0.1);
        color: #ffffff !important;
        transform: translateY(-1px);
        box-shadow: 0 10px 18px rgba(2, 6, 23, 0.22);
    }

    div[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="primary"] {
        background: linear-gradient(180deg, #ff6668 0%, #ff4f57 100%);
        border-color: rgba(255, 133, 140, 0.4);
        color: #ffffff !important;
        box-shadow: 0 10px 20px rgba(255, 79, 87, 0.26);
    }

    div[data-testid="stSidebar"] [data-baseweb="select"] > div,
    div[data-testid="stSidebar"] input,
    div[data-testid="stSidebar"] textarea,
    div[data-testid="stSidebar"] [data-baseweb="input"] > div {
        background: rgba(10, 19, 34, 0.88) !important;
        border: 1px solid rgba(96, 165, 250, 0.2) !important;
        border-radius: 14px !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(6, 14, 26, 0.52);
        border: 1px solid rgba(96, 165, 250, 0.12);
        border-radius: 18px;
        padding: 8px;
        margin-bottom: 16px;
    }

    .stTabs [data-baseweb="tab"] {
        background: #1e293b;
        border-radius: 12px;
        border: 1px solid rgba(148,163,184,0.15);
        padding: 10px 16px;
        font-weight: 700;
        color: #94a3b8 !important;
    }

    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: #0f766e !important;
        border-color: #0d9488 !important;
        color: #ffffff !important;
    }

    .stTabs [data-baseweb="tab-highlight"] {
        background: transparent !important;
    }

    .stTabs [data-baseweb="tab-border"] {
        background: rgba(148,163,184,0.10) !important;
    }

    /* Fix Streamlit's default white main area blocks */
    .stMainBlockContainer, [data-testid="stAppViewContainer"] > .main {
        background: transparent !important;
    }

    /* Dataframe dark theme */
    [data-testid="stDataFrame"] {
        background: #1e293b;
        border-radius: 12px;
        border: 1px solid rgba(148,163,184,0.12);
    }

    .cred-card {
        background:
            radial-gradient(circle at top right, rgba(45,212,191,0.10), transparent 38%),
            linear-gradient(180deg, rgba(18, 26, 44, 0.98) 0%, rgba(11, 18, 32, 0.98) 100%);
        border: 1px solid rgba(96,165,250,0.18);
        border-radius: 18px;
        padding: 16px 14px 14px 14px;
        margin-top: 14px;
        box-shadow: 0 16px 28px rgba(2, 6, 23, 0.28);
    }

    .cred-label {
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 0.18em;
        color: #7dd3fc !important;
        font-weight: 800;
        margin-bottom: 10px;
    }

    .cred-name {
        font-size: 15px;
        font-weight: 800;
        color: #f8fafc !important;
        margin-bottom: 4px;
    }

    .cred-link {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 12px;
        color: #cbd5e1 !important;
        text-decoration: none;
        padding: 8px 10px;
        border-radius: 10px;
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.06);
        margin-bottom: 8px;
    }

    .cred-link:hover {
        background: rgba(255,255,255,0.08);
        border-color: rgba(96,165,250,0.22);
        color: #ffffff !important;
    }
             
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.24), rgba(139, 92, 246, 0.22)) !important;
        color: #f8fbff !important;
        box-shadow: inset 0 0 0 1px rgba(96, 165, 250, 0.24), 0 10px 24px rgba(2, 6, 23, 0.32);
    }

    div[data-testid="stPlotlyChart"],
    div[data-testid="stDataFrame"] {
        border-radius: 22px;
        padding: 10px 10px 2px 10px;
        margin-bottom: 14px;
    }

    div[data-testid="stDataFrame"] {
        padding-bottom: 10px;
    }

    div[data-testid="stDataFrame"] [data-testid="stDataFrameResizable"] {
        border-radius: 16px;
        overflow: hidden;
    }

    div[data-testid="stAlert"] {
        border-radius: 18px;
        color: var(--text-main);
    }

</style>
""", unsafe_allow_html=True)

# =========================================================
# HELPERS
# =========================================================
DATA_FILE = "foodexpress_data_uncleaned.csv"  # change this if your CSV name is different
CHART_TEMPLATE = "plotly_dark"

pio.templates.default = CHART_TEMPLATE


@st.cache_data
def load_data(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # ---------- Standardize column names ----------
    df.columns = [col.strip() for col in df.columns]

    # ---------- Numeric columns ----------
    numeric_cols = [
        'DeliveryTime', 'RestaurantRating', 'CustomerRating',
        'DeliveryPartnerRating', 'TipAmount', 'DeliveryDistance',
        'DiscountAmount', 'PromoDiscount', 'DeliveryFee', 'OrderValue'
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # ---------- Handle DeliveryTime placeholder ----------
    if 'DeliveryTime' in df.columns:
        valid_delivery = df.loc[df['DeliveryTime'] != 99999, 'DeliveryTime'].dropna()
        if not valid_delivery.empty:
            delivery_median = valid_delivery.median()
            df['DeliveryTime'] = df['DeliveryTime'].replace(99999, delivery_median)

    # ---------- Clean invalid strings in CustomerRating ----------
    if 'CustomerRating' in df.columns:
        df['CustomerRating'] = (
            df['CustomerRating']
            .replace(['INVALID', 'N/A', 'NA', ''], np.nan)
        )
        df['CustomerRating'] = pd.to_numeric(df['CustomerRating'], errors='coerce')

    # ---------- Fill missing numeric values with median ----------
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].median())

    # ---------- Dates ----------
    if 'OrderDate' in df.columns:
        df['OrderDate'] = pd.to_datetime(df['OrderDate'], errors='coerce')

    # ---------- String cleanup ----------
    for col in ['CuisineType', 'City', 'CustomerSegment', 'PaymentMethod']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # ---------- Remove outliers ----------
    if 'DeliveryTime' in df.columns:
        delivery_99 = df['DeliveryTime'].quantile(0.99)
        df = df[df['DeliveryTime'] <= delivery_99]

    if 'OrderValue' in df.columns:
        df = df[df['OrderValue'] >= 5]

    # ---------- Feature engineering ----------
    if {'OrderValue', 'DiscountAmount', 'PromoDiscount'}.issubset(df.columns):
        df['RestaurantCommission'] = df['OrderValue'] * 0.20
        df['TotalDiscount'] = df['DiscountAmount'].fillna(0) + df['PromoDiscount'].fillna(0)
        df['NetRevenue'] = (
            df['OrderValue']
            - df['DiscountAmount'].fillna(0)
            - df['PromoDiscount'].fillna(0)
            - df['RestaurantCommission']
        )

    if 'OrderDate' in df.columns:
        df['DayName'] = df['OrderDate'].dt.day_name()
        df['Month'] = df['OrderDate'].dt.month_name()
        df['Week'] = df['OrderDate'].dt.isocalendar().week.astype(str)
        df['DayType'] = np.where(df['OrderDate'].dt.dayofweek >= 5, 'Weekend', 'Weekday')

    if 'OrderValue' in df.columns and 'DiscountAmount' in df.columns:
        df['DiscountPercentage'] = np.where(
            df['OrderValue'] > 0,
            (df['DiscountAmount'].fillna(0) / df['OrderValue']) * 100,
            0
        )

    return df


def metric_card(label: str, value: str, delta_text: str = ""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-delta">{delta_text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def insight_card(title: str, text: str):
    st.markdown(
        f"""
        <div class="insight-box">
            <div class="insight-title">{title}</div>
            <div class="insight-text">{text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def safe_series_mean(df: pd.DataFrame, col: str):
    return df[col].mean() if col in df.columns and not df.empty else np.nan


def style_figure(fig, height: int):
    fig.update_layout(
        template=CHART_TEMPLATE,
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(9, 17, 31, 0.75)",
        font=dict(color="#dbeafe"),
        title_font=dict(size=20, color="#f8fbff"),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0,
            font=dict(color="#cbd5e1")
        ),
        margin=dict(l=24, r=24, t=64, b=28)
    )
    fig.update_xaxes(
        showgrid=False,
        linecolor="rgba(148, 163, 184, 0.22)",
        tickfont=dict(color="#9fb3d1"),
        title_font=dict(color="#dbeafe")
    )
    fig.update_yaxes(
        gridcolor="rgba(148, 163, 184, 0.16)",
        zerolinecolor="rgba(148, 163, 184, 0.12)",
        tickfont=dict(color="#9fb3d1"),
        title_font=dict(color="#dbeafe")
    )
    return fig


# =========================================================
# LOAD DATA
# =========================================================
st.markdown("""
<div class="hero-box">
    <div class="hero-kicker">Food Delivery Analytics · Executive Dashboard</div>
    <div class="hero-title">🍔 FoodExpress Analytics Dashboard</div>
    <div class="hero-subtitle">
        A professional analytics dashboard for monitoring food delivery operations,
        customer behavior, revenue performance, and service efficiency.
        Built from the FoodExpress data analysis workflow and redesigned into an
        executive-friendly interactive application.
    </div>
</div>
""", unsafe_allow_html=True)

file_path = Path(DATA_FILE)

if not file_path.exists():
    st.error(
        f"CSV file not found: `{DATA_FILE}`\n\n"
        "Place your dataset in the same folder as `app.py`, or update the `DATA_FILE` variable."
    )
    st.stop()

raw_df = load_data(DATA_FILE)
df = clean_data(raw_df)

# =========================================================
# SIDEBAR FILTERS
# =========================================================
st.sidebar.markdown("""
<div class="sidebar-brand">
    <span class="sidebar-brand-logo">🍔</span>
    <div class="sidebar-brand-title">FoodExpress BI</div>
    <div class="sidebar-brand-tag">Analytics Dashboard</div>
    <div class="sidebar-brand-subtitle">
        Decision-focused interface for operational efficiency, customer dynamics, and commercial performance.
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<div class="sidebar-filter-title">📊 Dashboard Filters</div>
<div class="sidebar-filter-subtitle">Adjust the scope of analysis</div>
""", unsafe_allow_html=True)

filtered_df = df.copy()

if 'OrderDate' in filtered_df.columns and filtered_df['OrderDate'].notna().any():
    min_date = filtered_df['OrderDate'].min().date()
    max_date = filtered_df['OrderDate'].max().date()

    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (filtered_df['OrderDate'].dt.date >= start_date) &
            (filtered_df['OrderDate'].dt.date <= end_date)
        ]

if 'City' in filtered_df.columns:
    city_options = sorted([x for x in filtered_df['City'].dropna().unique() if x != 'nan'])

    if 'selected_cities' not in st.session_state:
        st.session_state.selected_cities = set(city_options)

    st.sidebar.markdown('<div class="sidebar-filter-label">🏙️ Select City</div>', unsafe_allow_html=True)

    city_cols = st.sidebar.columns(2)
    for i, city in enumerate(city_options):
        col = city_cols[i % 2]
        is_active = city in st.session_state.selected_cities
        label = f"{'✓ ' if is_active else ''}{city}"
        btn_type = "primary" if is_active else "secondary"
        if col.button(label, key=f"city_{city}", use_container_width=True, type=btn_type):
            if city in st.session_state.selected_cities:
                if len(st.session_state.selected_cities) > 1:
                    st.session_state.selected_cities.discard(city)
            else:
                st.session_state.selected_cities.add(city)
            st.rerun()

    selected_cities = list(st.session_state.selected_cities)
    if selected_cities:
        filtered_df = filtered_df[filtered_df['City'].isin(selected_cities)]

if 'CuisineType' in filtered_df.columns:
    cuisine_options = sorted([x for x in filtered_df['CuisineType'].dropna().unique() if x != 'nan'])

    if 'selected_cuisines' not in st.session_state:
        st.session_state.selected_cuisines = set(cuisine_options)

    st.sidebar.markdown('<div class="sidebar-filter-label">🍽️ Select Cuisine Type</div>', unsafe_allow_html=True)

    cuisine_cols = st.sidebar.columns(2)
    for i, cuisine in enumerate(cuisine_options):
        col = cuisine_cols[i % 2]
        is_active = cuisine in st.session_state.selected_cuisines
        label = f"{'✓ ' if is_active else ''}{cuisine}"
        btn_type = "primary" if is_active else "secondary"
        if col.button(label, key=f"cuisine_{cuisine}", use_container_width=True, type=btn_type):
            if cuisine in st.session_state.selected_cuisines:
                if len(st.session_state.selected_cuisines) > 1:
                    st.session_state.selected_cuisines.discard(cuisine)
            else:
                st.session_state.selected_cuisines.add(cuisine)
            st.rerun()

    selected_cuisines = list(st.session_state.selected_cuisines)
    if selected_cuisines:
        filtered_df = filtered_df[filtered_df['CuisineType'].isin(selected_cuisines)]

if 'CustomerSegment' in filtered_df.columns:
    segment_options = sorted([x for x in filtered_df['CustomerSegment'].dropna().unique() if x != 'nan'])

    if 'selected_segments' not in st.session_state:
        st.session_state.selected_segments = set(segment_options)

    st.sidebar.markdown('<div class="sidebar-filter-label">👥 Customer Segment</div>', unsafe_allow_html=True)

    seg_icons = {"New Customer": "🔷", "Regular Customer": "🔷", "VIP Customer": "⭐"}
    for seg in segment_options:
        is_active = seg in st.session_state.selected_segments
        icon = seg_icons.get(seg, "•")
        label = f"{icon} {'✓ ' if is_active else ''}{seg}"
        btn_type = "primary" if is_active else "secondary"
        if st.sidebar.button(label, key=f"seg_{seg}", use_container_width=True, type=btn_type):
            if seg in st.session_state.selected_segments:
                if len(st.session_state.selected_segments) > 1:
                    st.session_state.selected_segments.discard(seg)
            else:
                st.session_state.selected_segments.add(seg)
            st.rerun()

    selected_segments = list(st.session_state.selected_segments)
    if selected_segments:
        filtered_df = filtered_df[filtered_df['CustomerSegment'].isin(selected_segments)]

st.sidebar.markdown("---")
st.sidebar.markdown(
    f"""
    <div class="sidebar-row-count">
        <span class="sidebar-row-label">🧾 Rows in View</span>
        <span class="sidebar-row-value">{len(filtered_df):,}</span>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("""
<div class="cred-card">
    <div class="cred-label">Contact</div>
    <div class="cred-name">Mir Shahadut Hossain</div>
    <a class="cred-link" href="https://www.linkedin.com/in/mir-shahadut-hossain/" target="_blank">
        <span>LinkedIn</span>
    </a>
    <a class="cred-link" href="https://github.com/doyancha" target="_blank">
        <span>GitHub</span>
    </a>
    <a class="cred-link" href="mailto:sujon6901@gmail.com">
        <span>sujon6901@gmail.com</span>
    </a>
</div>
""", unsafe_allow_html=True)


if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# =========================================================
# KPI SECTION
# =========================================================
st.markdown('<div class="section-title">Executive Summary</div>', unsafe_allow_html=True)

total_orders = len(filtered_df)
total_revenue = filtered_df['OrderValue'].sum() if 'OrderValue' in filtered_df.columns else 0
avg_order_value = filtered_df['OrderValue'].mean() if 'OrderValue' in filtered_df.columns else 0
avg_delivery_time = filtered_df['DeliveryTime'].mean() if 'DeliveryTime' in filtered_df.columns else 0
avg_customer_rating = filtered_df['CustomerRating'].mean() if 'CustomerRating' in filtered_df.columns else 0
net_revenue = filtered_df['NetRevenue'].sum() if 'NetRevenue' in filtered_df.columns else 0

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    metric_card("Total Orders", f"{total_orders:,}", "Filtered operational volume")

with col2:
    metric_card("Total Revenue", f"${total_revenue:,.2f}", "Gross order value")

with col3:
    metric_card("Avg Order Value", f"${avg_order_value:,.2f}", "Revenue per order")

with col4:
    metric_card("Avg Delivery Time", f"{avg_delivery_time:,.1f} min", "Operational efficiency")

with col5:
    metric_card("Avg Customer Rating", f"{avg_customer_rating:,.2f}", "Customer satisfaction")

col6, col7 = st.columns([1, 1])
with col6:
    metric_card("Estimated Net Revenue", f"${net_revenue:,.2f}", "After discounts and commission")
with col7:
    premium_orders = 0
    if {'DeliveryFee', 'DeliveryTime'}.issubset(filtered_df.columns):
        premium_orders = ((filtered_df['DeliveryFee'] > 5) & (filtered_df['DeliveryTime'] < 25)).sum()
    metric_card("Premium Deliveries", f"{premium_orders:,}", "High-fee fast deliveries")

# =========================================================
# TABS
# =========================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📌 Overview",
    "🚚 Operations",
    "👥 Customer Insights",
    "💰 Revenue & Data"
])

# =========================================================
# TAB 1 - OVERVIEW
# =========================================================
with tab1:
    left, right = st.columns([1.15, 0.85])

    with left:
        if 'CuisineType' in filtered_df.columns:
            cuisine_counts = (
                filtered_df['CuisineType']
                .value_counts()
                .reset_index()
            )
            cuisine_counts.columns = ['CuisineType', 'Orders']

            fig_cuisine = px.bar(
                cuisine_counts,
                x='CuisineType',
                y='Orders',
                text='Orders',
                title="Total Orders by Cuisine Type"
            )
            fig_cuisine.update_layout(
                xaxis_title="Cuisine Type",
                yaxis_title="Total Orders"
            )
            style_figure(fig_cuisine, 460)
            st.plotly_chart(fig_cuisine, use_container_width=True)

    with right:
        if 'CustomerSegment' in filtered_df.columns:
            segment_counts = (
                filtered_df['CustomerSegment']
                .value_counts()
                .reset_index()
            )
            segment_counts.columns = ['CustomerSegment', 'Count']

            fig_segment = px.pie(
                segment_counts,
                names='CustomerSegment',
                values='Count',
                hole=0.45,
                title="Customer Segment Distribution"
            )
            style_figure(fig_segment, 460)
            st.plotly_chart(fig_segment, use_container_width=True)

    trend_col, insight_col = st.columns([1.35, 0.65])

    with trend_col:
        if {'OrderDate', 'CuisineType'}.issubset(filtered_df.columns):
            daily_orders = (
                filtered_df.groupby(['OrderDate', 'CuisineType'])
                .size()
                .reset_index(name='Orders')
                .sort_values('OrderDate')
            )

            fig_daily = px.line(
                daily_orders,
                x='OrderDate',
                y='Orders',
                color='CuisineType',
                title="Daily Order Trend by Cuisine Type",
                markers=True
            )
            fig_daily.update_layout(
                xaxis_title="Order Date",
                yaxis_title="Number of Orders"
            )
            style_figure(fig_daily, 460)
            st.plotly_chart(fig_daily, use_container_width=True)

    with insight_col:
        top_cuisine = (
            filtered_df['CuisineType'].mode().iloc[0]
            if 'CuisineType' in filtered_df.columns and not filtered_df['CuisineType'].mode().empty
            else "N/A"
        )
        top_segment = (
            filtered_df['CustomerSegment'].mode().iloc[0]
            if 'CustomerSegment' in filtered_df.columns and not filtered_df['CustomerSegment'].mode().empty
            else "N/A"
        )

        insight_card(
            "Most Ordered Cuisine",
            f"<b>{top_cuisine}</b> appears to be the strongest contributor to total order volume in the filtered view."
        )

        insight_card(
            "Largest Customer Segment",
            f"<b>{top_segment}</b> currently represents the dominant user group in the selected data scope."
        )

        insight_card(
            "Operational View",
            f"The current dashboard slice contains <b>{total_orders:,}</b> orders with an average delivery time of "
            f"<b>{avg_delivery_time:.1f} minutes</b> and average order value of <b>${avg_order_value:.2f}</b>."
        )

# =========================================================
# TAB 2 - OPERATIONS
# =========================================================
with tab2:
    col_a, col_b = st.columns(2)

    with col_a:
        if 'DeliveryTime' in filtered_df.columns:
            mean_dt = filtered_df['DeliveryTime'].mean()
            median_dt = filtered_df['DeliveryTime'].median()

            fig_hist = px.histogram(
                filtered_df,
                x='DeliveryTime',
                nbins=25,
                title="Distribution of Delivery Times"
            )
            fig_hist.add_vline(x=mean_dt, line_dash="dash", annotation_text="Mean", annotation_position="top")
            fig_hist.add_vline(x=median_dt, line_dash="dot", annotation_text="Median", annotation_position="top")
            fig_hist.update_layout(
                xaxis_title="Delivery Time (minutes)",
                yaxis_title="Frequency"
            )
            style_figure(fig_hist, 440)
            st.plotly_chart(fig_hist, use_container_width=True)

    with col_b:
        if 'City' in filtered_df.columns and 'DeliveryTime' in filtered_df.columns:
            fig_box = px.box(
                filtered_df,
                x='City',
                y='DeliveryTime',
                points='outliers',
                title="Delivery Time by City"
            )
            fig_box.update_layout(
                xaxis_title="City",
                yaxis_title="Delivery Time (minutes)"
            )
            style_figure(fig_box, 440)
            st.plotly_chart(fig_box, use_container_width=True)

    col_c, col_d = st.columns([1.25, 0.75])

    with col_c:
        if {'OrderValue', 'DeliveryTime', 'CustomerSegment'}.issubset(filtered_df.columns):
            corr = filtered_df[['OrderValue', 'DeliveryTime']].corr().iloc[0, 1]

            fig_scatter = px.scatter(
                filtered_df,
                x='OrderValue',
                y='DeliveryTime',
                color='CustomerSegment',
                trendline='ols',
                title=f"Order Value vs Delivery Time (Correlation: {corr:.2f})",
                opacity=0.7
            )
            fig_scatter.update_layout(
                xaxis_title="Order Value",
                yaxis_title="Delivery Time"
            )
            style_figure(fig_scatter, 470)
            st.plotly_chart(fig_scatter, use_container_width=True)

    with col_d:
        if 'City' in filtered_df.columns and 'DeliveryTime' in filtered_df.columns:
            city_perf = (
                filtered_df.groupby('City', as_index=False)['DeliveryTime']
                .mean()
                .sort_values('DeliveryTime')
            )

            if not city_perf.empty:
                best_city = city_perf.iloc[0]['City']
                worst_city = city_perf.iloc[-1]['City']

                insight_card(
                    "Best Performing City",
                    f"<b>{best_city}</b> shows the lowest average delivery time in the selected view."
                )

                insight_card(
                    "Operational Risk Zone",
                    f"<b>{worst_city}</b> has the highest average delivery time and may require workflow optimization."
                )

                insight_card(
                    "Delivery Efficiency Insight",
                    "Higher delivery variability usually signals capacity issues, routing inefficiencies, or inconsistent preparation time."
                )

# =========================================================
# TAB 3 - CUSTOMER INSIGHTS
# =========================================================
with tab3:
    left_cust, right_cust = st.columns([1.1, 0.9])

    with left_cust:
        if {'CustomerSegment', 'OrderValue'}.issubset(filtered_df.columns):
            seg_value = (
                filtered_df.groupby('CustomerSegment', as_index=False)['OrderValue']
                .mean()
                .sort_values('OrderValue', ascending=False)
            )

            fig_seg_value = px.bar(
                seg_value,
                x='CustomerSegment',
                y='OrderValue',
                text_auto=".2f",
                title="Average Order Value by Customer Segment"
            )
            fig_seg_value.update_layout(
                xaxis_title="Customer Segment",
                yaxis_title="Average Order Value"
            )
            style_figure(fig_seg_value, 430)
            st.plotly_chart(fig_seg_value, use_container_width=True)

    with right_cust:
        if {'CustomerSegment', 'CustomerRating'}.issubset(filtered_df.columns):
            seg_rating = (
                filtered_df.groupby('CustomerSegment', as_index=False)['CustomerRating']
                .mean()
                .sort_values('CustomerRating', ascending=False)
            )

            fig_seg_rating = px.bar(
                seg_rating,
                x='CustomerSegment',
                y='CustomerRating',
                text_auto=".2f",
                title="Average Customer Rating by Segment"
            )
            fig_seg_rating.update_layout(
                xaxis_title="Customer Segment",
                yaxis_title="Average Rating"
            )
            style_figure(fig_seg_rating, 430)
            st.plotly_chart(fig_seg_rating, use_container_width=True)

    lower_left, lower_right = st.columns([1.2, 0.8])

    with lower_left:
        if {'DayType', 'OrderValue'}.issubset(filtered_df.columns):
            daytype_df = (
                filtered_df.groupby('DayType', as_index=False)
                .agg(
                    Orders=('OrderValue', 'size'),
                    AvgOrderValue=('OrderValue', 'mean')
                )
            )

            fig_daytype = go.Figure()
            fig_daytype.add_bar(
                x=daytype_df['DayType'],
                y=daytype_df['Orders'],
                name='Orders'
            )
            fig_daytype.add_scatter(
                x=daytype_df['DayType'],
                y=daytype_df['AvgOrderValue'],
                mode='lines+markers',
                name='Avg Order Value',
                yaxis='y2'
            )

            fig_daytype.update_layout(
                title="Weekend vs Weekday Performance",
                yaxis=dict(title="Orders"),
                yaxis2=dict(
                    title="Avg Order Value",
                    overlaying="y",
                    side="right"
                ),
                xaxis=dict(title="Day Type")
            )
            style_figure(fig_daytype, 430)
            st.plotly_chart(fig_daytype, use_container_width=True)

    with lower_right:
        top_seg = (
            filtered_df.groupby('CustomerSegment')['OrderValue'].mean().idxmax()
            if {'CustomerSegment', 'OrderValue'}.issubset(filtered_df.columns)
            else "N/A"
        )

        insight_card(
            "Highest Value Segment",
            f"<b>{top_seg}</b> currently generates the highest average order value among customer groups."
        )

        insight_card(
            "Customer Strategy",
            "Premium service design, targeted promotions, and loyalty offers can be aligned to the most valuable customer segments."
        )

        insight_card(
            "Behavioral Lens",
            "Segment-level trends help identify whether the business is driven more by repeat demand, high-ticket orders, or broad user volume."
        )

# =========================================================
# TAB 4 - REVENUE & DATA
# =========================================================
with tab4:
    rev_left, rev_right = st.columns([1.1, 0.9])

    with rev_left:
        if {'CuisineType', 'NetRevenue'}.issubset(filtered_df.columns):
            cuisine_rev = (
                filtered_df.groupby('CuisineType', as_index=False)['NetRevenue']
                .sum()
                .sort_values('NetRevenue', ascending=False)
            )

            fig_rev = px.bar(
                cuisine_rev,
                x='CuisineType',
                y='NetRevenue',
                text_auto=".2s",
                title="Estimated Net Revenue by Cuisine Type"
            )
            fig_rev.update_layout(
                xaxis_title="Cuisine Type",
                yaxis_title="Net Revenue"
            )
            style_figure(fig_rev, 440)
            st.plotly_chart(fig_rev, use_container_width=True)

    with rev_right:
        if {'PaymentMethod', 'OrderValue'}.issubset(filtered_df.columns):
            payment_summary = (
                filtered_df.groupby('PaymentMethod', as_index=False)
                .agg(
                    Orders=('OrderValue', 'size'),
                    Revenue=('OrderValue', 'sum')
                )
                .sort_values('Revenue', ascending=False)
            )

            fig_pay = px.bar(
                payment_summary,
                x='PaymentMethod',
                y='Revenue',
                text_auto=".2s",
                title="Revenue by Payment Method"
            )
            fig_pay.update_layout(
                xaxis_title="Payment Method",
                yaxis_title="Revenue"
            )
            style_figure(fig_pay, 440)
            st.plotly_chart(fig_pay, use_container_width=True)

    st.markdown("### 🧾 Filtered Data Preview")
    preview_cols = [col for col in [
        'OrderDate', 'City', 'CuisineType', 'CustomerSegment',
        'OrderValue', 'DeliveryTime', 'CustomerRating', 'NetRevenue'
    ] if col in filtered_df.columns]

    st.dataframe(
        filtered_df[preview_cols].sort_values(
            by='OrderDate' if 'OrderDate' in filtered_df.columns else preview_cols[0],
            ascending=False
        ),
        use_container_width=True,
        height=360
    )
