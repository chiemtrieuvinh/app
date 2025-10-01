import pytest
from models.base import Base as ModelsBase
from schemas.base import Base as SchemasBase
from schemas.base import Base as SchemasBase

def test_models_base_import():
    """Test that models.base.Base can be imported"""
    assert ModelsBase is not None

def test_schemas_base_import():
    """Test that schemas.base.Base can be imported"""
    assert SchemasBase is not None