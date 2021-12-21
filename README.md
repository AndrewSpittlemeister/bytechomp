# bytechomp

> *A pure python, declarative custom binary protocol parser using dataclasses and type hinting.*

`bytechomp` leverages Python's type hinting system at runtime to build binary protocol parsing schemas from dataclass implementations. Deserialization of the binary data is now abstracted away by `bytechomp`, leaving you to work in the land of typed and structured data.

**Features:**
- [x] Pure Python
- [x] Zero Dependencies
- [x] Uses native type-hinting & dataclasses
- [x] Supports lower-precision numerics
- [x] Supports `bytes` and `str` fields of known length
- [x] Supports `list` types for repeated, continuous fields of known length
- [x] Supports nested structures

## Installation

`bytechomp` is a small, pure python library with zero dependencies. It can be installed via PyPI:

```
pip install bytechomp
```

or Git for the latest unreleased code:

```
pip install https://github.com/AndrewSpittlemeister/bytechomp.git@main
```

## Example Usage

```python
from typing import Annotated
from dataclasses import dataclass

from bytechomp import Reader
from bytechomp.datatypes import U16, F32


@dataclass
class Header:
    timestamp: float  # native datatypes can be used when assuming full precision
    message_count: int  # similarly with 64-bit integers
    message_identity: U16  # custom datatypes are available and will be cast to native when deserialized


@dataclass
class Body:
    unique_id: Annotated[bytes, 5]  # use of typing.Annotated to denote length
    name: Annotated[str, 64]  # string values are decoded from byte streams too 
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
```

### Reader API


## How does this work?

## Additional Notes

- uses undocumented reflection API