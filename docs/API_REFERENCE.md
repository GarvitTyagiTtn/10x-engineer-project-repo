# PromptLab API Reference

This document provides detailed information on the API endpoints available in PromptLab, including request and response formats, error handling, and authentication notes.

## General Information

- **Base URL**: `http://localhost:8000`
- **Content-Type**: `application/json`
- **Authentication**: None required currently.

---

## Endpoints

### Health Check

#### `GET /health`

**Description**: Check the health and version of the API service.

- **Response 200**: 
  ```json
  {
    "status": "healthy",
    "version": "1.0.0"
  }
  ```

---

### Prompt Endpoints

#### `GET /prompts`

**Description**: Retrieve a list of all prompts, optionally filtered by collection ID or search query.

- **Query Parameters**:
  - `collection_id`: (Optional) ID of the collection to filter prompts.
  - `search`: (Optional) Text to search in the prompt's title or description.
  
- **Response 200**: 
  ```json
  {
    "prompts": [
      {
        "id": "abc123",
        "title": "Sample Prompt",
        "content": "What is AI?",
        "description": "A prompt about AI basics.",
        "collection_id": "def456",
        "created_at": "2023-10-14T00:00:00Z",
        "updated_at": "2023-10-14T00:00:00Z"
      }
    ],
    "total": 1
  }
  ```

#### `GET /prompts/{prompt_id}`

**Description**: Retrieve a specific prompt by its ID.

- **Response 200**:
  ```json
  {
    "id": "abc123",
    "title": "Sample Prompt",
    "content": "What is AI?",
    "description": "A prompt about AI basics.",
    "collection_id": "def456",
    "created_at": "2023-10-14T00:00:00Z",
    "updated_at": "2023-10-14T00:00:00Z"
  }
  ```

- **Error Response 404**:
  ```json
  {
    "detail": "Prompt not found"
  }
  ```

#### `POST /prompts`

**Description**: Create a new prompt.

- **Request Body**:
  ```json
  {
    "title": "Sample Prompt",
    "content": "What is AI?",
    "description": "A prompt about AI basics.",
    "collection_id": "def456"
  }
  ```

- **Response 201**: 
  ```json
  {
    "id": "abc123",
    "title": "Sample Prompt",
    "content": "What is AI?",
    "description": "A prompt about AI basics.",
    "collection_id": "def456",
    "created_at": "2023-10-14T00:00:00Z",
    "updated_at": "2023-10-14T00:00:00Z"
  }
  ```

- **Error Response 400**:
  ```json
  {
    "detail": "Collection not found"
  }
  ```

#### `PUT /prompts/{prompt_id}`

**Description**: Update an entire existing prompt.

- **Request Body**:
  ```json
  {
    "title": "Updated Prompt Title",
    "content": "Updated content.",
    "description": "Updated description.",
    "collection_id": "def456"
  }
  ```

- **Response 200**:
  ```json
  {
    "id": "abc123",
    "title": "Updated Prompt Title",
    "content": "Updated content.",
    "description": "Updated description.",
    "collection_id": "def456",
    "created_at": "2023-10-14T00:00:00Z",
    "updated_at": "2023-10-15T00:00:00Z"
  }
  ```

- **Error Response 404**:
  ```json
  {
    "detail": "Prompt not found"
  }
  ```

#### `PATCH /prompts/{prompt_id}`

**Description**: Partially update a prompt.

- **Request Body**:
  ```json
  {
    "description": "Partially updated description."
  }
  ```

- **Response 200**:
  ```json
  {
    "id": "abc123",
    "title": "Sample Prompt",
    "content": "What is AI?",
    "description": "Partially updated description.",
    "collection_id": "def456",
    "created_at": "2023-10-14T00:00:00Z",
    "updated_at": "2023-10-15T00:00:00Z"
  }
  ```

#### `DELETE /prompts/{prompt_id}`

**Description**: Delete a prompt by its ID.

- **Response 204**: No content.

- **Error Response 404**:
  ```json
  {
    "detail": "Prompt not found"
  }
  ```

---

### Collection Endpoints

#### `GET /collections`

**Description**: Retrieve a list of all collections.

- **Response 200**: 
  ```json
  {
    "collections": [
      {
        "id": "def456",
        "name": "Sample Collection",
        "description": "This is a sample collection description.",
        "created_at": "2023-10-10T00:00:00Z"
      }
    ],
    "total": 1
  }
  ```

#### `GET /collections/{collection_id}`

**Description**: Retrieve a specific collection by its ID.

- **Response 200**:
  ```json
  {
    "id": "def456",
    "name": "Sample Collection",
    "description": "This is a sample collection description.",
    "created_at": "2023-10-10T00:00:00Z"
  }
  ```

- **Error Response 404**:
  ```json
  {
    "detail": "Collection not found"
  }
  ```

#### `POST /collections`

**Description**: Create a new collection.

- **Request Body**:
  ```json
  {
    "name": "New Collection",
    "description": "Description of the new collection"
  }
  ```

- **Response 201**:
  ```json
  {
    "id": "ghi789",
    "name": "New Collection",
    "description": "Description of the new collection",
    "created_at": "2023-10-15T00:00:00Z"
  }
  ```

#### `DELETE /collections/{collection_id}`

**Description**: Delete a collection by its ID. Prompts in this collection will be orphaned.

- **Response 204**: No content.

- **Error Response 404**:
  ```json
  {
    "detail": "Collection not found"
  }
  ```

---

## Error Handling

- **404 Not Found**: Returned when a requested resource, like a prompt or collection, cannot be located.
- **400 Bad Request**: Occurs when an invalid request is sent, such as referencing a non-existent collection during prompt creation.

---

## Authentication

- **Current Status**: No authentication required. Endpoints are accessible without credentials.

