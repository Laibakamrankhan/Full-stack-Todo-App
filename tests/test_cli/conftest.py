"""Configuration for CLI tests."""

import pytest
from src.common import service_manager


@pytest.fixture(autouse=True)
def reset_service_manager():
    """Reset the service manager before each test to ensure clean state."""
    service_manager.reset_service()