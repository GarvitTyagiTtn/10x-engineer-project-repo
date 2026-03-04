"""Utility function tests for PromptLab.

Covers all utility functions with edge cases and error conditions.
"""

import pytest
from datetime import datetime, timedelta
from app.models import Prompt
from app.utils import (
    sort_prompts_by_date,
    filter_prompts_by_collection,
    search_prompts,
    validate_prompt_content,
    extract_variables,
)


@pytest.fixture
def prompts_with_dates():
    """Create prompts with distinct creation dates for sorting tests."""
    base = datetime(2024, 1, 1)
    return [
        Prompt(title="Old", content="C", created_at=base),
        Prompt(title="Mid", content="C", created_at=base + timedelta(days=1)),
        Prompt(title="New", content="C", created_at=base + timedelta(days=2)),
    ]


@pytest.fixture
def prompts_with_collections():
    """Create prompts with various collection assignments."""
    return [
        Prompt(title="A", content="C", collection_id="col-1"),
        Prompt(title="B", content="C", collection_id="col-1"),
        Prompt(title="C", content="C", collection_id="col-2"),
        Prompt(title="D", content="C", collection_id=None),
    ]


# ============== sort_prompts_by_date ==============


class TestSortPromptsByDate:
    """Tests for the sort_prompts_by_date utility."""

    def test_sort_descending(self, prompts_with_dates):
        result = sort_prompts_by_date(prompts_with_dates, descending=True)
        assert result[0].title == "New"
        assert result[1].title == "Mid"
        assert result[2].title == "Old"

    def test_sort_ascending(self, prompts_with_dates):
        result = sort_prompts_by_date(prompts_with_dates, descending=False)
        assert result[0].title == "Old"
        assert result[1].title == "Mid"
        assert result[2].title == "New"

    def test_sort_empty_list(self):
        assert sort_prompts_by_date([]) == []

    def test_sort_single_item(self):
        prompt = Prompt(title="Solo", content="C")
        result = sort_prompts_by_date([prompt])
        assert len(result) == 1
        assert result[0].title == "Solo"

    def test_sort_default_is_descending(self, prompts_with_dates):
        result = sort_prompts_by_date(prompts_with_dates)
        assert result[0].title == "New"

    def test_sort_preserves_original_list(self, prompts_with_dates):
        original_order = [p.title for p in prompts_with_dates]
        sort_prompts_by_date(prompts_with_dates, descending=True)
        assert [p.title for p in prompts_with_dates] == original_order


# ============== filter_prompts_by_collection ==============


class TestFilterPromptsByCollection:
    """Tests for the filter_prompts_by_collection utility."""

    def test_filter_matching_collection(self, prompts_with_collections):
        result = filter_prompts_by_collection(prompts_with_collections, "col-1")
        assert len(result) == 2
        assert all(p.collection_id == "col-1" for p in result)

    def test_filter_single_match(self, prompts_with_collections):
        result = filter_prompts_by_collection(prompts_with_collections, "col-2")
        assert len(result) == 1

    def test_filter_no_match(self, prompts_with_collections):
        result = filter_prompts_by_collection(prompts_with_collections, "col-999")
        assert result == []

    def test_filter_empty_list(self):
        assert filter_prompts_by_collection([], "col-1") == []

    def test_filter_none_collection_id_no_match(self, prompts_with_collections):
        """Filtering by a string won't match prompts with collection_id=None."""
        result = filter_prompts_by_collection(prompts_with_collections, "None")
        assert result == []


# ============== search_prompts ==============


