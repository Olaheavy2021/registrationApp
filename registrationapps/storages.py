from storages.backends.azure_storage import AzureStorage

from .settings import AZURE_SA_KEY, AZURE_SA_NAME


class AzureMediaStorage(AzureStorage):
    """
    Custom storage backend for Azure Blob Storage tailored for media files.

    This class is intended to handle the storage of uploaded media files such as
    profile pictures on Azure Blob Storage.

    Attributes:
    - account_name: The name of the Azure Blob Storage account.
    - account_key: The authentication key for the Azure Blob Storage account.
    - azure_container: The container to store files.
    - expiration_secs: Duration (in seconds) after which a signed URL will expire. None indicates no expiration.
    """

    account_name = AZURE_SA_NAME
    account_key = AZURE_SA_KEY
    azure_container = "media"
    expiration_secs = None


class AzureStaticStorage(AzureStorage):
    """
    Custom storage backend for Azure Blob Storage to handle the storage of application static files

    Attributes:
    - account_name: The name of the Azure Blob Storage account.
    - account_key: The authentication key for the Azure Blob Storage account.
    - azure_container: The container to store files.
    - expiration_secs: Duration (in seconds) after which a signed URL will expire. None indicates no expiration.
    """

    account_name = AZURE_SA_NAME
    account_key = AZURE_SA_KEY
    azure_container = "static"
    expiration_secs = None
