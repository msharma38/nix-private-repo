import glob
import re
from collections import Counter
from os import remove, path
from time import sleep

from azure.storage.blob import BlobServiceClient
from prometheus_client import start_http_server, Gauge

import config
from utils import delete_file, upload_file_to_cloud, zip_file, get_file_extension


blob_service_client = BlobServiceClient.from_connection_string(
    config.blob_storage_connection_str
)

start_http_server(config.prometheus_http_server_port)
files_queued_for_upload_gauge = Gauge(
    "files_queued_for_upload", "Number of files that yet to uploaded", ["ext"]
)

while True:

    glob_path = f"{config.read_dir}/**/completed_*"
    found_files = glob.glob(glob_path, recursive=True)
    found_files.sort(key=path.getmtime)
    ext_counter = Counter()

    # Gzip the relevant .npy files
    for file_path in found_files:
        ext = get_file_extension(file_path)
        ext_counter[ext] += 1
        files_queued_for_upload_gauge.labels(ext=ext).set(ext_counter[ext])
        if ext == "npy":
            zipped_file_path = zip_file(file_path)
            print(f"Compressed, deleting {file_path} now")
            remove(file_path)
            file_path = zipped_file_path
            new_ext = get_file_extension(file_path)
            if new_ext != ext:
                ext_counter[new_ext] += 1
            files_queued_for_upload_gauge.labels(ext=ext).set(ext_counter[ext])

    files_queued_for_upload_gauge.labels(ext='npy').set(0)

    # Upload files to cloud
    for file_path in found_files:
        try:
            ext = get_file_extension(file_path)
            if ext == "npy":
                file_path = file_path + ".gz"
                ext = get_file_extension(file_path)
            upload_file_to_cloud(
                config.read_dir,
                blob_service_client,
                file_path,
                config.blob_container_name,
                config.upload_timeout_seconds,
                config.serial_number,
            )
            delete_file(file_path)
            ext_counter[ext] -= 1
            print(f"Current count of files for {ext} - {ext_counter[ext]}")
            files_queued_for_upload_gauge.labels(ext=ext).set(ext_counter[ext])
        except Exception as e:
            print(f"Error for file {file_path}: {e}")

    sleep(config.polling_frequency_seconds)
