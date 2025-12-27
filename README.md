# Food# FoodExpress Data Analytics Assignment 📊🚀

**Case Study**: FoodExpress – A fast-growing food delivery platform optimizing operations through data-driven insights.

**Dataset**: `foodexpress_data_uncleaned.csv`  
**Time Period**: One full month (September 2024)  
**Total Orders Analyzed**: 1,000  
**Total Revenue Generated**: **$35,575.93**

---

## 📈 Key Business Highlights & Insights

| Metric                        | Value                  | Insight                                                                 |
|-------------------------------|------------------------|-------------------------------------------------------------------------|
| **Total Platform Revenue**    | **$35,575.93**         | Strong monthly performance across all cities                            |
| **Average Order Value (AOV)** | ~$35.58                | Solid baseline – room for upselling strategies                          |
| **Premium Deliveries**        | **49 orders**          | High-value fast deliveries (Fee > $5 & Time < 25 min) – 4.9% of total    |
| **Customer Segments**         | New, Regular, VIP      | VIP customers typically drive higher AOV and loyalty                    |
| **Top Performing Areas**      | Multiple zones/cuisines| Opportunities for targeted marketing and partnerships                   |

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Dataset Overview](#dataset-overview)
3. [Data Quality Check](#data-quality-check)
4. [Section 1: Python Fundamentals](#section-1-python-fundamentals)
   - [Total Revenue via Loop](#1-total-revenue-calculation)
   - [Premium Delivery Function](#2-premium-delivery-identifier)
   - [All Premium Deliveries](#bonus-all-premium-deliveries)
5. [Advanced Analysis: Promotional Campaign Impact](#advanced-analysis-promotional-campaign-impact)
   - [Paired t-test Results](#paired-t-test-results)
   - [Visualization](#visualization)
   - [ROI Calculation](#roi-calculation)
6. [Strategic Business Recommendations](#strategic-business-recommendations)
7. [Technical Stack](#technical-stack)

---

## Project Overview

This comprehensive analytics assignment showcases practical application of **Python programming, data manipulation, statistical testing, and visualization** to drive actionable business decisions for FoodExpress.

**Core Objectives Achieved**:
- Implement fundamental programming concepts (loops, conditionals, functions)
- Perform data cleaning and exploratory checks
- Identify high-value delivery segments
- Rigorously evaluate promotional campaign effectiveness using **paired t-test**
- Deliver clear, data-backed recommendations

---

## Dataset Overview

**Key Dimensions**:

| Category               | Key Columns                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| Orders                 | `OrderID`, `OrderDate`, `OrderTime`, `DayOfWeek`, `TimePeriod`              |
| Customers              | `CustomerSegment` (New / Regular / VIP), `City`                             |
| Restaurants            | `RestaurantID`, `CuisineType`, `RestaurantRating`                           |
| Delivery               | `DeliveryTime`, `DeliveryDistance`, `DeliveryFee`, `WeatherCondition`       |
| Financials             | `OrderValue`, `DiscountAmount`, `PromoDiscount`, `TipAmount`, Payment types |
| Ratings                | `CustomerRating`, `DeliveryPartnerRating`                                   |

**Unique Values**:
- **Cities/Zones**: East Zone, West Zone, South Zone
- **Cuisine Types**: Fast Food, Mexican, Chinese, American, and more
- **Payment Methods**: Cash, Card, Wallet, UPI

---

## Data Quality Check

**Missing Values Summary**:

| Column                | Missing Count | % of Total |
|-----------------------|---------------|------------|
| CustomerRating        | 79            | 7.9%       |
| RestaurantRating      | 75            | 7.5%       |
| DeliveryTime          | 70            | 7.0%       |
| TipAmount             | 70            | 7.0%       |
| **Total Missing**     | **294**       | ~7.35%     |

**Strategy**: Imputation or exclusion applied as needed for specific analyses.

---

## Section 1: Python Fundamentals

### 1. Total Revenue Calculation

**Task**: Compute total revenue using a **pure Python for-loop** (no `.sum()` shortcut).

```python
total_revenue = 0.0
for value in df['OrderValue']:
    total_revenue += value

print(f"Total Revenue: ${total_revenue:,.2f}")Express-Data-Analytics
```
### Advanced Analysis: Promotional Campaign Impact 📈

**Objective**:  
Measure if a Week 2 promotional campaign **sustainably increased Average Order Value (AOV)** in Week 3 compared to Week 1.

**Methodology**:
- Matched restaurants active in **both Week 1 (Before)** and **Week 3 (After)**
- Computed **per-restaurant Average Order Value (AOV)** for each period
- Applied **paired t-test** for statistical rigor

#### Paired t-test Results

| Metric                     | Value                          |
|----------------------------|--------------------------------|
| **Sample Size**            | Matched restaurants across periods |
| **Average Change**         | **-13.3%**                     |
| **p-value**                | Not significant (≥ 0.05)       |
| **Conclusion**             | **No statistically significant impact on AOV** |

#### Visualization

![Campaign Impact: Average Order Value Before vs After](Campaign%20Impact:%20Average%20Order%20Value%20Before%20vs%20After.png)

*Paired scatter plot with 45° reference line — most points near or below the line indicate neutral or negative shift.*

#### ROI Calculation

| Metric                        | Value             |
|-------------------------------|-------------------|
| Estimated Revenue Lift        | **-$7,228.79**    |
| Percentage Lift               | **-13.3%**        |
| Statistical Significance      | No                |

**Verdict**:  
The campaign **did not deliver positive ROI** on AOV uplift.

#### Strategic Business Recommendations

| Scenario Outcome                  | Recommendation                                                                                   | Priority  |
|-----------------------------------|--------------------------------------------------------------------------------------------------|-----------|
| **No Significant AOV Change**     | Do not repeat identical promo mechanics                                                          | High      |
|                                   | Extend observation window (4–6 weeks post-campaign)                                               | High      |
|                                   | Shift focus to **order volume** drivers (e.g., free delivery thresholds)                         | High      |
|                                   | Test alternative incentives: bundling, limited-time menus, loyalty points                       | Medium    |
|                                   | Segment analysis: Did promo attract lower-AOV customers?                                          | Medium    |
| **Future Campaign Best Practices**| Always implement **pre/post paired analysis** on same entities                                   | Critical  |
|                                   | Track both **AOV** and **order frequency**                                                       | Critical  |
|                                   | Prioritize **profitable growth** over raw revenue spikes                                         | Critical  |

**Biggest Opportunity Identified**:  
**Premium Deliveries** – Only **49** identified, but they combine **high delivery fees** with **fast service (<25 min)**.  
**Actionable Insight**: Scaling this segment through dedicated partner routing, priority dispatch, and targeted marketing could **significantly boost margins**.

---

# FoodExpress September 2024 Analytics 📊

## Key Findings Summary

═══════════════════════════════════════════════════════

### 1. Delivery Performance 🚚
- Delivery times are **highly consistent** across all four city zones (no significant differences, **p = 0.49**).
- **North Zone** stands out as the most predictable (lowest variability).
- Typical delivery time is **~37 minutes**, but extreme outliers (likely data errors) inflate averages.

**Key Takeaway**: Excellent operational uniformity — a major competitive strength.

### 2. Customer Segments & Ratings ⭐
- Orders are well-balanced:
  - **VIP**: 36.5%
  - **Regular**: 32.5%
  - **New**: 31.0%
- VIP and Regular customers rate the service almost identically (no significant difference, **p = 0.24**).

**Key Takeaway**: Service consistency is strong, but the **VIP program isn't creating a clear "premium" satisfaction boost**.

### 3. Cuisine Popularity 🍕
- **Indian** dominates at **24%**, closely followed by:
  - Fast Food (20%)
  - Italian (20%)
  - Mexican (19%)
  - Chinese (17%)
- Distribution is close to uniform (no significant deviation, **p = 0.06**).

**Key Takeaway**: Indian leads slightly, but all major cuisines enjoy healthy popularity and variety.

### 4. Payment Preferences 💳
- Preferences are **similar across all customer segments**: Card and UPI lead, followed by Cash and Wallet.
- No significant association between customer segment and payment method (**p = 0.45**).

**Key Takeaway**: Payment behavior is uniform → broad campaigns and offers will reach all users effectively.

### 5. Factors Affecting Ratings & Revenue 📈
- **Weak correlations** overall: delivery time, order value, and discounts have minimal impact on customer or restaurant ratings.
- **Loyalty** (repeat orders) shows the strongest (though still moderate) link to higher restaurant ratings.

**Key Takeaway**: Ratings are driven more by **food quality and consistency** than by speed or price.

### 6. Campaign Effectiveness 🎯
- The recent promotional campaign showed **no significant impact** on average order value (slight -13% change, **p = 0.38**).

**Key Takeaway**: The current promo structure **did not increase spending per order**.

## Overall Business Implications

FoodExpress has achieved **rare operational consistency** across zones, customer segments, and days of the week. This reliability is a **powerful foundation** and a true differentiator in the competitive food delivery space.

While speed matters, it is **not the primary driver** of customer satisfaction — food quality and restaurant consistency play a bigger role.

The **VIP program** and recent promotions need refinement to deliver clearer, measurable value.

## Top Priorities Moving Forward

1. **Leverage consistency in marketing**  
   → Position FoodExpress as the "Most Reliable Delivery Everywhere"

2. **Strengthen VIP perks**  
   → Introduce benefits that create real perceived premium value and higher satisfaction

3. **Focus partnerships on restaurants loved by loyal customers**  
   → Prioritize high-rated, repeat-order restaurants to boost overall ratings

4. **Clean data outliers and optimize operations**  
   → Further reduce variability and aim for uniform speed improvements

5. **Test new promotion types**  
   → Design campaigns that explicitly boost **order value** (e.g., bundling, upselling) rather than just volume

**Conclusion**:  
FoodExpress is in a **strong position**, small, targeted improvements on top of this solid foundation can drive **significant profitability and growth**.

---
**Analysis completed: December 27, 2025**  
**Data period: September 2024**

#### Technical Stack

- **Language**: Python 3
- **Libraries**: `pandas`, `numpy`, `matplotlib`, `seaborn`, `scipy.stats`, `statsmodels`
- **Techniques**: Loops, functions, conditional logic, statistical testing, data visualization

---

**Prepared by**: [Mir Shahadut Hossain]  
**Date**: December 27, 2025  

**Ready to drive FoodExpress to the next level with data!** 💪🍔📈
