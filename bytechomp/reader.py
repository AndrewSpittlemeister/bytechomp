from __future__ import annotations
from typing import Optional, Generic, TypeVar
from dataclasses import is_dataclass
from collections import OrderedDict
from enum import Enum
import inspect

from bytechomp.data_descriptor import build_data_description, BasicProtocolSchema

T = TypeVar("T")


class ByteOrder(Enum):
    BIG = 1
    LITTLE = 2


class Reader(Generic[T]):
    def __init__(self, byte_order: ByteOrder = ByteOrder.LITTLE) -> None:
        self.__datatype: Optional[type] = None
        self.__byte_order: ByteOrder = byte_order
        self.__is_complete: bool = False
        self.__data: bytes = b""
        self.__data_description: OrderedDict = OrderedDict()

    def allocate(self) -> Reader:
        self.__datatype = self.__orig_class__.__args__[0]  # type: ignore

        if (
            not inspect.isclass(self.__datatype)
            or not is_dataclass(self.__datatype)
            or self.__datatype is None
        ):
            raise Exception("datatype must be a dataclass declaration")

        print(self.__datatype)

        # verify that the datatype contains only known types
        self.__data_description = build_data_description(self.__datatype)
        print(self.__data_description)

        return self

    def feed(self, data: bytes) -> None:
        self.__data += data

    def __lshift__(self, data: bytes) -> Reader:
        self.feed(data)
        return self

    def is_complete(self) -> bool:
        return self.__is_complete

    def build(self) -> T:
        pass
