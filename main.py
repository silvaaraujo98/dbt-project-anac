from utils import anac_extractor
from utils import bq_loader
import logging 

year = "2025"
month = "10"

logger = logging.getLogger("ANAC ETL")

# Configure the root logger to accept INFO levels and above
logging.basicConfig(level=logging.INFO)

logger.info("Start to extract the data from ANAC")

anac_extractor  = anac_extractor.AnacExtractor(year,month)
clean_text = anac_extractor.extract_data()
logger.info("Finished the extraction")

logger.info("Starting the ingestion to GCS")
gcp_ingester = bq_loader.GCPDataIngester("data-core-platform")
gcp_ingester.upload_to_gcs("anac-landing-zone",f"airplane_movements_{year}{month}.csv",clean_text)
logger.info("Finished the ingestion to GCS")

logger.info("Starting the ingestion to BigQuery")
gcp_ingester.load_gcs_to_bigquery("gs://anac-landing-zone/airplane_movements_*.csv","anac_source","movements_raw")
logger.info("Finished the ingestion to BigQuery")