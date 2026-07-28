"""Tests for the API class (pods, templates, catalog, volumes)."""
import pytest
import rpapi
from unittest.mock import MagicMock


class TestAPIGpuTypes:
    """Tests for GPU type / catalog methods."""

    def test_get_gpu_types_calls_correct_endpoint(self, mock_get):
        api = rpapi.API()
        api.get_gpu_types()
        mock_get.assert_called_once()
        args, _ = mock_get.call_args
        assert args[0] == "https://api.runpod.io/v2/catalog/gpus"

    def test_get_gpu_type_calls_correct_endpoint(self, mock_get):
        api = rpapi.API()
        api.get_gpu_type("NVIDIA RTX 4090")
        mock_get.assert_called_once()
        args, _ = mock_get.call_args
        assert "/catalog/gpus/NVIDIA RTX 4090" in args[0]

    def test_get_bid_price_delegates_to_get_gpu_type(self, mock_get):
        api = rpapi.API()
        api.get_bid_price("NVIDIA RTX 3090")
        mock_get.assert_called_once()
        args, _ = mock_get.call_args
        assert "/catalog/gpus/NVIDIA RTX 3090" in args[0]


class TestAPIPods:
    """Tests for pod management methods."""

    def test_get_pod(self, mock_get):
        api = rpapi.API()
        api.get_pod("pod123")
        mock_get.assert_called_once()
        args, _ = mock_get.call_args
        assert "/pods/pod123" in args[0]

    def test_get_pods(self, mock_get):
        api = rpapi.API()
        api.get_pods()
        mock_get.assert_called_once()
        args, _ = mock_get.call_args
        assert args[0] == "https://api.runpod.io/v2/pods"

    def test_create_pod(self, mock_post):
        api = rpapi.API()
        config = {"name": "test-pod", "image": "nginx", "gpu": {"id": "A100", "count": 1}}
        api.create_pod(config)
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert kwargs["json"] == config

    def test_update_pod(self, mock_patch):
        api = rpapi.API()
        api.update_pod("pod123", {"name": "updated"})
        mock_patch.assert_called_once()
        args, kwargs = mock_patch.call_args
        assert "/pods/pod123" in args[0]
        assert kwargs["json"] == {"name": "updated"}

    def test_delete_pod(self, mock_delete):
        api = rpapi.API()
        api.delete_pod("pod123")
        mock_delete.assert_called_once()
        args, _ = mock_delete.call_args
        assert "/pods/pod123" in args[0]

    def test_pod_action(self, mock_post):
        api = rpapi.API()
        api.pod_action("pod123", "stop")
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert "/pods/pod123/action" in args[0]
        assert kwargs["json"] == {"action": "stop"}

    def test_start_pod(self, mock_post):
        api = rpapi.API()
        api.start_pod("pod123")
        kwargs = mock_post.call_args[1]
        assert kwargs["json"] == {"action": "start"}

    def test_start_on_demand_pod(self, mock_post):
        api = rpapi.API()
        api.start_on_demand_pod("pod123")
        kwargs = mock_post.call_args[1]
        assert kwargs["json"] == {"action": "start"}

    def test_start_spot_pod_ignores_bid_price(self, mock_post):
        api = rpapi.API()
        api.start_spot_pod("pod123", bid_price=0.123)
        kwargs = mock_post.call_args[1]
        assert kwargs["json"] == {"action": "start"}

    def test_start_spot_pod_without_bid_price(self, mock_post):
        api = rpapi.API()
        api.start_spot_pod("pod123")
        kwargs = mock_post.call_args[1]
        assert kwargs["json"] == {"action": "start"}

    def test_stop_pod(self, mock_post):
        api = rpapi.API()
        api.stop_pod("pod123")
        kwargs = mock_post.call_args[1]
        assert kwargs["json"] == {"action": "stop"}

    def test_terminate_pod(self, mock_delete):
        api = rpapi.API()
        api.terminate_pod("pod123")
        mock_delete.assert_called_once()
        args, _ = mock_delete.call_args
        assert "/pods/pod123" in args[0]

    def test_create_on_demand_pod_defaults_to_secure(self, mock_post):
        api = rpapi.API()
        api.create_on_demand_pod({"name": "test", "image": "nginx"})
        kwargs = mock_post.call_args[1]
        assert kwargs["json"]["cloud"] == "SECURE"

    def test_create_on_demand_pod_preserves_cloud(self, mock_post):
        api = rpapi.API()
        api.create_on_demand_pod({"name": "test", "image": "nginx", "cloud": "COMMUNITY"})
        kwargs = mock_post.call_args[1]
        assert kwargs["json"]["cloud"] == "COMMUNITY"

    def test_create_spot_pod_forces_community(self, mock_post):
        api = rpapi.API()
        api.create_spot_pod({"name": "test", "image": "nginx"})
        kwargs = mock_post.call_args[1]
        assert kwargs["json"]["cloud"] == "COMMUNITY"

    def test_get_pod_logs_defaults(self, mock_get):
        api = rpapi.API()
        api.get_pod_logs("pod123")
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert "/pods/pod123/logs" in args[0]
        assert kwargs["params"] == {"tail": 100}
        assert kwargs["timeout"] == 300

    def test_get_pod_logs_with_all_params(self, mock_get):
        api = rpapi.API()
        api.get_pod_logs("pod123", source="container", tail=50, since="2024-01-01T00:00:00Z")
        kwargs = mock_get.call_args[1]
        assert kwargs["params"] == {
            "tail": 50,
            "source": "container",
            "since": "2024-01-01T00:00:00Z",
        }


