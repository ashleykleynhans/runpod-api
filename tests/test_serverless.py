"""Tests for the Serverless class."""
import pytest
import rpapi


class TestServerlessEndpoints:
    """Tests for endpoint management methods."""

    def test_get_endpoints(self, mock_get):
        sl = rpapi.Serverless()
        sl.get_endpoints()
        mock_get.assert_called_once()
        args, _ = mock_get.call_args
        assert args[0] == "https://api.runpod.io/v2/serverless"

    def test_get_endpoint(self, mock_get):
        sl = rpapi.Serverless()
        sl.get_endpoint("ep123")
        args, _ = mock_get.call_args
        assert "/serverless/ep123" in args[0]

    def test_create_endpoint(self, mock_post):
        sl = rpapi.Serverless()
        config = {"name": "test-ep", "gpu": {"pools": ["AMPERE_48"], "count": 1}}
        sl.create_endpoint(config)
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert "/serverless" == args[0].replace("https://api.runpod.io/v2", "")
        assert kwargs["json"] == config

    def test_update_endpoint(self, mock_patch):
        sl = rpapi.Serverless()
        sl.update_endpoint("ep123", {"workers": {"min": 1}})
        mock_patch.assert_called_once()
        args, kwargs = mock_patch.call_args
        assert "/serverless/ep123" in args[0]
        assert kwargs["json"] == {"workers": {"min": 1}}

    def test_delete_endpoint(self, mock_delete):
        sl = rpapi.Serverless()
        sl.delete_endpoint("ep123")
        mock_delete.assert_called_once()
        args, _ = mock_delete.call_args
        assert "/serverless/ep123" in args[0]

    def test_get_workers(self, mock_get):
        sl = rpapi.Serverless()
        sl.get_workers("ep123")
        args, _ = mock_get.call_args
        assert "/serverless/ep123/workers" in args[0]

    def test_get_releases(self, mock_get):
        sl = rpapi.Serverless()
        sl.get_releases("ep123")
        args, _ = mock_get.call_args
        assert "/serverless/ep123/releases" in args[0]


class TestServerlessWorkerLogs:
    """Tests for worker logs."""

    def test_get_worker_logs_defaults(self, mock_get):
        sl = rpapi.Serverless()
        sl.get_worker_logs("ep123", "w456")
        args, kwargs = mock_get.call_args
        assert "/serverless/ep123/workers/w456/logs" in args[0]
        assert kwargs["params"] == {"tail": 100}
        assert kwargs["timeout"] == 300

    def test_get_worker_logs_with_all_params(self, mock_get):
        sl = rpapi.Serverless()
        sl.get_worker_logs("ep123", "w456", source="system", tail=0, since="T0")
        kwargs = mock_get.call_args[1]
        assert kwargs["params"] == {"tail": 0, "source": "system", "since": "T0"}


class TestServerlessBackwardCompat:
    """Tests for backward-compatible mutation wrappers."""

    def test_update_min_workers(self, mock_patch):
        sl = rpapi.Serverless()
        sl.update_min_workers("ep123", 2)
        args, kwargs = mock_patch.call_args
        assert "/serverless/ep123" in args[0]
        assert kwargs["json"] == {"workers": {"min": 2}}

    def test_update_max_workers(self, mock_patch):
        sl = rpapi.Serverless()
        sl.update_max_workers("ep123", 5)
        kwargs = mock_patch.call_args[1]
        assert kwargs["json"] == {"workers": {"max": 5}}

    def test_update_endpoint_gpu_ids(self, mock_patch):
        sl = rpapi.Serverless()
        sl.update_endpoint_gpu_ids("ep123", "my-ep", "AMPERE_48, ADA_24")
        kwargs = mock_patch.call_args[1]
        assert kwargs["json"]["name"] == "my-ep"
        assert kwargs["json"]["gpu"]["pools"] == ["AMPERE_48", "ADA_24"]

    def test_update_endpoint_gpu_ids_single(self, mock_patch):
        sl = rpapi.Serverless()
        sl.update_endpoint_gpu_ids("ep123", "my-ep", "AMPERE_48")
        kwargs = mock_patch.call_args[1]
        assert kwargs["json"]["gpu"]["pools"] == ["AMPERE_48"]

    def test_update_endpoint_gpu_ids_empty(self, mock_patch):
        sl = rpapi.Serverless()
        sl.update_endpoint_gpu_ids("ep123", "my-ep", "")
        kwargs = mock_patch.call_args[1]
        assert kwargs["json"]["gpu"]["pools"] == []

    def test_update_endpoint_template(self, mock_patch):
        sl = rpapi.Serverless()
        sl.update_endpoint_template("ep123", "tpl456")
        kwargs = mock_patch.call_args[1]
        assert kwargs["json"] == {"image": None}


class TestServerlessLegacyEndpoints:
    """Tests for legacy metrics/logs endpoints (separate API)."""

    def test_get_serverless_logs(self, mock_get):
        sl = rpapi.Serverless()
        sl.get_serverless_logs("ep123", "2024-01-01T00:00:00Z", "2024-02-01T00:00:00Z", 500)
        args, kwargs = mock_get.call_args
        assert "https://api.runpod.ai/v2/ep123/logs" in args[0]
        assert "batch=500" in args[0]
        assert "from=2024-01-01T00:00:00Z" in args[0]
        assert "to=2024-02-01T00:00:00Z" in args[0]

    def test_get_serverless_requests(self, mock_get):
        sl = rpapi.Serverless()
        sl.get_serverless_requests("ep123")
        args, _ = mock_get.call_args
        assert "https://api.runpod.ai/v2/ep123/requests" in args[0]

    def test_get_serverless_metrics(self, mock_get):
        sl = rpapi.Serverless()
        sl.get_serverless_metrics("ep123")
        args, _ = mock_get.call_args
        assert "https://api.runpod.ai/v2/ep123/metrics" in args[0]

    def test_get_serverless_request_metrics(self, mock_get):
        sl = rpapi.Serverless()
        sl.get_serverless_request_metrics("ep123", interval="d")
        args, _ = mock_get.call_args
        assert "request_ts_v1" in args[0]
        assert "interval=d" in args[0]

    def test_get_serverless_request_metrics_default_interval(self, mock_get):
        sl = rpapi.Serverless()
        sl.get_serverless_request_metrics("ep123")
        args, _ = mock_get.call_args
        assert "interval=h" in args[0]

    def test_get_serverless_cold_start_metrics(self, mock_get):
        sl = rpapi.Serverless()
        sl.get_serverless_cold_start_metrics("ep123", interval="w")
        args, _ = mock_get.call_args
        assert "cold_start_ts_v1" in args[0]
        assert "interval=w" in args[0]

    def test_get_serverless_cold_start_metrics_default_interval(self, mock_get):
        sl = rpapi.Serverless()
        sl.get_serverless_cold_start_metrics("ep123")
        args, _ = mock_get.call_args
        assert "interval=h" in args[0]


class TestServerlessSummary:
    """Tests for get_serverless_summary convenience method."""

    def test_get_serverless_summary(self, mock_get):
        sl = rpapi.Serverless()
        result = sl.get_serverless_summary("ep123")
        assert "endpoint" in result
        assert "workers" in result
        assert "releases" in result
        assert mock_get.call_count == 3

    def test_get_serverless_summary_returns_responses(self, mock_get):
        sl = rpapi.Serverless()
        result = sl.get_serverless_summary("ep123")
        assert result["endpoint"].status_code == 200
        assert result["workers"].status_code == 200
        assert result["releases"].status_code == 200
