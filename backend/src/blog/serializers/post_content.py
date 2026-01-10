from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from .post_content_list import DataPostList


class DataWarning(BaseModel):
    model_config = ConfigDict(extra='forbid')

    title: str
    message: str


class DataQuote(BaseModel):
    model_config = ConfigDict(extra='forbid')

    text: str
    caption: str
    alignment: Literal['left', 'right'] = Field(default='left')


class DataHeader(BaseModel):
    model_config = ConfigDict(extra='forbid')

    text: str
    level: int = Field(ge=2, le=6)


class DataParagraph(BaseModel):
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
    model_config = ConfigDict(extra='forbid')

    time: datetime
    blocks: list[ContentBlock]
    version: str