class TestAPITemplates:
    """Tests for template management methods."""

    def test_get_templates(self, mock_get):
        api = rpapi.API()
        api.get_templates()
        mock_get.assert_called_once()
        args, _ = mock_get.call_args
        assert args[0] == "https://api.runpod.io/v2/templates"

    def test_get_template(self, mock_get):
        api = rpapi.API()
        api.get_template("tpl123")
        args, _ = mock_get.call_args
        assert "/templates/tpl123" in args[0]

    def test_create_template_config_dict(self, mock_post):
        api = rpapi.API()
        api.create_template(config={"name": "test", "image": "nginx"})
        kwargs = mock_post.call_args[1]
        assert kwargs["json"] == {"name": "test", "image": "nginx"}

    def test_create_template_keyword_args(self, mock_post):
        api = rpapi.API()
        api.create_template(
            name="test-template",
            image_name="ashleykza/foo:1.0",
            container_disk_in_gb=10,
            docker_args="",
            env={"KEY": "val"},
            ports="22/tcp,3000/http",
            is_public=True,
            is_serverless=False,
            category="NVIDIA",
            volume_in_gb=80,
            volume_mount_path="/workspace",
            container_registry_auth_id="reg123",
        )
        kwargs = mock_post.call_args[1]
        body = kwargs["json"]
        assert body["name"] == "test-template"
        assert body["image"] == "ashleykza/foo:1.0"
        assert body["disk"] == 10
        assert body["args"] == ""
        assert body["env"] == {"KEY": "val"}
        assert body["ports"] == ["22/tcp", "3000/http"]
        assert body["public"] is True
        assert body["serverless"] is False
        assert body["category"] == "NVIDIA"
        assert body["registry"] == "reg123"
        assert body["mounts"]["persistent"]["size"] == 80
        assert body["mounts"]["persistent"]["path"] == "/workspace"

    def test_create_template_env_as_list(self, mock_post):
        api = rpapi.API()
        api.create_template(
            name="test",
            image_name="img",
            env=[{"key": "k", "value": "v"}],
        )
        body = mock_post.call_args[1]["json"]
        assert body["env"] == {"k": "v"}

    def test_create_template_minimal_keywords(self, mock_post):
        api = rpapi.API()
        api.create_template()
        body = mock_post.call_args[1]["json"]
        assert body == {}

    def test_create_template_volume_defaults(self, mock_post):
        api = rpapi.API()
        api.create_template(name="test", image_name="img", volume_mount_path="/data")
        body = mock_post.call_args[1]["json"]
        assert body["mounts"]["persistent"]["size"] == 0
        assert body["mounts"]["persistent"]["path"] == "/data"

    def test_create_template_name_only(self, mock_post):
        api = rpapi.API()
        api.create_template(name="test")
        body = mock_post.call_args[1]["json"]
        assert body == {"name": "test"}

    def test_update_template(self, mock_patch):
        api = rpapi.API()
        api.update_template("tpl123", {"name": "updated"})
        mock_patch.assert_called_once()
        args, kwargs = mock_patch.call_args
        assert "/templates/tpl123" in args[0]
        assert kwargs["json"] == {"name": "updated"}

    def test_delete_template(self, mock_delete):
        api = rpapi.API()
        api.delete_template("tpl123")
        mock_delete.assert_called_once()
        args, _ = mock_delete.call_args
        assert "/templates/tpl123" in args[0]

    def test_get_templates_and_endpoints(self, mock_get):
        api = rpapi.API()
        result = api.get_templates_and_endpoints()
        assert "templates" in result
        assert "endpoints" in result
        assert mock_get.call_count == 2

    def test_get_endpoints(self, mock_get):
        api = rpapi.API()
        api.get_endpoints()
        mock_get.assert_called_once()
        args, _ = mock_get.call_args
        assert args[0] == "https://api.runpod.io/v2/serverless"


