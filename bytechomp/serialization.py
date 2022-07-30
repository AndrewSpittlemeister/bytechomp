"""
bytechomp.serialization
"""

import struct
from typing import Annotated, get_origin, get_args
from dataclasses import is_dataclass, fields

from bytechomp.datatypes.lookups import (
    ELEMENTARY_TYPE_LIST,
    TYPE_TO_TAG,
    TYPE_TO_PYTYPE,
)
from bytechomp.byte_order import ByteOrder


def flatten_dataclass(data_object: type) -> tuple[str, list[int | float | bytes]]:
    """Flattens out the dataclass into a pattern and a list of values.

    Args:
        data_object (type): Dataclass object.

    Returns:
        tuple[str, list[int | float | bytes]]: (pattern string, values list)
    """
    # pylint: disable=too-many-branches
    # pylint: disable=line-too-long
    # pylint: disable=too-many-nested-blocks
    # pylint: disable=too-many-statements
    # pylint: disable=duplicate-code

    if not is_dataclass(data_object):
        raise TypeError("provided object must be a valid dataclass")

    pattern: str = ""
    values: list[int | float | bytes] = []

    for field in fields(data_object):
        val = getattr(data_object, field.name)
        val_t = type(val)

        if field.type in ELEMENTARY_TYPE_LIST:
            if not isinstance(val, TYPE_TO_PYTYPE[field.type]):  # type: ignore
                raise TypeError(
                    f"{field.name} field contains {val_t} type but requires {field.type}"
                )

            pattern += TYPE_TO_TAG[field.type]
            values.append(val)  # type: ignore
        elif is_dataclass(field.type):
            if not isinstance(val, val_t):
                raise TypeError(
                    f"{field.name} field contains {val_t} type but requires {field.type}"
                )

            nested_pattern, nested_values = flatten_dataclass(val)
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

            # # deal with string type
            # if arg_type == str:
            #     if not isinstance(val, str):
            #         raise TypeError(
            #             f"{field.name} field contains {val_t} type but requires {field.type}"
            #         )
            #     if length != len(val):
            #         raise TypeError(
            #             f"{field.name} string field has a length of {len(val)} but requires a length of {length}"
            #         )

            #     pattern += f"{length}s"
            #     values.append(val.encode())

            # deal with bytes type
            if arg_type == bytes:
                if not isinstance(val, bytes):
                    raise TypeError(
                        f"{field.name} field contains {val_t} type but requires {field.type}"
                    )
                if length != len(val):
                    raise TypeError(
                        f"{field.name} bytes field has a length of {len(val)} but requires a length of {length}"
                    )

                pattern += f"{length}s"
                values.append(val)

            # deal with list type
            elif get_origin(arg_type) == list:
                if not isinstance(val, list):
                    raise TypeError(
                        f"{field.name} field contains {val_t} type but requires {field.type}"
                    )
                if length != len(val):
                    raise TypeError(
                        f"{field.name} list field has a length of {len(val)} but requires a length of {length}"
                    )

                list_type_args = get_args(arg_type)

                if len(list_type_args) != 1:
                    raise Exception(
                        f"list must contain only one kind of data type (field: {field.name})"
                    )

                list_type = list_type_args[0]

                if list_type in ELEMENTARY_TYPE_LIST:
                    element_type = TYPE_TO_PYTYPE[list_type]
                    for field_element in val:
                        if not isinstance(field_element, element_type):  # type: ignore
                            raise TypeError(
                                f"{field.name} field contains {val_t} type but requires {field.type}"
                            )

                    pattern += TYPE_TO_TAG[list_type] * length
                    values.extend(val)
                elif is_dataclass(list_type):
                    element_type = list_type
                    for field_element in val:
                        if not isinstance(field_element, element_type):  # type: ignore
                            raise TypeError(
                                f"{field.name} field contains {val_t} type but requires {field.type}"
                            )

                        nested_pattern, nested_values = flatten_dataclass(field_element)  # type: ignore
                        pattern += nested_pattern
                        values.extend(nested_values)
                else:
                    raise Exception(f"unsupported list type: {list_type} (field: {field.name})")

            else:
                raise Exception(f"unsupported annotated type: {arg_type} (field: {field.name})")
        elif field.type in [list, bytes]:
            raise Exception(
                f"annotation needed for list/bytes (length required, field: {field.name})"
            )
        else:
            raise Exception(f"unsupported data type ({field.type}) on field {field.name}")

    return pattern, values


def serialize(data_object: type, byte_order: ByteOrder = ByteOrder.NATIVE) -> bytes:
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
    pattern = byte_order.to_pattern() + pattern
    # print(f"\nPattern to use '{pattern}' for values to serialize: ", values)
    return struct.pack(pattern, *values)
