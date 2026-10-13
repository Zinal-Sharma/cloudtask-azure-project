import logging
import azure.functions as func

app = func.FunctionApp()


@app.function_name(name="ProcessTask")
@app.queue_trigger(
    arg_name="msg",
    queue_name="task-processing",
    connection="AzureWebJobsStorage"
)
def ProcessTask(msg: func.QueueMessage) -> None:

    message = msg.get_body().decode("utf-8")

    logging.info("===================================")
    logging.info("CloudTask ProcessTask Function")
    logging.info("Queue message received:")
    logging.info(message)
    logging.info("===================================")