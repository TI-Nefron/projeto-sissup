import logging
from django.conf import settings
from minio import Minio
from minio.error import S3Error

logger = logging.getLogger(__name__)

def ensure_minio_buckets_exist():
    """
    Connects to MinIO and creates the required application buckets if they
    do not already exist. Intended to be run on application startup.
    """
    try:
        client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_USE_HTTPS
        )

        required_buckets = [
            settings.MINIO_BUCKET_PATIENT_DOCS,
            settings.MINIO_BUCKET_GUIDE_DOCS
        ]

        for bucket_name in required_buckets:
            if not client.bucket_exists(bucket_name):
                client.make_bucket(bucket_name)
                logger.info(f"MinIO bucket '{bucket_name}' created successfully.")
            else:
                logger.info(f"MinIO bucket '{bucket_name}' already exists.")

    except S3Error as exc:
        logger.error(f"Error communicating with MinIO: {exc}")
    except Exception as exc:
        logger.error(f"An unexpected error occurred during MinIO setup: {exc}")