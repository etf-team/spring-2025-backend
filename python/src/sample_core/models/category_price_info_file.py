from datetime import date

import boto3
from sqlalchemy import Column
from fastapi_storages.integrations.sqlalchemy import FileType
from fastapi_storages.filesystem import FileSystemStorage
from sqlalchemy.orm import Mapped

from .base import Base, IntegerPk


class TimeWebS3Storage(FileSystemStorage):
    AWS_S3_ENDPOINT_URL = "s3.twcstorage.ru"
    AWS_S3_BUCKET_NAME = "746f2a22-9b28f20b-555d-4f24-985f-5b490477b884"

    def __init__(self) -> None:
        self._http_scheme = "https"
        self._url = f"https://s3.timeweb.com"
        self._s3 = boto3.resource(
            's3',
            endpoint_url='https://s3.timeweb.com',
            region_name='ru-1',
            aws_access_key_id=self.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY,
        )
        self._bucket = self._s3.Bucket(name=self.AWS_S3_BUCKET_NAME)


class CategoryPriceInfoFile(Base):
    __tablename__ = "category_price_info_file"

    id: Mapped[IntegerPk]
    file = Column(FileType(
        storage=FileSystemStorage(
            path="/var/uploaded-files",
        )),
    )
    comes_into_force_from: Mapped[date]
    comment: Mapped[str | None]
