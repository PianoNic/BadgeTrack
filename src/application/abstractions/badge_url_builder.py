from typing import Protocol, runtime_checkable

from src.domain.models.badge_request import BadgeRequest


@runtime_checkable
class IBadgeUrlBuilder(Protocol):
    def build(self, request: BadgeRequest, count: int) -> str: ...
