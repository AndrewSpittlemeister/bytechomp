import struct

import pytest

from bytechomp import Reader, dataclass, Annotated, ByteOrder
from bytechomp.datatypes import (
    U8,
    U16,
    U32,
    U64,
    I8,
    I16,
    I32,
    I64,
    F16,
    F32,
    F64,
)
from bytechomp.datatypes.lookups import TYPE_TO_TAG


@dataclass
class BasicMessage:
    uint8: U8
    uint16: U16
    uint32: U32
    uint64: U64
    int8: I8
    int16: I16
    int32: I32
    int64: I64
    float16: F16
    float32: F32
    float64: F64
    int_native: int
    float_native: float


def test_read_basic_datatypes() -> None:
    reader = Reader[BasicMessage]().allocate()

    # build struct pattern
    pattern = ByteOrder.NATIVE.to_pattern()
    pattern += TYPE_TO_TAG[U8]
    pattern += TYPE_TO_TAG[U16]
    pattern += TYPE_TO_TAG[U32]
    pattern += TYPE_TO_TAG[U64]
    pattern += TYPE_TO_TAG[I8]
    pattern += TYPE_TO_TAG[I16]
    pattern += TYPE_TO_TAG[I32]
    pattern += TYPE_TO_TAG[I64]
    pattern += TYPE_TO_TAG[F16]
    pattern += TYPE_TO_TAG[F32]
    pattern += TYPE_TO_TAG[F64]
    pattern += TYPE_TO_TAG[int]
    pattern += TYPE_TO_TAG[float]
    assert pattern == "@BHIQbhiqefdQd"

    # define values and build binary data
    values = (1, 2, 3, 4, 5, 6, 7, 8, 9.0, 10.0, 11.0, 12, 13.0)
    data: bytes = struct.pack(pattern, *values)

    # add to the reader in a stream-like way
    for i in range(len(data)):
        # should not be complete yet
        assert not reader.is_complete()
        # add the data
        reader.feed(data[i:i+1])

    # should be complete now
    assert reader.is_complete()

    # build the dataclass
    msg = reader.build()
    assert isinstance(msg, BasicMessage)

    # make sure the values are correct
    assert isinstance(msg.uint8, int)
    assert msg.uint8 == 1
    assert isinstance(msg.uint16, int)
    assert msg.uint16 == 2
    assert isinstance(msg.uint32, int)
    assert msg.uint32 == 3
    assert isinstance(msg.uint64, int)
    assert msg.uint64 == 4
    assert isinstance(msg.int8, int)
    assert msg.int8 == 5
    assert isinstance(msg.int16, int)
    assert msg.int16 == 6
    assert isinstance(msg.int32, int)
    assert msg.int32 == 7
    assert isinstance(msg.int64, int)
    assert msg.int64 == 8
    assert isinstance(msg.float16, float)
    assert msg.float16 == 9.0
    assert isinstance(msg.float32, float)
    assert msg.float32 == 10.0
    assert isinstance(msg.float64, float)
    assert msg.float64 == 11.0
    assert isinstance(msg.int_native, int)
    assert msg.int_native == 12
    assert isinstance(msg.float_native, float)
    assert msg.float_native == 13.0


# @dataclass
# class StringMessage:
#     data: Annotated[str, 8]


# def test_read_string_data() -> None:
#     reader = Reader[StringMessage]().allocate()

#     # build struct pattern
#     pattern = f"{ByteOrder.NATIVE.to_pattern()}8s"
#     assert pattern == "@8s"

#     # build message
#     data = struct.pack(pattern, "12345678".encode("utf-8"))

#     # add to the reader in a stream-like way
#     for i in range(len(data)):
#         # should not be complete yet
#         assert not reader.is_complete()
#         # add the data
#         reader.feed(data[i:i+1])

#     # should be complete now
#     assert reader.is_complete()

#     # build the dataclass
#     msg = reader.build()
#     assert isinstance(msg, StringMessage)
#     assert isinstance(msg.data, str)
#     assert msg.data == "12345678"


@dataclass
class BytesMessage:
    data: Annotated[bytes, 8]


