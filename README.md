# PromptLab

## Project Overview

PromptLab is a sophisticated platform for AI engineers designed to manage, store, and organize prompt engineering workflows efficiently. The project is developed to provide a workspace for prompt management, akin to "Postman for Prompts."

## Key Features

- **Prompt Template Storage**: Store prompts with customizable variables for varied input scenarios.
- **Organization Tools**: Structure prompts into collections.
- **Search and Tagging**: Efficiently find prompts with tag-based searches.
- **Version Tracking**: Maintain and review history of prompt changes.
- **Testing Facilities**: In-built features to test prompts with various inputs.

## Architecture / High-Level Design

PromptLab is built using:
- **Backend**: Python with FastAPI for managing API services.
- **Frontend**: React (to be implemented) for interactive UI.
- **Testing**: Pytest for ensuring code quality.
- **DevOps**: Docker and GitHub Actions for CI/CD.
- **Data Models**: Utilizes Pydantic for schema validation and SQLAlchemy/SQLite (future potential) for data storage.

The backend manages several modules including API route handling, data models, and storage interfaces, which coordinate to provide a full suite of management functionalities.

## Prerequisites

- **Python**: Version 3.10 or above
- **Node.js**: Version 18 or above for frontend (upcoming)
- **Git**: For version control
- **Environment Variables**: Define in `.env` (template or specify required)

## Installation and Setup

### How to Clone the Repo

```bash
git clone <your-repo-url>
cd promptlab
```

### Configure Environment

- Ensure Python and Node.js are installed.
- Configure any environment variables in a `.env` file if using database or external services.

### Build the Project

- **Backend**: 
  ```bash
  cd backend
  pip install -r requirements.txt
  ```

## Quick Start Guide

### Running Locally

1. Start Backend:
   ```bash
   cd backend
   python main.py
   ```
   Access API at [http://localhost:8000](http://localhost:8000).

2. Run Tests:
   ```bash
   pytest tests/ -v
   ```

### Default Ports and Credentials

- **API Port**: `8000`
- **Documentation**: Accessible via `/docs` endpoint.

## API Endpoints Summary

### Prompts Module

| Method | Endpoint          | Description                     | Auth | Query Params        |
|--------|-------------------|---------------------------------|------|---------------------|
| GET    | `/health`         | Health check                    | None | None                |
| GET    | `/prompts`        | List all prompts                | None | None                |
| GET    | `/prompts/{id}`   | Get prompt by id                | None | None                |
| POST   | `/prompts`        | Create a new prompt             | None | None                |
| PUT    | `/prompts/{id}`   | Update a prompt                 | None | None                |
| DELETE | `/prompts/{id}`   | Delete a prompt                 | None | None                |

## Development Setup

### Running in Dev Mode

- **Backend** Hot Reload: Modify Python files and auto-reload occurs.
  
### Unit and Integration Tests

Run all tests with:
```bash
pytest tests/
```

### Local Tooling

- **Docker**: Ensure Docker is installed for containerization.
- **Postman**: Available collection for endpoint testing.

## Configuration and Environment

### Important Application Properties

- `API_KEY`: Placeholder for future use, `export API_KEY='your_key'`

### Logging and Monitoring

Basic logging available, integrate with standard tools like `Sentry` as needed.

## Contributing Guidelines

1. **Open Issues**: Describe bugs or suggest features.
2. **Create Branches**: Use descriptive naming conventions.
3. **Submit PRs**: Ensure code reviews and CI pass before merging.