from bytechomp.byte_order import ByteOrder


def test_byte_order_serialization() -> None:
    assert ByteOrder.NATIVE.to_pattern() == "@"
    assert ByteOrder.BIG.to_pattern() == ">"
    assert ByteOrder.LITTLE.to_pattern() == "<"
