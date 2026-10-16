"""Unexecuted intended contracts; no passing result is claimed."""
from dataclasses import replace
import pytest
from aiarchitect.models import DefinitionError, ParameterError
from aiarchitect.validation import validate_parameters

def test_missing_parameter_is_distinct_from_bad_schema(catalogue, customer, tmp_path):
    pattern = catalogue.describe("database.entity")
    del customer["name"]
    with pytest.raises(ParameterError, match="name"):
        validate_parameters(pattern, customer)
    bad = tmp_path / "schema.json"
    bad.write_text('{"type":"not-a-json-schema-type"}')
    with pytest.raises(DefinitionError):
        validate_parameters(replace(pattern, schema_path=bad), {})

def test_reserved_entity_field_is_rejected(catalogue, customer):
    customer["fields"].append({"name": "id", "type": "string"})
    with pytest.raises(ParameterError, match="shadow"):
        validate_parameters(catalogue.describe("database.entity"), customer)
