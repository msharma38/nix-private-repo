from os import getenv

read_dir: str = getenv("READ_DIR")

blob_storage_connection_str: str = getenv("BLOB_STORAGE_CONNECTION_STR")
blob_container_name: str = getenv("BLOB_CONTAINER_NAME")
upload_timeout_seconds: int = int(getenv("UPLOAD_TIMEOUT_SECONDS", "600"))

prometheus_http_server_port: int = int(getenv("PROMETHEUS_HTTP_SERVER_PORT", "3000"))

polling_frequency_seconds: int = int(getenv("POLLING_FREQUENCY_SECONDS", "1"))

serial_number_file_path: str = getenv(
    "SERIAL_NUMBER_FILE_PATH", "/sys/firmware/devicetree/base/serial-number"
)
serial_number_file = open(serial_number_file_path, "r")
serial_number = serial_number_file.read().rstrip('\x00')
serial_number_file.close()


if not read_dir:
    raise ValueError("READ_DIR not set!")
elif not blob_storage_connection_str:
    raise ValueError("BLOB_STORAGE_CONNECTION_STR not set!")
elif not blob_container_name:
    raise ValueError("BLOB_CONTAINER_NAME not set!")
