"""Unexecuted illustrative test fixtures. Do not run; see README disclaimer."""
import json
from pathlib import Path
import pytest
from aiarchitect.catalogue import PatternCatalogue

ROOT = Path(__file__).resolve().parents[1]

@pytest.fixture
def catalogue():
    return PatternCatalogue(ROOT / "patterns")

@pytest.fixture
def customer():
    return json.loads((ROOT / "examples/customer-entity.json").read_text())
