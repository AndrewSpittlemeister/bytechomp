"""
bytechomp.data_descriptor
"""

from __future__ import annotations
from typing import Annotated, Any, get_origin, get_args
from dataclasses import dataclass, is_dataclass, fields, MISSING
from collections import OrderedDict
import inspect

from bytechomp.datatypes import (
    ELEMENTARY_TYPE,
    ELEMENTARY_TYPE_LIST,
    TYPE_TO_PYTYPE,
    TYPE_TO_TAG,
    TYPE_TO_LENGTH,
)


@dataclass
class BasicParsingElement:
    """Describes a node in the type tree."""

    parsing_type: ELEMENTARY_TYPE | str | bytes  # type: ignore
    python_type: type | None
    parser_tag: str
    length: int
    default_value: int | float | str | bytes | None = None
    raw_data: bytes = b""
    parsed_value: int | float | str | bytes | None = None


def build_data_description(
    datatype: type,
) -> OrderedDict[str, BasicParsingElement | type | list | OrderedDict]:
    """Uses reflection on the provided type to provide a tokenized type tree.

    Args:
        datatype (type): Type object for the user-defined dataclass.

    Returns:
        OrderedDict[str, BasicParsingElement | list | OrderedDict]: Type tree of BasicParsingElement
            nodes.
    """
    # pylint: disable=too-many-branches

    object_description: OrderedDict[
        str, BasicParsingElement | list | OrderedDict | type
    ] = OrderedDict()
    object_description["__struct_type__"] = datatype

    for field in fields(datatype):
        if field.type in ELEMENTARY_TYPE_LIST:
            object_description[field.name] = BasicParsingElement(
                parsing_type=field.type,
                python_type=TYPE_TO_PYTYPE[field.type],
                parser_tag=TYPE_TO_TAG[field.type],
                length=TYPE_TO_LENGTH[field.type],
                default_value=None if field.default == MISSING else field.default,
            )
        elif inspect.isclass(field.type) and is_dataclass(field.type):
            if field.default != MISSING:
                raise Exception(f"cannot have default value on nested types (field: {field.name})")
            object_description[field.name] = build_data_description(field.type)
        elif get_origin(field.type) == Annotated:
            args = get_args(field.type)

            if len(args) != 2:
                raise Exception(
                    f"annotated value should only have two arguments (field: {field.name})"
                )

            arg_type = args[0]
            length = args[1]

            if not isinstance(length, int):
                raise Exception("second annotated argument must be an integer to denote length")

            # deal with string type
            if arg_type == str:
                object_description[field.name] = BasicParsingElement(
                    parsing_type=str,
                    python_type=str,
                    parser_tag=f"{length}s",
                    length=length,
                    default_value=None if field.default == MISSING else field.default,
                )

            # deal with bytes type
            elif arg_type == bytes:
                object_description[field.name] = BasicParsingElement(
                    parsing_type=bytes,
                    python_type=bytes,
                    parser_tag=f"{length}p",
                    length=length,
                    default_value=None if field.default == MISSING else field.default,
                )

            # deal with list type
            elif get_origin(arg_type) == list:
                list_type_args = get_args(arg_type)

                if len(list_type_args) != 1:
                    raise Exception(
                        f"list must contain only one kind of data type (field: {field.name})"
                    )

                list_type = list_type_args[0]

                if list_type in ELEMENTARY_TYPE_LIST:
                    object_description[field.name] = [
                        BasicParsingElement(
                            parsing_type=list_type,
                            python_type=TYPE_TO_PYTYPE[list_type],
                            parser_tag=TYPE_TO_TAG[list_type],
                            length=TYPE_TO_LENGTH[list_type],
                        )
                    ] * length
                elif inspect.isclass(list_type) and is_dataclass(list_type):
                    object_description[field.name] = [build_data_description(list_type)] * length
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

    return object_description


def build_data_pattern(
    description: OrderedDict[
        str, BasicParsingElement | type | list[BasicParsingElement | OrderedDict] | OrderedDict
    ]
) -> str:
    """Determines a packed data representation using the struct module binary pattern characters.

    Args:
        description (
            OrderedDict[
                str, BasicParsingElement | list[BasicParsingElement | OrderedDict] | OrderedDict
            ]
        ): Type tree of BasicParsingElement nodes.

    Returns:
        str: Struct module pattern string.
    """

    pattern: str = ""
    for name, root_element in description.items():
        if name == "__struct_type__":
            continue

        if isinstance(root_element, BasicParsingElement):
            pattern += root_element.parser_tag
        elif isinstance(root_element, list):
            for sub_element in root_element:
                # sub elements can only be a elementary data types or other dataclasses
                if isinstance(sub_element, BasicParsingElement):
                    pattern += sub_element.parser_tag
                elif isinstance(sub_element, OrderedDict):
                    pattern += build_data_pattern(sub_element)
                else:
                    raise Exception(f"invalid list type found ({name})")
        elif isinstance(root_element, OrderedDict):
            pattern += build_data_pattern(root_element)
        else:
            raise Exception(f"invalid element type found ({name}: {type(root_element)})")
    return pattern


def resolve_basic_type(
    arg: int | float | bytes, element: BasicParsingElement
) -> int | float | bytes | str:
    """Returns the value of the element while checking the intended type in the node.

    Raises:
        Exception: [description]

    Returns:
        int | float | bytes | str: Pythonic parsed value.
    """

    if element.python_type is not None and isinstance(arg, element.python_type):
        return arg
    if isinstance(arg, bytes) and element.python_type is str:
        return arg.decode("utf-8")
    raise Exception("invalid match between types")


def build_structure(
    args: list[int | float | bytes],
    description: OrderedDict[
        str, BasicParsingElement | type | list[BasicParsingElement | OrderedDict] | OrderedDict
    ],
) -> Any:
    """Constructs an instantiation of the data type described by the description argument.

    Args:
        args (list[int): Flat list of values returned from the struct module.
        description (
            OrderedDict[
                str, BasicParsingElement | list[BasicParsingElement | OrderedDict] | OrderedDict
            ]
        ): Type tree of BasicParsingElement nodes.

    Returns:
        Any: Instantiated dataclass
    """

    cls_type = description.get("__struct_type__")
    if cls_type is not None and not isinstance(cls_type, type):
        raise Exception("lost struct type information in description")
    if cls_type is None:
        raise Exception("unable to find type information in description")
    cls_args: dict[str, Any] = {}
    # print(f"constructing type {cls_type}")

    for name, root_element in filter(
        lambda item: item[0] != "__struct_type__", description.items()
    ):
        if isinstance(root_element, BasicParsingElement):
            cls_args[name] = resolve_basic_type(args.pop(0), root_element)
        elif isinstance(root_element, list):
            list_element: list[Any] = []
            for sub_element in root_element:
                # sub elements can only be a elementary data types or other dataclasses
                if isinstance(sub_element, BasicParsingElement):
                    resolve_basic_type(args.pop(0), sub_element)
                elif isinstance(sub_element, OrderedDict):
                    list_element.append(build_structure(args, sub_element))
                else:
                    raise Exception(f"invalid list type found ({name})")
            cls_args[name] = list_element
        elif isinstance(root_element, OrderedDict):
            cls_args[name] = build_structure(args, root_element)
        else:
            raise Exception(f"invalid element type found ({name}: {type(root_element)})")

    return cls_type(**cls_args)
