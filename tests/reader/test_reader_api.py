import struct

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


def test_byte_order_native_native() -> None:
    reader = Reader[BasicMessage](ByteOrder.NATIVE).allocate()

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

def test_byte_order_big_big() -> None:
    reader = Reader[BasicMessage](ByteOrder.BIG).allocate()

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


def test_byte_order_little_little() -> None:
    reader = Reader[BasicMessage](ByteOrder.LITTLE).allocate()

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


def test_byte_order_big_little() -> None:
    reader = Reader[BasicMessage](ByteOrder.BIG).allocate()

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
    assert msg.uint16 != 2
    assert isinstance(msg.uint32, int)
    assert msg.uint32 != 3
    assert isinstance(msg.uint64, int)
    assert msg.uint64 != 4
    assert isinstance(msg.int8, int)
    assert msg.int8 == 5
    assert isinstance(msg.int16, int)
    assert msg.int16 != 6
    assert isinstance(msg.int32, int)
    assert msg.int32 != 7
    assert isinstance(msg.int64, int)
    assert msg.int64 != 8
    assert isinstance(msg.float16, float)
    assert msg.float16 != 9.0
    assert isinstance(msg.float32, float)
    assert msg.float32 != 10.0
    assert isinstance(msg.float64, float)
    assert msg.float64 != 11.0
    assert isinstance(msg.int_native, int)
    assert msg.int_native != 12
    assert isinstance(msg.float_native, float)
    assert msg.float_native != 13.0


def test_byte_order_little_big() -> None:
    reader = Reader[BasicMessage](ByteOrder.LITTLE).allocate()

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
    assert msg.uint16 != 2
    assert isinstance(msg.uint32, int)
    assert msg.uint32 != 3
    assert isinstance(msg.uint64, int)
    assert msg.uint64 != 4
    assert isinstance(msg.int8, int)
    assert msg.int8 == 5
    assert isinstance(msg.int16, int)
    assert msg.int16 != 6
    assert isinstance(msg.int32, int)
    assert msg.int32 != 7
    assert isinstance(msg.int64, int)
    assert msg.int64 != 8
    assert isinstance(msg.float16, float)
    assert msg.float16 != 9.0
    assert isinstance(msg.float32, float)
    assert msg.float32 != 10.0
    assert isinstance(msg.float64, float)
    assert msg.float64 != 11.0
    assert isinstance(msg.int_native, int)
    assert msg.int_native != 12
    assert isinstance(msg.float_native, float)
    assert msg.float_native != 13.0


def test_bitshift_api() -> None:
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
        if reader << data[i:i+1]:
            # should only be complete when on the last byte
            assert i == len(data) - 1

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


def test_iterator_api() -> None:
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
    assert pattern == "@BHIQbhiqefdQdBHIQbhiqefdQd"

    # define values and build binary data
    values = (1, 2, 3, 4, 5, 6, 7, 8, 9.0, 10.0, 11.0, 12, 13.0, 1, 2, 3, 4, 5, 6, 7, 8, 9.0, 10.0, 11.0, 12, 13.0)
    data: bytes = struct.pack(pattern, *values)
    data_iterator = [data[i:i+1] for i in range(len(data))]

    i = 0
    for i, msg in enumerate(reader.iter(data_iterator)):

        # should not be complete because message was just built
        assert not reader.is_complete()

        # make sure the values are correct
        assert isinstance(msg, BasicMessage)
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

    # make sure only two messages were built
    assert i == 1
    assert not reader.is_complete()


def test_reader_clear() -> None:
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

        if i == 4:
            reader.clear()

    assert not reader.is_complete()


def test_reader_export() -> None:
    reader = Reader[BasicMessage]().allocate()

    reader.feed(b"asdf")
    assert reader.export() == b"asdf"
    assert not reader.is_complete()
    assert reader.export() == b""
