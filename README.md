# Amazon_EDA_project
# 📊 Amazon Product Data Analysis (EDA)

## 🧠 Project Overview

This project performs **Exploratory Data Analysis (EDA)** on an Amazon product dataset to uncover insights about:

* Pricing strategies
* Discounts
* Customer ratings
* Product popularity

The analysis focuses on answering **real business questions** using data visualization and statistical techniques.

---

## 📁 Dataset Description

The dataset contains the following key features:

* `product_name` – Name of the product
* `category` – Product category
* `actual_price` – Original price
* `discounted_price` – Discounted price
* `discount_percentage` – Discount applied
* `rating` – Product rating (1–5)
* `rating_count` – Number of reviews

---

## 🧹 Data Cleaning

Before analysis, the dataset was cleaned:

* Removed currency symbols (₹) and converted prices to numeric
* Converted discount percentages to float
* Cleaned `rating_count` from commas
* Created a `short_name` column for better visualization

---

## 📊 Data Visualization

Each visualization answers a **specific business question**:

### 1️⃣ Category Distribution

**Question:** Which categories dominate the market?
**Insight:** Tech-related categories (e.g., Computers & Accessories) dominate product listings.

---

### 2️⃣ Price vs Discount

**Question:** Do expensive products get higher discounts?
**Insight:** No strong relationship — discounts vary across all price ranges.

---

### 3️⃣ Rating Distribution

**Question:** How satisfied are customers?
**Insight:** Most ratings fall between **3.5 and 4.5**, indicating generally positive feedback.

---

### 4️⃣ Top Rated Products

**Question:** Which products have the highest quality?
**Insight:** High-rated products often have consistent positive reviews.

---

### 5️⃣ Most Reviewed Products

**Question:** Which products are most popular?
**Insight:** Products with more reviews tend to be more trusted.

---

## ⚠️ Outlier Detection

### 🔍 Price Outliers

* Detected using **IQR method**
* Extreme values were identified

**Decision:**
Outliers were **not removed completely** because:

* They represent **premium products**
* They reflect **real-world market variation**

---

### 🔍 Rating Outliers

* Ratings outside range (1–5) were checked
* No major invalid values found

**Decision:**
All valid ratings were kept

---

### 🔍 Key Insight

> Not all outliers are errors — some represent valuable business insights.

---

## 📈 Before vs After Cleaning

* Visual comparison shows reduced skewness after filtering extreme values
* Cleaned data improves readability and analysis reliability

---

## 🚀 Key Insights

* The dataset is highly **skewed in price distribution**
* Discounts are applied across all price ranges
* High ratings dominate the dataset
* Popular products (high review count) are more reliable

---

## 🛠️ Tools & Technologies

* Python 🐍
* Pandas
* NumPy
* Matplotlib
* Seaborn

---

## 🎯 Conclusion

This project demonstrates how EDA can:

* Reveal hidden patterns
* Support business decisions
* Improve data quality

---

## 👨‍💻 Author

**Mostafa Gamal**


**Amany ibrahim**
---

## ⭐ Future Improvements

* Add machine learning model (price prediction)
* Build dashboard using Power BI or Streamlit
* Perform category-level deep analysis

---
