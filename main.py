from utils.bq_loader import GCPDataIngester
from google.cloud import bigquery

if __name__ == "__main__":
    data_ingester = GCPDataIngester('data-core-platform','service_account_credentials.json')
    bucket= 'anac-landing-zone'
    gcs_filename = 'data/raw_test'
    data_ingester.upload_to_gcs(bucket,'test.csv',gcs_filename)
    data_ingester.load_gcs_to_bigquery(
        gcs_uri=f"gs://{bucket}/{gcs_filename}",
        dataset_id="anac_source",
        table_id="test",
        source_format=bigquery.SourceFormat.CSV
    )

