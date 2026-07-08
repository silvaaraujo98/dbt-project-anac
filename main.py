from utils import anac_extractor
from utils import bq_loader
import logging 
import timeit

year = "2025"
month = "12"

logger = logging.getLogger("")

# Configure the root logger to accept INFO levels and above
logging.basicConfig(level=logging.INFO)
extraction_start = timeit.default_timer()
logger.info(f"Start to extract the data from ANAC{month}-{year}")

anac_extractor  = anac_extractor.AnacExtractor(year,month)
df = anac_extractor.extract_data()
extraction_end = timeit.default_timer()
logger.info(f"Finished the extraction and the execution time was: {extraction_end - extraction_start:.3f} secs")

ingestion_gcs_start = timeit.default_timer()
logger.info("Starting the ingestion to GCS")
gcp_ingester = bq_loader.GCPDataIngester("data-core-platform")
path = gcp_ingester.upload_to_gcs(f"airplane_movements_{year}{month}",df)

ingestion_gcs_end = timeit.default_timer()
logger.info(f"Finished the ingestion to GCS and the ingestion time was: {ingestion_gcs_end - ingestion_gcs_start:.3f} secs")

ingestion_bq_start = timeit.default_timer()
logger.info("Starting the ingestion to BigQuery")
gcp_ingester.load_gcs_to_bigquery(path,"anac_source","movements_raw")
ingestion_bq_end = timeit.default_timer()
logger.info(f"Finished the ingestion to BigQuery and the ingestion time was: {ingestion_bq_end - ingestion_bq_start:.3f} secs")
logger.info(f"All the process taked {ingestion_bq_end - extraction_start:.3f} secs")