from enum import StrEnum


class BadgeStyle(StrEnum):
    FLAT = "flat"
    FLAT_SQUARE = "flat-square"
    PLASTIC = "plastic"
    FOR_THE_BADGE = "for-the-badge"
    SOCIAL = "social"

    @classmethod
    def parse(cls, value: str) -> BadgeStyle:
        # an unknown style must not break a badge that is already embedded somewhere
        try:
            return cls(value.strip().lower())
        except ValueError:
            return cls.FLAT
