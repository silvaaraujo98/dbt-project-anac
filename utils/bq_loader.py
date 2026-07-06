from google.cloud import storage,bigquery
import pandas as pd
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

    def upload_to_gcs(self,file_name:str,df:pd.DataFrame) -> str:
        """
        Upload a dataframe to gcs in parquet format
        """
        try:
            
            df.to_parquet(f"gs://anac-landing-zone/{file_name}.parquet",index=False)
            
            
        except GoogleCloudError as e:
            print(f"GCS Upload failed: {e}")
            raise

        return f"gs://anac-landing-zone/{file_name}.parquet"


    def load_gcs_to_bigquery(
        self, 
        gcs_uri: str, 
        dataset_id: str, 
        table_id: str, 
        source_format: bigquery.SourceFormat = bigquery.SourceFormat.PARQUET,
        autodetect_schema: bool = True
    ) -> bigquery.LoadJob:
        """
        Triggers a BigQuery load job to ingest a file directly from GCS.
        """
        try:
            # Note: I noticed "NR_AERON" repeats or has variations in headers. 
            # Ensure "NR_AERON_1" or similar matches your file exactly if they are distinct columns!

            # 2. Programmatically generate the schema with all fields as STRING
            table_ref = f"{self.bigquery_client.project}.{dataset_id}.{table_id}"
            
            # Configure the load job
            job_config = bigquery.LoadJobConfig(
                source_format=source_format,
                autodetect=False,
                write_disposition=bigquery.WriteDisposition.WRITE_APPEND
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


