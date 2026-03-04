"""Pydantic models for PromptLab"""

from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


def generate_id() -> str:
    """Generate a unique identifier using UUID4.

    Returns:
        str: The generated unique identifier as a string.
    """
    return str(uuid4())


def get_current_time() -> datetime:
    """Get the current UTC time.

    Returns:
        datetime: The current UTC datetime.
    """
    return datetime.utcnow()


# ============== Prompt Models ==============


class PromptBase(BaseModel):
    """Base model for prompts containing common fields."""

    title: str = Field(..., min_length=1, max_length=200, description="Title of the prompt.")
    content: str = Field(..., min_length=1, description="Content or body of the prompt.")
    description: Optional[str] = Field(None, max_length=500, description="Optional description of the prompt.")
    collection_id: Optional[str] = Field(None, description="Identifier of the collection to which the prompt belongs.")


class PromptCreate(PromptBase):
    """Model for creating a new prompt, inherits from PromptBase."""
    pass


class PromptUpdate(PromptBase):
    """Model for updating an existing prompt, inherits from PromptBase."""
    pass


class Prompt(PromptBase):
    """Model representing a prompt including its metadata."""

    model_config = ConfigDict(from_attributes=True)

    id: str = Field(default_factory=generate_id, description="Unique identifier for the prompt.")
    created_at: datetime = Field(default_factory=get_current_time, description="Timestamp when the prompt was created.")
    updated_at: datetime = Field(default_factory=get_current_time, description="Timestamp when the prompt was last updated.")


# ============== Collection Models ==============


class CollectionBase(BaseModel):
    """Base model for collections containing common fields."""

    name: str = Field(..., min_length=1, max_length=100, description="Name of the collection.")
    description: Optional[str] = Field(None, max_length=500, description="Optional description of the collection.")


class CollectionCreate(CollectionBase):
    """Model for creating a new collection, inherits from CollectionBase."""
    pass


class Collection(CollectionBase):
    """Model representing a collection including its metadata."""

    model_config = ConfigDict(from_attributes=True)

    id: str = Field(default_factory=generate_id, description="Unique identifier for the collection.")
    created_at: datetime = Field(default_factory=get_current_time, description="Timestamp when the collection was created.")


# ============== Response Models ==============


class PromptList(BaseModel):
    """Response model for a list of prompts, along with the total count."""

    prompts: List[Prompt] = Field(description="List of prompt objects.")
    total: int = Field(description="Total number of prompts available.")


class CollectionList(BaseModel):
    """Response model for a list of collections, along with the total count."""

    collections: List[Collection] = Field(description="List of collection objects.")
    total: int = Field(description="Total number of collections available.")


class HealthResponse(BaseModel):
    """Model for health check response including status and version of the API."""

    status: str = Field(description="Current status of the application.")
    version: str = Field(description="Current version of the application.")
