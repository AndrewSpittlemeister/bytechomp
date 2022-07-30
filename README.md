# bytechomp

[![ci](https://github.com/AndrewSpittlemeister/bytechomp/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/AndrewSpittlemeister/bytechomp/actions/workflows/ci.yml)
[![PyPI Version](https://img.shields.io/pypi/v/bytechomp.svg)](https://pypi.org/project/bytechomp/)
[![Python Versions](https://img.shields.io/pypi/pyversions/bytechomp.svg)](https://pypi.org/project/bytechomp/)
![Lines of Code](https://tokei.rs/b1/github/AndrewSpittlemeister/bytechomp?category=code)

> *A pure python, declarative custom binary protocol parser & generator using dataclasses and type hinting.*

`bytechomp` leverages Python's type hinting system at runtime to build binary protocol parsing schemas from dataclass implementations. Deserialization/Serialization of the binary data is now abstracted away by `bytechomp`, leaving you to work in the land of typed and structured data.

**Features:**
- [x] Pure Python
- [x] Zero Dependencies
- [x] Uses native type-hinting & dataclasses
- [x] Supports lower-precision numerics
- [x] Supports `bytes` fields of known length
- [x] Supports `list` types for repeated, continuous fields of known length
- [x] Supports nested structures
- [x] Supports serialization of populated data structures

## Installation

`bytechomp` is a small, pure python library with zero dependencies. It can be installed via PyPI:

```
pip install bytechomp
```

or Git for the latest unreleased code:

```
pip install https://github.com/AndrewSpittlemeister/bytechomp.git@main
```

## Reader API

The `Reader` class uses Python's built-in [generics](https://docs.python.org/3/library/typing.html#generics) determine the dataclass used when parsing. This dataclass is defined by the user to mimic the binary protocol. Once instantiated, the `Reader` class can be fed `bytes` and used to construct the dataclass when ready. There are various ways to accomplish this with the `Reader` class:

```python
from dataclasses import dataclass

from bytechomp import Reader

@dataclass
class MyStruct:
    timestamp: float
    identity: int

# instantiate a reader
reader = Reader[MyStruct]().allocate()

# add data to the internal buffer
reader.feed(stream.read(512))

# check if enough data is present to build
print(reader.is_complete())

# add via the bitshift method
reader << stream.read(512)

# check via bool magic method
print(bool(reader))

# combine alternative methods
if reader << stream.read(512):
    # construct dataclass
    my_struct = reader.build()

# clear internal byte buffer
reader.clear()

# use the iterator API
simulated_byte_iterator = [b"a"] * 10
for my_struct in reader.iter(simulated_byte_iterator):
    print(my_struct)
```

## Serialization API
Similar to the `Reader`, serialization of data is accomplished through defining dataclasses in the same manner.

```python
from bytechomp import serialize

my_struct = MyStruct(1.1, 15)

serialized_struct: bytes = serialize(my_struct)
```

## Supported Type Fields
Fields on the dataclasses can be integers, floats, strings, bytes, lists, or other dataclasses. Python-native `int` and `float` represent 64-bit variants. Other sizes can be imported from `bytechomp`:

```python
from bytechomp.datatypes import (
    U8,  # 8-bit unsigned integer
    U16,  # 16-bit unsigned integer
    U32,  # 32-bit unsigned integer
    U64,  # 64-bit unsigned integer
    I8,  # 8-bit signed integer
    I16,  # 16-bit signed integer
    I32,  # 32-bit signed integer
    I64,  # 64-bit signed integer
    F16,  # 16-bit float
    F32,  # 32-bit float
    F64,  # 64-bit float
)
```

Although these allow a `Reader` to parse a field of a custom size, the resulting value populated in a dataclass field will always be the python-natives `int` or `float`.

Repeated fields like `bytes` and `list` require the use of Python's `typing.Annotated` to allow defining a length.

```python
from bytechomp import Annotated, dataclass  # re-exported by bytechomp

@dataclass
class Message:
    name: Annotated[bytes, 10]
    identity: Annotated[bytes, 10]
    flags: Annotated[list[int], 5]
```

Finally, `list` fields can contain any other supported datatype, including other dataclass structures to handle complex, nested protocols.

## Byte Ordering
Byte default the byte-ordering is set to the machine's native format, but can be changed:

```python
from bytechomp import Reader, ByteOrder, dataclass, serialize

@dataclass
class MyStruct:
    timestamp: float
    identity: int

# use native (the default)
reader = Reader[MyStruct](ByteOrder.NATIVE).allocate()
data = serialize(MyStruct(1.1, 15), ByteOrder.NATIVE)

# use little endian
reader = Reader[MyStruct](ByteOrder.LITTLE).allocate()
data = serialize(MyStruct(1.1, 15), ByteOrder.LITTLE)

# use big endian
reader = Reader[MyStruct](ByteOrder.BIG).allocate()
data = serialize(MyStruct(1.1, 15), ByteOrder.BIG)
```

## A Longer Example

```python
from bytechomp import Reader, dataclass, Annotated, serialize
from bytechomp.datatypes import U16, F32


@dataclass
class Header:
    timestamp: float  # native datatypes can be used when assuming full precision
    message_count: int  # similarly with 64-bit integers
    message_identity: U16  # custom datatypes are available and will be cast to native when deserialized


@dataclass
class Body:
    unique_id: Annotated[bytes, 5]  # use of typing.Annotated to denote length
    balance: F32


@dataclass
class Message:
    header: Header  # nested data structures are allowed
    body: Body


@dataclass
class MessageBundle:
    messages: Annotated[list[Message], 8]  # so are lists of data structures!


def main() -> None:
    # build Reader object using the MessageBundle class as its generic argument
    reader = Reader[MessageBundle]().allocate()

    with open("my-binary-data-stream.dat", "rb") as fp:
        while (data := fp.read(4)):
            # feed stream into the reader
            reader.feed(data)

            # check if the structure has been saturated with enough data
            if reader.is_complete():
                # parse the stream and create your typed data structure!
                msg_bundle = reader.build()
                print(msg_bundle)

                # re-serialize this data
                print(f"serialized data: {serialize(msg_bundle)}")
```

## Other Examples
- See [parse-sqlite-header.py](./examples/parse-sqlite-header.py) for an example of using `bytechomp` to read the header message of an sqlite file. A rough estimate of what this should result in can be found [here](https://docs.fileformat.com/database/sqlite/).
- See [tcp-client-server.py](./examples/tcp-client-server.py) for an example of using `bytechomp` to serialize/deserialize binary messages across a TCP connection.


## How does this work?

While a binary stream is usually represented as a flat, continuous data, `bytechomp` can be used as a structural abstraction over this data. Therefore, if there was a message with the following structure for a message called `UserState`:

| Field | Type | Description |
| ----- | ---- | ----------- |
| `user_id` | uint64 | user's unique identity |
| `balance` | float32 | user's balance |

The resulting translation to a dataclass would be the following:

```python
from bytechomp import Reader, dataclass
from bytechomp.datatypes import F32

@dataclass
class UserState:
    user_id: int
    balance: F32
```

When parsing messages that contain other messages, you will need to be aware of how the embedded messages are contained and how the resulting memory layout will look for the container message as whole. Since the container message is still represented as one set of continuous bytes, nested classes in bytechomp are constructed using a depth first search of the contained fields in nested structures to build out a flattened parsing pattern for Python's `struct` module.

Consider the following structures:

```python
from bytechomp import Reader, dataclass, Annotated  # using re-export from within bytechomp
from bytechomp.datatypes import F32

@dataclass
class UserState:
    user_id: int
    balance: F32

@dataclass
class Transaction:
    amount: F32
    sender: int
    receiver: int

@dataclass
class User:
    user_state: UserState
    recent_transactions: Annotated[list[Transaction], 3]
```

The `User` message would correspond to the following memory layout:

```
uint64, float32, float32, int64, int64, float32, int64, int64, float32, int64, int64
```

## Additional Notes

This package is based on a mostly undocumented feature in standard implementation of CPython. This is the ability to inspect the type information generic parameters via the `self.__orig_class__.__args__` structures. The information in this structure is only populated after initialization (hence the need for the `allocate()` method when instantiated a `Reader` object). Should this behavior change in future versions of Python, `bytechomp` will adapt accordingly. For now, it will stay away from passing a type object as a argument to initialization because that just seems hacky.

**Future Improvements:**
- Perhaps allowing for parameterized fields to reference previously declared fields (i.e. allowing a list of size `n` where `n` is the previous field)
- Allow declaring value restraints on fields
    - Making use of the `typing.Literal` python class
- Allow for enums to be generated for integer fields
