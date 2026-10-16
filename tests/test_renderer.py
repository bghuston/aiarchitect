"""Unexecuted examples of meaningful preview boundary checks."""
from dataclasses import replace
import pytest
from aiarchitect.models import PlanningError, TemplateDefinition
from aiarchitect.planner import plan

def test_preview_has_audit_fields_but_does_not_write(catalogue, customer, tmp_path):
    files = plan(catalogue.describe("database.entity"), customer, tmp_path)
    assert len(files) == 1
    assert "createdAt: Date;" in files[0].content
    assert "registeredAt?: Date;" in files[0].content
    assert not files[0].path.exists()

@pytest.mark.parametrize("destination", ["../escape.ts", "/absolute.ts", "C:/escape.ts"])
def test_escaping_destination_is_rejected(catalogue, customer, tmp_path, destination):
    pattern = catalogue.describe("database.entity")
    unsafe = replace(pattern, templates=(TemplateDefinition(pattern.templates[0].source, destination),))
    with pytest.raises(PlanningError):
        plan(unsafe, customer, tmp_path)

def test_existing_file_is_never_overwritten(catalogue, customer, tmp_path):
    occupied = tmp_path / "customer.entity.ts"
    occupied.write_text("existing work")
    with pytest.raises(PlanningError):
        plan(catalogue.describe("database.entity"), customer, tmp_path)
    assert occupied.read_text() == "existing work"

def test_duplicate_outputs_are_rejected(catalogue, customer, tmp_path):
    pattern = catalogue.describe("database.entity")
    duplicate = replace(pattern, templates=pattern.templates * 2)
    with pytest.raises(PlanningError):
        plan(duplicate, customer, tmp_path)
