"""Model tests for PromptLab.

Covers model validation, default values, and serialization.
"""

import pytest
from datetime import datetime
from pydantic import ValidationError
from app.models import (
    Prompt,
    PromptCreate,
    PromptUpdate,
    PromptBase,
    Collection,
    CollectionCreate,
    CollectionBase,
    PromptList,
    CollectionList,
    HealthResponse,
    generate_id,
    get_current_time,
)


# ============== Helper Functions ==============


class TestHelperFunctions:
    """Tests for generate_id and get_current_time."""

    def test_generate_id_returns_string(self):
        assert isinstance(generate_id(), str)

    def test_generate_id_unique(self):
        ids = {generate_id() for _ in range(100)}
        assert len(ids) == 100

    def test_get_current_time_returns_datetime(self):
        assert isinstance(get_current_time(), datetime)

    def test_get_current_time_is_recent(self):
        now = get_current_time()
        assert (datetime.utcnow() - now).total_seconds() < 2


# ============== Prompt Model Validation ==============


class TestPromptValidation:
    """Tests for Prompt and PromptCreate validation rules."""

    def test_create_prompt_valid(self):
        p = PromptCreate(title="Valid", content="Valid content")
        assert p.title == "Valid"

    def test_create_prompt_all_fields(self):
        p = PromptCreate(
            title="Title",
            content="Content",
            description="Desc",
            collection_id="col-1",
        )
        assert p.description == "Desc"
        assert p.collection_id == "col-1"

    def test_create_prompt_missing_title(self):
        with pytest.raises(ValidationError):
            PromptCreate(content="Content")

    def test_create_prompt_missing_content(self):
        with pytest.raises(ValidationError):
            PromptCreate(title="Title")

    def test_create_prompt_empty_title(self):
        with pytest.raises(ValidationError):
            PromptCreate(title="", content="Content")

    def test_create_prompt_empty_content(self):
        with pytest.raises(ValidationError):
            PromptCreate(title="Title", content="")

    def test_create_prompt_title_max_length(self):
        p = PromptCreate(title="A" * 200, content="C")
        assert len(p.title) == 200

    def test_create_prompt_title_exceeds_max(self):
        with pytest.raises(ValidationError):
            PromptCreate(title="A" * 201, content="C")

    def test_create_prompt_description_max_length(self):
        p = PromptCreate(title="T", content="C", description="D" * 500)
        assert len(p.description) == 500

    def test_create_prompt_description_exceeds_max(self):
        with pytest.raises(ValidationError):
            PromptCreate(title="T", content="C", description="D" * 501)

    def test_prompt_update_same_validation_as_create(self):
        with pytest.raises(ValidationError):
            PromptUpdate(title="", content="C")


# ============== Prompt Default Values ==============


class TestPromptDefaults:
    """Tests for Prompt model default values."""

    def test_prompt_has_default_id(self):
        p = Prompt(title="T", content="C")
        assert p.id is not None
        assert isinstance(p.id, str)
        assert len(p.id) > 0

    def test_prompt_has_default_created_at(self):
        p = Prompt(title="T", content="C")
        assert isinstance(p.created_at, datetime)

    def test_prompt_has_default_updated_at(self):
        p = Prompt(title="T", content="C")
        assert isinstance(p.updated_at, datetime)

    def test_prompt_description_defaults_to_none(self):
        p = Prompt(title="T", content="C")
        assert p.description is None

    def test_prompt_collection_id_defaults_to_none(self):
        p = Prompt(title="T", content="C")
        assert p.collection_id is None

    def test_prompt_ids_are_unique(self):
        p1 = Prompt(title="T", content="C")
        p2 = Prompt(title="T", content="C")
        assert p1.id != p2.id

    def test_prompt_custom_id(self):
        p = Prompt(id="custom-id", title="T", content="C")
        assert p.id == "custom-id"


# ============== Prompt Serialization ==============


