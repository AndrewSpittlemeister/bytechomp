"""
bytechomp.datatypes
"""

from typing import NewType, Final, Union


### Elementary Data Types ##########################################################################

PAD = NewType("PAD", int)
U8 = NewType("U8", int)
U16 = NewType("U16", int)
U32 = NewType("U32", int)
U64 = NewType("U64", int)
I8 = NewType("I8", int)
I16 = NewType("I16", int)
I32 = NewType("I32", int)
I64 = NewType("I64", int)
F16 = NewType("F16", float)
F32 = NewType("F32", float)
F64 = NewType("F64", float)

ELEMENTARY_TYPE = type | NewType
ELEMENTARY_TYPE_LIST: Final[list[ELEMENTARY_TYPE]] = [  # type: ignore
    PAD,
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
    int,
    float,
]

####################################################################################################

### Data Type Lookup Tables ########################################################################

TYPE_TO_TAG: Final[dict[ELEMENTARY_TYPE, str]] = {  # type: ignore
    PAD: "x",
    U8: "B",
    U16: "H",
    U32: "I",
    U64: "Q",
    I8: "b",
    I16: "h",
    I32: "i",
    I64: "q",
    F16: "e",
    F32: "f",
    F64: "d",
    int: "Q",
    float: "d",
}

TYPE_TO_PYTYPE: Final[dict[ELEMENTARY_TYPE, Union[type, None]]] = {  # type: ignore
    PAD: None,
    U8: int,
    U16: int,
    U32: int,
    U64: int,
    I8: int,
    I16: int,
    I32: int,
    I64: int,
    F16: float,
    F32: float,
    F64: float,
    int: int,
    float: float,
}

TYPE_TO_LENGTH: Final[dict[ELEMENTARY_TYPE, int]] = {  # type: ignore
    PAD: 1,
    U8: 1,
    U16: 2,
    U32: 4,
    U64: 8,
    I8: 1,
    I16: 2,
    I32: 4,
    I64: 8,
    F16: 2,
    F32: 4,
    F64: 8,
    int: 8,
    float: 8,
}

####################################################################################################
