"""Utility functions for PromptLab"""

import re
from typing import List

from app.models import Prompt

def sort_prompts_by_date(prompts: List[Prompt], descending: bool = True) -> List[Prompt]:
    """Sort a list of prompts by their creation date.

    Args:
        prompts (List[Prompt]): The list of prompt objects to sort.
        descending (bool): If True, sort from newest to oldest. If False, sort from oldest to newest.

    Returns:
        List[Prompt]: The sorted list of prompts.
    """
    return sorted(prompts, key=lambda p: p.created_at, reverse=descending)

def filter_prompts_by_collection(prompts: List[Prompt], collection_id: str) -> List[Prompt]:
    """Filter prompts based on a specific collection ID.

    Args:
        prompts (List[Prompt]): The list of prompt objects to filter.
        collection_id (str): The ID of the collection to filter prompts by.

    Returns:
        List[Prompt]: A list of prompts that belong to the specified collection.
    """
    return [p for p in prompts if p.collection_id == collection_id]

def search_prompts(prompts: List[Prompt], query: str) -> List[Prompt]:
    """Search prompts by title or description using a query string.

    Args:
        prompts (List[Prompt]): The list of prompt objects to search.
        query (str): The search query string.

    Returns:
        List[Prompt]: A list of prompts that match the query in their title or description.
    """
    query_lower = query.lower()
    return [
        p for p in prompts 
        if query_lower in p.title.lower() or 
           (p.description and query_lower in p.description.lower())
    ]

def validate_prompt_content(content: str) -> bool:
    """Validate the content of a prompt to ensure it meets criteria.

    A valid prompt should not be empty, should not be just whitespace,
    and should be at least 10 characters long.

    Args:
        content (str): The content of the prompt to validate.

    Returns:
        bool: True if the prompt content is valid, otherwise False.
    """
    if not content or not content.strip():
        return False
    return len(content.strip()) >= 10

def extract_variables(content: str) -> List[str]:
    """Extract template variables from prompt content.

    Variables are defined in the format {{variable_name}}.

    Args:
        content (str): The content from which to extract variables.

    Returns:
        List[str]: A list of variable names found within the content.
    """
    return re.findall(r'\{\{(\w+)\}\}', content)
