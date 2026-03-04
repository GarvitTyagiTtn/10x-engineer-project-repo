"""FastAPI routes for PromptLab"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Any, Dict, List, Optional

from app.models import (
    Prompt, PromptCreate, PromptUpdate,
    Collection, CollectionCreate,
    PromptList, CollectionList, HealthResponse,
    get_current_time,
)
from app.storage import storage
from app.utils import (
    sort_prompts_by_date,
    filter_prompts_by_collection,
    search_prompts,
    filter_prompts_by_tags,
)
from app import __version__

app = FastAPI(
    title="PromptLab API",
    description="AI Prompt Engineering Platform",
    version=__version__,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== Helpers ==============


def _get_prompt_or_404(prompt_id: str) -> Prompt:
    """Fetch a prompt by ID or raise a 404 HTTPException.

    Args:
        prompt_id (str): The unique identifier of the prompt.

    Returns:
        Prompt: The prompt object if found.

    Raises:
        HTTPException: 404 error if the prompt is not found.
    """
    prompt = storage.get_prompt(prompt_id)
    if prompt is None:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt


def _get_collection_or_404(collection_id: str) -> Collection:
    """Fetch a collection by ID or raise a 404 HTTPException.

    Args:
        collection_id (str): The unique identifier of the collection.

    Returns:
        Collection: The collection object if found.

    Raises:
        HTTPException: 404 error if the collection is not found.
    """
    collection = storage.get_collection(collection_id)
    if collection is None:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


def _validate_collection_exists(collection_id: Optional[str]) -> None:
    """Validate that a collection exists in storage if a collection_id is provided.

    Args:
        collection_id (Optional[str]): The collection ID to validate, or None.

    Raises:
        HTTPException: 400 error if the collection_id is provided but not found.
    """
    if collection_id and not storage.get_collection(collection_id):
        raise HTTPException(status_code=400, detail="Collection not found")


# ============== Health Check ==============


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """Check the health of the API service.

    Returns:
        HealthResponse: Object containing status and version information of the API.
    """
    return HealthResponse(status="healthy", version=__version__)


# ============== Prompt Endpoints ==============


@app.get("/prompts", response_model=PromptList)
def list_prompts(
    collection_id: Optional[str] = None,
    search: Optional[str] = None,
    tags: Optional[str] = None,
) -> PromptList:
    """Retrieve a list of prompts, with optional filtering by collection, search query, or tags.

    Args:
        collection_id (Optional[str]): The ID of the collection to filter prompts by.
        search (Optional[str]): The search query to filter prompts by matching titles.
        tags (Optional[str]): Comma-separated tags to filter by (all must match).

    Returns:
        PromptList: A list of prompts and the total count.
    """
    prompts = storage.get_all_prompts()

    if collection_id:
        prompts = filter_prompts_by_collection(prompts, collection_id)
    if tags:
        tag_list = [t.strip() for t in tags.split(",") if t.strip()]
        prompts = filter_prompts_by_tags(prompts, tag_list)
    if search:
        prompts = search_prompts(prompts, search)

    prompts = sort_prompts_by_date(prompts, descending=True)
    return PromptList(prompts=prompts, total=len(prompts))


@app.get("/prompts/{prompt_id}", response_model=Prompt)
def get_prompt(prompt_id: str) -> Prompt:
    """Get details of a specific prompt by its ID.

    Args:
        prompt_id (str): The unique identifier of the prompt.

    Returns:
        Prompt: The prompt object if found.

    Raises:
        HTTPException: 404 error if the prompt is not found.
    """
    return _get_prompt_or_404(prompt_id)


@app.post("/prompts", response_model=Prompt, status_code=201)
def create_prompt(prompt_data: PromptCreate) -> Prompt:
    """Create a new prompt with the given data.

    Args:
        prompt_data (PromptCreate): The data needed to create a new prompt.

    Returns:
        Prompt: The newly created prompt object.

    Raises:
        HTTPException: 400 error if the provided collection ID is not found.
    """
    _validate_collection_exists(prompt_data.collection_id)
    prompt = Prompt(**prompt_data.model_dump())
    return storage.create_prompt(prompt)


@app.put("/prompts/{prompt_id}", response_model=Prompt)
def update_prompt(prompt_id: str, prompt_data: PromptUpdate) -> Prompt:
    """Update an existing prompt's details.

    Args:
        prompt_id (str): The unique identifier of the prompt to update.
        prompt_data (PromptUpdate): The new data for updating the prompt.

    Returns:
        Prompt: The updated prompt object.

    Raises:
        HTTPException: 404 if the prompt is not found, 400 if collection is not found.
    """
    existing = _get_prompt_or_404(prompt_id)
    _validate_collection_exists(prompt_data.collection_id)

    updated_prompt = Prompt(
        id=existing.id,
        title=prompt_data.title,
        content=prompt_data.content,
        description=prompt_data.description,
        collection_id=prompt_data.collection_id,
        tags=prompt_data.tags,
        created_at=existing.created_at,
        updated_at=get_current_time(),
    )
    return storage.update_prompt(prompt_id, updated_prompt)


@app.patch("/prompts/{prompt_id}", response_model=Prompt)
def patch_prompt(prompt_id: str, prompt_data: Dict[str, Any]) -> Prompt:
    """Partially update a prompt with the provided fields.

    Args:
        prompt_id (str): The unique identifier of the prompt.
        prompt_data (Dict[str, Any]): The fields to update with new values.

    Returns:
        Prompt: The updated prompt object.

    Raises:
        HTTPException: 404 if the prompt is not found.
    """
    existing = _get_prompt_or_404(prompt_id)

    for key, value in prompt_data.items():
        if hasattr(existing, key) and value is not None:
            setattr(existing, key, value)

    existing.updated_at = get_current_time()
    return storage.update_prompt(prompt_id, existing)


@app.delete("/prompts/{prompt_id}", status_code=204)
def delete_prompt(prompt_id: str) -> None:
    """Delete a prompt by its ID.

    Args:
        prompt_id (str): The unique identifier of the prompt to delete.

    Raises:
        HTTPException: 404 if the prompt is not found.
    """
    if not storage.delete_prompt(prompt_id):
        raise HTTPException(status_code=404, detail="Prompt not found")


@app.put("/prompts/{prompt_id}/tags", response_model=Prompt)
def set_prompt_tags(prompt_id: str, tags: List[str]) -> Prompt:
    """Add or replace tags for a specific prompt.

    Args:
        prompt_id (str): The unique identifier of the prompt.
        tags (List[str]): The new list of tags.

    Returns:
        Prompt: The updated prompt with new tags.

    Raises:
        HTTPException: 404 if the prompt is not found.
    """
    existing = _get_prompt_or_404(prompt_id)
    existing.tags = tags
    existing.updated_at = get_current_time()
    return storage.update_prompt(prompt_id, existing)


# ============== Collection Endpoints ==============


@app.get("/collections", response_model=CollectionList)
def list_collections() -> CollectionList:
    """Retrieve a list of all collections.

    Returns:
        CollectionList: A list of collection objects and the total count.
    """
    collections = storage.get_all_collections()
    return CollectionList(collections=collections, total=len(collections))


@app.get("/collections/{collection_id}", response_model=Collection)
def get_collection(collection_id: str) -> Collection:
    """Get details of a specific collection by its ID.

    Args:
        collection_id (str): The unique identifier of the collection.

    Returns:
        Collection: The collection object if found.

    Raises:
        HTTPException: 404 if the collection is not found.
    """
    return _get_collection_or_404(collection_id)


@app.post("/collections", response_model=Collection, status_code=201)
def create_collection(collection_data: CollectionCreate) -> Collection:
    """Create a new collection with the given data.

    Args:
        collection_data (CollectionCreate): The data needed to create a new collection.

    Returns:
        Collection: The newly created collection object.
    """
    collection = Collection(**collection_data.model_dump())
    return storage.create_collection(collection)


@app.delete("/collections/{collection_id}", status_code=204)
def delete_collection(collection_id: str) -> None:
    """Delete a collection by its ID and orphan its associated prompts.

    Args:
        collection_id (str): The unique identifier of the collection to delete.

    Raises:
        HTTPException: 404 if the collection is not found.
    """
    if not storage.delete_collection(collection_id):
        raise HTTPException(status_code=404, detail="Collection not found")

    for prompt in storage.get_prompts_by_collection(collection_id):
        prompt.collection_id = None
        storage.update_prompt(prompt.id, prompt)
