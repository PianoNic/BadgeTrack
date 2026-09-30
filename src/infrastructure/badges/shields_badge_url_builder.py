from urllib.parse import quote, urlencode

from src.domain.models.badge_request import BadgeRequest


class ShieldsBadgeUrlBuilder:
    BASE_URL = "https://img.shields.io/badge/"

    def build(self, request: BadgeRequest, count: int) -> str:
        path = f"{self._segment(request.label)}-{count}-{self._segment(request.color)}.svg"
        query = {"style": request.style.value}
        if request.logo:
            query["logo"] = request.logo
        return f"{self.BASE_URL}{path}?{urlencode(query)}"

    @staticmethod
    def _segment(text: str) -> str:
        # shields.io splits the path on "-" and reads "_" as a space, so both are doubled to stay literal
        return quote(text.replace("-", "--").replace("_", "__"))
