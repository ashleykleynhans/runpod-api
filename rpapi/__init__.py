"""Runpod REST API v2 client library."""
import httpx
from dotenv import dotenv_values

BASE_URL = "https://api.runpod.io/v2"
GRAPHQL_URL = "https://api.runpod.io/graphql"


class Client:
    """Base REST v2 client with Bearer token authentication."""

    def __init__(self):
        env = dotenv_values('.env')
        self.api_key = env['RUNPOD_API_KEY']
        self.metrics_api_key = env.get('RUNPOD_METRICS_API_KEY')
        self._headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.api_key}',
        }

    @property
    def headers(self):
        return dict(self._headers)

    def _get(self, path, params=None, timeout=60.0):
        return httpx.get(
            f'{BASE_URL}{path}',
            headers=self._headers,
            params=params,
            timeout=timeout,
        )

    def _post(self, path, json_data=None, timeout=60.0):
        headers = {**self._headers, 'Content-Type': 'application/json'}
        return httpx.post(
            f'{BASE_URL}{path}',
            headers=headers,
            json=json_data,
            timeout=timeout,
        )

    def _patch(self, path, json_data=None, timeout=60.0):
        headers = {**self._headers, 'Content-Type': 'application/json'}
        return httpx.patch(
            f'{BASE_URL}{path}',
            headers=headers,
            json=json_data,
            timeout=timeout,
        )

    def _delete(self, path, timeout=60.0):
        return httpx.delete(
            f'{BASE_URL}{path}',
            headers=self._headers,
            timeout=timeout,
        )