class TestPromptSerialization:
    """Tests for Prompt model serialization (model_dump / JSON)."""

    def test_model_dump(self):
        p = Prompt(title="T", content="C")
        data = p.model_dump()
        assert "id" in data
        assert "title" in data
        assert "content" in data
        assert "description" in data
        assert "collection_id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_model_dump_values(self):
        p = Prompt(title="My Title", content="My Content", description="Desc")
        data = p.model_dump()
        assert data["title"] == "My Title"
        assert data["content"] == "My Content"
        assert data["description"] == "Desc"

    def test_json_serialization(self):
        p = Prompt(title="T", content="C")
        json_str = p.model_dump_json()
        assert isinstance(json_str, str)
        assert "T" in json_str

    def test_prompt_create_model_dump(self):
        p = PromptCreate(title="T", content="C")
        data = p.model_dump()
        assert "title" in data
        assert "content" in data
        assert "id" not in data

    def test_from_attributes_config(self):
        """Prompt model has from_attributes=True in Config."""
        assert Prompt.model_config.get("from_attributes") is True


# ============== Collection Model Validation ==============


class TestCollectionValidation:
    """Tests for Collection and CollectionCreate validation."""

    def test_create_collection_valid(self):
        c = CollectionCreate(name="Valid")
        assert c.name == "Valid"

    def test_create_collection_with_description(self):
        c = CollectionCreate(name="N", description="D")
        assert c.description == "D"

    def test_create_collection_missing_name(self):
        with pytest.raises(ValidationError):
            CollectionCreate()

    def test_create_collection_empty_name(self):
        with pytest.raises(ValidationError):
            CollectionCreate(name="")

    def test_create_collection_name_max_length(self):
        c = CollectionCreate(name="N" * 100)
        assert len(c.name) == 100

    def test_create_collection_name_exceeds_max(self):
        with pytest.raises(ValidationError):
            CollectionCreate(name="N" * 101)

    def test_create_collection_description_exceeds_max(self):
        with pytest.raises(ValidationError):
            CollectionCreate(name="N", description="D" * 501)


# ============== Collection Default Values ==============


class TestCollectionDefaults:
    """Tests for Collection model default values."""

    def test_collection_has_default_id(self):
        c = Collection(name="N")
        assert c.id is not None
        assert isinstance(c.id, str)

    def test_collection_has_default_created_at(self):
        c = Collection(name="N")
        assert isinstance(c.created_at, datetime)

    def test_collection_description_defaults_to_none(self):
        c = Collection(name="N")
        assert c.description is None

    def test_collection_ids_are_unique(self):
        c1 = Collection(name="A")
        c2 = Collection(name="B")
        assert c1.id != c2.id


# ============== Collection Serialization ==============


class TestCollectionSerialization:
    """Tests for Collection model serialization."""

    def test_model_dump(self):
        c = Collection(name="N", description="D")
        data = c.model_dump()
        assert data["name"] == "N"
        assert data["description"] == "D"
        assert "id" in data
        assert "created_at" in data

    def test_json_serialization(self):
        c = Collection(name="N")
        json_str = c.model_dump_json()
        assert isinstance(json_str, str)
        assert "N" in json_str

    def test_collection_create_model_dump(self):
        c = CollectionCreate(name="N")
        data = c.model_dump()
        assert "name" in data
        assert "id" not in data

    def test_from_attributes_config(self):
        assert Collection.model_config.get("from_attributes") is True


# ============== Response Models ==============


class TestResponseModels:
    """Tests for PromptList, CollectionList, and HealthResponse."""

    def test_prompt_list(self):
        p = Prompt(title="T", content="C")
        pl = PromptList(prompts=[p], total=1)
        assert pl.total == 1
        assert len(pl.prompts) == 1

    def test_prompt_list_empty(self):
        pl = PromptList(prompts=[], total=0)
        assert pl.total == 0
        assert pl.prompts == []

    def test_collection_list(self):
        c = Collection(name="N")
        cl = CollectionList(collections=[c], total=1)
        assert cl.total == 1

    def test_collection_list_empty(self):
        cl = CollectionList(collections=[], total=0)
        assert cl.total == 0

    def test_health_response(self):
        hr = HealthResponse(status="healthy", version="1.0.0")
        assert hr.status == "healthy"
        assert hr.version == "1.0.0"

    def test_health_response_serialization(self):
        hr = HealthResponse(status="healthy", version="1.0.0")
        data = hr.model_dump()
        assert data == {"status": "healthy", "version": "1.0.0"}
