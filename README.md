# ANAC Airport Data Engineering Pipeline using Modern Data Warehouse Architeture


> An end-to-end automated ELT pipeline that ingests public civil aviation data from Brazil’s ANAC (Agência Nacional de Aviação Civil) which uses Python, Google Cloud Storage, Google BigQuery, dbt and Terraform to simulate a Modern DataWarehouse Architeture. The data is make available in Big Query datasets.

## 🏗 Pipeline Architecture
<picture>
  <!-- Image shown in GitHub Dark Mode -->
  <source media="(prefers-color-scheme: dark)" srcset="ELT_using_dbt-darkmode.drawio.png" width= 800>
  
  <!-- Image shown in GitHub Light Mode (Fallback) -->
  <img alt="ETL Architeture" src="ELT-using-dbtclear.drawio.png" width= 800>
</picture>

## 💡 Business Scenario & Objectives
* **Objective:** Ingest data from Brazil´s ANAC portal inside Google BigQuery and create a dbt pipeline to transform data with some analytic model to answer questions like:
  - Which flight was delayed?
  - How many trips occurred in a certain state?
  - What is the average cargo carried by an airplane?
  - All these questions can be answered using the models deployed in the project.

## 🛠 Tech Stack

| Component | Tool / Technology |
| :--- | :--- |
| **Ingestion (Extract/Load)** | Python
| **Storage (Data Lake)** | GCP GCS
| **Data Warehouse** | BigQuery
| **Transformation** | dbt (Data Build Tool)
| **IaC** | Terraform
| **Data Quality & Testing** | dbt tests 

---

## 📐 Data Modeling & Schema

Describe how data flows from landing to presentation layers:

* **Staging Layer (`stg_`):** Standardizes field names, casts data types, and deduplicates raw JSON/CSV inputs.
* **Intermediate Layer (`int_`):** Handles complex joins between dimensional and fact table
* **Marts Layer (`fct_`, `dim_`):** Star-schema layout optimized for querying.
  * `fct_flight_movement`: The central fact table for Brazilian flight operations, recording every recorded aircraft landing or takeoff event along with consolidated passenger volumes and freight logistics.

  * `fct_flight_delays`:  A specialized analytical fact table focused on flight schedule reliability and delays. It flags whether individual flight movements missed their scheduled slots based on actual gate chocks timestamps. 

  * `fct_cargo_logistics`: A specialized analytical fact table focused on cargo and postal logistics across Brazilian flight movements. It calculates the consolidated weight handled per flight and is ordered by the heaviest payloads.

  * `reporting/fct_flights_groupby_airports`: A high-level regional summary mart aggregating monthly flight frequencies and total passenger volumes. It partitions atomic movement events by year, month, and airport state/city localization.

---
## 🧪 Data Quality & Governance

Data integrity is tested automatically on every run:
* **Schema Tests:** Uniqueness, non-null, and referential integrity (foreign keys) enforced via `dbt`.

---

## 🚀 Running the Pipeline Locally


## Prerequisites
- **Terraform**: >= 1.5.0
- **uv**: [Installed](https://docs.astral.sh/uv/getting-started/installation/)
- **dbt-core** (or specific adapter, e.g., `dbt-snowflake`, `dbt-bigquery` managed via `uv`)
- **Cloud Credentials**: Authenticated CLI access
- Python 3.10+

### Reproducing Results

#### 1. Environment & Setup
Before running the pipeline, you must configure your environment variables and Terraform values.

Clone the repo and sync Python dependencies (including dbt):

```bash

git clone https://github.com/silvaaraujo98/dbt-project-anac.git

cd dbt-project-anac

chmod +x run_pipeline.sh

./run_pipeline.sh
```

### 2. Verification
Once dbt build finishes, verify your pipeline output:

- **dbt status:** All models,  tests and seed pass.
- **Output tables:** Created in target schema (e.g., `analytics.fct_results`) or check the tables in Google BigQuery. 
- **Evaluation tables:** We use dbt_project_evaluator to evaluate all our dbt models against dbt best practices, and the evaluation tables are created in BigQuery.







