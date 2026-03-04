"""TDD tests for the Tagging System feature.

Written FIRST as failing tests, then implementation follows.
Covers: model changes, storage, utility filtering, and API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from app.models import Prompt, PromptCreate
from app.storage import Storage
from app.utils import filter_prompts_by_tags


# ============== Model Tests ==============


class TestTaggingModel:
    """Test that the Prompt model supports tags."""

    def test_prompt_default_tags_empty_list(self):
        p = Prompt(title="T", content="C")
        assert p.tags == []

    def test_prompt_with_tags(self):
        p = Prompt(title="T", content="C", tags=["python", "ai"])
        assert p.tags == ["python", "ai"]

    def test_prompt_create_with_tags(self):
        p = PromptCreate(title="T", content="C", tags=["dev", "test"])
        assert p.tags == ["dev", "test"]

    def test_prompt_create_without_tags(self):
        p = PromptCreate(title="T", content="C")
        assert p.tags == []

    def test_prompt_tags_in_model_dump(self):
        p = Prompt(title="T", content="C", tags=["a"])
        data = p.model_dump()
        assert "tags" in data
        assert data["tags"] == ["a"]

    def test_prompt_tags_serialization_json(self):
        p = Prompt(title="T", content="C", tags=["x", "y"])
        json_str = p.model_dump_json()
        assert '"tags"' in json_str


# ============== Storage Tests ==============


class TestTaggingStorage:
    """Test storage operations with tagged prompts."""

    def test_create_prompt_with_tags(self):
        store = Storage()
        p = Prompt(title="T", content="C", tags=["python"])
        result = store.create_prompt(p)
        assert result.tags == ["python"]

    def test_get_prompt_preserves_tags(self):
        store = Storage()
        p = Prompt(title="T", content="C", tags=["ai", "ml"])
        store.create_prompt(p)
        fetched = store.get_prompt(p.id)
        assert fetched.tags == ["ai", "ml"]

    def test_update_prompt_tags(self):
        store = Storage()
        p = Prompt(title="T", content="C", tags=["old"])
        store.create_prompt(p)
        p.tags = ["new", "updated"]
        store.update_prompt(p.id, p)
        fetched = store.get_prompt(p.id)
        assert fetched.tags == ["new", "updated"]


# ============== Utility Filter Tests ==============


class TestFilterPromptsByTags:
    """Test the filter_prompts_by_tags utility function."""

    def _make_prompts(self):
        return [
            Prompt(title="A", content="C", tags=["python", "ai"]),
            Prompt(title="B", content="C", tags=["javascript", "web"]),
            Prompt(title="C", content="C", tags=["python", "web"]),
            Prompt(title="D", content="C", tags=[]),
        ]

    def test_filter_single_tag(self):
        prompts = self._make_prompts()
        result = filter_prompts_by_tags(prompts, ["python"])
        titles = [p.title for p in result]
        assert "A" in titles
        assert "C" in titles
        assert "B" not in titles
        assert "D" not in titles

    def test_filter_multiple_tags_intersection(self):
        """Multiple tags should return prompts that have ALL specified tags."""
        prompts = self._make_prompts()
        result = filter_prompts_by_tags(prompts, ["python", "ai"])
        assert len(result) == 1
        assert result[0].title == "A"

    def test_filter_no_match(self):
        prompts = self._make_prompts()
        result = filter_prompts_by_tags(prompts, ["rust"])
        assert result == []

    def test_filter_case_insensitive(self):
        prompts = self._make_prompts()
        result = filter_prompts_by_tags(prompts, ["PYTHON"])
        assert len(result) == 2

    def test_filter_empty_tag_list(self):
        prompts = self._make_prompts()
        result = filter_prompts_by_tags(prompts, [])
        assert len(result) == len(prompts)

    def test_filter_empty_prompts_list(self):
        result = filter_prompts_by_tags([], ["python"])
        assert result == []


# ============== API Endpoint Tests: Create/Update with Tags ==============


class TestTaggingAPICreateUpdate:
    """Test creating and updating prompts with tags via the API."""

    def test_create_prompt_with_tags(self, client: TestClient):
        response = client.post(
            "/prompts",
            json={"title": "T", "content": "C", "tags": ["python", "ai"]},
        )
        assert response.status_code == 201
        assert response.json()["tags"] == ["python", "ai"]

    def test_create_prompt_without_tags_defaults_empty(self, client: TestClient):
        response = client.post("/prompts", json={"title": "T", "content": "C"})
        assert response.status_code == 201
        assert response.json()["tags"] == []

    def test_put_update_preserves_tags_field(self, client: TestClient):
        created = client.post(
            "/prompts",
            json={"title": "T", "content": "C", "tags": ["old"]},
        ).json()
        response = client.put(
            f"/prompts/{created['id']}",
            json={"title": "T2", "content": "C2", "tags": ["new"]},
        )
        assert response.status_code == 200
        assert response.json()["tags"] == ["new"]

    def test_patch_prompt_tags(self, client: TestClient):
        created = client.post(
            "/prompts",
            json={"title": "T", "content": "C", "tags": ["a"]},
        ).json()
        response = client.patch(
            f"/prompts/{created['id']}",
            json={"tags": ["b", "c"]},
        )
        assert response.status_code == 200
        assert response.json()["tags"] == ["b", "c"]


# ============== API Endpoint Tests: PUT /prompts/{id}/tags ==============


class TestTagsEndpoint:
    """Test the dedicated PUT /prompts/{id}/tags endpoint."""

    def test_set_tags(self, client: TestClient, sample_prompt_data):
        created = client.post("/prompts", json=sample_prompt_data).json()
        response = client.put(
            f"/prompts/{created['id']}/tags",
            json=["python", "ai"],
        )
        assert response.status_code == 200
        assert response.json()["tags"] == ["python", "ai"]

    def test_set_tags_replaces_existing(self, client: TestClient, sample_prompt_data):
        created = client.post("/prompts", json={**sample_prompt_data, "tags": ["old"]}).json()
        response = client.put(
            f"/prompts/{created['id']}/tags",
            json=["new"],
        )
        assert response.json()["tags"] == ["new"]

    def test_set_tags_empty_list_clears(self, client: TestClient, sample_prompt_data):
        created = client.post("/prompts", json={**sample_prompt_data, "tags": ["x"]}).json()
        response = client.put(
            f"/prompts/{created['id']}/tags",
            json=[],
        )
        assert response.json()["tags"] == []

    def test_set_tags_nonexistent_prompt_404(self, client: TestClient):
        response = client.put("/prompts/nonexistent/tags", json=["a"])
        assert response.status_code == 404

    def test_set_tags_persists(self, client: TestClient, sample_prompt_data):
        created = client.post("/prompts", json=sample_prompt_data).json()
        client.put(f"/prompts/{created['id']}/tags", json=["persisted"])
        fetched = client.get(f"/prompts/{created['id']}").json()
        assert fetched["tags"] == ["persisted"]


# ============== API Endpoint Tests: GET /prompts?tags= ==============


class TestTagsFiltering:
    """Test filtering prompts by tags via query parameter."""

    def _seed(self, client):
        client.post("/prompts", json={"title": "P1", "content": "C", "tags": ["python", "ai"]})
        client.post("/prompts", json={"title": "P2", "content": "C", "tags": ["javascript", "web"]})
        client.post("/prompts", json={"title": "P3", "content": "C", "tags": ["python", "web"]})
        client.post("/prompts", json={"title": "P4", "content": "C", "tags": []})

    def test_filter_single_tag(self, client: TestClient):
        self._seed(client)
        data = client.get("/prompts?tags=python").json()
        titles = [p["title"] for p in data["prompts"]]
        assert "P1" in titles
        assert "P3" in titles
        assert data["total"] == 2

    def test_filter_multiple_tags(self, client: TestClient):
        self._seed(client)
        data = client.get("/prompts?tags=python,ai").json()
        assert data["total"] == 1
        assert data["prompts"][0]["title"] == "P1"

    def test_filter_no_match(self, client: TestClient):
        self._seed(client)
        data = client.get("/prompts?tags=rust").json()
        assert data["total"] == 0

    def test_filter_case_insensitive(self, client: TestClient):
        self._seed(client)
        data = client.get("/prompts?tags=PYTHON").json()
        assert data["total"] == 2

    def test_no_tags_param_returns_all(self, client: TestClient):
        self._seed(client)
        data = client.get("/prompts").json()
        assert data["total"] == 4

    def test_tags_combined_with_search(self, client: TestClient):
        self._seed(client)
        data = client.get("/prompts?tags=python&search=P1").json()
        assert data["total"] == 1
        assert data["prompts"][0]["title"] == "P1"

    def test_tags_combined_with_collection(self, client: TestClient, sample_collection_data):
        col = client.post("/collections", json=sample_collection_data).json()
        client.post("/prompts", json={"title": "InCol", "content": "C", "tags": ["python"], "collection_id": col["id"]})
        client.post("/prompts", json={"title": "NoCol", "content": "C", "tags": ["python"]})
        data = client.get(f"/prompts?tags=python&collection_id={col['id']}").json()
        assert data["total"] == 1
        assert data["prompts"][0]["title"] == "InCol"
