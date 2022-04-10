"""
bytechomp.reader
"""

from __future__ import annotations
from typing import Generic, TypeVar, Iterable, Iterator
from dataclasses import is_dataclass
from collections import OrderedDict
from struct import Struct
import inspect

from bytechomp.byte_order import ByteOrder
from bytechomp.data_descriptor import (
    build_data_description,
    build_data_pattern,
    build_structure,
)

T = TypeVar("T")  # pylint: disable=invalid-name


class Reader(Generic[T]):
    """A binary protocol reader.

    Args:
        Generic (T): The dataclass type that defines the binary protocol.
    """

    def __init__(self, byte_order: ByteOrder = ByteOrder.NATIVE) -> None:
        self.__datatype: type | None = None
        self.__byte_order = byte_order
        self.__data: bytes = b""
        self.__data_description: OrderedDict = OrderedDict()
        self.__data_pattern: str = ""
        self.__struct = Struct(self.__data_pattern)

    def allocate(self) -> Reader[T]:
        """Allocates the reader with a tokenized description of the protocol defined by the type T.

        Returns:
            Reader: The allocated binary protocol reader.
        """
        # pylint: disable=no-member

        self.__datatype = self.__orig_class__.__args__[0]  # type: ignore

        if (
            not inspect.isclass(self.__datatype)
            or not is_dataclass(self.__datatype)
            or self.__datatype is None
        ):
            raise Exception("generic datatype must be a dataclass")

        # verify that the datatype contains only known types
        self.__data_description = build_data_description(self.__datatype)
        # print(self.__data_description)

        # build struct parsing pattern from the description
        self.__data_pattern = self.__byte_order.to_pattern() + build_data_pattern(
            self.__data_description
        )
        # print(self.__data_pattern)

        # create struct from this pattern
        self.__struct = Struct(self.__data_pattern)
        # print(self.__struct.size)

        return self

    def feed(self, data: bytes) -> None:
        """Add binary data to the internal buffer.

        Args:
            data (bytes): Binary data.
        """

        self.__data += data

    def __lshift__(self, data: bytes) -> Reader:
        """Alternative to the feed method.

        Args:
            data (bytes): Binary data

        Returns:
            Reader: Binary protocol reader.
        """

        self.feed(data)
        return self

    def is_complete(self) -> bool:
        """Tests if the internal buffer contains enough data to construct the class T.

        Returns:
            bool: True if the internal buffer is sufficiently large.
        """

        return len(self.__data) >= self.__struct.size

    def __bool__(self) -> bool:
        """Alternative to the is_complete method.

        Returns:
            bool: True if the internal buffer is sufficiently large.
        """

        return self.is_complete()

    def __len__(self) -> int:
        """Returns the size of the internal buffer.

        Returns:
            int: Size of internal buffer.
        """

        return len(self.__data)

    def build(self) -> T | None:
        """Constructs the class T from the binary data collected in the internal buffer.

        Returns:
            Optional[T]: Instantiated class T if the internal buffer is sufficiently large,
                otherwise None.
        """
        if self.is_complete():
            struct_bytes = self.__data[: self.__struct.size]
            self.__data = self.__data[self.__struct.size :]
            # print(f"unpacked: {self.__struct.unpack(struct_bytes)}")
            return build_structure(
                list(self.__struct.unpack(struct_bytes)), self.__data_description
            )
        return None

    def iter(self, byte_iterator: Iterable[bytes]) -> Iterator[T]:
        """Allows the reader to use a stream of bytes to yield the constructed dataclasses as an
            iterator.

        Args:
            byte_iterator (Iterable[bytes]): Byte stream.

        Yields:
            Iterator[T]: Yielded dataclass iterator.
        """

        for chunk in byte_iterator:
            self.__data += chunk
            if self.is_complete():
                struct_bytes = self.__data[: self.__struct.size]
                self.__data = self.__data[self.__struct.size :]
                yield build_structure(
                    list(self.__struct.unpack(struct_bytes)), self.__data_description
                )

    def clear(self) -> None:
        """Clears the data in the internal buffer."""

        self.__data = b""

    def export(self) -> bytes:
        """Exports the data from the internal buffer.

        Returns:
            bytes: All bytes contained in the internal buffer
        """

        data = self.__data
        self.__data = b""
        return data