def test_read_bytes_data() -> None:
    reader = Reader[BytesMessage]().allocate()

    # build struct pattern
    pattern = f"{ByteOrder.NATIVE.to_pattern()}8s"
    assert pattern == "@8s"

    # build message
    data = struct.pack(pattern, "12345678".encode("utf-8"))

    # add to the reader in a stream-like way
    for i in range(len(data)):
        # should not be complete yet
        assert not reader.is_complete()
        # add the data
        reader.feed(data[i:i+1])

    # should be complete now
    assert reader.is_complete()

    # build the dataclass
    msg = reader.build()
    assert isinstance(msg, BytesMessage)
    assert isinstance(msg.data, bytes)
    assert msg.data == b"12345678"


@dataclass
class IntListMessage:
    data: Annotated[list[U32], 8]


def test_read_int_list_data() -> None:
    reader = Reader[IntListMessage]().allocate()

    # build struct pattern
    pattern = f"{ByteOrder.NATIVE.to_pattern()}{TYPE_TO_TAG[U32] * 8}"
    assert pattern == "@IIIIIIII"

    # build message
    data = struct.pack(pattern, *[1, 2, 3, 4, 5, 6, 7, 8])

    # add to the reader in a stream-like way
    for i in range(len(data)):
        # should not be complete yet
        assert not reader.is_complete()
        # add the data
        reader.feed(data[i:i+1])

    # should be complete now
    assert reader.is_complete()

    # build the dataclass
    msg = reader.build()
    assert isinstance(msg, IntListMessage)
    assert isinstance(msg.data, list)
    assert msg.data == [1, 2, 3, 4, 5, 6, 7, 8]


@dataclass
class FloatListMessage:
    data: Annotated[list[F32], 8]


def test_read_float_list_data() -> None:
    reader = Reader[FloatListMessage]().allocate()

    # build struct pattern
    pattern = f"{ByteOrder.NATIVE.to_pattern()}{TYPE_TO_TAG[F32] * 8}"
    assert pattern == "@ffffffff"

    # build message
    data = struct.pack(pattern, *[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0])

    # add to the reader in a stream-like way
    for i in range(len(data)):
        # should not be complete yet
        assert not reader.is_complete()
        # add the data
        reader.feed(data[i:i+1])

    # should be complete now
    assert reader.is_complete()

    # build the dataclass
    msg = reader.build()
    assert isinstance(msg, FloatListMessage)
    assert isinstance(msg.data, list)
    assert msg.data == [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]


@dataclass
class InnerMessage:
    data_alpha: int
    data_beta: int


@dataclass
class OuterMessage:
    data_inner_alpha: InnerMessage
    data_inner_beta: InnerMessage


def test_read_nested_data() -> None:
    reader = Reader[OuterMessage]().allocate()

    # build struct pattern
    pattern = f"{ByteOrder.NATIVE.to_pattern()}{TYPE_TO_TAG[int] * 4}"
    assert pattern == "@QQQQ"

    # build message
    data = struct.pack(pattern, *[10, 20, 30, 40])

    # add to the reader in a stream-like way
    for i in range(len(data)):
        # should not be complete yet
        assert not reader.is_complete()
        # add the data
        reader.feed(data[i:i+1])

    # should be complete now
    assert reader.is_complete()

    # build the dataclass
    msg = reader.build()
    assert isinstance(msg, OuterMessage)
    assert isinstance(msg.data_inner_alpha, InnerMessage)
    assert isinstance(msg.data_inner_alpha.data_alpha, int)
    assert msg.data_inner_alpha.data_alpha == 10
    assert isinstance(msg.data_inner_alpha.data_beta, int)
    assert msg.data_inner_alpha.data_beta == 20
    assert isinstance(msg.data_inner_beta, InnerMessage)
    assert isinstance(msg.data_inner_beta.data_alpha, int)
    assert msg.data_inner_beta.data_alpha == 30
    assert isinstance(msg.data_inner_beta.data_beta, int)
    assert msg.data_inner_beta.data_beta == 40


@dataclass
class StructuredListMessage:
    data: Annotated[list[InnerMessage], 2]

