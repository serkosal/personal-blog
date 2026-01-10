"""file with Pydantic schemas to validate EditorJS JSON."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from .post_content_list import DataPostList


class DataWarning(BaseModel):
    """EditorJS Warning data of the post content."""
    
    model_config = ConfigDict(extra='forbid')

    title: str
    message: str


class DataQuote(BaseModel):
    """EditorJS Quote data of the post content."""
    
    model_config = ConfigDict(extra='forbid')

    text: str
    caption: str
    alignment: Literal['left', 'right'] = Field(default='left')


class DataHeader(BaseModel):
    """EditorJS Header data of the post content."""
    
    model_config = ConfigDict(extra='forbid')

    text: str
    level: int = Field(ge=2, le=6)


class DataParagraph(BaseModel):
    """EditorJS Paragraph data of the post content."""
    
    model_config = ConfigDict(extra='forbid')

    text: str


BaseDataBlock = (
    DataWarning | DataQuote | DataHeader | DataParagraph | DataPostList
)


BlockDataMapping = {
    Literal['warning']: DataWarning,
    Literal['paragraph']: DataParagraph,
    Literal['quote']: DataQuote,
    Literal['header']: DataHeader,
    Literal['list']: DataPostList,
}


class ContentBlock(BaseModel):
    """EditorJS Block data of the post content."""
    
    model_config = ConfigDict(extra='forbid')

    id: str
    type: (
        Literal['warning']
        | Literal['paragraph']
        | Literal['quote']
        | Literal['header']
        | Literal['list']
    )
    data: BaseDataBlock


class PostContentSchema(BaseModel):
    """Pydantic schema of the post content."""
    
    model_config = ConfigDict(extra='forbid')

    time: datetime
    blocks: list[ContentBlock]
    version: str
