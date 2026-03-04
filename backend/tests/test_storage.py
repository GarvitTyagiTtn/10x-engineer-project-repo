"""Storage layer tests for PromptLab.

Covers CRUD operations, data persistence within session, and edge cases.
"""

import pytest
from app.storage import Storage
from app.models import Prompt, Collection


@pytest.fixture
def store():
    """Return a fresh Storage instance for each test."""
    return Storage()


@pytest.fixture
def make_prompt():
    """Factory fixture to create Prompt instances."""
    def _make(title="Test Prompt", content="Test content", collection_id=None):
        return Prompt(title=title, content=content, collection_id=collection_id)
    return _make


@pytest.fixture
def make_collection():
    """Factory fixture to create Collection instances."""
    def _make(name="Test Collection", description=None):
        return Collection(name=name, description=description)
    return _make


# ============== Prompt CRUD ==============


class TestPromptCRUD:
    """Test basic CRUD operations for prompts."""

    def test_create_prompt(self, store, make_prompt):
        prompt = make_prompt()
        result = store.create_prompt(prompt)
        assert result.id == prompt.id
        assert result.title == "Test Prompt"

    def test_get_prompt(self, store, make_prompt):
        prompt = make_prompt()
        store.create_prompt(prompt)
        fetched = store.get_prompt(prompt.id)
        assert fetched is not None
        assert fetched.id == prompt.id
        assert fetched.title == prompt.title

    def test_get_prompt_not_found(self, store):
        assert store.get_prompt("nonexistent") is None

    def test_get_all_prompts_empty(self, store):
        assert store.get_all_prompts() == []

    def test_get_all_prompts(self, store, make_prompt):
        store.create_prompt(make_prompt(title="A"))
        store.create_prompt(make_prompt(title="B"))
        prompts = store.get_all_prompts()
        assert len(prompts) == 2

    def test_update_prompt(self, store, make_prompt):
        prompt = make_prompt()
        store.create_prompt(prompt)
        updated = Prompt(
            id=prompt.id,
            title="Updated",
            content="Updated content",
            created_at=prompt.created_at,
        )
        result = store.update_prompt(prompt.id, updated)
        assert result is not None
        assert result.title == "Updated"

    def test_update_prompt_not_found(self, store, make_prompt):
        prompt = make_prompt()
        result = store.update_prompt("nonexistent", prompt)
        assert result is None

    def test_delete_prompt(self, store, make_prompt):
        prompt = make_prompt()
        store.create_prompt(prompt)
        assert store.delete_prompt(prompt.id) is True
        assert store.get_prompt(prompt.id) is None

    def test_delete_prompt_not_found(self, store):
        assert store.delete_prompt("nonexistent") is False


# ============== Collection CRUD ==============


class TestCollectionCRUD:
    """Test basic CRUD operations for collections."""

    def test_create_collection(self, store, make_collection):
        col = make_collection()
        result = store.create_collection(col)
        assert result.id == col.id
        assert result.name == "Test Collection"

    def test_get_collection(self, store, make_collection):
        col = make_collection()
        store.create_collection(col)
        fetched = store.get_collection(col.id)
        assert fetched is not None
        assert fetched.id == col.id

    def test_get_collection_not_found(self, store):
        assert store.get_collection("nonexistent") is None

    def test_get_all_collections_empty(self, store):
        assert store.get_all_collections() == []

    def test_get_all_collections(self, store, make_collection):
        store.create_collection(make_collection(name="A"))
        store.create_collection(make_collection(name="B"))
        assert len(store.get_all_collections()) == 2

    def test_delete_collection(self, store, make_collection):
        col = make_collection()
        store.create_collection(col)
        assert store.delete_collection(col.id) is True
        assert store.get_collection(col.id) is None

    def test_delete_collection_not_found(self, store):
        assert store.delete_collection("nonexistent") is False


# ============== Data Persistence Within Session ==============