class TestSearchPrompts:
    """Tests for the search_prompts utility."""

    def test_search_by_title(self):
        prompts = [
            Prompt(title="Python Guide", content="C"),
            Prompt(title="Java Guide", content="C"),
        ]
        result = search_prompts(prompts, "Python")
        assert len(result) == 1
        assert result[0].title == "Python Guide"

    def test_search_case_insensitive(self):
        prompts = [Prompt(title="Python Guide", content="C")]
        assert len(search_prompts(prompts, "python")) == 1
        assert len(search_prompts(prompts, "PYTHON")) == 1

    def test_search_by_description(self):
        prompts = [
            Prompt(title="Prompt", content="C", description="machine learning tips"),
        ]
        result = search_prompts(prompts, "machine")
        assert len(result) == 1

    def test_search_no_match(self):
        prompts = [Prompt(title="Hello", content="C")]
        assert search_prompts(prompts, "zzz") == []

    def test_search_empty_list(self):
        assert search_prompts([], "anything") == []

    def test_search_partial_match(self):
        prompts = [Prompt(title="JavaScript Tutorial", content="C")]
        result = search_prompts(prompts, "Script")
        assert len(result) == 1

    def test_search_prompt_without_description(self):
        prompts = [Prompt(title="No Desc", content="C", description=None)]
        result = search_prompts(prompts, "No Desc")
        assert len(result) == 1

    def test_search_does_not_match_content(self):
        """search_prompts only checks title and description, not content."""
        prompts = [Prompt(title="Title", content="secret keyword")]
        result = search_prompts(prompts, "secret")
        assert len(result) == 0

    def test_search_matches_both_title_and_description(self):
        prompts = [Prompt(title="Alpha Beta", content="C", description="Alpha Gamma")]
        result = search_prompts(prompts, "Alpha")
        assert len(result) == 1  # should not duplicate


# ============== validate_prompt_content ==============


class TestValidatePromptContent:
    """Tests for the validate_prompt_content utility."""

    def test_valid_content(self):
        assert validate_prompt_content("This is valid content") is True

    def test_exactly_10_chars(self):
        assert validate_prompt_content("1234567890") is True

    def test_less_than_10_chars(self):
        assert validate_prompt_content("short") is False

    def test_empty_string(self):
        assert validate_prompt_content("") is False

    def test_whitespace_only(self):
        assert validate_prompt_content("   ") is False

    def test_whitespace_with_short_content(self):
        assert validate_prompt_content("   hi   ") is False

    def test_whitespace_with_valid_content(self):
        assert validate_prompt_content("   valid content here   ") is True

    def test_none_content(self):
        assert validate_prompt_content(None) is False

    def test_newlines_only(self):
        assert validate_prompt_content("\n\n\n") is False

    def test_tabs_only(self):
        assert validate_prompt_content("\t\t\t") is False


# ============== extract_variables ==============


class TestExtractVariables:
    """Tests for the extract_variables utility."""

    def test_single_variable(self):
        assert extract_variables("Hello {{name}}") == ["name"]

    def test_multiple_variables(self):
        result = extract_variables("{{greeting}} {{name}}, welcome to {{place}}")
        assert result == ["greeting", "name", "place"]

    def test_no_variables(self):
        assert extract_variables("No variables here") == []

    def test_empty_string(self):
        assert extract_variables("") == []

    def test_duplicate_variables(self):
        result = extract_variables("{{x}} and {{x}}")
        assert result == ["x", "x"]

    def test_nested_braces_ignored(self):
        """Only matches {{word}} pattern, not deeper nesting."""
        result = extract_variables("{{{nested}}}")
        assert "nested" in result

    def test_variable_with_underscores(self):
        assert extract_variables("{{my_var}}") == ["my_var"]

    def test_variable_with_numbers(self):
        assert extract_variables("{{var1}}") == ["var1"]

    def test_no_match_for_single_braces(self):
        assert extract_variables("{not_a_var}") == []

    def test_no_match_for_spaces_in_variable(self):
        assert extract_variables("{{not a var}}") == []

    def test_mixed_content(self):
        content = "Dear {{name}},\n\nPlease review {{code}} and provide {{feedback}}."
        result = extract_variables(content)
        assert result == ["name", "code", "feedback"]
