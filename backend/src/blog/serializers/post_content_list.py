"""file with Pydantic schemas to validate EditorJS lists data."""

from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field

# StrEnums


class PostListStyles(StrEnum):
    """Enum with available styles for the list."""
    
    ordered = 'ordered'
    unordered = 'unordered'
    checklist = 'checklist'


class CounterTypes(StrEnum):
    """Enum with available counter styles for the list."""
    
    numeric = 'numeric'

    lower_roman = 'lower-roman'
    upper_roman = 'upper-roman'

    lower_alpha = 'lower-alpha'
    upper_alpha = 'upper-alpha'


# META


class ItemMetaChecklist(BaseModel):
    """Metadata of the Checklists."""
    
    model_config = ConfigDict(extra='forbid')

    checked: bool = Field(default=False)


class ItemMetaOrdered(BaseModel):
    """Metadata of the ordered lists."""
    
    model_config = ConfigDict(extra='forbid')

    start: int = Field(default=1)
    counterType: CounterTypes = Field(default=CounterTypes.numeric)


class ItemMetaUnordered(BaseModel):
    """Metadata of the unordered lists."""
    
    model_config = ConfigDict(extra='forbid')

    pass


ItemMeta = ItemMetaChecklist | ItemMetaOrdered | ItemMetaUnordered

# MAIN


class Item(BaseModel):
    """Data of the list's element."""
    
    model_config = ConfigDict(extra='forbid')

    content: str = Field(default='')
    meta: ItemMeta
    items: list[Self]


class DataPostList(BaseModel):
    """List's data."""
    
    model_config = ConfigDict(extra='forbid')

    style: PostListStyles = PostListStyles.ordered
    meta: ItemMeta
    items: list[Item]