class TestAPINetworkVolumes:
    """Tests for network volume methods."""

    def test_get_network_volumes(self, mock_get):
        api = rpapi.API()
        api.get_network_volumes()
        mock_get.assert_called_once()
        args, _ = mock_get.call_args
        assert args[0] == "https://api.runpod.io/v2/network-volumes"

    def test_get_network_volume(self, mock_get):
        api = rpapi.API()
        api.get_network_volume("nv123")
        args, _ = mock_get.call_args
        assert "/network-volumes/nv123" in args[0]

    def test_create_network_volume(self, mock_post):
        api = rpapi.API()
        api.create_network_volume({"name": "nv", "size": 100, "dataCenter": "us-east"})
        kwargs = mock_post.call_args[1]
        assert kwargs["json"] == {"name": "nv", "size": 100, "dataCenter": "us-east"}

    def test_delete_network_volume(self, mock_delete):
        api = rpapi.API()
        api.delete_network_volume("nv123")
        mock_delete.assert_called_once()


class TestAPIDataCenters:
    """Tests for data center methods."""

    def test_get_datacenters_no_params(self, mock_get):
        api = rpapi.API()
        api.get_datacenters()
        kwargs = mock_get.call_args[1]
        assert kwargs["params"] == {}

    def test_get_datacenters_with_include(self, mock_get):
        api = rpapi.API()
        api.get_datacenters(include="GPU_AVAILABILITY")
        kwargs = mock_get.call_args[1]
        assert kwargs["params"] == {"include": "GPU_AVAILABILITY"}


class TestAPIBilling:
    """Tests for billing methods."""

    def test_get_billing_defaults(self, mock_get):
        api = rpapi.API()
        api.get_billing()
        kwargs = mock_get.call_args[1]
        assert kwargs["params"] == {"bucketSize": "day"}

    def test_get_billing_with_all_params(self, mock_get):
        api = rpapi.API()
        api.get_billing(
            start_time="2024-01-01T00:00:00Z",
            end_time="2024-01-07T00:00:00Z",
            bucket_size="hour",
            last_n=10,
        )
        kwargs = mock_get.call_args[1]
        assert kwargs["params"] == {
            "bucketSize": "hour",
            "startTime": "2024-01-01T00:00:00Z",
            "endTime": "2024-01-07T00:00:00Z",
            "lastN": 10,
        }


class TestAPIRegistry:
    """Tests for registry methods."""

    def test_get_registries(self, mock_get):
        api = rpapi.API()
        api.get_registries()
        mock_get.assert_called_once()
        args, _ = mock_get.call_args
        assert args[0] == "https://api.runpod.io/v2/registries"


class TestAPIGetMyself:
    """Tests for get_myself (legacy GraphQL fallback)."""

    def test_get_myself_uses_graphql(self, mock_post):
        api = rpapi.API()
        api.get_myself()
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert "https://api.runpod.io/graphql?api_key=" in args[0]
        assert "query" in kwargs["json"]
        assert "myself" in kwargs["json"]["query"]