class API(Client):
    """Pods, templates, catalog, and network volumes via REST v2."""

    # -- Catalog ------------------------------------------------------------

    def get_gpu_types(self):
        """List all available GPU types with pricing."""
        return self._get('/catalog/gpus')

    def get_gpu_type(self, gpu_id):
        """Get a single GPU type by ID."""
        return self._get(f'/catalog/gpus/{gpu_id}')

    def get_bid_price(self, gpu_id):
        """Get pricing for a specific GPU type.

        Kept for backward compatibility; delegates to get_gpu_type.
        """
        return self.get_gpu_type(gpu_id)

    # -- Pods ---------------------------------------------------------------

    def get_pod(self, pod_id):
        """Get a single pod by ID."""
        return self._get(f'/pods/{pod_id}')

    def get_pods(self):
        """List all pods for the authenticated user."""
        return self._get('/pods')

    def create_pod(self, config):
        """Create a pod.

        Args:
            config: dict matching CreatePodRequest schema.
                Required: name, image, plus exactly one of gpu or cpu.
                Optional: args, disk, ports, env, registry, mounts,
                          cloud (SECURE/COMMUNITY), dataCenterIds,
                          globalNetworking.
        """
        return self._post('/pods', config)

    def update_pod(self, pod_id, config):
        """Partially update a pod (PATCH)."""
        return self._patch(f'/pods/{pod_id}', config)

    def delete_pod(self, pod_id):
        """Permanently terminate and delete a pod."""
        return self._delete(f'/pods/{pod_id}')

    def pod_action(self, pod_id, action):
        """Trigger a state transition on a pod.

        Args:
            pod_id: The pod ID.
            action: One of 'start', 'stop', 'restart', 'terminate'.
        """
        return self._post(f'/pods/{pod_id}/action', {'action': action})

    def start_pod(self, pod_id):
        """Start a stopped pod."""
        return self.pod_action(pod_id, 'start')

    def start_on_demand_pod(self, pod_id):
        """Start an on-demand pod (backward compat)."""
        return self.start_pod(pod_id)

    def start_spot_pod(self, pod_id, bid_price=None):
        """Start a spot pod (backward compat).

        Note: REST v2 uses cloud:'COMMUNITY' at pod creation time,
        not a separate spot resume. bid_price is ignored.
        """
        return self.start_pod(pod_id)

    def stop_pod(self, pod_id):
        """Stop a running pod."""
        return self.pod_action(pod_id, 'stop')

    def terminate_pod(self, pod_id):
        """Terminate a pod (backward compat; use delete_pod)."""
        return self.delete_pod(pod_id)

    def create_on_demand_pod(self, config):
        """Create an on-demand pod (backward compat).

        Args:
            config: dict matching CreatePodRequest schema.
        """
        if 'cloud' not in config:
            config['cloud'] = 'SECURE'
        return self.create_pod(config)

    def create_spot_pod(self, config):
        """Create a spot (community cloud) pod (backward compat).

        Args:
            config: dict matching CreatePodRequest schema.
        """
        config['cloud'] = 'COMMUNITY'
        return self.create_pod(config)

    def get_pod_logs(self, pod_id, source=None, tail=100, since=None):
        """Stream pod logs as SSE.

        Args:
            pod_id: The pod ID.
            source: 'container', 'system', or None for both.
            tail: Historical lines to backfill (default 100, 0 = live only).
            since: RFC 3339 timestamp to resume from.
        """
        params = {'tail': tail}
        if source:
            params['source'] = source
        if since:
            params['since'] = since
        return self._get(f'/pods/{pod_id}/logs', params=params, timeout=300)

    # -- Templates ----------------------------------------------------------

    def get_templates(self):
        """List all templates."""
        return self._get('/templates')

    def get_template(self, template_id):
        """Get a single template by ID."""
        return self._get(f'/templates/{template_id}')

    def create_template(self, config=None, *, template=None,
                        name=None, image_name=None, container_disk_in_gb=None,
                        docker_args=None, env=None, volume_in_gb=None,
                        volume_mount_path=None, ports=None, readme=None,
                        is_public=None, is_serverless=None,
                        start_jupyter=None, start_ssh=None, start_script=None,
                        advanced_start=None, category=None,
                        recommended_gpu_ids=None, incompatible_gpu_ids=None,
                        allowed_cuda_versions=None, min_vram=None, min_ram=None,
                        network_volume_ids=None, ports_config=None,
                        container_registry_auth_id=None):
        """Create a template via REST v2.

        Supports both structured keyword arguments and a raw config dict.
        The legacy 'template' parameter (GraphQL input string) is no longer
        supported; use structured parameters instead.

        Args:
            config: A dict matching CreateTemplateRequest schema
                (name, image, args, disk, ports, env, registry, mounts,
                 serverless, public, category).
            template: Deprecated legacy parameter (ignored).
            name: Template name.
            image_name: Docker image reference.
            container_disk_in_gb: Ephemeral disk in GB.
            docker_args: Container entrypoint args.
            env: Dict of environment variable key/value pairs.
            volume_in_gb: DEPRECATED in v2; use mounts instead.
            volume_mount_path: DEPRECATED in v2; use mounts instead.
            ports: Ports string (e.g. '3000/http,8888/http,22/tcp').
            readme: Markdown readme content (v2: stored as description).
            is_public: Make template publicly visible.
            is_serverless: Mark as serverless template.
            start_jupyter: DEPRECATED in v2.
            start_ssh: DEPRECATED in v2.
            start_script: DEPRECATED in v2.
            advanced_start: DEPRECATED in v2.
            category: 'NVIDIA', 'AMD', or 'CPU'.
            recommended_gpu_ids: DEPRECATED in v2.
            incompatible_gpu_ids: DEPRECATED in v2.
            allowed_cuda_versions: DEPRECATED in v2.
            min_vram: DEPRECATED in v2.
            min_ram: DEPRECATED in v2.
            network_volume_ids: DEPRECATED in v2; use mounts.
            ports_config: DEPRECATED in v2.
            container_registry_auth_id: Registry credential ID.
        """
        if config is not None:
            return self._post('/templates', config)

        body = {}
        if name is not None:
            body['name'] = name
        if image_name is not None:
            body['image'] = image_name
        if container_disk_in_gb is not None:
            body['disk'] = container_disk_in_gb
        if docker_args is not None:
            body['args'] = docker_args
        if env is not None and isinstance(env, dict):
            body['env'] = env
        elif env is not None:
            body['env'] = {e['key']: e['value'] for e in env}
        if ports is not None:
            body['ports'] = ports.split(',')
        if is_public is not None:
            body['public'] = is_public
        if is_serverless is not None:
            body['serverless'] = is_serverless
        if category is not None:
            body['category'] = category
        if container_registry_auth_id is not None:
            body['registry'] = container_registry_auth_id

        if volume_in_gb is not None or volume_mount_path is not None:
            body['mounts'] = {
                'persistent': {
                    'size': volume_in_gb or 0,
                    'path': volume_mount_path or '/workspace',
                }
            }

        return self._post('/templates', body)

    def update_template(self, template_id, config):
        """Partially update a template (PATCH)."""
        return self._patch(f'/templates/{template_id}', config)

    def delete_template(self, template_id):
        """Delete a template by ID."""
        return self._delete(f'/templates/{template_id}')

    def get_templates_and_endpoints(self):
        """Get combined templates and serverless endpoints.

        Returns a dict with 'templates' and 'endpoints' lists.
        """
        t_resp = self.get_templates()
        e_resp = self.get_endpoints()
        return {
            'templates': t_resp.json().get('templates', []),
            'endpoints': e_resp.json().get('endpoints', []),
        }

    def get_endpoints(self):
        """List all serverless endpoints (convenience)."""
        return self._get('/serverless')

    # -- Network volumes ----------------------------------------------------

    def get_network_volumes(self):
        """List all network volumes."""
        return self._get('/network-volumes')

    def get_network_volume(self, volume_id):
        """Get a single network volume by ID."""
        return self._get(f'/network-volumes/{volume_id}')

    def create_network_volume(self, config):
        """Create a network volume.

        Args:
            config: dict with name (str), size (int GB), dataCenter (str).
        """
        return self._post('/network-volumes', config)

    def delete_network_volume(self, volume_id):
        """Delete a network volume by ID."""
        return self._delete(f'/network-volumes/{volume_id}')

    # -- Data centers -------------------------------------------------------

    def get_datacenters(self, include=None):
        """List data centers.

        Args:
            include: 'GPU_AVAILABILITY' or 'CPU_AVAILABILITY' (optional).
        """
        params = {}
        if include:
            params['include'] = include
        return self._get('/catalog/datacenters', params=params)

    # -- Billing ------------------------------------------------------------

    def get_billing(self, start_time=None, end_time=None, bucket_size='day',
                    last_n=None):
        """Get aggregated billing history."""
        params = {'bucketSize': bucket_size}
        if start_time:
            params['startTime'] = start_time
        if end_time:
            params['endTime'] = end_time
        if last_n:
            params['lastN'] = last_n
        return self._get('/billing', params=params)

    def get_myself(self):
        """Get full account/user info.

        Uses the legacy GraphQL API since no single REST v2 equivalent
        exists for referral/account data.
        """
        query = """
            query myself {
                myself {
                    id authId email
                    notifyPodsStale notifyPodsGeneral notifyLowBalance
                    creditAlertThreshold notifyOther
                    currentSpendPerHr machineQuota
                    referralEarned signedTermsOfService spendLimit
                    templateEarned multiFactorEnabled
                    clientBalance clientLifetimeSpend referralId
                    hostBalance underBalance minBalance
                    dailyCharges {
                        amount updatedAt diskCharges podCharges
                        apiCharges serverlessCharges type
                    }
                    serverlessDiscount {
                        userId type discountFactor expirationDate
                    }
                    spendDetails {
                        localStoragePerHour networkStoragePerHour
                        gpuComputePerHour
                    }
                    creditCodes { id issuerId createdAt redeemedAt amount }
                    referral { code currentMonth { totalReferrals totalSpend } }
                    apiKeys { id permissions createdAt }
                    pubKey
                    containerRegistryCreds { id name registryAuth }
                    information {
                        firstName lastName addressLine1 addressLine2
                        countryCode companyName companyIdentification
                        taxIdentification
                    }
                    podTemplates {
                        id name imageName isPublic isRunpod isServerless
                        ports runtimeInMin startJupyter startScript startSsh
                        volumeInGb volumeMountPath advancedStart
                        containerDiskInGb containerRegistryAuthId
                        dockerArgs earned
                        env { key value }
                    }
                    pods {
                        name id desiredStatus costPerHr
                        containerDiskInGb volumeInGb memoryInGb vcpuCount
                        runtime { uptimeInSeconds }
                        machine { podHostId }
                    }
                    maxServerlessConcurrency
                    endpoints {
                        gpuIds id idleTimeout name networkVolumeId
                        locations scalerType scalerValue
                        template { name imageName }
                        templateId type userId version
                        workersMax workersMin workersStandby
                    }
                    networkVolumes { id name size dataCenterId }
                    savingsPlans {
                        startTime endTime podId gpuTypeId
                        pod { name id desiredStatus costPerHr
                              containerDiskInGb volumeInGb memoryInGb vcpuCount }
                        savingsPlanType costPerHr upfrontCost planLength
                    }
                }
            }
        """
        return httpx.post(
            f'{GRAPHQL_URL}?api_key={self.api_key}',
            json={'query': query},
            timeout=60.0,
        )

    # -- Registry -----------------------------------------------------------

    def get_registries(self):
        """List container registry credentials."""
        return self._get('/registries')