class TestDataPersistence:
    """Test that data persists correctly within a storage session."""

    def test_prompt_persists_after_creation(self, store, make_prompt):
        prompt = make_prompt()
        store.create_prompt(prompt)
        assert store.get_prompt(prompt.id) is not None

    def test_updated_prompt_reflects_changes(self, store, make_prompt):
        prompt = make_prompt(title="Original")
        store.create_prompt(prompt)
        updated = Prompt(id=prompt.id, title="Changed", content="C", created_at=prompt.created_at)
        store.update_prompt(prompt.id, updated)
        fetched = store.get_prompt(prompt.id)
        assert fetched.title == "Changed"

    def test_deleted_prompt_no_longer_in_list(self, store, make_prompt):
        prompt = make_prompt()
        store.create_prompt(prompt)
        store.delete_prompt(prompt.id)
        assert prompt.id not in [p.id for p in store.get_all_prompts()]

    def test_multiple_prompts_independent(self, store, make_prompt):
        p1 = make_prompt(title="One")
        p2 = make_prompt(title="Two")
        store.create_prompt(p1)
        store.create_prompt(p2)
        store.delete_prompt(p1.id)
        assert store.get_prompt(p2.id) is not None
        assert store.get_prompt(p1.id) is None

    def test_collection_persists_after_creation(self, store, make_collection):
        col = make_collection()
        store.create_collection(col)
        assert store.get_collection(col.id) is not None

    def test_clear_removes_all_data(self, store, make_prompt, make_collection):
        store.create_prompt(make_prompt())
        store.create_collection(make_collection())
        store.clear()
        assert store.get_all_prompts() == []
        assert store.get_all_collections() == []


# ============== Edge Cases ==============


class TestStorageEdgeCases:
    """Edge-case tests for the storage layer."""

    def test_get_prompts_by_collection(self, store, make_prompt, make_collection):
        col = make_collection()
        store.create_collection(col)
        p1 = make_prompt(title="In col", collection_id=col.id)
        p2 = make_prompt(title="No col")
        store.create_prompt(p1)
        store.create_prompt(p2)
        results = store.get_prompts_by_collection(col.id)
        assert len(results) == 1
        assert results[0].title == "In col"

    def test_get_prompts_by_collection_empty(self, store):
        assert store.get_prompts_by_collection("nonexistent") == []

    def test_overwrite_prompt_with_same_id(self, store, make_prompt):
        prompt = make_prompt(title="Original")
        store.create_prompt(prompt)
        replacement = Prompt(id=prompt.id, title="Replaced", content="New", created_at=prompt.created_at)
        store.update_prompt(prompt.id, replacement)
        assert store.get_prompt(prompt.id).title == "Replaced"

    def test_create_prompt_with_special_characters(self, store):
        prompt = Prompt(title="<script>alert('xss')</script>", content="Content & \"quotes\"")
        store.create_prompt(prompt)
        fetched = store.get_prompt(prompt.id)
        assert fetched.title == "<script>alert('xss')</script>"

    def test_create_prompt_with_unicode(self, store):
        prompt = Prompt(title="日本語", content="こんにちは 🌍")
        store.create_prompt(prompt)
        fetched = store.get_prompt(prompt.id)
        assert fetched.title == "日本語"

    def test_delete_prompt_twice(self, store, make_prompt):
        prompt = make_prompt()
        store.create_prompt(prompt)
        assert store.delete_prompt(prompt.id) is True
        assert store.delete_prompt(prompt.id) is False

    def test_update_after_delete_returns_none(self, store, make_prompt):
        prompt = make_prompt()
        store.create_prompt(prompt)
        store.delete_prompt(prompt.id)
        result = store.update_prompt(prompt.id, prompt)
        assert result is None

    def test_clear_then_add(self, store, make_prompt):
        store.create_prompt(make_prompt(title="Before"))
        store.clear()
        store.create_prompt(make_prompt(title="After"))
        prompts = store.get_all_prompts()
        assert len(prompts) == 1
        assert prompts[0].title == "After"
