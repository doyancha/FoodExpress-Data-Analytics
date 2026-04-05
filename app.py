import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
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
    .main {
        background: linear-gradient(180deg, #f8fafc 0%, #eef2f7 100%);
    }

    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    .hero-box {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 28px 32px;
        border-radius: 22px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.18);
    }

    .hero-title {
        font-size: 34px;
        font-weight: 800;
        margin-bottom: 8px;
        letter-spacing: 0.2px;
    }

    .hero-subtitle {
        font-size: 15px;
        color: #cbd5e1;
        line-height: 1.7;
    }

    .section-title {
        font-size: 22px;
        font-weight: 700;
        color: #0f172a;
        margin-top: 10px;
        margin-bottom: 12px;
    }

    .metric-card {
        background: white;
        padding: 18px 18px;
        border-radius: 18px;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.08);
        border: 1px solid rgba(148, 163, 184, 0.18);
        margin-bottom: 10px;
    }

    .metric-label {
        font-size: 13px;
        color: #64748b;
        margin-bottom: 6px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.4px;
    }

    .metric-value {
        font-size: 28px;
        font-weight: 800;
        color: #0f172a;
        line-height: 1.1;
    }

    .metric-delta {
        font-size: 13px;
        color: #16a34a;
        margin-top: 5px;
        font-weight: 600;
    }

    .insight-box {
        background: white;
        border-left: 5px solid #0f766e;
        border-radius: 14px;
        padding: 16px 18px;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
        margin-bottom: 12px;
    }

    .insight-title {
        font-size: 15px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 6px;
    }

    .insight-text {
        font-size: 14px;
        color: #475569;
        line-height: 1.6;
    }

    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #172554 100%);
    }

    div[data-testid="stSidebar"] * {
        color: white !important;
    }

    .footer-box {
        text-align: center;
        padding: 16px;
        color: #64748b;
        font-size: 13px;
        margin-top: 18px;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# HELPERS
# =========================================================
DATA_FILE = "foodexpress_data_uncleaned.csv"  # change this if your CSV name is different


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


# =========================================================
# LOAD DATA
# =========================================================
st.markdown("""
<div class="hero-box">
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
st.sidebar.markdown("## 📊 Dashboard Filters")

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
    selected_cities = st.sidebar.multiselect("Select City", city_options, default=city_options)
    if selected_cities:
        filtered_df = filtered_df[filtered_df['City'].isin(selected_cities)]

if 'CuisineType' in filtered_df.columns:
    cuisine_options = sorted([x for x in filtered_df['CuisineType'].dropna().unique() if x != 'nan'])
    selected_cuisines = st.sidebar.multiselect("Select Cuisine Type", cuisine_options, default=cuisine_options)
    if selected_cuisines:
        filtered_df = filtered_df[filtered_df['CuisineType'].isin(selected_cuisines)]

if 'CustomerSegment' in filtered_df.columns:
    segment_options = sorted([x for x in filtered_df['CustomerSegment'].dropna().unique() if x != 'nan'])
    selected_segments = st.sidebar.multiselect("Select Customer Segment", segment_options, default=segment_options)
    if selected_segments:
        filtered_df = filtered_df[filtered_df['CustomerSegment'].isin(selected_segments)]

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
                yaxis_title="Total Orders",
                template="plotly_white",
                height=460
            )
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
            fig_segment.update_layout(template="plotly_white", height=460)
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
                yaxis_title="Number of Orders",
                template="plotly_white",
                height=460
            )
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
                yaxis_title="Frequency",
                template="plotly_white",
                height=440
            )
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
                yaxis_title="Delivery Time (minutes)",
                template="plotly_white",
                height=440
            )
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
                yaxis_title="Delivery Time",
                template="plotly_white",
                height=470
            )
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
                yaxis_title="Average Order Value",
                template="plotly_white",
                height=430
            )
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
                yaxis_title="Average Rating",
                template="plotly_white",
                height=430
            )
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
                template="plotly_white",
                height=430,
                yaxis=dict(title="Orders"),
                yaxis2=dict(
                    title="Avg Order Value",
                    overlaying="y",
                    side="right"
                ),
                xaxis=dict(title="Day Type")
            )
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
                yaxis_title="Net Revenue",
                template="plotly_white",
                height=440
            )
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
                yaxis_title="Revenue",
                template="plotly_white",
                height=440
            )
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

# =========================================================
# FOOTER
# =========================================================
st.markdown("""
<div class="footer-box">
    Built with Streamlit for the FoodExpress Data Analytics Project · Designed for portfolio-grade presentation
</div>
""", unsafe_allow_html=True)