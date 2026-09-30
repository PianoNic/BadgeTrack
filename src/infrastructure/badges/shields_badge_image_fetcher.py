import logging
from collections import OrderedDict

import httpx

logger = logging.getLogger(__name__)

_CACHE_SIZE = 2048
_TIMEOUT_SECONDS = 3.0


class ShieldsBadgeImageFetcher:
    # the same label, count, colour and style always render the same image, so fetched SVGs are reused
    def __init__(self, cache_size: int = _CACHE_SIZE, timeout_seconds: float = _TIMEOUT_SECONDS) -> None:
        self._cache: OrderedDict[str, bytes] = OrderedDict()
        self._cache_size = cache_size
        self._client = httpx.AsyncClient(timeout=timeout_seconds)

    async def fetch(self, url: str) -> bytes | None:
        if url in self._cache:
            self._cache.move_to_end(url)
            return self._cache[url]

        try:
            response = await self._client.get(url)
            response.raise_for_status()
        except httpx.HTTPError:
            logger.warning("Fetching %s failed, falling back to a redirect", url)
            return None
        if not response.headers.get("content-type", "").startswith("image/svg+xml"):
            return None

        self._cache[url] = response.content
        if len(self._cache) > self._cache_size:
            self._cache.popitem(last=False)
        return response.content
