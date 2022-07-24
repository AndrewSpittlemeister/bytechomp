from random import choice

import pytest

from bytechomp import dataclass, serialize, Annotated
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
    # string: Annotated[str, 4]
    binary: Annotated[bytes, 4]
    repeated: Annotated[list[int], 4]
    nested: NestedMessage



def test_clean_validation() -> None:
    obj = ComplexMessage(
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1.1,
        1.1,
        1.1,
        1,
        1.1,
        # "asdf",
        b"asdf",
        [1, 2, 3, 4],
        NestedMessage(1)
    )

    serialize(obj)


def test_uint8_validation() -> None:
    val = choice([1.1, "asdf", b"asdf", [1, 2, 3], NestedMessage(1)])

    obj = ComplexMessage(
        val,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1.1,
        1.1,
        1.1,
        1,
        1.1,
        # "asdf",
        b"asdf",
        [1, 2, 3, 4],
        NestedMessage(1)
    )

    with pytest.raises(TypeError) as e:
        serialize(obj)


def test_uint16_validation() -> None:
    val = choice([1.1, "asdf", b"asdf", [1, 2, 3], NestedMessage(1)])

    obj = ComplexMessage(
        1,
        val,
        1,
        1,
        1,
        1,
        1,
        1,
        1.1,
        1.1,
        1.1,
        1,
        1.1,
        # "asdf",
        b"asdf",
        [1, 2, 3, 4],
        NestedMessage(1)
    )

    with pytest.raises(TypeError) as e:
        serialize(obj)


def test_uint32_validation() -> None:
    val = choice([1.1, "asdf", b"asdf", [1, 2, 3], NestedMessage(1)])

    obj = ComplexMessage(
        1,
        1,
        val,
        1,
        1,
        1,
        1,
        1,
        1.1,
        1.1,
        1.1,
        1,
        1.1,
        # "asdf",
        b"asdf",
        [1, 2, 3, 4],
        NestedMessage(1)
    )

    with pytest.raises(TypeError) as e:
        serialize(obj)


def test_uint64_validation() -> None:
    val = choice([1.1, "asdf", b"asdf", [1, 2, 3], NestedMessage(1)])

    obj = ComplexMessage(
        1,
        1,
        1,
        val,
        1,
        1,
        1,
        1,
        1.1,
        1.1,
        1.1,
        1,
        1.1,
        # "asdf",
        b"asdf",
        [1, 2, 3, 4],
        NestedMessage(1)
    )

    with pytest.raises(TypeError) as e:
        serialize(obj)


def test_int8_validation() -> None:
    val = choice([1.1, "asdf", b"asdf", [1, 2, 3], NestedMessage(1)])

    obj = ComplexMessage(
        1,
        1,
        1,
        1,
        val,
        1,
        1,
        1,
        1.1,
        1.1,
        1.1,
        1,
        1.1,
        # "asdf",
        b"asdf",
        [1, 2, 3, 4],
        NestedMessage(1)
    )

    with pytest.raises(TypeError) as e:
        serialize(obj)


def test_int16_validation() -> None:
    val = choice([1.1, "asdf", b"asdf", [1, 2, 3], NestedMessage(1)])

    obj = ComplexMessage(
        1,
        1,
        1,
        1,
        1,
        val,
        1,
        1,
        1.1,
        1.1,
        1.1,
        1,
        1.1,
        # "asdf",
        b"asdf",
        [1, 2, 3, 4],
        NestedMessage(1)
    )

    with pytest.raises(TypeError) as e:
        serialize(obj)


def test_int32_validation() -> None:
    val = choice([1.1, "asdf", b"asdf", [1, 2, 3], NestedMessage(1)])

    obj = ComplexMessage(
        1,
        1,
        1,
        1,
        1,
        1,
        val,
        1,
        1.1,
        1.1,
        1.1,
        1,
        1.1,
        # "asdf",
        b"asdf",
        [1, 2, 3, 4],
        NestedMessage(1)
    )

    with pytest.raises(TypeError) as e:
        serialize(obj)


def test_int64_validation() -> None:
    val = choice([1.1, "asdf", b"asdf", [1, 2, 3], NestedMessage(1)])

    obj = ComplexMessage(
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        val,
        1.1,
        1.1,
        1.1,
        1,
        1.1,
        # "asdf",
        b"asdf",
        [1, 2, 3, 4],
        NestedMessage(1)
    )

    with pytest.raises(TypeError) as e:
        serialize(obj)


def test_float16_validation() -> None:
    val = choice([1, "asdf", b"asdf", [1, 2, 3], NestedMessage(1)])

    obj = ComplexMessage(
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        val,
        1.1,
        1.1,
        1,
        1.1,
        # "asdf",
        b"asdf",
        [1, 2, 3, 4],
        NestedMessage(1)
    )

    with pytest.raises(TypeError) as e:
        serialize(obj)


