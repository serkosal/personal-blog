from typing import Literal, List, Union, Dict
from datetime import datetime

from pydantic import BaseModel, Field, model_validator
        

class DataWarning(BaseModel):
    title: str
    message: str


class DataQuote(BaseModel):
    text: str
    caption: str
    alignment : Literal["left", "right"] = Field(default="left")


class DataHeader(BaseModel):
    text: str
    level: int = Field(ge=2, le=6)


class DataParagraph(BaseModel):    
    text: str


DATA_TYPES = Union[DataWarning, DataQuote, DataHeader, DataParagraph]
BLOCK_DATA_MAPPING: Dict[str, DATA_TYPES] = {
    "warning":      DataWarning,
    "quote":        DataQuote,
    "header":       DataHeader,
    "paragraph":    DataParagraph
}
    
class BaseBlock(BaseModel):
    id: str
    type: Literal["warning", "quote", "header", "paragraph"]
    data: DATA_TYPES
    
    @model_validator(mode="after")
    def check_data(self):
        
        mapped_type = BLOCK_DATA_MAPPING.get(self.type)
        
        if mapped_type != type(self.data):
            raise ValueError(f"type of {self.type} is in")



class PostContentSerializer(BaseModel):
    time: datetime
    blocks: List[BaseBlock]
    version: str
