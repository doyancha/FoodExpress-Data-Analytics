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
# THEME / CSS
# =========================================================
st.markdown("""
<style>
    :root {
        --bg: #0f172a;
        --card: #1e293b;
        --text: #f1f5f9;
        --muted: #94a3b8;
        --border: rgba(148, 163, 184, 0.12);
        --shadow: 0 10px 30px rgba(0, 0, 0, 0.30);
        --accent: #2dd4bf;
        --accent-2: #60a5fa;
        --hero-1: #0f172a;
        --hero-2: #1e293b;
    }

    .stApp {
        background: #0f172a;
    }

    .block-container {
        padding-top: 1.1rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    /* ── HERO ── */
    .hero-box {
        position: relative;
        overflow: hidden;
        background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #0f766e 100%);
        padding: 44px 48px;
        border-radius: 28px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 20px 60px rgba(15, 23, 42, 0.35);
        border: 1px solid rgba(255, 255, 255, 0.10);
    }

    .hero-box::before {
        content: "";
        position: absolute;
        top: -80px; right: -80px;
        width: 340px; height: 340px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(99,210,191,0.18) 0%, transparent 70%);
        pointer-events: none;
    }

    .hero-box::after {
        content: "";
        position: absolute;
        bottom: -60px; left: 30%;
        width: 260px; height: 260px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(59,130,246,0.12) 0%, transparent 70%);
        pointer-events: none;
    }

    .hero-topline {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #6ee7df;
        font-weight: 700;
        margin-bottom: 14px;
        background: rgba(99,210,191,0.12);
        border: 1px solid rgba(99,210,191,0.25);
        padding: 5px 14px;
        border-radius: 999px;
    }

    .hero-title {
        font-size: 40px;
        font-weight: 900;
        margin-bottom: 10px;
        letter-spacing: -0.5px;
        line-height: 1.15;
        text-shadow: 0 2px 12px rgba(0,0,0,0.3);
    }

    .hero-subtitle {
        font-size: 15px;
        color: #94a3b8;
        line-height: 1.8;
        max-width: 720px;
    }

    .hero-stats {
        display: flex;
        gap: 28px;
        margin-top: 28px;
        flex-wrap: wrap;
    }

    .hero-stat-item {
        display: flex;
        flex-direction: column;
        gap: 2px;
        padding: 10px 18px;
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 14px;
        backdrop-filter: blur(4px);
    }

    .hero-stat-label {
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: #64748b;
        font-weight: 700;
    }

    .hero-stat-value {
        font-size: 18px;
        font-weight: 800;
        color: #e2e8f0;
    }

    /* ── SECTIONS ── */
    .section-title {
        font-size: 22px;
        font-weight: 800;
        color: var(--text);
        margin: 8px 0 12px 0;
    }

    .section-caption {
        font-size: 13px;
        color: var(--muted);
        margin-bottom: 12px;
    }

    /* ── METRIC CARDS ── */
    .metric-card {
        background: var(--card);
        padding: 18px 18px;
        border-radius: 18px;
        box-shadow: var(--shadow);
        border: 1px solid var(--border);
        margin-bottom: 10px;
        min-height: 116px;
    }

    .metric-label {
        font-size: 12px;
        color: var(--muted);
        margin-bottom: 6px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }

    .metric-value {
        font-size: 28px;
        font-weight: 800;
        color: var(--text);
        line-height: 1.1;
    }

    .metric-delta {
        font-size: 13px;
        color: #2dd4bf;
        margin-top: 7px;
        font-weight: 600;
    }

    /* ── INSIGHT BOXES ── */
    .insight-box {
        background: var(--card);
        border-left: 5px solid var(--accent);
        border-radius: 16px;
        padding: 16px 18px;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.20);
        margin-bottom: 12px;
        border-top: 1px solid var(--border);
        border-right: 1px solid var(--border);
        border-bottom: 1px solid var(--border);
    }

    .insight-title {
        font-size: 15px;
        font-weight: 800;
        color: #f1f5f9;
        margin-bottom: 6px;
    }

    .insight-text {
        font-size: 14px;
        color: #94a3b8;
        line-height: 1.65;
    }

    .panel-card {
        background: var(--card);
        border-radius: 18px;
        box-shadow: var(--shadow);
        border: 1px solid var(--border);
        padding: 14px 16px 6px 16px;
        margin-bottom: 14px;
    }

    .mini-chip {
        display: inline-block;
        padding: 6px 10px;
        border-radius: 999px;
        background: #e2e8f0;
        color: #0f172a;
        font-size: 12px;
        font-weight: 700;
        margin-right: 8px;
        margin-bottom: 8px;
    }

    /* ── SIDEBAR BASE ── */
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0f1e 0%, #0f1f3d 55%, #0d2b2a 100%);
        border-right: 1px solid rgba(255,255,255,0.06);
    }

    /* Fix text visibility: only target known text elements, not all children */
    div[data-testid="stSidebar"] p,
    div[data-testid="stSidebar"] span,
    div[data-testid="stSidebar"] label,
    div[data-testid="stSidebar"] div[class*="caption"],
    div[data-testid="stSidebar"] .stMarkdown {
        color: #e2e8f0 !important;
    }

    div[data-testid="stSidebar"] h1,
    div[data-testid="stSidebar"] h2,
    div[data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }

    /* ── SIDEBAR BRAND ── */
    .sidebar-brand {
        background: linear-gradient(135deg, rgba(14,165,136,0.20) 0%, rgba(29,78,216,0.15) 100%);
        border: 1px solid rgba(99,210,191,0.22);
        border-radius: 20px;
        padding: 18px 16px 16px 16px;
        margin-bottom: 18px;
        position: relative;
        overflow: hidden;
    }

    .sidebar-brand::before {
        content: "";
        position: absolute;
        top: -30px; right: -30px;
        width: 110px; height: 110px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(99,210,191,0.15) 0%, transparent 70%);
    }

    .sidebar-brand-logo {
        font-size: 32px;
        line-height: 1;
        margin-bottom: 8px;
        display: block;
    }

    .sidebar-brand-title {
        font-size: 20px;
        font-weight: 900;
        color: #ffffff !important;
        letter-spacing: -0.3px;
        margin-bottom: 2px;
    }

    .sidebar-brand-tag {
        display: inline-block;
        font-size: 9px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #6ee7df !important;
        background: rgba(99,210,191,0.15);
        border: 1px solid rgba(99,210,191,0.30);
        padding: 2px 8px;
        border-radius: 999px;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .sidebar-brand-subtitle {
        font-size: 12px;
        color: #94a3b8 !important;
        line-height: 1.6;
    }

    /* ── SIDEBAR FILTERS SECTION ── */
    .sidebar-filter-title {
        font-size: 13px;
        font-weight: 800;
        color: #ffffff !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 4px;
        margin-bottom: 2px;
    }

    .sidebar-filter-subtitle {
        font-size: 11px;
        color: #64748b !important;
        margin-bottom: 10px;
    }

    .sidebar-filter-label {
        font-size: 12px;
        font-weight: 700;
        color: #cbd5e1 !important;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 6px;
        margin-top: 14px;
    }

    /* ── TOGGLE BUTTON GRID (City & Segment) ── */
    .toggle-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 7px;
        margin-bottom: 10px;
    }

    .toggle-btn {
        cursor: pointer;
        padding: 7px 13px;
        border-radius: 10px;
        font-size: 12px;
        font-weight: 700;
        border: 1.5px solid rgba(99,210,191,0.25);
        background: rgba(255,255,255,0.05);
        color: #94a3b8 !important;
        transition: all 0.18s ease;
        user-select: none;
        letter-spacing: 0.2px;
    }

    .toggle-btn.active {
        background: linear-gradient(135deg, #0f766e 0%, #0d9488 100%);
        border-color: #14b8a6;
        color: #ffffff !important;
        box-shadow: 0 3px 10px rgba(14,165,136,0.35);
    }

    div[data-testid="stSidebar"] div[data-testid="stButton"] > button {
        min-height: 42px;
        border-radius: 14px;
        border: 1px solid rgba(148,163,184,0.16);
        background: linear-gradient(180deg, rgba(20, 29, 48, 0.98) 0%, rgba(13, 21, 36, 0.96) 100%);
        color: #cbd5e1;
        font-weight: 700;
        font-size: 12px;
        letter-spacing: 0.02em;
        box-shadow: 0 8px 18px rgba(2, 6, 23, 0.24);
        transition: all 0.18s ease;
    }

    div[data-testid="stSidebar"] div[data-testid="stButton"] > button:hover {
        border-color: rgba(96, 165, 250, 0.34);
        color: #ffffff;
        transform: translateY(-1px);
        box-shadow: 0 12px 24px rgba(2, 6, 23, 0.34), 0 0 18px rgba(34, 211, 238, 0.10);
    }

    div[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="primary"] {
        background: linear-gradient(135deg, rgba(14,165,136,0.92) 0%, rgba(37,99,235,0.9) 100%);
        border-color: rgba(110, 231, 223, 0.36);
        color: #ffffff;
        box-shadow: 0 14px 28px rgba(14,165,136,0.22), 0 0 18px rgba(96,165,250,0.18);
    }

    /* ── SIDEBAR FOOTER ── */
    .sidebar-row-count {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 10px 14px;
        margin-top: 10px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .sidebar-row-label {
        font-size: 11px;
        color: #64748b !important;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        font-weight: 700;
    }

    .sidebar-row-value {
        font-size: 16px;
        font-weight: 900;
        color: #6ee7df !important;
    }

    /* ── FOOTER ── */
    .footer-box {
        text-align: center;
        padding: 16px;
        color: #64748b;
        font-size: 13px;
        margin-top: 18px;
    }

    /* ── TABS ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent !important;
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
            
    /* ── CREDENTIALS CARD ── */
    .cred-card {
        background:
            radial-gradient(circle at top right, rgba(45,212,191,0.12), transparent 38%),
            linear-gradient(180deg, rgba(18, 26, 44, 0.96) 0%, rgba(11, 18, 32, 0.98) 100%);
        border: 1px solid rgba(96,165,250,0.18);
        border-radius: 22px;
        padding: 18px 16px 16px 16px;
        margin-top: 16px;
        box-shadow: 0 18px 36px rgba(2, 6, 23, 0.34);
        position: relative;
        overflow: hidden;
    }

    .cred-card::before {
        content: "";
        position: absolute;
        inset: 0 auto auto 0;
        width: 100%;
        height: 3px;
        background: linear-gradient(90deg, #22d3ee, #60a5fa, #8b5cf6);
        opacity: 0.95;
    }

    .sidebar-brand ~ div .cred-card {
        display: none;
    }

    .about-card + .cred-card {
        display: block;
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
        font-size: 16px;
        font-weight: 800;
        color: #f1f5f9 !important;
        margin-bottom: 4px;
    }

    .cred-role {
        font-size: 11px;
        color: #2dd4bf !important;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 12px;
    }

    .cred-link {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 12px;
        color: #94a3b8 !important;
        text-decoration: none;
        padding: 9px 11px;
        border-radius: 12px;
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.06);
        margin-bottom: 8px;
    }

    .cred-link:hover {
        background: rgba(255,255,255,0.08);
        border-color: rgba(96,165,250,0.22);
        color: #f1f5f9 !important;
    }

    /* ── ABOUT BLOCK ── */
    .about-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 14px;
        padding: 13px 14px;
        margin-top: 10px;
    }

    .about-label {
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: #64748b !important;
        font-weight: 700;
        margin-bottom: 7px;
    }

    .about-text {
        font-size: 12px;
        color: #94a3b8 !important;
        line-height: 1.7;
        margin-bottom: 10px;
    }

    .about-pill {
        display: inline-block;
        font-size: 10px;
        font-weight: 700;
        padding: 3px 9px;
        border-radius: 999px;
        background: rgba(45,212,191,0.10);
        border: 1px solid rgba(45,212,191,0.20);
        color: #2dd4bf !important;
        margin-right: 5px;
        margin-bottom: 4px;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# HELPERS
# =========================================================
DATA_FILE = "foodexpress_data_uncleaned.csv"
CHART_TEMPLATE = "plotly_dark"

pio.templates.default = CHART_TEMPLATE


@st.cache_data
def load_data(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)


def derive_payment_method(df: pd.DataFrame) -> pd.DataFrame:
    """Create PaymentMethod from wide payment columns if a single column is absent."""
    df = df.copy()

    if 'PaymentMethod' in df.columns:
        df['PaymentMethod'] = df['PaymentMethod'].astype(str).str.strip()
        return df

    payment_map = {
        'CashPayment': 'Cash',
        'CardPayment': 'Card',
        'WalletPayment': 'Wallet',
        'UPIPayment': 'UPI'
    }

    available_cols = [c for c in payment_map if c in df.columns]
    if not available_cols:
        return df

    payment_values = df[available_cols].apply(pd.to_numeric, errors='coerce').fillna(0)

    def pick_method(row):
        positive = [payment_map[col] for col in available_cols if row[col] > 0]
        if len(positive) == 1:
            return positive[0]
        if len(positive) > 1:
            return "Multiple"
        return "Unknown"

    df['PaymentMethod'] = payment_values.apply(pick_method, axis=1)
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [col.strip() for col in df.columns]

    numeric_cols = [
        'DeliveryTime', 'RestaurantRating', 'CustomerRating',
        'DeliveryPartnerRating', 'TipAmount', 'DeliveryDistance',
        'DiscountAmount', 'PromoDiscount', 'DeliveryFee', 'OrderValue'
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if 'DeliveryTime' in df.columns:
        valid_delivery = df.loc[df['DeliveryTime'] != 99999, 'DeliveryTime'].dropna()
        if not valid_delivery.empty:
            delivery_median = valid_delivery.median()
            df['DeliveryTime'] = df['DeliveryTime'].replace(99999, delivery_median)

    if 'CustomerRating' in df.columns:
        df['CustomerRating'] = (
            df['CustomerRating']
            .replace(['INVALID', 'N/A', 'NA', ''], np.nan)
        )
        df['CustomerRating'] = pd.to_numeric(df['CustomerRating'], errors='coerce')

    for col in numeric_cols:
        if col in df.columns:
            median_value = df[col].median()
            df[col] = df[col].fillna(median_value)

    if 'OrderDate' in df.columns:
        df['OrderDate'] = pd.to_datetime(df['OrderDate'], errors='coerce')

    for col in ['CuisineType', 'City', 'CustomerSegment']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    df = derive_payment_method(df)

    if 'PaymentMethod' in df.columns:
        df['PaymentMethod'] = df['PaymentMethod'].astype(str).str.strip()

    if 'DeliveryTime' in df.columns:
        delivery_99 = df['DeliveryTime'].quantile(0.99)
        df = df[df['DeliveryTime'] <= delivery_99]

    if 'OrderValue' in df.columns:
        df = df[df['OrderValue'] >= 5]

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
        iso_cal = df['OrderDate'].dt.isocalendar()
        df['Week'] = (iso_cal['week'] if 'week' in iso_cal.columns else iso_cal.week).astype(str)
        df['DayType'] = np.where(df['OrderDate'].dt.dayofweek >= 5, 'Weekend', 'Weekday')

    if 'OrderValue' in df.columns and 'DiscountAmount' in df.columns:
        df['DiscountPercentage'] = np.where(
            df['OrderValue'] > 0,
            (df['DiscountAmount'].fillna(0) / df['OrderValue']) * 100,
            0
        )

    return df


def fmt_currency(value) -> str:
    return f"${value:,.2f}" if pd.notna(value) else "N/A"


def fmt_number(value, digits: int = 1, suffix: str = "") -> str:
    return f"{value:,.{digits}f}{suffix}" if pd.notna(value) else "N/A"


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


def wrap_chart(fig, title: str = None):
    fig.update_layout(
        template=CHART_TEMPLATE,
        height=430,
        margin=dict(l=20, r=20, t=60, b=20),
        legend_title_text="",
        title_x=0.02,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(9, 17, 31, 0.78)",
        font=dict(color="#dbeafe"),
        title_font=dict(size=20, color="#f8fbff"),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0,
            font=dict(color="#cbd5e1")
        )
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
    if title:
        fig.update_layout(title=title)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# =========================================================
# LOAD DATA
# =========================================================
st.markdown("""
<div class="hero-box" style="display:flex; flex-direction:column; align-items:center; text-align:center; width:100%;">
    <div class="hero-topline">⚡ Live Operational Intelligence</div>
    <div class="hero-title">🍔 FoodExpress Analytics</div>
    <div class="hero-subtitle">
        Executive-grade dashboard for real-time monitoring of order volume, delivery efficiency,
        customer behavior, and revenue performance — all in one view.
    </div>
    <div class="hero-stats">
        <div class="hero-stat-item">
            <span class="hero-stat-label">Platform</span>
            <span class="hero-stat-value">FoodExpress BI</span>
        </div>
        <div class="hero-stat-item">
            <span class="hero-stat-label">Coverage</span>
            <span class="hero-stat-value">4 City Zones</span>
        </div>
        <div class="hero-stat-item">
            <span class="hero-stat-label">Segments</span>
            <span class="hero-stat-value">New · Regular · VIP</span>
        </div>
        <div class="hero-stat-item">
            <span class="hero-stat-label">Module</span>
            <span class="hero-stat-value">v2.0 · Portfolio Edition</span>
        </div>
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
# SIDEBAR
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

# ── City: clickable toggle buttons ──
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

# ── Customer Segment: clickable toggle buttons ──
if 'CustomerSegment' in filtered_df.columns:
    segment_options = sorted([x for x in filtered_df['CustomerSegment'].dropna().unique() if x != 'nan'])

    if 'selected_segments' not in st.session_state:
        st.session_state.selected_segments = set(segment_options)

    st.sidebar.markdown('<div class="sidebar-filter-label">👥 Customer Segment</div>', unsafe_allow_html=True)

    seg_icons = {"New Customer": "🆕", "Regular Customer": "🔄", "VIP Customer": "⭐"}
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

# ── CREDENTIALS ──
st.sidebar.markdown("""
<div class="cred-card">
    <div class="cred-label">Contact</div>
    <div class="cred-name">Mir Shahadut Hossain</div>
    <div class="cred-role">Data Analyst</div>
    <a class="cred-link" href="https://www.linkedin.com/in/mir-sahadut-hossain" target="_blank">
        <span>🔗</span> LinkedIn Profile
    </a>
    <a class="cred-link" href="https://github.com/doyancha" target="_blank">
        <span>🐙</span> github.com/doyancha
    </a>
    <a class="cred-link" href="mailto:sujon6901@gmail.com">
        <span>✉️</span> sujon6901@gmail.com
    </a>
</div>

<div class="about-card">
    <div class="about-label">About This Project</div>
    <div class="about-text">
        Real-world food delivery dataset covering 4 city zones across September 2024.
        Demonstrates end-to-end analytics from data cleaning and EDA to an interactive
        executive-grade BI dashboard.
    </div>
    <span class="about-pill">Python</span>
    <span class="about-pill">Streamlit</span>
    <span class="about-pill">Plotly</span>
    <span class="about-pill">Pandas</span>
</div>

<div class="cred-card">
    <div class="cred-label">Contact</div>
    <div class="cred-name">Mir Shahadut Hossain</div>
    <div class="cred-role">Data Analyst</div>
    <a class="cred-link" href="https://www.linkedin.com/in/mir-sahadut-hossain" target="_blank">
        <span>LinkedIn</span>
    </a>
    <a class="cred-link" href="https://github.com/doyancha" target="_blank">
        <span>GitHub</span>
    </a>
    <a class="cred-link" href="mailto:sujon6901@gmail.com">
        <span>Email</span>
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
st.markdown('<div class="section-caption">High-level performance indicators for the filtered business view.</div>', unsafe_allow_html=True)

total_orders = len(filtered_df)
total_revenue = filtered_df['OrderValue'].sum() if 'OrderValue' in filtered_df.columns else np.nan
avg_order_value = filtered_df['OrderValue'].mean() if 'OrderValue' in filtered_df.columns else np.nan
avg_delivery_time = filtered_df['DeliveryTime'].mean() if 'DeliveryTime' in filtered_df.columns else np.nan
avg_customer_rating = filtered_df['CustomerRating'].mean() if 'CustomerRating' in filtered_df.columns else np.nan
net_revenue = filtered_df['NetRevenue'].sum() if 'NetRevenue' in filtered_df.columns else np.nan

all_avg_delivery = df['DeliveryTime'].mean() if 'DeliveryTime' in df.columns else np.nan
all_avg_aov = df['OrderValue'].mean() if 'OrderValue' in df.columns else np.nan
all_avg_rating = df['CustomerRating'].mean() if 'CustomerRating' in df.columns else np.nan

premium_orders = 0
if {'DeliveryFee', 'DeliveryTime'}.issubset(filtered_df.columns):
    premium_orders = int(((filtered_df['DeliveryFee'] > 5) & (filtered_df['DeliveryTime'] < 25)).sum())

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    metric_card("Total Orders", f"{total_orders:,}", "Filtered operational volume")
with col2:
    metric_card("Total Revenue", fmt_currency(total_revenue), "Gross order value")
with col3:
    delta_aov = f"vs full data: {fmt_currency(avg_order_value - all_avg_aov)}"
    metric_card("Avg Order Value", fmt_currency(avg_order_value), delta_aov)
with col4:
    delta_time = f"vs full data: {fmt_number(avg_delivery_time - all_avg_delivery, 1, ' min')}"
    metric_card("Avg Delivery Time", fmt_number(avg_delivery_time, 1, " min"), delta_time)
with col5:
    delta_rating = f"vs full data: {fmt_number(avg_customer_rating - all_avg_rating, 2)}"
    metric_card("Avg Customer Rating", fmt_number(avg_customer_rating, 2), delta_rating)

col6, col7 = st.columns(2)
with col6:
    metric_card("Estimated Net Revenue", fmt_currency(net_revenue), "After discounts and commission")
with col7:
    metric_card("Premium Deliveries", f"{premium_orders:,}", "High-fee, fast-delivery orders")

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
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        if 'CuisineType' in filtered_df.columns:
            cuisine_counts = filtered_df['CuisineType'].value_counts().reset_index()
            cuisine_counts.columns = ['CuisineType', 'Orders']

            fig_cuisine = px.bar(
                cuisine_counts,
                x='CuisineType',
                y='Orders',
                text='Orders',
                title="Order Volume by Cuisine Type"
            )
            fig_cuisine.update_traces(textposition="outside")
            fig_cuisine.update_xaxes(title="Cuisine Type")
            fig_cuisine.update_yaxes(title="Orders")
            wrap_chart(fig_cuisine)
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        if 'CustomerSegment' in filtered_df.columns:
            segment_counts = filtered_df['CustomerSegment'].value_counts().reset_index()
            segment_counts.columns = ['CustomerSegment', 'Count']

            fig_segment = px.pie(
                segment_counts,
                names='CustomerSegment',
                values='Count',
                hole=0.50,
                title="Customer Segment Mix"
            )
            wrap_chart(fig_segment)
        st.markdown('</div>', unsafe_allow_html=True)

    trend_col, insight_col = st.columns([1.35, 0.65])

    with trend_col:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
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
            fig_daily.update_xaxes(title="Order Date")
            fig_daily.update_yaxes(title="Orders")
            wrap_chart(fig_daily)
        st.markdown('</div>', unsafe_allow_html=True)

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
        best_revenue_city = (
            filtered_df.groupby('City')['NetRevenue'].sum().idxmax()
            if {'City', 'NetRevenue'}.issubset(filtered_df.columns) and not filtered_df.empty
            else "N/A"
        )

        insight_card(
            "Top Cuisine",
            f"<b>{top_cuisine}</b> contributes the highest order volume in the current filtered view."
        )
        insight_card(
            "Largest Segment",
            f"<b>{top_segment}</b> is the dominant customer cohort across the selected data slice."
        )
        insight_card(
            "Revenue Leader",
            f"<b>{best_revenue_city}</b> currently leads the filtered view in estimated net revenue."
        )

# =========================================================
# TAB 2 - OPERATIONS
# =========================================================
with tab2:
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
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
            fig_hist.update_xaxes(title="Delivery Time (minutes)")
            fig_hist.update_yaxes(title="Frequency")
            wrap_chart(fig_hist)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        if {'City', 'DeliveryTime'}.issubset(filtered_df.columns):
            fig_box = px.box(
                filtered_df,
                x='City',
                y='DeliveryTime',
                points='outliers',
                title="Delivery Time by City"
            )
            fig_box.update_xaxes(title="City")
            fig_box.update_yaxes(title="Delivery Time (minutes)")
            wrap_chart(fig_box)
        st.markdown('</div>', unsafe_allow_html=True)

    col_c, col_d = st.columns([1.25, 0.75])

    with col_c:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        if {'OrderValue', 'DeliveryTime', 'CustomerSegment'}.issubset(filtered_df.columns):
            corr = filtered_df[['OrderValue', 'DeliveryTime']].corr().iloc[0, 1]

            fig_scatter = px.scatter(
                filtered_df,
                x='OrderValue',
                y='DeliveryTime',
                color='CustomerSegment',
                trendline='ols',
                title=f"Order Value vs Delivery Time · Correlation {corr:.2f}",
                opacity=0.7
            )
            fig_scatter.update_xaxes(title="Order Value")
            fig_scatter.update_yaxes(title="Delivery Time")
            wrap_chart(fig_scatter)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_d:
        if {'City', 'DeliveryTime'}.issubset(filtered_df.columns):
            city_perf = (
                filtered_df.groupby('City', as_index=False)['DeliveryTime']
                .mean()
                .sort_values('DeliveryTime')
            )

            if not city_perf.empty:
                best_city = city_perf.iloc[0]['City']
                worst_city = city_perf.iloc[-1]['City']
                on_time_rate = (
                    (filtered_df['DeliveryTime'] <= 30).mean() * 100
                    if 'DeliveryTime' in filtered_df.columns else np.nan
                )

                insight_card(
                    "Best Performing City",
                    f"<b>{best_city}</b> has the lowest average delivery time in the selected view."
                )
                insight_card(
                    "Operational Risk Zone",
                    f"<b>{worst_city}</b> shows the slowest average delivery performance and may require workflow optimization."
                )
                insight_card(
                    "On-Time Service Rate",
                    f"<b>{on_time_rate:.1f}%</b> of filtered orders were delivered within 30 minutes."
                )

# =========================================================
# TAB 3 - CUSTOMER INSIGHTS
# =========================================================
with tab3:
    left_cust, right_cust = st.columns([1.1, 0.9])

    with left_cust:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
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
            fig_seg_value.update_xaxes(title="Customer Segment")
            fig_seg_value.update_yaxes(title="Average Order Value")
            wrap_chart(fig_seg_value)
        st.markdown('</div>', unsafe_allow_html=True)

    with right_cust:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
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
            fig_seg_rating.update_xaxes(title="Customer Segment")
            fig_seg_rating.update_yaxes(title="Average Rating")
            wrap_chart(fig_seg_rating)
        st.markdown('</div>', unsafe_allow_html=True)

    lower_left, lower_right = st.columns([1.2, 0.8])

    with lower_left:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        if {'DayType', 'OrderValue'}.issubset(filtered_df.columns):
            daytype_df = (
                filtered_df.groupby('DayType', as_index=False)
                .agg(
                    Orders=('OrderValue', 'size'),
                    AvgOrderValue=('OrderValue', 'mean')
                )
            )

            fig_daytype = go.Figure()
            fig_daytype.add_bar(x=daytype_df['DayType'], y=daytype_df['Orders'], name='Orders')
            fig_daytype.add_scatter(
                x=daytype_df['DayType'],
                y=daytype_df['AvgOrderValue'],
                mode='lines+markers',
                name='Avg Order Value',
                yaxis='y2'
            )
            fig_daytype.update_layout(
                title="Weekend vs Weekday Performance",
                template="plotly_white",
                height=430,
                margin=dict(l=20, r=20, t=60, b=20),
                yaxis=dict(title="Orders"),
                yaxis2=dict(title="Avg Order Value", overlaying="y", side="right"),
                xaxis=dict(title="Day Type"),
                legend_title_text=""
            )
            st.plotly_chart(fig_daytype, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with lower_right:
        top_seg = (
            filtered_df.groupby('CustomerSegment')['OrderValue'].mean().idxmax()
            if {'CustomerSegment', 'OrderValue'}.issubset(filtered_df.columns) and not filtered_df.empty
            else "N/A"
        )

        best_rating_seg = (
            filtered_df.groupby('CustomerSegment')['CustomerRating'].mean().idxmax()
            if {'CustomerSegment', 'CustomerRating'}.issubset(filtered_df.columns) and not filtered_df.empty
            else "N/A"
        )

        insight_card(
            "Highest Value Segment",
            f"<b>{top_seg}</b> generates the highest average order value in the filtered view."
        )
        insight_card(
            "Highest Satisfaction Segment",
            f"<b>{best_rating_seg}</b> leads on average customer rating across the current selection."
        )
        insight_card(
            "Commercial Implication",
            "Retention offers and premium service design should prioritize the segments showing both strong value and consistent satisfaction."
        )

# =========================================================
# TAB 4 - REVENUE & DATA
# =========================================================
with tab4:
    rev_left, rev_right = st.columns([1.1, 0.9])

    with rev_left:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
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
            fig_rev.update_xaxes(title="Cuisine Type")
            fig_rev.update_yaxes(title="Net Revenue")
            wrap_chart(fig_rev)
        st.markdown('</div>', unsafe_allow_html=True)

    with rev_right:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
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
            fig_pay.update_xaxes(title="Payment Method")
            fig_pay.update_yaxes(title="Revenue")
            wrap_chart(fig_pay)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">🧾 Filtered Data Preview</div>', unsafe_allow_html=True)
    preview_cols = [col for col in [
        'OrderDate', 'City', 'CuisineType', 'CustomerSegment',
        'PaymentMethod', 'OrderValue', 'DeliveryTime', 'CustomerRating', 'NetRevenue'
    ] if col in filtered_df.columns]

    preview_df = filtered_df[preview_cols].copy()
    if 'OrderDate' in preview_df.columns:
        preview_df = preview_df.sort_values(by='OrderDate', ascending=False)

    st.dataframe(preview_df, use_container_width=True, height=360)

