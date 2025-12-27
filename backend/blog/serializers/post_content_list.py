from typing import List, Self
from enum import StrEnum

from pydantic import BaseModel, Field

# StrEnums

class PostListStyles(StrEnum): 
    ordered   = "ordered"
    unordered = "unordered"
    checklist = "checklist"


class CounterTypes(StrEnum):
    numeric = "numeric"
    
    lower_roman = "lower-roman"
    upper_roman = "upper-roman"
    
    lower_alpha = "lower-alpha"
    upper_alpha = "upper-alpha"


# META

class ItemMetaChecklist(BaseModel):
    checked: bool = Field(default=False)


class ItemMetaOrdered(BaseModel):
    start: int = Field(default=1)
    counterType: CounterTypes = Field(default=CounterTypes.numeric)


class ItemMetaUnordered(BaseModel):
    pass


ItemMeta = ItemMetaChecklist | ItemMetaOrdered | ItemMetaUnordered

# MAIN

class Item(BaseModel):
    content: str = Field(default="")
    meta: ItemMeta
    items: List[Self]
 

class PostListSerializer(BaseModel):    
    style: PostListStyles  = PostListStyles.ordered
    items : List[Item]