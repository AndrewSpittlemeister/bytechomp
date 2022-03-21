import struct

from bytechomp import dataclass, ByteOrder, serialize
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


def test_byte_order_native_native() -> None:
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

    # construct dataclass with the same data
    obj = BasicMessage(*values)

    assert serialize(obj, ByteOrder.NATIVE) == data


def test_byte_order_big_big() -> None:
    # build struct pattern
    pattern = ByteOrder.BIG.to_pattern()
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
    assert pattern == ">BHIQbhiqefdQd"

    # define values and build binary data
    values = (1, 2, 3, 4, 5, 6, 7, 8, 9.0, 10.0, 11.0, 12, 13.0)
    data: bytes = struct.pack(pattern, *values)

    # construct dataclass with the same data
    obj = BasicMessage(*values)

    assert serialize(obj, ByteOrder.BIG) == data


def test_byte_order_little_little() -> None:
    # build struct pattern
    pattern = ByteOrder.LITTLE.to_pattern()
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
    assert pattern == "<BHIQbhiqefdQd"

    # define values and build binary data
    values = (1, 2, 3, 4, 5, 6, 7, 8, 9.0, 10.0, 11.0, 12, 13.0)
    data: bytes = struct.pack(pattern, *values)

    # construct dataclass with the same data
    obj = BasicMessage(*values)

    assert serialize(obj, ByteOrder.LITTLE) == data


def test_byte_order_big_little() -> None:
    # build struct pattern
    pattern = ByteOrder.LITTLE.to_pattern()
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
    assert pattern == "<BHIQbhiqefdQd"

    # define values and build binary data
    values = (1, 2, 3, 4, 5, 6, 7, 8, 9.0, 10.0, 11.0, 12, 13.0)
    data: bytes = struct.pack(pattern, *values)
    

    # construct dataclass with the same data
    obj = BasicMessage(*values)

    assert serialize(obj, ByteOrder.BIG) != data


def test_byte_order_little_big() -> None:
    # build struct pattern
    pattern = ByteOrder.BIG.to_pattern()
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
    assert pattern == ">BHIQbhiqefdQd"

    # define values and build binary data
    values = (1, 2, 3, 4, 5, 6, 7, 8, 9.0, 10.0, 11.0, 12, 13.0)
    data: bytes = struct.pack(pattern, *values)

    # construct dataclass with the same data
    obj = BasicMessage(*values)

    assert serialize(obj, ByteOrder.LITTLE) != data
