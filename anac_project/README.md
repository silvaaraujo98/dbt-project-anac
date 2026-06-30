# ✈️ ANAC Airport Movement Analysis 🇧🇷

Welcome! This is a dbt project to process, model, and analyze airport movement data from Brazil's National Civil Aviation Agency (ANAC).

The goal of this project is to transform raw, semi-structured CSV files into a clean, reliable, and analytics-ready data warehouse in Google BigQuery.

To get started:
1. Set up your database connection in `~/.dbt/profiles.yml`. If you got here by running `dbt init`, you should already be good to go.
2. Ensure your raw data has been loaded into the `anac_source.movements_raw` table in BigQuery.
3. Run `dbt build` to materialize all models and run tests.

> [!NOTE]
> If you're brand-new to dbt, we recommend starting with the [dbt Learn](https://learn.getdbt.com/) platform. It's a free, interactive way to learn dbt, and it's a great way to get started if you're new to the tool.