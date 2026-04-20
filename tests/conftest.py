"""Pytest configuration and fixtures."""
import pytest
import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

@pytest.fixture
def project_root():
    """Return project root path."""
    return Path(__file__).parent.parent
