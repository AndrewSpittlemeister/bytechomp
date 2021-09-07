from __future__ import annotations
from typing import TypeVar, Generic
from dataclasses import is_dataclass, fields
import inspect

# NOTE: can't seem to get the instantiation of T from within the class, may need to revert to variable or look into abstract base classes.
T = TypeVar("T")
class Reader(Generic[T]):
    def __init__(self, datatype: type) -> None:
        # for member in inspect.getmembers(self):
        #     print(member)
        if not inspect.isclass(datatype) or not is_dataclass(datatype):
            raise Exception("datatype must be a dataclass declaration")

        self.__datatype: type = datatype

        # verify that the datatype contains only known types
        self.__object_description: list = self.__build_nested_data_description(datatype)

    def __build_nested_data_description(self, datatype: type) -> list:
        object_description: list = []

        for field in fields(datatype):
            # if field is a dataclass, recurse
            if is_dataclass(field.type):
                object_description.append(
                    {
                        "name": field.name,
                        "is_anchor": False,
                    }
                )

    def feed(self, data: bytes) -> None:
        pass

    def __lshift__(self, data: bytes) -> Reader:
        self.feed(data)
        return self

    def is_valid(self) -> bool:
        pass

    def build(self):
        pass
