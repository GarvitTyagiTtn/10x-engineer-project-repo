# Custom AI Coding Agent Instructions

This document provides guidelines and standards for AI coding assistants working on the PromptLab project.

## Project Coding Standards
- Follow PEP 8 standards for Python code, ensuring consistent styling and formatting.
- Employ type hints to enhance code clarity and support static analysis.

## Preferred Patterns and Conventions
- Utilize dependency injection where possible to promote testability and modularity.
- Leverage Python's `dataclasses` or `pydantic` models for structured data representation.
- Ensure function and variable names are descriptive and follow `snake_case` format.

## File Naming Conventions
- Use `snake_case` for all file and directory names, enhancing readability and consistency.
- Prefix test files with `test_` and place them within the corresponding module or `tests` directory.

## Error Handling Approach
- Use Python `exceptions` judiciously to manage errors, providing detailed messages for debugging.
- When handling exceptions, catch specific errors rather than using a broad `except Exception:` block.
- Return clear error messages to API clients with appropriate HTTP status codes.

## Testing Requirements
- Achieve a minimum of 80% code coverage with unit and integration tests using `pytest`.
- Structure tests following Arrange-Act-Assert (AAA) pattern to promote clarity.
- Utilize fixtures and mocks to handle external dependencies in unit tests.

By following these guidelines, the AI coding assistant can produce consistent and maintainable code that aligns with the project's standards and practices.
