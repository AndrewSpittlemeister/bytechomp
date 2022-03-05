"""
bytechomp
"""

# re-exports
from dataclasses import dataclass
from typing import Annotated

# module exports
from bytechomp.reader import Reader
from bytechomp.byte_order import ByteOrder
from bytechomp.serialization import serialize

__version__ = "0.2.0"
