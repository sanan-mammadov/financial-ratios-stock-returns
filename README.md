# Financial Ratios & Stock Returns Analysis (BIST 100)

## Overview
This project investigates whether fundamental financial ratios can be used to forecast short-term stock returns. I programmatically collected and processed 8 years of quarterly financial statements (2016-2023) for 27 manufacturing firms listed on Türkiye's BIST 100 index. 

## Tech Stack & Methodology
* **Data Mining (Python):** Automated the extraction of financial statements and historical stock prices using `pandas` and `requests`. Engineered features including ROA, ROE, Net Income Margin, EBITDA Margin, Current/Quick/Cash Ratios, and Debt-to-Equity.
* **Statistical Modeling (R):** * Applied **Ordinary Least Squares (OLS)** as a baseline.
  * Deployed **Robust Regression** (MM-estimator) to downweigh the impact of extreme outliers in quarterly financial data.
  * Utilized **Lasso Regularization** to handle multicollinearity among profitability metrics.
  * Built a **Random Forest** machine learning model to test for non-linear predictive signals.

## Key Findings
* **Debt-to-Equity** showed a statistically significant negative correlation with short-term stock returns.
* **Cash Ratios** negatively impacted investor sentiment when evaluated under robust regression models.
* **Conclusion:** The models indicate that while fundamental ratios are crucial for long-term valuation, they explain a very small percentage of *short-term* stock volatility (~1.8%), which is more heavily driven by macroeconomic news and immediate market sentiment.

## View the Full Report
For an in-depth breakdown of the correlation matrices, descriptive statistics, and model summaries, please view the [Full PDF Report](DSBE510_Final_Project_Report_SM.pdf) included in this repository.

*(Tip: You can drag and drop your Correlation Heatmap image right here into the GitHub editor and it will automatically display it!)*<img width="672" height="468" alt="Figure 1_Correlation Heatmap" src="https://github.com/user-attachments/assets/187ac2a3-7135-40df-871d-6b7b296232dc" />
![Uploading Figure 1_Correlation Heatmap.png…]()
<img width="1021" height="467" alt="Table 5_Robust Regression Coefficients" src="https://github.com/user-attachments/assets/15866338-3c1b-49d6-b1f8-d1d5dba8ef25" />
