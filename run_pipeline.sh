
#!/usr/bin/env bash
set -e # Exit immediately if a command fails

echo "==> [1/3] Provisioning Terraform infrastructure..."
terraform init
terraform apply -auto-approve

echo "==> [2/3] Running Python ingestion script..."
uv sync
uv run python main.py

echo "==> [3/3] Running dbt build..."
cd anac_project
uv run dbt deps
uv run dbt build
uv run dbt build --select package:dbt_project_evaluator
echo "==> Pipeline execution complete!"