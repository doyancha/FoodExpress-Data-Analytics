# 🍔 FoodExpress Data Analytics

> End-to-end exploratory data analysis and statistical inference on one month of food delivery operations — covering data cleaning, feature engineering, visualization, and hypothesis testing.

<br>

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Dataset](#-dataset)
- [Project Structure](#-project-structure)
- [Tech Stack](#-tech-stack)
- [Installation & Setup](#-installation--setup)
- [Key Analyses](#-key-analyses)
  - [1. Data Cleaning](#1-data-cleaning)
  - [2. Python Fundamentals](#2-python-fundamentals)
  - [3. Feature Engineering](#3-feature-engineering)
  - [4. Visualizations](#4-visualizations)
  - [5. Statistical Tests](#5-statistical-tests)
  - [6. Business Intelligence](#6-business-intelligence)
- [Key Findings](#-key-findings)
- [Recommendations](#-recommendations)
- [License](#-license)

<br>

---

## 📌 Project Overview

**FoodExpress** is a rapidly growing food delivery platform connecting customers with local restaurants and delivery partners across multiple city zones. This project performs a comprehensive analysis of **1,000 orders** from September 2024 to surface operational insights, test business hypotheses, and guide data-driven decisions.

| Scope | Detail |
|---|---|
| Period | September 2024 (1 month) |
| Raw orders | 1,000 |
| Clean records | 990 |
| Total revenue | $35,575.93 |
| Columns | 24 |
| City zones | North · South · East · West |

<br>

---

## 📂 Dataset

The dataset `foodexpress_data_uncleaned.csv` contains **24 columns** spanning five categories:

| Category | Columns |
|---|---|
| **Order details** | `OrderID`, `OrderDate`, `OrderTime`, `DayOfWeek`, `TimePeriod` |
| **Customer info** | `CustomerSegment` (New / Regular / VIP), `City` |
| **Restaurant** | `RestaurantID`, `CuisineType`, `RestaurantRating` |
| **Delivery metrics** | `DeliveryTime`, `DeliveryDistance`, `DeliveryFee`, `WeatherCondition` |
| **Financials** | `OrderValue`, `DiscountAmount`, `PromoDiscount`, `TipAmount`, `CashPayment`, `CardPayment`, `WalletPayment`, `UPIPayment` |
| **Performance** | `CustomerRating`, `DeliveryPartnerRating` |

> ⚠️ **Note:** The raw file contains missing values, sentinel errors (`99999`), and invalid strings (`"INVALID"`, `"N/A"`). All issues are resolved in the cleaning pipeline documented below.

<br>

---

## 📁 Project Structure

```
FoodExpress-Data-Analytics/
│
├── FoodExpress Data Analytics Project.ipynb   # Main analysis notebook
├── foodexpress_data_uncleaned.csv             # Raw dataset
└── README.md                                  # This file
```

<br>

---

## 🛠 Tech Stack

| Library | Purpose |
|---|---|
| `pandas` | Data loading, cleaning, groupby, melt, feature engineering |
| `numpy` | Numerical operations, median imputation |
| `scipy` | t-tests, chi-square tests, winsorization |
| `matplotlib` | Base plotting |
| `seaborn` | Heatmaps, box plots, regression plots, facet grids |
| `statsmodels` | Tukey HSD post-hoc tests |

**Python version:** 3.13

<br>

---

## ⚙️ Installation & Setup

```bash
# 1. Clone the repository
git clone https://github.com/doyancha/FoodExpress-Data-Analytics.git
cd FoodExpress-Data-Analytics

# 2. Install dependencies
pip install pandas numpy scipy matplotlib seaborn statsmodels

# 3. Launch the notebook
jupyter notebook "FoodExpress Data Analytics Project.ipynb"
```

<br>

---

## 🔍 Key Analyses

### 1. Data Cleaning

The raw dataset contained **294 missing values** across 4 columns. A 6-step pipeline was applied:

| Step | Action | Result |
|---|---|---|
| 1 | Impute `CustomerRating`, `RestaurantRating`, `DeliveryTime`, `TipAmount` with column median | 294 nulls resolved |
| 2 | Replace sentinel value `99999` in `DeliveryTime` with median | Outlier corrected |
| 3 | Clean `"INVALID"` / `"N/A"` strings in `CustomerRating` → NaN → median fill | dtype fixed to `float64` |
| 4 | Convert `OrderDate` to `datetime64`; all financial columns to `float64` | Types corrected |
| 5 | Remove rows where `DeliveryTime > 99th percentile` OR `OrderValue < $5` | 10 rows dropped → **990 rows** |
| 6 | Reshape 4 payment columns from wide → long format using `melt()` | 1 row per payment |

```python
# Example: Reshape payment data (wide → long)
payment_cols = ['CashPayment', 'CardPayment', 'WalletPayment', 'UPIPayment']

df_payment = df_clean.melt(
    id_vars=[c for c in df_clean.columns if c not in payment_cols],
    value_vars=payment_cols,
    var_name='PaymentType',
    value_name='PaymentAmount'
)
df_payment = df_payment[df_payment['PaymentAmount'] > 0].copy()
# Result: 990 orders → 990 real payments (1:1 mapping)
```

<br>

---

### 2. Python Fundamentals

#### Total Revenue — For Loop

```python
total_revenue = 0.0
for value in df['OrderValue']:
    total_revenue += value

# Output: Total Revenue: $35,575.93
```

#### Premium Delivery Classifier

A delivery is **"Premium"** when `DeliveryFee > $5.00` AND `DeliveryTime < 25 minutes`.

```python
def is_premium_delivery(order_id):
    row = df[df['OrderID'] == order_id]
    if row.empty:
        return False
    return (row['DeliveryFee'].iloc[0] > 5.00) and (row['DeliveryTime'].iloc[0] < 25)

# Result: 49 premium deliveries identified
```

#### Average Order Value by Cuisine

```python
def avg_order_value_by_cuisine(cuisine_type):
    subset = df[df['CuisineType'] == cuisine_type]['OrderValue']
    if subset.empty:
        return None
    return {'cuisine': cuisine_type, 'avg': subset.mean(), 'count': len(subset)}
```

<br>

---

### 3. Feature Engineering — Net Revenue

A new `NetRevenue` column was engineered to capture true platform revenue after discounts and the 20% restaurant commission:

```
NetRevenue = OrderValue − DiscountAmount − PromoDiscount − (OrderValue × 0.20)
```

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

| Rank | City Zone | Net Revenue |
|---|---|---|
| 🥇 | North Zone | $6,631.72 |
| 🥈 | West Zone | $6,374.00 |
| 🥉 | South Zone | $6,060.36 |
| 4 | East Zone | $5,947.21 |

<br>

---

### 4. Visualizations

Six charts were produced to surface patterns in orders, revenue, and delivery performance:

| Chart | Type | Key Insight |
|---|---|---|
| Orders by cuisine | Bar chart | Indian leads with 152 orders |
| Revenue by cuisine × city | Heatmap | Identifies top cuisine-city combos |
| Payment method by segment | 100% stacked bar | Uniform spread across segments |
| Daily order trend | Line plot | Temporal patterns over September |
| Delivery time distribution | Box plot | Heavy right-skew; outliers in North Zone |
| Campaign impact | Paired scatter | Before vs After AOV per restaurant |

```python
# Heatmap: cuisine × city net revenue
pivot = df_payment.pivot_table(
    values='NetRevenue', index='CuisineType', columns='City', aggfunc='sum'
)
sns.heatmap(pivot, annot=True, fmt='.0f', cmap='YlOrRd', linewidths=0.5)

# Stacked bar: payment method preference by customer segment
pct = pd.crosstab(df_clean['CustomerSegment'], df_clean['PaymentMethod'],
                  normalize='index') * 100
pct.plot(kind='bar', stacked=True)
```

<br>

---

### 5. Statistical Tests

All tests conducted at significance level **α = 0.05**.

#### Test 1 — Independent Samples t-test: VIP vs Regular Ratings

```
H₀: Mean rating of VIP customers = Mean rating of Regular customers
H₁: The means are different
```

```python
from scipy import stats
vip_ratings     = df[df['CustomerSegment'] == 'VIP Customer']['CustomerRating']
regular_ratings = df[df['CustomerSegment'] == 'Regular Customer']['CustomerRating']
t_stat, p_value = stats.ttest_ind(vip_ratings, regular_ratings)
```

**Result:** `p ≥ 0.05` → **Fail to reject H₀**
> No significant difference in satisfaction between VIP and Regular customers. Operations are consistent across segments.

---

#### Test 2 — One-Sample t-test: North Zone Delivery Target

```
H₀: Mean delivery time in North Zone = 30 minutes
H₁: Mean delivery time ≠ 30 minutes
```

```python
north_delivery = df[df['City'] == 'North Zone']['DeliveryTime'].dropna()
t_stat, p_value = stats.ttest_1samp(north_delivery, popmean=30.0)
```

**Result:** Observed mean = **125 min** · Only **36.7%** of orders delivered within 30 min → **Reject H₀**
> North Zone significantly misses its 30-minute delivery target. Operational intervention needed.

---

#### Test 3 — Chi-Square Test of Association: Payment Method vs Customer Segment

```
H₀: Payment method choice is independent of customer segment
H₁: There is a significant association
```

**Result:** `p ≥ 0.05` → **Fail to reject H₀**
> Payment preferences are similar across all customer segments. A uniform payment promotion strategy is appropriate.

---

#### Test 4 — Chi-Square Goodness of Fit: Cuisine Distribution

```
H₀: Orders are equally distributed across 5 cuisines (20% each)
H₁: Distribution is not uniform
```

```python
from scipy.stats import chisquare
observed = df_clean[df_clean['CuisineType'].isin(
    ['Italian','Chinese','Indian','Fast Food','Mexican']
)]['CuisineType'].value_counts()
chi2, p_value = chisquare(observed)
# χ² = 9.11,  p = 0.0585
```

**Result:** `p = 0.0585` → **Fail to reject H₀** (marginal)
> Indian cuisine leads (152 orders) but the distribution is not significantly unequal at α = 0.05.

<br>

---

### 6. Business Intelligence

#### Correlation Analysis — Drivers of Customer Rating

Four factors were tested for correlation with `CustomerRating`:

| Factor | Direction | Strength | Insight |
|---|---|---|---|
| `DeliveryPartnerRating` | Positive | Strong | Biggest driver of customer satisfaction |
| `RestaurantRating` | Positive | Weak | Food quality matters but is secondary |
| `DeliveryDistance` | Negative | Weak | Longer distance → lower satisfaction |
| `OrderValue` | ~Zero | None | Spend level does not predict satisfaction |

```python
factors = ['DeliveryDistance', 'OrderValue', 'RestaurantRating', 'DeliveryPartnerRating']
correlations = {f: df['CustomerRating'].corr(df[f]) for f in factors}

# Visualize with 2x2 regression scatter grid
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
for idx, factor in enumerate(factors):
    sns.regplot(data=df, x=factor, y='CustomerRating',
                ax=axes.ravel()[idx], line_kws={'color': 'red'})
```

#### Promotional Campaign — Paired t-test

Average order value (AOV) per restaurant was compared **before (Week 1)** and **after (Week 3)** a promotional campaign using a paired t-test.

```python
before = df_campaign[df_campaign['Period'] == 'Before (Week 1)'] \
             .groupby('RestaurantID')['OrderValue'].mean()
after  = df_campaign[df_campaign['Period'] == 'After (Week 3)'] \
             .groupby('RestaurantID')['OrderValue'].mean()

paired = pd.concat([before, after], axis=1, join='inner')
t_stat, p_value = stats.ttest_rel(paired.iloc[:, 0], paired.iloc[:, 1])
```

| Metric | Value |
|---|---|
| AOV change | −13.3% |
| Revenue lift | −$7,228.79 |
| p-value | ≥ 0.05 |
| Verdict | No significant change |

<br>

---

## 💡 Key Findings

- **North Zone** generates the highest net revenue (**$6,631.72**) but has the worst delivery performance — only 36.7% of orders meet the 30-minute target.
- **Delivery partner quality** is the strongest predictor of customer satisfaction, not food quality or order value.
- **Indian cuisine** is the most ordered (152 orders), though cuisine demand is not significantly unequal across the five major types.
- **VIP and Regular customers** give statistically equivalent ratings — the platform delivers a consistent experience across segments.
- **Payment preferences** are uniform across customer segments — no segment shows a strong affinity for any one payment method.
- The **promotional campaign** showed no statistically significant impact on average order value.

<br>

---

## 📣 Recommendations

1. **Fix North Zone delivery operations** — invest in route optimization, partner allocation, or zone-specific SLAs to push the ≤30-min delivery rate above 70%.
2. **Prioritize delivery partner quality** — since partner rating is the top driver of customer satisfaction, implement tiered partner incentives tied to rating performance.
3. **Redesign the promo campaign** — flat discounts did not move AOV. Test bundling, free delivery thresholds, or limited-time cuisine-specific offers instead.
4. **Use volume-based campaigns** — since AOV is unresponsive to promos, shift marketing goals to order frequency and new customer acquisition.
5. **Always run pre/post paired tests** — formalize A/B measurement for every future campaign before committing budget.

<br>

---

## 📄 License

This project is for educational and analytical purposes.

---

<div align="center">
  <sub>Built with Python · pandas · scipy · seaborn · statsmodels</sub>
</div>
