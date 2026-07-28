"""Tests for the base Client class."""
import pytest
import rpapi
from tests.conftest import FAKE_API_KEY, FAKE_METRICS_KEY


class TestClientInit:
    """Tests for Client.__init__."""

    def test_api_key_loaded(self):
        client = rpapi.Client()
        assert client.api_key == FAKE_API_KEY

    def test_metrics_key_loaded(self):
        client = rpapi.Client()
        assert client.metrics_api_key == FAKE_METRICS_KEY

    def test_headers_contain_bearer_token(self):
        client = rpapi.Client()
        assert client.headers["Authorization"] == f"Bearer {FAKE_API_KEY}"
        assert client.headers["Accept"] == "application/json"

    def test_headers_is_a_copy(self):
        client = rpapi.Client()
        h1 = client.headers
        h2 = client.headers
        assert h1 is not h2
        assert h1 == h2


class TestClientGet:
    """Tests for Client._get."""

    def test_calls_get_with_correct_url(self, mock_get):
        client = rpapi.Client()
        client._get("/test/path")
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert args[0] == "https://api.runpod.io/v2/test/path"

    def test_passes_default_timeout(self, mock_get):
        client = rpapi.Client()
        client._get("/test")
        kwargs = mock_get.call_args[1]
        assert kwargs["timeout"] == 60.0

    def test_passes_custom_timeout(self, mock_get):
        client = rpapi.Client()
        client._get("/test", timeout=120.0)
        kwargs = mock_get.call_args[1]
        assert kwargs["timeout"] == 120.0

    def test_passes_params(self, mock_get):
        client = rpapi.Client()
        client._get("/test", params={"a": 1})
        kwargs = mock_get.call_args[1]
        assert kwargs["params"] == {"a": 1}

    def test_returns_response(self, mock_get):
        client = rpapi.Client()
        resp = client._get("/test")
        assert resp.status_code == 200
        assert resp.json() == {}


class TestClientPost:
    """Tests for Client._post."""

    def test_calls_post_with_correct_url(self, mock_post):
        client = rpapi.Client()
        client._post("/test/path", {"key": "val"})
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert args[0] == "https://api.runpod.io/v2/test/path"

    def test_passes_json_data(self, mock_post):
        client = rpapi.Client()
        client._post("/test", {"key": "val"})
        kwargs = mock_post.call_args[1]
        assert kwargs["json"] == {"key": "val"}

    def test_adds_content_type_header(self, mock_post):
        client = rpapi.Client()
        client._post("/test")
        kwargs = mock_post.call_args[1]
        headers = kwargs["headers"]
        assert headers["Content-Type"] == "application/json"

    def test_default_timeout(self, mock_post):
        client = rpapi.Client()
        client._post("/test")
        kwargs = mock_post.call_args[1]
        assert kwargs["timeout"] == 60.0


class TestClientPatch:
    """Tests for Client._patch."""

    def test_calls_patch_with_correct_url(self, mock_patch):
        client = rpapi.Client()
        client._patch("/test/path", {"key": "val"})
        mock_patch.assert_called_once()
        args, kwargs = mock_patch.call_args
        assert args[0] == "https://api.runpod.io/v2/test/path"

    def test_passes_json_data(self, mock_patch):
        client = rpapi.Client()
        client._patch("/test", {"key": "val"})
        kwargs = mock_patch.call_args[1]
        assert kwargs["json"] == {"key": "val"}


class TestClientDelete:
    """Tests for Client._delete."""

    def test_calls_delete_with_correct_url(self, mock_delete):
        client = rpapi.Client()
        client._delete("/test/path")
        mock_delete.assert_called_once()
        args, kwargs = mock_delete.call_args
        assert args[0] == "https://api.runpod.io/v2/test/path"

    def test_returns_response(self, mock_delete):
        client = rpapi.Client()
        resp = client._delete("/test")
        assert resp.status_code == 204
