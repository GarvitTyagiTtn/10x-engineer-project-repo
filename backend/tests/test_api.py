"""Comprehensive API tests for PromptLab.

Covers all endpoints: happy paths, error cases, edge cases, and query parameters.
"""

import pytest
from fastapi.testclient import TestClient


class TestHealthEndpoint:
    """Tests for the /health endpoint."""

    def test_health_check_returns_200(self, client: TestClient):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_check_status_healthy(self, client: TestClient):
        response = client.get("/health")
        assert response.json()["status"] == "healthy"

    def test_health_check_includes_version(self, client: TestClient):
        response = client.get("/health")
        data = response.json()
        assert "version" in data
        assert isinstance(data["version"], str)
        assert len(data["version"]) > 0


class TestPromptEndpointsHappyPath:
    """Happy-path tests for all prompt endpoints."""

    def test_create_prompt(self, client: TestClient, sample_prompt_data):
        response = client.post("/prompts", json=sample_prompt_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == sample_prompt_data["title"]
        assert data["content"] == sample_prompt_data["content"]
        assert data["description"] == sample_prompt_data["description"]
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_prompt_minimal(self, client: TestClient):
        """Create prompt with only required fields."""
        response = client.post("/prompts", json={"title": "T", "content": "C"})
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "T"
        assert data["description"] is None
        assert data["collection_id"] is None

    def test_create_prompt_with_collection(self, client: TestClient, sample_prompt_data, sample_collection_data):
        col = client.post("/collections", json=sample_collection_data).json()
        prompt_data = {**sample_prompt_data, "collection_id": col["id"]}
        response = client.post("/prompts", json=prompt_data)
        assert response.status_code == 201
        assert response.json()["collection_id"] == col["id"]

    def test_list_prompts_empty(self, client: TestClient):
        response = client.get("/prompts")
        assert response.status_code == 200
        data = response.json()
        assert data["prompts"] == []
        assert data["total"] == 0

    def test_list_prompts_with_data(self, client: TestClient, sample_prompt_data):
        client.post("/prompts", json=sample_prompt_data)
        response = client.get("/prompts")
        assert response.status_code == 200
        data = response.json()
        assert len(data["prompts"]) == 1
        assert data["total"] == 1

    def test_list_prompts_multiple(self, client: TestClient):
        for i in range(3):
            client.post("/prompts", json={"title": f"Prompt {i}", "content": f"Content {i}"})
        data = client.get("/prompts").json()
        assert data["total"] == 3
        assert len(data["prompts"]) == 3

    def test_get_prompt(self, client: TestClient, sample_prompt_data):
        created = client.post("/prompts", json=sample_prompt_data).json()
        response = client.get(f"/prompts/{created['id']}")
        assert response.status_code == 200
        assert response.json()["id"] == created["id"]
        assert response.json()["title"] == sample_prompt_data["title"]

    def test_update_prompt_put(self, client: TestClient, sample_prompt_data):
        created = client.post("/prompts", json=sample_prompt_data).json()
        updated_data = {"title": "New Title", "content": "New content here", "description": "New desc"}
        response = client.put(f"/prompts/{created['id']}", json=updated_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "New Title"
        assert data["content"] == "New content here"
        assert data["description"] == "New desc"
        assert data["id"] == created["id"]

    def test_update_prompt_preserves_id_and_created_at(self, client: TestClient, sample_prompt_data):
        created = client.post("/prompts", json=sample_prompt_data).json()
        updated_data = {"title": "Changed", "content": "Changed content"}
        response = client.put(f"/prompts/{created['id']}", json=updated_data)
        data = response.json()
        assert data["id"] == created["id"]
        assert data["created_at"] == created["created_at"]

    def test_patch_prompt(self, client: TestClient, sample_prompt_data):
        created = client.post("/prompts", json=sample_prompt_data).json()
        response = client.patch(f"/prompts/{created['id']}", json={"title": "Patched"})
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Patched"
        assert data["content"] == sample_prompt_data["content"]
        assert data["description"] == sample_prompt_data["description"]

    def test_patch_prompt_multiple_fields(self, client: TestClient, sample_prompt_data):
        created = client.post("/prompts", json=sample_prompt_data).json()
        response = client.patch(
            f"/prompts/{created['id']}",
            json={"title": "New", "description": "New desc"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "New"
        assert data["description"] == "New desc"
        assert data["content"] == sample_prompt_data["content"]

    def test_patch_prompt_persists(self, client: TestClient, sample_prompt_data):
        created = client.post("/prompts", json=sample_prompt_data).json()
        client.patch(f"/prompts/{created['id']}", json={"title": "Persisted"})
        fetched = client.get(f"/prompts/{created['id']}").json()
        assert fetched["title"] == "Persisted"

    def test_delete_prompt(self, client: TestClient, sample_prompt_data):
        created = client.post("/prompts", json=sample_prompt_data).json()
        response = client.delete(f"/prompts/{created['id']}")
        assert response.status_code == 204

    def test_delete_prompt_removes_from_list(self, client: TestClient, sample_prompt_data):
        created = client.post("/prompts", json=sample_prompt_data).json()
        client.delete(f"/prompts/{created['id']}")
        data = client.get("/prompts").json()
        assert data["total"] == 0


class TestPromptEndpointsErrors:
    """Error-case tests for prompt endpoints (404, 400, etc.)."""

    def test_get_nonexistent_prompt_404(self, client: TestClient):
        response = client.get("/prompts/nonexistent-id")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_update_nonexistent_prompt_404(self, client: TestClient):
        response = client.put(
            "/prompts/nonexistent-id",
            json={"title": "X", "content": "Y"},
        )
        assert response.status_code == 404

    def test_patch_nonexistent_prompt_404(self, client: TestClient):
        response = client.patch("/prompts/nonexistent-id", json={"title": "X"})
        assert response.status_code == 404

    def test_delete_nonexistent_prompt_404(self, client: TestClient):
        response = client.delete("/prompts/nonexistent-id")
        assert response.status_code == 404

    def test_create_prompt_missing_title(self, client: TestClient):
        response = client.post("/prompts", json={"content": "Some content"})
        assert response.status_code == 422

    def test_create_prompt_missing_content(self, client: TestClient):
        response = client.post("/prompts", json={"title": "A title"})
        assert response.status_code == 422

    def test_create_prompt_empty_body(self, client: TestClient):
        response = client.post("/prompts", json={})
        assert response.status_code == 422

    def test_create_prompt_invalid_collection_id(self, client: TestClient):
        response = client.post(
            "/prompts",
            json={"title": "T", "content": "C", "collection_id": "bad-id"},
        )
        assert response.status_code == 400
        assert "collection not found" in response.json()["detail"].lower()

    def test_update_prompt_invalid_collection_id(self, client: TestClient, sample_prompt_data):
        created = client.post("/prompts", json=sample_prompt_data).json()
        response = client.put(
            f"/prompts/{created['id']}",
            json={"title": "T", "content": "C", "collection_id": "bad-id"},
        )
        assert response.status_code == 400

    def test_delete_already_deleted_prompt(self, client: TestClient, sample_prompt_data):
        created = client.post("/prompts", json=sample_prompt_data).json()
        client.delete(f"/prompts/{created['id']}")
        response = client.delete(f"/prompts/{created['id']}")
        assert response.status_code == 404


class TestPromptEndpointsEdgeCases:
    """Edge-case tests: empty strings, special characters, boundary values."""

    def test_create_prompt_title_max_length(self, client: TestClient):
        title = "A" * 200
        response = client.post("/prompts", json={"title": title, "content": "C"})
        assert response.status_code == 201
        assert response.json()["title"] == title

    def test_create_prompt_title_exceeds_max_length(self, client: TestClient):
        title = "A" * 201
        response = client.post("/prompts", json={"title": title, "content": "C"})
        assert response.status_code == 422

    def test_create_prompt_description_max_length(self, client: TestClient):
        desc = "D" * 500
        response = client.post("/prompts", json={"title": "T", "content": "C", "description": desc})
        assert response.status_code == 201

    def test_create_prompt_description_exceeds_max_length(self, client: TestClient):
        desc = "D" * 501
        response = client.post("/prompts", json={"title": "T", "content": "C", "description": desc})
        assert response.status_code == 422

    def test_create_prompt_special_characters_in_title(self, client: TestClient):
        title = "Prompt <script>alert('xss')</script> & \"quotes\" 'single'"
        response = client.post("/prompts", json={"title": title, "content": "C"})
        assert response.status_code == 201
        assert response.json()["title"] == title

    def test_create_prompt_unicode_content(self, client: TestClient):
        response = client.post(
            "/prompts",
            json={"title": "日本語テスト", "content": "こんにちは世界 🌍"},
        )
        assert response.status_code == 201
        assert response.json()["title"] == "日本語テスト"

    def test_create_prompt_multiline_content(self, client: TestClient):
        content = "Line 1\nLine 2\nLine 3\n\n{{variable}}"
        response = client.post("/prompts", json={"title": "Multi", "content": content})
        assert response.status_code == 201
        assert response.json()["content"] == content

    def test_create_prompt_empty_string_title(self, client: TestClient):
        response = client.post("/prompts", json={"title": "", "content": "C"})
        assert response.status_code == 422

    def test_patch_with_empty_dict(self, client: TestClient, sample_prompt_data):
        created = client.post("/prompts", json=sample_prompt_data).json()
        response = client.patch(f"/prompts/{created['id']}", json={})
        assert response.status_code == 200
        assert response.json()["title"] == sample_prompt_data["title"]

    def test_patch_ignores_none_values(self, client: TestClient, sample_prompt_data):
        created = client.post("/prompts", json=sample_prompt_data).json()
        response = client.patch(f"/prompts/{created['id']}", json={"title": None})
        assert response.status_code == 200
        assert response.json()["title"] == sample_prompt_data["title"]

    def test_patch_ignores_unknown_fields(self, client: TestClient, sample_prompt_data):
        created = client.post("/prompts", json=sample_prompt_data).json()
        response = client.patch(f"/prompts/{created['id']}", json={"nonexistent_field": "value"})
        assert response.status_code == 200


class TestPromptQueryParameters:
    """Tests for sorting, filtering, and search query parameters."""

    def test_prompts_sorted_newest_first(self, client: TestClient):
        import time
        client.post("/prompts", json={"title": "First", "content": "Content A"})
        time.sleep(0.05)
        client.post("/prompts", json={"title": "Second", "content": "Content B"})
        prompts = client.get("/prompts").json()["prompts"]
        assert prompts[0]["title"] == "Second"
        assert prompts[1]["title"] == "First"

    def test_filter_by_collection_id(self, client: TestClient, sample_collection_data):
        col = client.post("/collections", json=sample_collection_data).json()
        client.post("/prompts", json={"title": "In col", "content": "C", "collection_id": col["id"]})
        client.post("/prompts", json={"title": "No col", "content": "C"})
        prompts = client.get(f"/prompts?collection_id={col['id']}").json()
        assert prompts["total"] == 1
        assert prompts["prompts"][0]["title"] == "In col"

    def test_filter_by_nonexistent_collection(self, client: TestClient, sample_prompt_data):
        client.post("/prompts", json=sample_prompt_data)
        prompts = client.get("/prompts?collection_id=nonexistent").json()
        assert prompts["total"] == 0

    def test_search_by_title(self, client: TestClient):
        client.post("/prompts", json={"title": "Python Guide", "content": "C"})
        client.post("/prompts", json={"title": "Java Guide", "content": "C"})
        prompts = client.get("/prompts?search=Python").json()
        assert prompts["total"] == 1
        assert prompts["prompts"][0]["title"] == "Python Guide"

    def test_search_case_insensitive(self, client: TestClient):
        client.post("/prompts", json={"title": "Python Guide", "content": "C"})
        prompts = client.get("/prompts?search=python").json()
        assert prompts["total"] == 1

    def test_search_by_description(self, client: TestClient):
        client.post(
            "/prompts",
            json={"title": "Prompt", "content": "C", "description": "machine learning tips"},
        )
        prompts = client.get("/prompts?search=machine").json()
        assert prompts["total"] == 1

    def test_search_no_results(self, client: TestClient, sample_prompt_data):
        client.post("/prompts", json=sample_prompt_data)
        prompts = client.get("/prompts?search=zzzznotfound").json()
        assert prompts["total"] == 0

    def test_search_and_filter_combined(self, client: TestClient, sample_collection_data):
        col = client.post("/collections", json=sample_collection_data).json()
        client.post("/prompts", json={"title": "Alpha", "content": "C", "collection_id": col["id"]})
        client.post("/prompts", json={"title": "Alpha Other", "content": "C"})
        prompts = client.get(f"/prompts?collection_id={col['id']}&search=Alpha").json()
        assert prompts["total"] == 1
        assert prompts["prompts"][0]["collection_id"] == col["id"]


class TestCollectionEndpointsHappyPath:
    """Happy-path tests for collection endpoints."""

    def test_create_collection(self, client: TestClient, sample_collection_data):
        response = client.post("/collections", json=sample_collection_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_collection_data["name"]
        assert data["description"] == sample_collection_data["description"]
        assert "id" in data
        assert "created_at" in data

    def test_create_collection_minimal(self, client: TestClient):
        response = client.post("/collections", json={"name": "X"})
        assert response.status_code == 201
        assert response.json()["description"] is None

    def test_list_collections_empty(self, client: TestClient):
        data = client.get("/collections").json()
        assert data["collections"] == []
        assert data["total"] == 0

    def test_list_collections(self, client: TestClient, sample_collection_data):
        client.post("/collections", json=sample_collection_data)
        data = client.get("/collections").json()
        assert len(data["collections"]) == 1
        assert data["total"] == 1

    def test_get_collection(self, client: TestClient, sample_collection_data):
        created = client.post("/collections", json=sample_collection_data).json()
        response = client.get(f"/collections/{created['id']}")
        assert response.status_code == 200
        assert response.json()["id"] == created["id"]

    def test_delete_collection(self, client: TestClient, sample_collection_data):
        created = client.post("/collections", json=sample_collection_data).json()
        response = client.delete(f"/collections/{created['id']}")
        assert response.status_code == 204

    def test_delete_collection_removes_from_list(self, client: TestClient, sample_collection_data):
        created = client.post("/collections", json=sample_collection_data).json()
        client.delete(f"/collections/{created['id']}")
        data = client.get("/collections").json()
        assert data["total"] == 0


class TestCollectionEndpointsErrors:
    """Error-case tests for collection endpoints."""

    def test_get_nonexistent_collection_404(self, client: TestClient):
        response = client.get("/collections/nonexistent-id")
        assert response.status_code == 404

    def test_delete_nonexistent_collection_404(self, client: TestClient):
        response = client.delete("/collections/nonexistent-id")
        assert response.status_code == 404

    def test_create_collection_missing_name(self, client: TestClient):
        response = client.post("/collections", json={})
        assert response.status_code == 422

    def test_create_collection_empty_name(self, client: TestClient):
        response = client.post("/collections", json={"name": ""})
        assert response.status_code == 422

    def test_create_collection_name_exceeds_max(self, client: TestClient):
        response = client.post("/collections", json={"name": "N" * 101})
        assert response.status_code == 422

    def test_create_collection_description_exceeds_max(self, client: TestClient):
        response = client.post("/collections", json={"name": "N", "description": "D" * 501})
        assert response.status_code == 422


class TestCollectionDeletionOrphansPrompts:
    """Tests that deleting a collection properly orphans its prompts."""

    def test_delete_collection_sets_prompt_collection_id_to_none(
        self, client: TestClient, sample_collection_data, sample_prompt_data
    ):
        col = client.post("/collections", json=sample_collection_data).json()
        prompt_data = {**sample_prompt_data, "collection_id": col["id"]}
        prompt = client.post("/prompts", json=prompt_data).json()
        client.delete(f"/collections/{col['id']}")
        fetched = client.get(f"/prompts/{prompt['id']}").json()
        assert fetched["collection_id"] is None

    def test_delete_collection_prompt_still_exists(
        self, client: TestClient, sample_collection_data, sample_prompt_data
    ):
        col = client.post("/collections", json=sample_collection_data).json()
        prompt_data = {**sample_prompt_data, "collection_id": col["id"]}
        prompt = client.post("/prompts", json=prompt_data).json()
        client.delete(f"/collections/{col['id']}")
        response = client.get(f"/prompts/{prompt['id']}")
        assert response.status_code == 200
