from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings

class PatientDocumentStorage(S3Boto3Storage):
    bucket_name = settings.MINIO_BUCKET_PATIENT_DOCS
    file_overwrite = False

class GuideDocumentStorage(S3Boto3Storage):
    bucket_name = settings.MINIO_BUCKET_GUIDE_DOCS
    file_overwrite = False