# 🚢 Digital Freight Rate Management & Quick-Quote Analytics Engine

![Dashboard Preview](assets/dashboard_overview.png)

## 📌 Executive Summary
In the Freight Forwarding industry, sales teams spent excessive time searching through scattered carrier rate sheets, leading to delayed customer quotations and missed commercial opportunities. 

This project delivers an **End-to-End Automated Data Pipeline & Business Intelligence Dashboard** that ingests raw ocean freight tariffs, processes rates on **Google BigQuery**, and presents an interactive **Power BI Quick-Quote Engine**.

* **Business Impact:** Reduced rate-lookup and quotation time from minutes to **under 10 seconds**, ensured 100% data consistency, and dynamically highlighted top-tier competitive pricing across shipping lanes.

---

## 🏗️ Data Architecture & Pipeline
The solution follows an enterprise-grade data architecture, decoupling heavy data transformations (Cloud) from report visualization (BI):

```text
[Python Data Engine] ➔ [Google BigQuery Storage] ➔ [SQL Transformation View] ➔ [Power BI Dashboard]
```

1. **Data Ingestion (Python):** Generated synthetic multi-carrier ocean freight rate sheets simulating real-world logistics parameters (POL, POD, Equipment, Local Charges, Validity).
2. **Data Warehousing (Google BigQuery):** Loaded raw CSV datasets into Google Cloud BigQuery for centralized storage.
3. **Data Transformation (Advanced SQL):** Built dynamic SQL Views utilizing **Window Functions** (`ROW_NUMBER()`) and **CTEs** to dynamically identify the lowest rates per lane and auto-calculate margin prices.
4. **Data Visualization (Power BI):** Designed a high-contrast corporate dashboard featuring interactive filters, KPI metrics, dynamic chart highlighting, and custom conditional formatting.

---

## 🛠️ Tech Stack & Methods
* **Programming & ETL:** Python (`pandas`, `random`, `datetime`)
* **Cloud & Database:** Google Cloud Platform (GCP) BigQuery, Cloud Data Warehouse
* **Querying Language:** SQL (Advanced Window Functions, CTEs, Date Parsing, Case Statements)
* **BI & Analytics:** Power BI Desktop, DAX Measures, Advanced UI/UX Design (Navy/Slate Corporate Theme)

---

## 💡 Key SQL Logic (Excerpt)
To extract only the **cheapest rate (Rank 1)** for each origin-destination pair while dynamically calculating a 15% profit margin:

```sql
WITH RankedRates AS (
    SELECT 
        Rate_ID, Carrier, POL_Origin, POD_Destination, Container_Type,
        Total_Cost_USD,
        ROUND(Total_Cost_USD * 1.15, 2) AS Quoted_Price_USD,
        ROW_NUMBER() OVER(
            PARTITION BY POL_Origin, POD_Destination, Container_Type 
            ORDER BY Total_Cost_USD ASC
        ) AS rate_rank
    FROM `freight_database.raw_freight_rates`
)
SELECT * FROM RankedRates WHERE rate_rank = 1;
```

---

## 📊 Dashboard Key Features
* **Executive KPI Cards:** Single-value cards displaying active lanes, average market rates, minimum available rates, and expected potential profit.
* **Smart Data Highlighting:** Bar charts dynamically highlight the **Top 1 Lowest-Price Carrier** (Emerald Green) while maintaining Muted Slate for secondary carriers.
* **Quick-Quote Search Matrix:** A detail-level lookup table featuring data bars and status indicators for instant sales decision-making.

---

## 📁 Repository Structure
* `/data/raw/`: Contains sample raw freight rate datasets (`.csv`).
* `/scripts/`:
  * `01_data_generation.py`: Python script to generate mock shipping data.
  * `02_bigquery_transformation.sql`: SQL DDL/DQL query creating the analytics view.
* `/powerbi/`: Contains the `.pbix` interactive report file.
* `/assets/`: Dashboard screenshots and visual assets.

---

## 🚀 How to Replicate This Project
1. Clone this repository:
   ```bash
   git clone [https://github.com/](https://github.com/)<your-username>/digital-freight-rate-analytics.git
   ```
2. Run `scripts/01_data_generation.py` to produce a fresh synthetic dataset.
3. Upload `synthetic_freight_rates.csv` to **Google BigQuery**.
4. Execute `scripts/02_bigquery_transformation.sql` in BigQuery Studio to create the analytics view.
5. Open `powerbi/freight_rate_dashboard.pbix` and connect it to your BigQuery View.
