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
    string: Annotated[str, 4]
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
        "asdf",
        b"asdf",
        [1, 2, 3, 4],
        NestedMessage(1)
    )

    serialize(obj)