from __future__ import annotations
from typing import Generic, TypeVar, Any
from dataclasses import is_dataclass
from collections import OrderedDict
from struct import Struct
from enum import Enum
import inspect

from bytechomp.data_descriptor import build_data_description, build_data_pattern, BasicParsingElement

T = TypeVar("T")


class ByteOrder(Enum):
    NATIVE = 1
    BIG = 2
    LITTLE = 3

    def to_pattern(self) -> str:
        """Returns the corresponding struct pattern."""

        match self:
            case ByteOrder.NATIVE:
                return "@"
            case ByteOrder.BIG:
                return ">"
            case ByteOrder.LITTLE:
                return "<"


class Reader(Generic[T]):
    def __init__(self, byte_order: ByteOrder = ByteOrder.NATIVE) -> None:
        self.__datatype: type | None = None
        self.__byte_order = byte_order
        self.__data: bytes = b""
        self.__data_description: OrderedDict = OrderedDict()
        self.__data_pattern: str = ""
        self.__struct = Struct(self.__data_pattern)

    def allocate(self) -> Reader:
        self.__datatype = self.__orig_class__.__args__[0]  # type: ignore

        if (
            not inspect.isclass(self.__datatype)
            or not is_dataclass(self.__datatype)
            or self.__datatype is None
        ):
            raise Exception("datatype must be a dataclass declaration")

        # print(self.__datatype)

        # verify that the datatype contains only known types
        self.__data_description = build_data_description(self.__datatype)
        # print(self.__data_description)

        # build struct parsing pattern from the description
        self.__data_pattern = self.__byte_order.to_pattern() + build_data_pattern(self.__data_description)
        # print(self.__data_pattern)

        # create struct from this pattern
        self.__struct = Struct(self.__data_pattern)
        # print(self.__struct.size)

        return self

    def __build_structure(
        self,
        args: list[int, float, bytes],
        datatype: Any,
        description: OrderedDict[str, BasicParsingElement | list[BasicParsingElement | OrderedDict] | OrderedDict]
    ) -> Any:
        pass


    def feed(self, data: bytes) -> None:
        self.__data += data

    def __lshift__(self, data: bytes) -> Reader:
        self.feed(data)
        return self

    def is_complete(self) -> bool:
        return len(self.__data) >= self.__struct.size

    def build(self) -> T | None:
        if not self.is_complete():
            return None
        else:
            pass
