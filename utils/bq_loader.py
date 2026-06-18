from google.cloud import storage
from dotenv import dotenv_values


# Instantiates a client

try:
    config = dotenv_values(".env")
    service_account_credential = config.SERVICE_ACCOUNT_CREDENTIALS
    storage_client = storage.Client(service_account_credential)
except Exception as e:
    print(f"We´ve got some error: {e}")
else:
    print("Everything works well, the client is ready to use")

