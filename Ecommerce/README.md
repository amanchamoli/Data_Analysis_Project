# 📊 From Chaos to Clarity: E-Commerce Data Analysis  
**Python | SQL | Power BI**

---

## 📌 Project Overview
This repository contains an **end-to-end E-Commerce Data Analysis project** using **Python, SQL, and Power BI** on a real-world dataset.

The project focuses on how **raw, unclean data leads to misleading business insights** and how proper **data cleaning, validation, and analysis** transform it into **accurate, decision-ready intelligence**.

---

## 📂 Dataset Information
- **Dataset:** Brazilian E-Commerce Public Dataset by Olist  
- **Source:** Kaggle  
  https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce  
- **Time Period:** 2016 – 2018  
- **Records:**  
  - Raw: ~115,610  
  - Cleaned: 96,516  
- **Tables Used:** Customers, Orders, Products, Sellers, Payments, Reviews, Geolocation, Categories  

---

## 🎯 Project Objectives
- Assess data quality issues in raw business data  
- Clean and prepare analysis-ready datasets  
- Compare insights **before vs after data cleaning**  
- Answer company-level business questions using SQL  
- Present insights through Power BI dashboards  

---

## 🛠 Tools & Technologies
- **Python:** pandas, numpy, matplotlib, seaborn  
- **SQL:** MySQL  
- **Visualization:** Power BI  
- **Reporting:** PowerPoint  

---

## 🔄 Project Workflow

1️⃣ Data Assessment
2️⃣ EDA on Raw Data
3️⃣ Data Cleaning & Feature Engineering
4️⃣ EDA on Cleaned Data
5️⃣ SQL Business Analysis
6️⃣ Power BI Dashboard
7️⃣ Final Report & Presentation


---

## 🧹 Key Data Cleaning Steps
- Removed ~10% duplicate records  
- Handled missing values and incorrect data types  
- Treated extreme outliers  
- Fixed multi-payment revenue duplication  
- Engineered new features:
  - Delivery time
  - Items per order
  - Product density
- Standardized category and regional labels  
- Grouped low-frequency states into **“Other”**

---

## 📈 EDA Comparison Highlights

### Before Cleaning
- Inflated revenue
- Unrealistic freight values
- Missing delivery dates
- Highly skewed ratings
- Misleading relationships

### After Cleaning
- 100% duplicate removal  
- ~90% freight noise reduction  
- Complete delivery coverage  
- Insight accuracy improved from ~70% to ~94%  

---

## 🧮 SQL Business Insights
- Average delivery time ≈ **11 days** (SP fastest)  
- Top revenue categories: **Home, Electronics, Health**  
- Delivery delay > 30 days → rating drops ~1.5⭐  
- High-value orders mainly use **2–4 installments**  
- Seller ratings consistent nationwide (~4⭐)  

---

## 💼 Business Insights
### 📦 Operations
- Delivery SLA established: 11 days  
- Multi-item orders take ~3 days longer  

### 💳 Finance
- ~10% revenue overstatement found in raw data  
- EMI usage increases with order value  

### 💬 Customer Experience
- Delivery ≤ 10 days → rating ≥ 4.2⭐  
- Delays > 25 days → ratings drop to ~3⭐  

---

## 📊 Key KPIs
- Total Revenue  
- Total Orders  
- Average Order Value (AOV)  
- Average Delivery Time  
- Delivery Delays  
- Customer Ratings  
- Payment Methods  
- Category & Regional Performance  

---

## 📊 Power BI Dashboard
- Interactive dashboard for stakeholders  
- KPI tracking and trend analysis  
- Designed for business decision-making  

---

## 📂 Repository Structure
📁 Data-Analysis-Project
│
├── 📁 data
│ ├── raw_data
│ └── cleaned_data
│
├── 📁 python_analysis
│ ├── data_assessment.ipynb
│ ├── eda_before_cleaning.ipynb
│ ├── data_cleaning.ipynb
│ └── eda_after_cleaning.ipynb
│
├── 📁 sql_queries
│ └── business_questions.sql
│
├── 📁 power_bi
│ └── dashboard.pbix
│
├── 📁 reports
│ ├── final_report.pdf
│ └── presentation.pptx
│
└── README.md


---

## 🏁 Conclusion
This project demonstrates how **clean, structured data enables accurate business insights**.

By integrating **Python for analysis, SQL for validation, and Power BI for visualization**, the project shifts analysis from assumptions to **evidence-based decision making**.

---

## ✨ Author
**Aman Chamoli**
