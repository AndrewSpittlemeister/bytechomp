"""
bytechomp.byte_order
"""

from enum import Enum


class ByteOrder(Enum):
    """Strict enumerations for byte ordering options."""

    NATIVE = 1
    BIG = 2
    LITTLE = 3

    def to_pattern(self) -> str:
        """Returns the corresponding struct pattern."""

        if self == ByteOrder.NATIVE:
            return "@"
        if self == ByteOrder.BIG:
            return ">"
        if self == ByteOrder.LITTLE:
            return "<"
        raise Exception("invalid enumeration value")
