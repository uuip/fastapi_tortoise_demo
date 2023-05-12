from urllib.parse import urlparse

from settings import settings

url = urlparse(settings.db).geturl()
