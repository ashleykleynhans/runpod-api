"""Shared fixtures for rpapi tests."""
import pytest
from unittest.mock import MagicMock, patch

FAKE_API_KEY = "rpa_fake_api_key_12345"
FAKE_METRICS_KEY = "rm_fake_metrics_key_67890"


@pytest.fixture(autouse=True)
def mock_env():
    """Mock dotenv_values to return fake API keys."""
    with patch("rpapi.dotenv_values", return_value={
        "RUNPOD_API_KEY": FAKE_API_KEY,
        "RUNPOD_METRICS_API_KEY": FAKE_METRICS_KEY,
    }):
        yield


@pytest.fixture
def mock_get():
    """Mock httpx.get returning a 200 response with empty JSON."""
    with patch("rpapi.httpx.get") as m:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        m.return_value = mock_response
        yield m


@pytest.fixture
def mock_post():
    """Mock httpx.post returning a 200 response with empty JSON."""
    with patch("rpapi.httpx.post") as m:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        m.return_value = mock_response
        yield m


@pytest.fixture
def mock_patch():
    """Mock httpx.patch returning a 200 response with empty JSON."""
    with patch("rpapi.httpx.patch") as m:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        m.return_value = mock_response
        yield m


@pytest.fixture
def mock_delete():
    """Mock httpx.delete returning a 204 response."""
    with patch("rpapi.httpx.delete") as m:
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_response.json.return_value = {}
        m.return_value = mock_response
        yield m


@pytest.fixture
def all_mocks(mock_get, mock_post, mock_patch, mock_delete):
    """Fixture that provides all four HTTP method mocks."""
    return {
        "get": mock_get,
        "post": mock_post,
        "patch": mock_patch,
        "delete": mock_delete,
    }
