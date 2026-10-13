import os
import json
import base64
from azure.storage.queue import QueueClient


QUEUE_NAME = "task-processing"


def get_queue_client():
    connection_string = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")

    if not connection_string:
        raise ValueError(
            "AZURE_STORAGE_CONNECTION_STRING environment variable is missing"
        )

    return QueueClient.from_connection_string(
        conn_str=connection_string,
        queue_name=QUEUE_NAME
    )


def send_task_message(task_id, file_name):
    queue_client = get_queue_client()

    message = {
        "taskId": task_id,
        "fileName": file_name,
        "action": "process-attachment"
    }

    message_json = json.dumps(message)

    encoded_message = base64.b64encode(
        message_json.encode("utf-8")
    ).decode("utf-8")

    response = queue_client.send_message(encoded_message)

    return {
        "status": "success",
        "queue": QUEUE_NAME,
        "message_id": response.id,
        "message": message
    }