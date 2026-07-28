"""Tests for the Endpoints class (Dreambooth API)."""
import pytest
import rpapi
from unittest.mock import MagicMock


class TestEndpointsInit:
    """Tests for Endpoints.__init__."""

    def test_has_api_key(self):
        ep = rpapi.Endpoints()
        assert ep.API_KEY == "rpa_fake_api_key_12345"

    def test_has_bearer_header(self):
        ep = rpapi.Endpoints()
        assert "Authorization" in ep.headers
        assert "Bearer" in ep.headers["Authorization"]


class TestDreamboothHealth:
    """Tests for dreambooth health check."""

    def test_calls_correct_url(self, mock_get):
        ep = rpapi.Endpoints()
        ep.get_dreambooth_health()
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert args[0] == "https://api.runpod.ai/v2/dream-booth-v1/health"
        assert "Authorization" in kwargs["headers"]


class TestDreamboothTrain:
    """Tests for dreambooth training."""

    def test_calls_correct_url(self, mock_post):
        ep = rpapi.Endpoints()
        payload = {"input": {"concept_name": "test"}}
        ep.train_dreambooth(payload)
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert args[0] == "https://api.runpod.ai/v2/dream-booth-v1/run"
        assert kwargs["json"] == payload
        assert kwargs["timeout"] == 120


class TestDreamboothCancel:
    """Tests for cancel dreambooth training."""

    def test_calls_correct_url(self, mock_post):
        ep = rpapi.Endpoints()
        ep.cancel_dreambooth_training("job123")
        mock_post.assert_called_once()
        args, _ = mock_post.call_args
        assert args[0] == "https://api.runpod.ai/v2/dream-booth-v1/cancel/job123"


class TestDreamboothStatus:
    """Tests for dreambooth job status."""

    def test_calls_correct_url(self, mock_get):
        ep = rpapi.Endpoints()
        ep.get_status("job123")
        mock_get.assert_called_once()
        args, _ = mock_get.call_args
        assert args[0] == "https://api.runpod.ai/v2/dream-booth-v1/status/job123"
