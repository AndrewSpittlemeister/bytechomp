"""
bytechomp.basic_parsing_element
"""

from __future__ import annotations
from dataclasses import dataclass

from bytechomp.datatypes.lookups import ELEMENTARY_TYPE


@dataclass
class BasicParsingElement:
    """Describes a node in the type tree."""

    parsing_type: ELEMENTARY_TYPE | bytes  # type: ignore
    python_type: type | None
    parser_tag: str
    length: int
    default_value: int | float | bytes | None = None
    raw_data: bytes = b""
    parsed_value: int | float | bytes | None = None
