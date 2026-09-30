from dataclasses import dataclass

from src.domain.enums.badge_style import BadgeStyle
from src.domain.exceptions import InvalidBadgeError

_LENGTH_LIMITS = {
    "tag": (1, 200),
    "label": (1, 20),
    "color": (3, 20),
    "logo": (0, 20),
}


@dataclass(frozen=True, slots=True)
class BadgeRequest:
    tag: str
    label: str
    color: str
    style: BadgeStyle
    logo: str

    @classmethod
    def parse(cls, tag: str, label: str, color: str, style: str, logo: str) -> BadgeRequest:
        values = {
            "tag": tag.strip(),
            "label": label.strip(),
            "color": color.strip().lstrip("#"),
            "logo": logo.strip(),
        }
        for field, (minimum, maximum) in _LENGTH_LIMITS.items():
            if not minimum <= len(values[field]) <= maximum:
                raise InvalidBadgeError(f"{field} must be {minimum}-{maximum} characters")
        return cls(style=BadgeStyle.parse(style), **values)
