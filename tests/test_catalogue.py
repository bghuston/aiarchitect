"""Unexecuted intended behaviour, not verification evidence."""
import pytest
from aiarchitect.models import DefinitionError

def test_discovery_has_three_distinct_capabilities(catalogue):
    assert {p.id for p in catalogue.list_patterns()} == {
        "database.entity", "cqrs.command", "project.module"}

def test_keyword_search_exposes_transaction_capability(catalogue):
    assert [p.id for p in catalogue.search("TRANSACTION")] == ["cqrs.command"]

def test_unknown_pattern_is_definition_error(catalogue):
    with pytest.raises(DefinitionError, match="Unknown pattern"):
        catalogue.describe("missing.pattern")
