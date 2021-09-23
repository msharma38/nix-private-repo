import gzip
from math import inf
import shutil
import os
from pathlib import Path
from time import time
from config import upload_timeout_seconds
from os import path
from azure.storage.blob import BlobServiceClient
from prometheus_client import Gauge, Histogram
import timeout_decorator

upload_file_to_cloud_histogram = Histogram(
    "upload_file_to_cloud", "Number of seconds to upload a file to azure"
)
bytes_per_second_upload_gauge = Gauge(
    "bytes_per_second_upload", "Speed of file uploads, bytes per second"
)
zip_file_histogram = Histogram(
    "zip_file",
    "How long it takes to gzip file",
    buckets=(.1, .25, .5, .75, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 7.5, 10.0, 15.0, inf)
)

def delete_file(file_path: str):
    print(f"Deleting {file_path}")
    parent_dir = os.path.dirname(file_path)
    os.remove(file_path)
    is_parent_dir_empty: bool = len(os.listdir(parent_dir)) == 0
    if is_parent_dir_empty:
        print(f"Directory {parent_dir} empty. Deleting it now")
        os.rmdir(parent_dir)


@timeout_decorator.timeout(upload_timeout_seconds)
@upload_file_to_cloud_histogram.time()
def upload_file_to_cloud(
    base_dir: str,
    blob_service_client: BlobServiceClient,
    file_path: str,
    blob_container_name: str,
    upload_file_timeout: int,
    serial_number: str,
):
    file_path_wihout_base_dir = file_path.lstrip(base_dir).replace("completed_", "")
    blob_path = os.path.join(
        "supply-chain-file-watcher",
        serial_number,
        file_path_wihout_base_dir,
    )
    blob_client = blob_service_client.get_blob_client(
        container=blob_container_name,
        blob=blob_path,
    )
    start_time = time()

    print(
        f"Uploading {file_path} to container {blob_container_name}/{blob_path}"
    )

    with open(file_path, "rb") as stream:
        blob_client.upload_blob(
            stream,
            timeout=upload_file_timeout,
            overwrite=True,
        )
        print("Done uploading")
    end_time = time()
    duration = end_time - start_time

    file_size_bytes: int = os.path.getsize(file_path)
    bytes_per_second_upload: float = file_size_bytes / duration
    bytes_per_second_upload_gauge.set(bytes_per_second_upload)

@zip_file_histogram.time()
def zip_file(file_path: str) -> str:
    """
    Keep the exact same file name, just add another extension
    """
    zip_file_path: str = file_path + ".gz"

    print(f"Compressing {file_path} into {zip_file_path}")
    timestamp=path.getmtime(file_path)
    with open(file_path, "rb") as read_stream:
        with gzip.open(zip_file_path, "wb") as write_stream:
            shutil.copyfileobj(read_stream, write_stream)
    os.utime(zip_file_path, (timestamp,timestamp) )

    return zip_file_path

def get_file_extension(file_path: str):
    return file_path.split(".")[-1]
