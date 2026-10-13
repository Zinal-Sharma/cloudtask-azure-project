import os
from azure.storage.blob import BlobServiceClient


def get_blob_service_client():

    connection_string = os.environ["AZURE_STORAGE_CONNECTION_STRING"]

    return BlobServiceClient.from_connection_string(
        connection_string
    )


def upload_file(file):

    blob_service_client = get_blob_service_client()

    container_name = "task-attachments"

    blob_client = blob_service_client.get_blob_client(
        container=container_name,
        blob=file.filename
    )

    blob_client.upload_blob(
        file,
        overwrite=True
    )

    return blob_client.blob_name