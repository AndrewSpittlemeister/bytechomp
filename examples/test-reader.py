from bytechomp import Reader, dataclass, Annotated
from bytechomp.datatypes import I32

@dataclass
class Alpha:
    a: int
    b: I32
    c: Annotated[str, 5]

@dataclass
class Beta:
    timestamp: float
    alpha: Alpha
    alphas: Annotated[list[Alpha], 2]


def main() -> None:
    reader = Reader[Beta]().allocate()
    reader << b"asdfas"
    print(reader.is_complete())
    if reader:
        print("here1")
    else:
        print("here2")

    if reader << b"fdsaasasdfasfdasdfasfasdfasdfasdfasdfasdfasdfasdf" * 10:
        print("here1")
        print(reader.build())
    else:
        print("here2")

    reader.clear()

    print(type(Beta))

    # print("building...")
    # print(reader.build())
    # print(reader.build())
    # print(reader.build())

    # print(Alpha(**{"a": 1, "b": 1, "c": "asdfg"}))
    # print(Beta(**{"timestamp": 101.1, "alpha": Alpha(**{"a": 1, "b": 1, "c": "asdfg"}), "alphas": [Alpha(**{"a": 1, "b": 1, "c": "asdfg"})] * 2}))


if __name__ == "__main__":
    main()
