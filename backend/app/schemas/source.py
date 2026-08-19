from pydantic import BaseModel, Field


class Source(BaseModel):

    id: int = Field(
        description="Unique citation number for this source."
    )

    title: str = Field(
        description="Title of the source."
    )

    url: str = Field(
        description="URL of the source."
    )