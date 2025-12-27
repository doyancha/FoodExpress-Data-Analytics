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
