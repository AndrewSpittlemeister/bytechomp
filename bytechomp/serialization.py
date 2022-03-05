"""
bytechomp.serialization
"""

import struct
from typing import Annotated, get_origin, get_args
from dataclasses import is_dataclass, fields

from bytechomp.datatypes.lookups import ELEMENTARY_TYPE_LIST, TYPE_TO_TAG


def flatten_dataclass(data_object: type) -> tuple[str, list[int | float | str | bytes]]:
    """Flattens out the dataclass into a pattern and a list of values.

    Args:
        data_object (type): Dataclass object.

    Returns:
        tuple[str, list[int | float | str | bytes]]: (pattern string, values list)
    """
    # pylint: disable=too-many-branches

    if not is_dataclass(data_object):
        raise TypeError("provided object must be a valid dataclass")

    pattern: str = ""
    values: list[int | float | str | bytes] = []

    for field in fields(data_object):
        field_value = getattr(data_object, field.name)

        if field.type in ELEMENTARY_TYPE_LIST:
            pattern += TYPE_TO_TAG[field.type]
            values.append(field_value)
        elif is_dataclass(field.type):
            nested_pattern, nested_values = flatten_dataclass(field_value)
            pattern += nested_pattern
            values.extend(nested_values)
        elif get_origin(field.type) == Annotated:
            args = get_args(field.type)

            if len(args) != 2:
                raise Exception(
                    f"annotated value should only have two arguments (field: {field.name})"
                )

            arg_type = args[0]
            length = args[1]

            if not isinstance(length, int):
                raise TypeError("second annotated argument must be an integer to denote length")

            # deal with string type
            if arg_type == str:
                pattern += f"{length}s"
                values.append(field_value.encode())

            # deal with bytes type
            elif arg_type == bytes:
                pattern += f"{length}p"
                values.append(field_value)

            # deal with list type
            elif get_origin(arg_type) == list:
                list_type_args = get_args(arg_type)

                if len(list_type_args) != 1:
                    raise Exception(
                        f"list must contain only one kind of data type (field: {field.name})"
                    )

                list_type = list_type_args[0]

                if list_type in ELEMENTARY_TYPE_LIST:
                    pattern += TYPE_TO_TAG[list_type] * length
                    values.extend(field_value)
                elif is_dataclass(list_type):
                    for element in field_value:
                        nested_pattern, nested_values = flatten_dataclass(element)
                        pattern += nested_pattern
                        values.extend(nested_values)
                else:
                    raise Exception(f"unsupported list type: {list_type} (field: {field.name})")

            else:
                raise Exception(f"unsupported annotated type: {arg_type} (field: {field.name})")
        elif field.type in [list, bytes, str]:
            raise Exception(
                f"annotation needed for list/string/bytes (length required, field: {field.name})"
            )
        else:
            raise Exception(f"unsupported data type ({field.type}) on field {field.name}")

    return pattern, values


def serialize(data_object: type) -> bytes:
    """Serializes a completely populated dataclass into a byte string according to the bytechomp
        serialization rules.

    Args:
        data_object (type): Dataclass object.

    Returns:
        bytes: Serialization of the datclass object.
    """

    if not is_dataclass(data_object):
        raise TypeError("provided object must be a valid dataclass")

    pattern, values = flatten_dataclass(data_object)
    return struct.pack(pattern, *values)
