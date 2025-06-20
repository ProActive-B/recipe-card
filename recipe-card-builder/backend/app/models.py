from __future__ import annotations

from typing import Optional
from sqlmodel import Field, SQLModel


class Job(SQLModel, table=True):
    id: str = Field(primary_key=True)
    video_url: str
    target_lang: str
    status: str
    recipe_id: Optional[str] = None


class Recipe(SQLModel, table=True):
    id: str = Field(primary_key=True)
    video_id: str
    title: str
    ingredients: str
    steps: str
    servings: Optional[str] = None
    cook_time: Optional[str] = None
