import functools
import os

import boto3
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import UploadedFile


class FileStorageFactory:
    @staticmethod
    @functools.lru_cache(maxsize=1)
    def instance() -> boto3.client:
        return boto3.client(
            "s3",
            endpoint_url=settings.FILE_STORAGE_ENDPOINT_URL,
            aws_access_key_id=settings.FILE_STORAGE_ACCESS_KEY_ID,
            aws_secret_access_key=settings.FILE_STORAGE_SECRET_ACCESS_KEY,
            region_name="us-east-1",
        )


class NewsImage:
    PATH = "uploads/news/"

    def __init__(self):
        self.file_storage_client = FileStorageFactory.instance()
        self.bucket_name = settings.FILE_STORAGE_BUCKET_NAME

    def upload(self, image_file: UploadedFile) -> str:
        file_path = f"{self.PATH}{image_file.name}"

        temp_file_path = default_storage.save(file_path, image_file)
        self.file_storage_client.upload_file(temp_file_path, self.bucket_name, file_path)

        os.remove(temp_file_path)

        return file_path