class Serverless(Client):
    """Serverless endpoint management via REST v2."""

    def get_endpoints(self):
        """List all serverless endpoints."""
        return self._get('/serverless')

    def get_endpoint(self, endpoint_id):
        """Get a single endpoint by ID."""
        return self._get(f'/serverless/{endpoint_id}')

    def create_endpoint(self, config):
        """Create a serverless endpoint.

        Args:
            config: dict matching CreateEndpointRequest schema.
                Required: name, gpu { pools, count }.
                Optional: image, args, disk, ports, env, registry,
                          workers, scaling, dataCenterIds,
                          networkVolumes, timeout, flashboot.
        """
        return self._post('/serverless', config)

    def update_endpoint(self, endpoint_id, config):
        """Partially update an endpoint (PATCH)."""
        return self._patch(f'/serverless/{endpoint_id}', config)

    def delete_endpoint(self, endpoint_id):
        """Permanently delete an endpoint."""
        return self._delete(f'/serverless/{endpoint_id}')

    def get_workers(self, endpoint_id):
        """List active workers for an endpoint."""
        return self._get(f'/serverless/{endpoint_id}/workers')

    def get_releases(self, endpoint_id):
        """List release history for an endpoint."""
        return self._get(f'/serverless/{endpoint_id}/releases')

    def get_worker_logs(self, endpoint_id, worker_id, source=None,
                        tail=100, since=None):
        """Stream worker logs as SSE."""
        params = {'tail': tail}
        if source:
            params['source'] = source
        if since:
            params['since'] = since
        return self._get(
            f'/serverless/{endpoint_id}/workers/{worker_id}/logs',
            params=params, timeout=300,
        )

    # -- Backward-compatible mutation wrappers -------------------------------

    def update_min_workers(self, endpoint_id, value):
        """Set minimum workers (backward compat)."""
        return self.update_endpoint(endpoint_id, {
            'workers': {'min': value},
        })

    def update_max_workers(self, endpoint_id, value):
        """Set maximum workers (backward compat)."""
        return self.update_endpoint(endpoint_id, {
            'workers': {'max': value},
        })

    def update_endpoint_gpu_ids(self, endpoint_id, name, gpu_ids):
        """Update GPU pool IDs (backward compat)."""
        pools = [p.strip() for p in gpu_ids.split(',') if p.strip()]
        return self.update_endpoint(endpoint_id, {
            'name': name,
            'gpu': {'pools': pools},
        })

    def update_endpoint_template(self, endpoint_id, template_id):
        """Update endpoint template (backward compat).

        Note: v2 endpoints don't reference templates by ID the same way.
        Use update_endpoint with image/container config from the template.
        """
        return self.update_endpoint(endpoint_id, {
            'image': None,  # caller should spread template config
        })

    # -- Legacy metrics/logs endpoints (separate API) -----------------------

    def get_serverless_logs(self, endpoint_id, start, end, batch_size):
        """Get serverless endpoint logs (legacy metrics API)."""
        url = f'https://api.runpod.ai/v2/{endpoint_id}/logs'
        url += f'?batch={batch_size}&from={start}&to={end}'
        headers = dict(self._headers)
        headers['Authorization'] = f'Bearer {self.metrics_api_key}'
        return httpx.get(url, headers=headers, timeout=120)

    def get_serverless_requests(self, endpoint_id):
        """Get serverless endpoint requests (legacy API)."""
        url = f'https://api.runpod.ai/v2/{endpoint_id}/requests'
        return httpx.get(url, headers=self._headers, timeout=120)

    def get_serverless_metrics(self, endpoint_id):
        """Get serverless endpoint metrics (legacy API)."""
        headers = dict(self._headers)
        headers['Authorization'] = f'Bearer {self.metrics_api_key}'
        return httpx.get(
            f'https://api.runpod.ai/v2/{endpoint_id}/metrics',
            headers=headers, timeout=120,
        )

    def get_serverless_request_metrics(self, endpoint_id, interval='h'):
        """Get serverless request metrics (legacy API)."""
        headers = dict(self._headers)
        headers['Authorization'] = f'Bearer {self.metrics_api_key}'
        return httpx.get(
            f'https://api.runpod.ai/v2/{endpoint_id}/metrics/request_ts_v1'
            f'?interval={interval}',
            headers=headers, timeout=120,
        )

    def get_serverless_cold_start_metrics(self, endpoint_id, interval='h'):
        """Get serverless cold start metrics (legacy API)."""
        headers = dict(self._headers)
        headers['Authorization'] = f'Bearer {self.metrics_api_key}'
        return httpx.get(
            f'https://api.runpod.ai/v2/{endpoint_id}/metrics/cold_start_ts_v1'
            f'?interval={interval}',
            headers=headers, timeout=120,
        )

    def get_serverless_summary(self, endpoint_id):
        """Convenience: get endpoint + workers + releases."""
        endpoint = self.get_endpoint(endpoint_id)
        workers = self.get_workers(endpoint_id)
        releases = self.get_releases(endpoint_id)
        return {
            'endpoint': endpoint,
            'workers': workers,
            'releases': releases,
        }
