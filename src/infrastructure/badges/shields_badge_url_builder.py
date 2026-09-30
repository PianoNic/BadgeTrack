import urllib.parse

from src.domain.models.badge_request import BadgeRequest


class ShieldsBadgeUrlBuilder:
    BASE_URL = "https://img.shields.io/badge/"

    def build(self, request: BadgeRequest, count: int) -> str:
        url = (
            f"{self.BASE_URL}{urllib.parse.quote(request.label)}-{count}-{request.color}.svg"
            f"?style={request.style}"
        )
        if request.logo:
            url += f"&logo={urllib.parse.quote(request.logo)}"
        return url
