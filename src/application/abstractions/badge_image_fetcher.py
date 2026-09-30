from typing import Protocol, runtime_checkable


@runtime_checkable
class IBadgeImageFetcher(Protocol):
    async def fetch(self, url: str) -> bytes | None: ...