def test_read_structured_list_data() -> None:
    reader = Reader[StructuredListMessage]().allocate()

    # build struct pattern
    pattern = f"{ByteOrder.NATIVE.to_pattern()}{TYPE_TO_TAG[int] * 4}"
    assert pattern == "@QQQQ"

    # build message
    data = struct.pack(pattern, *[10, 20, 30, 40])

    # add to the reader in a stream-like way
    for i in range(len(data)):
        # should not be complete yet
        assert not reader.is_complete()
        # add the data
        reader.feed(data[i:i+1])

    # should be complete now
    assert reader.is_complete()

    # build the dataclass
    msg = reader.build()
    assert isinstance(msg, StructuredListMessage)
    assert isinstance(msg.data, list)
    assert len(msg.data) == 2
    assert isinstance(msg.data[0], InnerMessage)
    assert isinstance(msg.data[0].data_alpha, int)
    assert msg.data[0].data_alpha == 10
    assert isinstance(msg.data[0].data_beta, int)
    assert msg.data[0].data_beta == 20
    assert isinstance(msg.data[1], InnerMessage)
    assert isinstance(msg.data[1].data_alpha, int)
    assert msg.data[1].data_alpha == 30
    assert isinstance(msg.data[1].data_beta, int)
    assert msg.data[1].data_beta == 40


@dataclass
class NestedStructuredListMessage:
    data: Annotated[list[OuterMessage], 2]


def test_read_nested_structured_list_data() -> None:
    reader = Reader[NestedStructuredListMessage]().allocate()

    # build struct pattern
    pattern = f"{ByteOrder.NATIVE.to_pattern()}{TYPE_TO_TAG[int] * 8}"
    assert pattern == "@QQQQQQQQ"

    # build message
    data = struct.pack(pattern, *[10, 20, 30, 40, 50, 60, 70, 80])

    # add to the reader in a stream-like way
    for i in range(len(data)):
        # should not be complete yet
        assert not reader.is_complete()
        # add the data
        reader.feed(data[i:i+1])

    # should be complete now
    assert reader.is_complete()

    # build the dataclass
    msg = reader.build()
    assert isinstance(msg, NestedStructuredListMessage)
    assert isinstance(msg.data, list)
    assert len(msg.data) == 2
    assert isinstance(msg.data[0], OuterMessage)
    assert isinstance(msg.data[0].data_inner_alpha, InnerMessage)
    assert isinstance(msg.data[0].data_inner_alpha.data_alpha, int)
    assert msg.data[0].data_inner_alpha.data_alpha == 10
    assert isinstance(msg.data[0].data_inner_alpha.data_beta, int)
    assert msg.data[0].data_inner_alpha.data_beta == 20
    assert isinstance(msg.data[0].data_inner_beta, InnerMessage)
    assert isinstance(msg.data[0].data_inner_beta.data_alpha, int)
    assert msg.data[0].data_inner_beta.data_alpha == 30
    assert isinstance(msg.data[0].data_inner_beta.data_beta, int)
    assert msg.data[0].data_inner_beta.data_beta == 40
    assert isinstance(msg.data[1], OuterMessage)
    assert isinstance(msg.data[1].data_inner_alpha, InnerMessage)
    assert isinstance(msg.data[1].data_inner_alpha.data_alpha, int)
    assert msg.data[1].data_inner_alpha.data_alpha == 50
    assert isinstance(msg.data[1].data_inner_alpha.data_beta, int)
    assert msg.data[1].data_inner_alpha.data_beta == 60
    assert isinstance(msg.data[1].data_inner_beta, InnerMessage)
    assert isinstance(msg.data[1].data_inner_beta.data_alpha, int)
    assert msg.data[1].data_inner_beta.data_alpha == 70
    assert isinstance(msg.data[1].data_inner_beta.data_beta, int)
    assert msg.data[1].data_inner_beta.data_beta == 80


@dataclass
class NestedListMessage:
    data: Annotated[list[Annotated[list[int], 5]], 5]


def test_read_nested_list_data() -> None:
    with pytest.raises(Exception) as e:
        reader = Reader[NestedListMessage]().allocate()
    assert str(e.value).startswith("unsupported list type")
