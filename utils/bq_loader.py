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

    def upload_to_gcs(self,bucket_name:str,destination_blob_name:str,clean_text:str) -> str:
        """
        Uploads a local file to a Google Cloud Storage bucket.
        """
        try:
            bucket = self.storage_client.bucket(bucket_name)
            blob = bucket.blob(destination_blob_name)
            
            print(f"Uploading file to gcs://{bucket_name}/{destination_blob_name}...")
            blob.upload_from_string(clean_text, content_type='text/csv')
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

            column_names = ["ANO","MES","NR_AEROPORTO_REFERENCIA","NR_MOVIMENTO_TIPO","NR_AERONAVE_OPERADOR","NR_AERONAVE_MARCAS",
                            "NR_AERONAVE_TIPO","NR_VOO_OUTRO_AEROPORTO",
                            "NR_VOO_NUMERO","NR_SERVICE_TYPE","NR_NATUREZA","DT_PREVISTO","HH_PREVISTO","DT_CALCO","HH_CALCO",
                            "DT_TOQUE","HH_TOQUE","NR_CABECEIRA","NR_BOX","NR_PONTE_CONECTOR_REMOTO","NR_TERMINAL","QT_PAX_LOCAL",
                            "QT_PAX_CONEXAO_DOMESTICO","QT_PAX_CONEXAO_INTERNACIONAL","QT_CORREIO","QT_CARGA"]

            # Note: I noticed "NR_AERON" repeats or has variations in headers. 
            # Ensure "NR_AERON_1" or similar matches your file exactly if they are distinct columns!

            # 2. Programmatically generate the schema with all fields as STRING
            all_string_schema = [bigquery.SchemaField(name, "STRING") for name in column_names]
            table_ref = f"{self.bigquery_client.project}.{dataset_id}.{table_id}"
            
            # Configure the load job
            job_config = bigquery.LoadJobConfig(
                source_format=source_format,
                autodetect=False,
                skip_leading_rows = 1,
                schema=all_string_schema,
                write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
                field_delimiter=";",
                null_marker="null" #To treat "null" as null
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


