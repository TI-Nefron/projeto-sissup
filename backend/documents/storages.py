from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings

class DocumentStorage(S3Boto3Storage):
    """
    Storage customizado para todos os documentos do projeto.
    A organização em pastas é feita pela função `document_upload_to` no models.py.
    """
    bucket_name = settings.MINIO_BUCKET_NAME
    file_overwrite = False
