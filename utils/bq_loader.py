from google.cloud import storage
from google.cloud import bigquery
from google.cloud.exceptions import GoogleCloudError
import os



class GCPDataIngester():
    def __init__(self,project_id: str = None, credentials_path: str = None):


        # Set credentials env variable if a path is provided manually
        if credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
            
        self.project_id = project_id
        
        # Initialize clients (will automatically look for GOOGLE_APPLICATION_CREDENTIALS)
        self.storage_client = storage.Client(project=self.project_id)
        self.bigquery_client = bigquery.Client(project=self.project_id)

    def upload_to_gcs(self,bucket_name:str,source_file_path:str,destination_blob_name:str):
        """
        Uploads a local file to a Google Cloud Storage bucket.
        """
        try:
            bucket = self.storage_client.bucket(bucket_name)
            blob = bucket.blob(destination_blob_name)
            
            print(f"Uploading {source_file_path} to gcs://{bucket_name}/{destination_blob_name}...")
            blob.upload_from_filename(source_file_path)
            print("GCS Upload successful.")
            
            return blob.public_url
            
        except GoogleCloudError as e:
            print(f"GCS Upload failed: {e}")
            raise

    def load_gcs_to_bigquery(
        self, 
        gcs_uri: str, 
        dataset_id: str, 
        table_id: str, 
        source_format: bigquery.SourceFormat = bigquery.SourceFormat.CSV,
        autodetect_schema: bool = True
    ) -> bigquery.LoadJob:
        """
        Triggers a BigQuery load job to ingest a file directly from GCS.
        """
        try:
            table_ref = f"{self.bigquery_client.project}.{dataset_id}.{table_id}"
            
            # Configure the load job
            job_config = bigquery.LoadJobConfig(
                source_format=source_format,
                autodetect=autodetect_schema,
                write_disposition=bigquery.WriteDisposition.WRITE_APPEND, # Or WRITE_TRUNCATE to overwrite
            )
            
            print(f"Starting BigQuery load job from {gcs_uri} to {table_ref}...")
            load_job = self.bigquery_client.load_table_from_uri(
                gcs_uri, table_ref, job_config=job_config
            )
            
            # Wait for the job to complete
            load_job.result() 
            print(f"BigQuery load completed successfully. Loaded {load_job.output_rows} rows.")
            return load_job
            
        except GoogleCloudError as e:
            print(f"BigQuery load job failed: {e}")
            raise


