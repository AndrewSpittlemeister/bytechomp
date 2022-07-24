from math import isclose
from random import randint, uniform

import pytest

from bytechomp import dataclass, Reader, serialize, Annotated
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


@dataclass
class NestedMessage:
    identity: int


@dataclass
class ComplexMessage:
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
    repeated: Annotated[list[int], 4]
    binary: Annotated[bytes, 4]
    nested: NestedMessage


@dataclass
class ByteDataMessage:
    data: Annotated[bytes, 10]

def test_read_write_loop() -> None:
    original = ComplexMessage(
        randint(0, 2**8 - 1),
        randint(0, 2**16 - 1),
        randint(0, 2**32 - 1),
        randint(0, 2**64 - 1),
        randint(2**8 // -2, 2**8 // 2 - 1),
        randint(2**16 // -2, 2**16 // 2 - 1),
        randint(2**32 // -2, 2**32 // 2 - 1),
        randint(2**64 // -2, 2**64 // 2 - 1),
        uniform(-10.0, 10.0),
        uniform(-10.0, 10.0),
        uniform(-10.0, 10.0),
        1,
        uniform(-10.0, 10.0),
        [randint(0, 2**64 - 1), randint(0, 2**64 - 1), randint(0, 2**64 - 1), randint(0, 2**64 - 1)],
        b"1111",
        NestedMessage(1)
    )

    data = serialize(original)

    reader = Reader[ComplexMessage]().allocate()
    for i in range(len(data)):
        assert not reader.is_complete()
        reader.feed(data[i:i+1])

    assert reader.is_complete()
    reconstructed = reader.build()
    assert reconstructed is not None

    assert original.uint8 == reconstructed.uint8
    assert original.uint16 == reconstructed.uint16
    assert original.uint32 == reconstructed.uint32
    assert original.uint64 == reconstructed.uint64
    assert original.int8 == reconstructed.int8
    assert original.int16 == reconstructed.int16
    assert original.int32 == reconstructed.int32
    assert original.int64 == reconstructed.int64
    assert isclose(original.float16, reconstructed.float16, abs_tol=0.01)
    assert isclose(original.float32, reconstructed.float32, abs_tol=0.000001)
    assert isclose(original.float64, reconstructed.float64, abs_tol=0.00000000000001)
    assert original.int_native == reconstructed.int_native
    assert isclose(original.float_native, reconstructed.float_native)
    assert original.binary == reconstructed.binary
    assert original.repeated == reconstructed.repeated
    assert original.nested == reconstructed.nested


def test_byte_only_message() -> None:
    original = ByteDataMessage(
        data=b"0123456789"
    )

    data = serialize(original)

    reader = Reader[ByteDataMessage]().allocate()
    for i in range(len(data)):
        assert not reader.is_complete()
        reader.feed(data[i:i+1])

    assert reader.is_complete()
    reconstructed = reader.build()
    assert reconstructed is not None

    print(reconstructed)

    assert reconstructed.data == original.data