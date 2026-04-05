<div align="center">

# 🍔 FoodExpress · Data Analytics

**Give your stakeholders the food delivery insights they need.**  
Clean, analyze, test, and visualize one month of FoodExpress platform data — end to end.

[![Python](https://img.shields.io/badge/Python-3.13-3776ab?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-f37626?style=flat-square&logo=jupyter&logoColor=white)](https://jupyter.org/)
[![pandas](https://img.shields.io/badge/pandas-2.x-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![scipy](https://img.shields.io/badge/scipy-stats-8caae6?style=flat-square&logo=scipy&logoColor=white)](https://scipy.org/)
[![License](https://img.shields.io/badge/License-MIT-06d6a0?style=flat-square)](./LICENSE)
[![Status](https://img.shields.io/badge/Status-Complete-3776ab?style=flat-square)]()

[Overview](#-overview) •
[Dataset](#-dataset) •
[Project Structure](#-project-structure) •
[Setup](#-setup) •
[Key Analyses](#-key-analyses) •
[Findings](#-key-findings) •
[Author](#-author) •
[Contributing](#-contributing)

</div>

---

## 📌 Overview

This project performs a comprehensive **exploratory data analysis (EDA)** and **statistical inference** study on one month of delivery operations for the FoodExpress platform — a rapidly growing food delivery service connecting customers with local restaurants across four city zones.

The analysis pipeline covers:

- ✅ **Data cleaning** — null imputation, sentinel correction, datatype standardization, outlier removal, and data reshaping
- ✅ **Feature engineering** — net revenue calculation, discount aggregation, and derived temporal features (day, week, segment)
- ✅ **Exploratory analysis (EDA)** — order distribution, customer segmentation, cuisine trends, and delivery performance patterns
- ✅ **Statistical testing** — hypothesis testing including t-tests and chi-square tests to validate operational and customer insights
- ✅ **Business insights** — identification of key drivers of customer satisfaction, revenue performance, and operational efficiency
- ✅ **Interactive dashboard (Streamlit)** — real-time filtering, KPI monitoring, and visualization of operational and revenue metrics

## 📊 Dashboard Preview



### 🖥️ Main Dashboard
<img width="2558" height="1232" alt="Screenshot 2026-04-05 165641" src="https://github.com/user-attachments/assets/8b38f57e-7b4a-422a-9051-e27e7dc7b598" />

### 📈 KPI & Metrics View
<!-- Add KPI screenshot here -->
<img width="2544" height="1220" alt="Screenshot 2026-04-05 164954" src="https://github.com/user-attachments/assets/04ff6ecb-9eac-45b9-b863-ef46a0c04f24" />

### 📉 Analytical Charts
<!-- Add charts screenshot here -->
<p align="center">
  <img width="45%" src="https://github.com/user-attachments/assets/76b2888e-722b-4df0-8bb0-43b4fe17bd19" alt="Dashboard Overview" />
  <img width="45%" src="https://github.com/user-attachments/assets/436eb5c0-4c05-47c0-ad95-db313aa6c47b" alt="Operations Tab" />
</p>
<p align="center">
  <img width="45%" src="https://github.com/user-attachments/assets/22119c68-5dc8-43d3-8f9b-5c61a77921e5" alt="Customer Insights" />
  <img width="45%" src="https://github.com/user-attachments/assets/1a80194e-7981-45af-89c7-07d99896c1a8" alt="Revenue & Data" />
</p>


---


| Metric | Value |
|---|---|
| Period | September 2024 |
| Raw orders | 1,000 |
| Clean records | 990 |
| Total revenue | $35,575.93 |
| Net platform revenue | $25,013.29 |
| City zones | North · South · East · West |

---

## 📂 Dataset

The dataset `foodexpress_data_uncleaned.csv` contains **24 columns** across six categories:

| Category | Columns |
|---|---|
| **Order details** | `OrderID`, `OrderDate`, `OrderTime`, `DayOfWeek`, `TimePeriod` |
| **Customer info** | `CustomerSegment` *(New / Regular / VIP)*, `City` |
| **Restaurant** | `RestaurantID`, `CuisineType`, `RestaurantRating` |
| **Delivery metrics** | `DeliveryTime`, `DeliveryDistance`, `DeliveryFee`, `WeatherCondition` |
| **Financials** | `OrderValue`, `DiscountAmount`, `PromoDiscount`, `TipAmount`, `CashPayment`, `CardPayment`, `WalletPayment`, `UPIPayment` |
| **Performance** | `CustomerRating`, `DeliveryPartnerRating` |

> ⚠️ **Raw data quality issues:** 294 missing values across 4 columns, sentinel error `99999` in `DeliveryTime`, and `"INVALID"` / `"N/A"` strings in `CustomerRating`. All resolved in the cleaning pipeline.

---

## 🗂 Project Structure

```
FoodExpress-Data-Analytics/
│
├── app.py # Streamlit dashboard
├── FoodExpress Data Analytics Project.ipynb # Analysis notebook
├── foodexpress_data_uncleaned.csv # Raw dataset
├── requirements.txt # Dependencies
├── assets/ # Images & visuals
├── README.md # Documentation

---

## ⚙️ Setup

**Requirements:** Python 3.10+, Jupyter Notebook

```bash
# 1. Clone the repository
git clone https://github.com/doyancha/FoodExpress-Data-Analytics.git
cd FoodExpress-Data-Analytics

# 2. Install dependencies
pip install pandas numpy scipy matplotlib seaborn statsmodels jupyterlab

# 3. Launch the notebook
jupyter notebook "FoodExpress Data Analytics Project.ipynb"
```

> The dataset `foodexpress_data_uncleaned.csv` must sit in the same directory as the notebook. All cleaning steps are self-contained within the notebook cells.

---

## 🔍 Key Analyses

### 1 · Data Cleaning — Six-Step Pipeline

The raw CSV required six discrete cleaning operations before analysis:

| Step | Action | Outcome |
|---|---|---|
| 1 | Impute `CustomerRating` (79), `RestaurantRating` (75), `DeliveryTime` (70), `TipAmount` (70) with column median | 294 nulls resolved |
| 2 | Replace sentinel value `99999` in `DeliveryTime` with median of valid values | Outlier corrected |
| 3 | Replace `"INVALID"` / `"N/A"` strings in `CustomerRating` → NaN → median fill | `dtype` fixed to `float64` |
| 4 | Convert `OrderDate` → `datetime64`; financial & rating columns → `float64` | Types corrected |
| 5 | Drop rows where `DeliveryTime > P99` or `OrderValue < $5` | 10 rows removed → **990 rows** |
| 6 | Reshape 4 wide payment columns → `PaymentMethod` + `PaymentAmount` using `melt()` | 1 payment per row |

```python
# Step 6 — Reshape payments from wide → long format
payment_cols = ['CashPayment', 'CardPayment', 'WalletPayment', 'UPIPayment']

df_payment = df_clean.melt(
    id_vars=[c for c in df_clean.columns if c not in payment_cols],
    value_vars=payment_cols,
    var_name='PaymentType',
    value_name='PaymentAmount'
)
df_payment = df_payment[df_payment['PaymentAmount'] > 0].copy()
# Result → 990 orders : 990 payments (1:1 mapping)
```

---

### 2 · Python Fundamentals

#### Revenue Calculation — For Loop

```python
total_revenue = 0.0
for value in df['OrderValue']:
    total_revenue += value

# → Total Revenue: $35,575.93
```

#### Premium Delivery Classifier

A delivery is **"Premium"** when `DeliveryFee > $5.00` **and** `DeliveryTime < 25 minutes`.

```python
def is_premium_delivery(order_id):
    row = df[df['OrderID'] == order_id]
    if row.empty:
        return False
    return (row['DeliveryFee'].iloc[0] > 5.00) and (row['DeliveryTime'].iloc[0] < 25)

# Vectorized scan → 49 premium deliveries found
```

#### Average Order Value by Cuisine

```python
def avg_order_value_by_cuisine(cuisine_type):
    subset = df[df['CuisineType'] == cuisine_type]['OrderValue']
    if subset.empty:
        return None
    return {'cuisine': cuisine_type, 'avg': subset.mean(), 'count': len(subset)}
```

---

### 3 · Feature Engineering — Net Revenue

```
NetRevenue = OrderValue − DiscountAmount − PromoDiscount − (OrderValue × 0.20)
```

A 20% platform commission is applied to every order. The `NetRevenue` column reflects true platform earnings after all deductions.

```python
COMMISSION_RATE = 0.20
df_payment['RestaurantCommission'] = df_payment['OrderValue'] * COMMISSION_RATE
df_payment['NetRevenue'] = (
    df_payment['OrderValue']
    - df_payment['DiscountAmount'].fillna(0)
    - df_payment['PromoDiscount'].fillna(0)
    - df_payment['RestaurantCommission']
)
```

**Net revenue by city zone:**

| Rank | Zone | Net Revenue |
|---|---|---|
| 🥇 | North Zone | $6,631.72 |
| 🥈 | West Zone | $6,374.00 |
| 🥉 | South Zone | $6,060.36 |
| 4th | East Zone | $5,947.21 |

---

### 4 · Visualizations

Six charts were produced using `matplotlib` and `seaborn`:

| Chart | Type | Key Insight |
|---|---|---|
| Orders by cuisine | Horizontal bar | Indian leads with 152 orders |
| Revenue by cuisine × city | Heatmap | Surface top cuisine-city revenue combinations |
| Payment method by segment | 100% stacked bar | Uniform spread — no segment preference |
| Daily order trend | Line plot | Temporal patterns across September |
ry time by city | Box plot | North Zone has heavy right-skew |
| Campaign AOV impact | Paired scatter | Before vs After AOV per restaurant |

<div align="center">

## 📊 Dashboard Visualizations

<table>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/0c7c568d-19a0-4280-a008-f09ff758b6cc" width="350"/></td>
    <td><img src="https://github.com/user-attachments/assets/c2ef6e00-b159-473d-8926-0440005bb978" width="350"/></td>
    <td><img src="https://github.com/user-attachments/assets/a6f16710-9863-4dab-8c17-5767f9422ede" width="350"/></td>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/660d183d-a3e1-4109-9e61-efddedfd5213" width="350"/></td>
    <td><img src="https://github.com/user-attachments/assets/a6d72295-f9bc-4127-9560-5e86e9da3505" width="350"/></td>
    <td><img src="https://github.com/user-attachments/assets/aa6da66c-35b7-4eb4-b19f-1df79ed4c99a" width="350"/></td>
  </tr>
</table>

</div>



```python
# Heatmap — cuisine × city net revenue
pivot = df_payment.pivot_table(
    values='NetRevenue', index='CuisineType', columns='City', aggfunc='sum'
)
sns.heatmap(pivot, annot=True, fmt='.0f', cmap='YlOrRd', linewidths=0.5)

# 100% Stacked bar — payment method by customer segment
pct = pd.crosstab(
    df_clean['CustomerSegment'], df_clean['PaymentMethod'], normalize='index'
) * 100
pct.plot(kind='bar', stacked=True,
         color=['#e74c3c', '#3498db', '#2ecc71', '#f1c40f'], edgecolor='black')
```

---

### 5 · Statistical Tests — α = 0.05

#### Test 1 — Independent Samples t-test: VIP vs Regular Ratings

```
H₀ : μ(VIP ratings) = μ(Regular ratings)
H₁ : The means differ
```

```python
from scipy import stats

vip_r     = df[df['CustomerSegment'] == 'VIP Customer']['CustomerRating']
regular_r = df[df['CustomerSegment'] == 'Regular Customer']['CustomerRating']
t_stat, p_value = stats.ttest_ind(vip_r, regular_r)
```

**Result:** `p ≥ 0.05` → **Fail to reject H₀**
> No significant difference in satisfaction between VIP and Regular customers. The platform delivers a consistent experience across tiers.

---

#### Test 2 — One-Sample t-test: North Zone Delivery Target

```
H₀ : μ(North Zone delivery time) = 30 minutes
H₁ : μ ≠ 30 minutes
```

```python
north = df[df['City'] == 'North Zone']['DeliveryTime'].dropna()
t_stat, p_value = stats.ttest_1samp(north, popmean=30.0)
# Observed mean: 125 min  |  Only 36.7% of orders delivered within 30 min
```

**Result:** `p < 0.05` → **Reject H₀**
> North Zone significantly misses its 30-minute target. Operational intervention is required.

---

#### Test 3 — Chi-Square Test of Association: Payment Method vs Segment

```
H₀ : Payment method choice is independent of customer segment
H₁ : There is a significant association
```

**Result:** `p ≥ 0.05` → **Fail to reject H₀**
> Payment habits are uniform across all customer segments. A single payment promotion strategy is sufficient.

---

#### Test 4 — Chi-Square Goodness of Fit: Cuisine Distribution

```
H₀ : Each of 5 cuisines accounts for exactly 20% of orders
H₁ : Distribution is not uniform
```

```python
from scipy.stats import chisquare

observed = df_clean[df_clean['CuisineType'].isin(
    ['Italian', 'Chinese', 'Indian', 'Fast Food', 'Mexican']
)]['CuisineType'].value_counts()

chi2, p_value = chisquare(observed)
# χ² = 9.11  |  p = 0.0585
```

**Result:** `p = 0.0585` → **Fail to reject H₀** *(marginal)*
> Indian cuisine leads at 152 orders, but no statistically significant imbalance detected at α = 0.05.

---

### 6 · Business Intelligence

#### Correlation Analysis — Drivers of Customer Rating

```python
factors = ['DeliveryDistance', 'OrderValue', 'RestaurantRating', 'DeliveryPartnerRating']
correlations = {f: df['CustomerRating'].corr(df[f]) for f in factors}

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
for idx, factor in enumerate(factors):
    sns.regplot(data=df, x=factor, y='CustomerRating',
                ax=axes.ravel()[idx], line_kws={'color': 'red'})
```

| Factor | Direction | Strength |
|---|---|---|
| `DeliveryPartnerRating` | Positive | **Strong** — biggest satisfaction driver |
| `RestaurantRating` | Positive | Weak — food quality is secondary |
| `DeliveryDistance` | Negative | Weak — longer distance → lower satisfaction |
| `OrderValue` | ~Zero | None — spend level doesn't predict satisfaction |

#### Promotional Campaign — Paired t-test

Average order value (AOV) per restaurant was compared **before (Week 1)** and **after (Week 3)** a promotional campaign.

```python
before = df_campaign[df_campaign['Period'] == 'Before (Week 1)'] \
             .groupby('RestaurantID')['OrderValue'].mean()
after  = df_campaign[df_campaign['Period'] == 'After (Week 3)'] \
             .groupby('RestaurantID')['OrderValue'].mean()

paired  = pd.concat([before, after], axis=1, join='inner')
t_stat, p_value = stats.ttest_rel(paired.iloc[:, 0], paired.iloc[:, 1])
# AOV change: −13.3%  |  Revenue lift: −$7,228.79  |  p ≥ 0.05
```

**Result:** `p ≥ 0.05` → No statistically significant change in AOV from the campaign.

---

## 💡 Key Findings

- 🏙️ **North Zone** generates the highest net revenue ($6,631.72) but misses the 30-minute delivery target — only 36.7% of orders arrive on time.
- 🚴 **Delivery partner rating** is the single strongest predictor of customer satisfaction, outweighing food quality and spend level.
- ⭐ **VIP and Regular customers** give statistically equivalent ratings — operations are fair and consistent across segments.
- 💳 **Payment preferences** are uniform across all customer segments — no targeted payment strategy is needed.
- 🍛 **Indian cuisine** leads in volume (152 orders), though no cuisine is statistically over- or under-represented.
- 📉 The **promotional campaign** had no statistically significant effect on average order value.

---

## 📣 Recommendations

1. **Fix North Zone delivery** — invest in route optimization or zone-specific partner allocation to push ≤30-min delivery rate above 70%.
2. **Prioritize partner quality** — since partner rating drives satisfaction above all else, implement tiered incentives tied to delivery rating performance.
3. **Redesign the promo mechanics** — flat discounts did not move AOV; test free delivery thresholds, bundling, or cuisine-specific limited-time offers.
4. **Shift to volume campaigns** — since AOV is unresponsive to promos, redirect marketing toward order frequency and new customer acquisition.
5. **Formalize A/B measurement** — every future campaign should have a pre/post paired t-test built in before budget is committed.

---

## 🛠 Tech Stack

| Library | Version | Purpose |
|---|---|---|
| `pandas` | 2.x | Data loading, cleaning, groupby, melt, feature engineering |
| `numpy` | 1.x | Numerical operations, median imputation |
| `scipy` | 1.x | t-tests, chi-square tests, winsorization |
| `matplotlib` | 3.x | Base plotting engine |
| `seaborn` | 0.13+ | Heatmaps, box plots, regression plots, facet grids |
| `statsmodels` | 0.14+ | Tukey HSD post-hoc tests |

---

## 👤 Author

<div align="center">

**Doyancha**

[![GitHub](https://img.shields.io/badge/GitHub-doyancha-1a1a2e?style=flat-square&logo=github)](https://github.com/doyancha)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/mir-shahadut-hossain/)

*Data analyst focused on operations analytics, statistical inference, and Python-based data pipelines.*

</div>

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create a feature branch — `git checkout -b feature/your-idea`
3. Commit your changes — `git commit -m "Add: your idea"`
4. Push to the branch — `git push origin feature/your-idea`
5. Open a Pull Request

Please open an **issue** first to discuss any significant change.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](./LICENSE) file for details.

---

<div align="center">

[![GitHub](https://img.shields.io/badge/GitHub-FoodExpress--Data--Analytics-1a1a2e?style=flat-square&logo=github)](https://github.com/doyancha/FoodExpress-Data-Analytics)
[![Python](https://img.shields.io/badge/Built%20with-Python-3776ab?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)

*Made with 🍔 and data*

</div>
