from celery import shared_task
from datetime import datetime
from io import BytesIO
import socket
import boto3
from backend.settings import VARICON_BUCKET_NAME
import logging
from counter.models import Counter
from time import sleep


LOGGER = logging.getLogger(__name__)


@shared_task
def s3_file_uploader(filename: str = None, content: str = None):
    LOGGER.debug(f"Started s3 file uploader: {filename=}, {content=}")
    hostname = socket.gethostname()
    now = datetime.utcnow()
    if filename is None:
        filename = now.isoformat().split(".")[0]
    filename = filename + "-" + hostname + ".txt"
    if not content:
        content = f"Uploaded by {hostname} on {now.isoformat()}".encode()
    bytes_data = BytesIO(content)
    s3 = boto3.client("s3")
    filepath = f"djangotest/{filename}"
    LOGGER.info(f"Uploading file on {VARICON_BUCKET_NAME}: {filepath}")
    s3.upload_fileobj(Fileobj=bytes_data, Bucket=VARICON_BUCKET_NAME, Key=filepath)


@shared_task(queue="last")
def counter_checker(timer):
    if timer:
        LOGGER.debug("Sleeping: {timer}")
        sleep(int(timer))
    last_counter = Counter.objects.all().order_by("-accessed_timestamp").first()
    if not last_counter:
        LOGGER.info("No counter")
        print("Print: No counter")
        return None
    LOGGER.info(f"Last accessed on: {last_counter}")
    print(f"Print: Last accessed on: {last_counter}")
    return last_counter.accessed_timestamp.isoformat()


@shared_task(queue="first")
def counter_checker_first(timer):
    if timer:
        LOGGER.debug("Sleeping: {timer}")
        sleep(int(timer))
    last_counter = Counter.objects.all().order_by("accessed_timestamp").first()
    if not last_counter:
        LOGGER.info("No counter")
        print("Print: No counter")
        return None
    LOGGER.info(f"Last accessed on: {last_counter}")
    print(f"Print: Last accessed on: {last_counter}")
    return last_counter.accessed_timestamp.isoformat()