def test_float32_validation() -> None:
    val = choice([1, "asdf", b"asdf", [1, 2, 3], NestedMessage(1)])

    obj = ComplexMessage(
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1.1,
        val,
        1.1,
        1,
        1.1,
        # "asdf",
        b"asdf",
        [1, 2, 3, 4],
        NestedMessage(1)
    )

    with pytest.raises(TypeError) as e:
        serialize(obj)


def test_float64_validation() -> None:
    val = choice([1, "asdf", b"asdf", [1, 2, 3], NestedMessage(1)])

    obj = ComplexMessage(
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1.1,
        1.1,
        val,
        1,
        1.1,
        # "asdf",
        b"asdf",
        [1, 2, 3, 4],
        NestedMessage(1)
    )

    with pytest.raises(TypeError) as e:
        serialize(obj)


def test_int_validation() -> None:
    val = choice([1.1, "asdf", b"asdf", [1, 2, 3], NestedMessage(1)])

    obj = ComplexMessage(
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1.1,
        1.1,
        1.1,
        val,
        1.1,
        # "asdf",
        b"asdf",
        [1, 2, 3, 4],
        NestedMessage(1)
    )

    with pytest.raises(TypeError) as e:
        serialize(obj)


def test_float_validation() -> None:
    val = choice([1, "asdf", b"asdf", [1, 2, 3], NestedMessage(1)])

    obj = ComplexMessage(
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1.1,
        1.1,
        1.1,
        1,
        val,
        # "asdf",
        b"asdf",
        [1, 2, 3, 4],
        NestedMessage(1)
    )

    with pytest.raises(TypeError) as e:
        serialize(obj)


# def test_string_validation() -> None:
#     val = choice([1, 1.1, b"asdf", [1, 2, 3], NestedMessage(1)])

#     obj = ComplexMessage(
#         1,
#         1,
#         1,
#         1,
#         1,
#         1,
#         1,
#         1,
#         1.1,
#         1.1,
#         1.1,
#         1,
#         1.1,
#         val,
#         b"asdf",
#         [1, 2, 3, 4],
#         NestedMessage(1)
#     )

#     with pytest.raises(TypeError) as e:
#         serialize(obj)


# def test_string_length_validation() -> None:
#     obj = ComplexMessage(
#         1,
#         1,
#         1,
#         1,
#         1,
#         1,
#         1,
#         1,
#         1.1,
#         1.1,
#         1.1,
#         1,
#         1.1,
#         "asd",
#         b"asdf",
#         [1, 2, 3, 4],
#         NestedMessage(1)
#     )

#     with pytest.raises(TypeError) as e:
#         serialize(obj)


def test_bytes_validation() -> None:
    val = choice([1, 1.1, "asdf", [1, 2, 3], NestedMessage(1)])

    obj = ComplexMessage(
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1.1,
        1.1,
        1.1,
        1,
        1.1,
        # "asdf",
        val,
        [1, 2, 3, 4],
        NestedMessage(1)
    )

    with pytest.raises(TypeError) as e:
        serialize(obj)


def test_bytes_length_validation() -> None:
    obj = ComplexMessage(
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1.1,
        1.1,
        1.1,
        1,
        1.1,
        # "asdf",
        b"asd",
        [1, 2, 3, 4],
        NestedMessage(1)
    )

    with pytest.raises(TypeError) as e:
        serialize(obj)


def test_list_validation() -> None:
    val = choice([1, 1.1, "asdf", b"asdf", NestedMessage(1)])

    obj = ComplexMessage(
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1.1,
        1.1,
        1.1,
        1,
        1.1,
        # "asdf",
        b"asdf",
        val,
        NestedMessage(1)
    )

    with pytest.raises(TypeError) as e:
        serialize(obj)


def test_list_length_validation() -> None:
    obj = ComplexMessage(
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1.1,
        1.1,
        1.1,
        1,
        1.1,
        # "asdf",
        b"asdf",
        [1, 2, 3, 4, 5],
        NestedMessage(1)
    )

    with pytest.raises(TypeError) as e:
        serialize(obj)


def test_list_element_validation() -> None:
    obj = ComplexMessage(
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1.1,
        1.1,
        1.1,
        1,
        1.1,
        # "asdf",
        b"asd",
        [1, 2, 3, "4"],
        NestedMessage(1)
    )

    with pytest.raises(TypeError) as e:
        serialize(obj)


def test_struct_validation() -> None:
    val = choice([1, 1.1, "asdf", b"asdf", [1, 2, 3]])

    obj = ComplexMessage(
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1.1,
        1.1,
        1.1,
        1,
        1.1,
        # "asdf",
        b"asdf",
        [1, 2, 3],
        val
    )

    with pytest.raises(TypeError) as e:
        serialize(obj)


def test_struct_element_validation() -> None:
    val = choice([1, 1.1, "asdf", b"asdf", [1, 2, 3]])

    obj = ComplexMessage(
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1.1,
        1.1,
        1.1,
        1,
        1.1,
        # "asdf",
        b"asdf",
        [1, 2, 3],
        NestedMessage(val)
    )

    with pytest.raises(TypeError) as e:
        serialize(obj)
