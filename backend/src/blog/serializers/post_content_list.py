from typing import List, Self, Union
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

# StrEnums


class PostListStyles(StrEnum):
    ordered = 'ordered'
    unordered = 'unordered'
    checklist = 'checklist'


class CounterTypes(StrEnum):
    numeric = 'numeric'

    lower_roman = 'lower-roman'
    upper_roman = 'upper-roman'

    lower_alpha = 'lower-alpha'
    upper_alpha = 'upper-alpha'


# META


class ItemMetaChecklist(BaseModel):
    model_config = ConfigDict(extra='forbid')

    checked: bool = Field(default=False)


class ItemMetaOrdered(BaseModel):
    model_config = ConfigDict(extra='forbid')

    start: int = Field(default=1)
    counterType: CounterTypes = Field(default=CounterTypes.numeric)


class ItemMetaUnordered(BaseModel):
    model_config = ConfigDict(extra='forbid')

    pass


ItemMeta = Union[ItemMetaChecklist, ItemMetaOrdered, ItemMetaUnordered]

# MAIN


class Item(BaseModel):
    model_config = ConfigDict(extra='forbid')

    content: str = Field(default='')
    meta: ItemMeta
    items: List[Self]


class DataPostList(BaseModel):
    model_config = ConfigDict(extra='forbid')

    style: PostListStyles = PostListStyles.ordered
    meta: ItemMeta
    items: List[Item]
