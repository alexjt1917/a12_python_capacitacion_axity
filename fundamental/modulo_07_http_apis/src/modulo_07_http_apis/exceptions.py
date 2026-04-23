class DownloadError(Exception):
    """Error general durante la descarga."""


class RetryableDownloadError(DownloadError):
    """Error transitorio que permite reintentos."""
