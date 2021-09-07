from __future__ import annotations
from typing import Any, Union, Annotated, get_origin, get_args, GenericAlias
from dataclasses import dataclass, is_dataclass, fields, MISSING
from collections import OrderedDict
import inspect

from bytechomp.datatypes import *


@dataclass
class BasicProtocolSchema:
    parsing_type: Union[ELEMENTARY_TYPE, STRING, BYTES]
    python_type: Union[int, float, str, bytes]
    parser_tag: str
    length: int
    default_value: Union[int, float, str, bytes, None] = None
    raw_data: bytes = b""
    parsed_value: Union[int, float, str, bytes, None] = None

    
class Reader:
    def __init__(self, datatype: type, byte_order: str = "little") -> None:
        if not inspect.isclass(datatype) or not is_dataclass(datatype):
            raise Exception("datatype must be a dataclass declaration")

        if byte_order not in ["big", "little"]:
            raise Exception("byte order must be one \"big\" or \"little\"")

        self.__datatype = datatype
        self.__byte_order = byte_order
        self.__is_complete = False
        self.__data = b""

        # verify that the datatype contains only known types
        self.__data_description: OrderedDict = self.__build_data_description(self.__datatype)

        print(self.__data_description)

    def __build_data_description(self, datatype: type) -> OrderedDict:
        object_description: dict[str, Union[list, dict, ELEMENTARY_TYPE]] = OrderedDict()

        for field in fields(datatype):
            if field.type in ELEMENTARY_TYPE_LIST:
                object_description[field.name] = BasicProtocolSchema(
                    parsing_type=field.type,
                    python_type=TYPE_TO_PYTYPE[field.type],
                    parser_tag=TYPE_TO_TAG[field.type],
                    length=TYPE_TO_LENGTH[field.type],
                    default_value=None if field.default == MISSING else field.default,
                )
            elif inspect.isclass(field.type) and is_dataclass(field.type):
                if field.default != MISSING:
                    raise Exception(f"cannot have default value on nested types (field: {field.name})")
                object_description[field.name] = self.__build_data_description(field.type)
            elif get_origin(field.type) == Annotated:
                args = get_args(field.type)

                if len(args) != 2:
                    raise Exception(f"annotated value should only have two arguments (field: {field.name})")

                arg_type = args[0]
                length = args[1]

                if type(length) != int:
                    raise Exception(f"second annotated argument must be an integer to denote length")

                # deal with string type
                if arg_type in [STRING, str]:
                    object_description[field.name] = BasicProtocolSchema(
                        parsing_type=STRING,
                        python_type=str,
                        parser_tag="c",
                        length=length,
                        default_value=None if field.default == MISSING else field.default,
                    )

                # deal with bytes type
                elif arg_type in [BYTES, bytes]:
                    object_description[field.name] = BasicProtocolSchema(
                        parsing_type=BYTES,
                        python_type=bytes,
                        parser_tag="c",
                        length=length,
                        default_value=None if field.default == MISSING else field.default,
                    )

                # deal with list type
                elif get_origin(arg_type) == list:
                    list_type_args = get_args(arg_type)

                    if len(list_type_args) != 1:
                        raise Exception(f"list must contain only one kind of data type (field: {field.name})")

                    list_type = list_type_args[0]

                    if list_type in ELEMENTARY_TYPE_LIST:
                        object_description[field.name] = [
                            BasicProtocolSchema(
                                parsing_type=list_type,
                                python_type=TYPE_TO_PYTYPE[list_type],
                                parser_tag=TYPE_TO_TAG[list_type],
                                length=TYPE_TO_LENGTH[list_type],
                            )
                        ] * length
                    elif inspect.isclass(list_type) and is_dataclass(list_type):
                        object_description[field.name] = [
                            self.__build_data_description(list_type)
                        ] * length
                    else:
                        raise Exception(f"unsupported list type: {list_type} (field: {field.name})")

                else:
                    raise Exception(f"unsupported annotated type: {arg_type} (field: {field.name})")

                pass
            elif field.type in [list, bytes, str, STRING, BYTES]:
                raise Exception(f"cannot have unannotated list, string, or bytes type (length required, field: {field.name})")
            else:
                raise Exception(f"unsupported data type ({field.type}) on field {field.name}")

        return object_description

    def feed(self, data: bytes) -> None:
        self.__data += data

    def __lshift__(self, data: bytes) -> Reader:
        self.feed(data)
        return self

    def is_complete(self) -> bool:
        return self.__is_complete

    def build(self) -> Any:
        pass
