import json
import httpx
from dotenv import dotenv_values


class API(object):
    def __init__(self):
        env = dotenv_values('.env')
        self.API_KEY = env['RUNPOD_API_KEY']

    def _run_query(self, payload, auth_required=False):
        url = 'https://api.runpod.io/graphql'

        if auth_required:
            url += f'?api_key={self.API_KEY}'

        response = httpx.post(
            url,
            json=payload
        )

        return response

    # https://docs.runpod.io/docs/get-gpu-types
    def get_gpu_types(self):
        return self._run_query({
            "query": """
                query GpuTypes {
                    gpuTypes {
                        maxGpuCount
                        id
                        displayName
                        manufacturer
                        memoryInGb
                        cudaCores
                        secureCloud
                        communityCloud
                        securePrice
                        communityPrice
                        lowestPrice(input: { gpuCount: 1 }) {
                            minimumBidPrice
                        }
                    }
                }
            """
        }, False)

    def get_bid_price(self, gpu_id):
        return self._run_query({
            "query": """
                query GpuTypes {{
                  gpuTypes(input: {{ id: "{gpu_id}" }}) {{
                    id
                    displayName
                    memoryInGb
                    secureCloud
                    communityCloud
                    lowestPrice(input: {{ gpuCount: 1 }}) {{
                      minimumBidPrice
                      uninterruptablePrice
                    }}
                  }}
                }}
            """.format(gpu_id=gpu_id)
        }, False)

    # https://docs.runpod.io/docs/get-pod#get-pod-by-id
    def get_pod(self, pod_id):
        return self._run_query({
            "query": """
                query Pod {{
                  pod(input: {{ podId: "{pod_id}" }}) {{
                    id
                    machineId
                    name
                    imageName
                    templateId
                    desiredStatus
                    costPerHr
                    costMultiplier
                    lowestBidPriceToResume
                    containerDiskInGb
                    volumeInGb
                    memoryInGb
                    vcpuCount
                    podType
                    ports
                    version
                    volumeEncrypted
                    volumeMountPath
                    runtime {{
                      uptimeInSeconds
                      ports {{
                        ip
                        isIpPublic
                        privatePort
                        publicPort
                        type
                      }}
                      gpus {{
                        id
                        gpuUtilPercent
                        memoryUtilPercent
                      }}
                      container {{
                        cpuPercent
                        memoryPercent
                      }}
                    }}
                  }}
                }}
            """.format(pod_id=pod_id)
        }, True)

    # https://docs.runpod.io/docs/get-pod#get-all-pods
    def get_pods(self):
        return self._run_query({
            "query": """
                query Pods {
                    myself {
                        pods {
                            id
                            machineId
                            name
                            imageName
                            templateId
                            desiredStatus
                            costPerHr
                            costMultiplier
                            lowestBidPriceToResume
                            containerDiskInGb
                            volumeInGb
                            memoryInGb
                            vcpuCount
                            podType
                            ports
                            version
                            volumeEncrypted
                            volumeMountPath
                            runtime {
                                uptimeInSeconds
                                ports {
                                    ip
                                    isIpPublic
                                    privatePort
                                    publicPort
                                    type
                                }
                                gpus {
                                    id
                                    gpuUtilPercent
                                    memoryUtilPercent
                                }
                                container {
                                    cpuPercent
                                    memoryPercent
                                }
                            }
                            machine {
                                podHostId
                            }
                            latestTelemetry {
                                cpuUtilization
                                memoryUtilization
                                averageGpuMetrics {
                                    percentUtilization
                                    temperatureCelcius
                                    memoryUtilization
                                    powerWatts
                                }
                            }
                        }
                    }
                }
            """
        }, True)

    def get_myself(self):
        return self._run_query({
            "query": """
                query myself {
                    myself {
                        id
                        currentSpendPerHr
                        machineQuota
                        referralEarned
                        signedTermsOfService
                        spendLimit
                        templateEarned
                        multiFactorEnabled
                        clientBalance
                        hostBalance
                        apiKeys {
                            id
                            permissions
                            createdAt
                        }
                        pubKey
                        information {
                            firstName
                            lastName
                            addressLine1
                            addressLine2
                            countryCode
                            companyName
                            companyIdentification
                            taxIdentification
                        }
                        creditCodes {
                            id
                            issuerId
                            createdAt
                            redeemedAt
                            amount
                        }
                        pods {
                            name
                            id
                            desiredStatus
                            costPerHr
                            containerDiskInGb
                            volumeInGb
                            memoryInGb
                            vcpuCount
                            runtime {
                                uptimeInSeconds
                            }
                            machine {
                                podHostId
                            }
                        }
                    }
                }
            """
        }, True)

    # https://docs.runpod.io/docs/start-pod#start-on-demand-pod
    def start_on_demand_pod(self, pod_id):
        return self._run_query({
            "query": """
                mutation {{
                    podResume(input: {{ podId: "{pod_id}", gpuCount: 1 }}) {{
                        id
                        costPerHr
                        desiredStatus
                        lastStatusChange
                        imageName
                        env
                        machineId
                        machine {{
                            podHostId
                        }}
                    }}
                }}
            """.format(pod_id=pod_id)
        }, True)

    # https://docs.runpod.io/docs/start-pod#start-spot-pod
    def start_spot_pod(self, pod_id, bid_price):
        return self._run_query({
            "query": """
                mutation {{
                    podBidResume(input: {{ podId: "{pod_id}", bidPerGpu: {bid_price} gpuCount: 1 }}) {{
                        id
                        costPerHr
                        desiredStatus
                        lastStatusChange
                        imageName
                        env
                        machineId
                        machine {{
                            podHostId
                        }}
                    }}
                }}
            """.format(pod_id=pod_id, bid_price=bid_price)
        }, True)

    # https://docs.runpod.io/docs/stop-pod
    def stop_pod(self, pod_id):
        return self._run_query({
            "query": """
                mutation {{
                    podStop(input: {{ podId: "{pod_id}" }}) {{
                        id
                        desiredStatus
                    }}
                }}
            """.format(pod_id=pod_id)
        }, True)

    def terminate_pod(self, pod_id):
        return self._run_query({
            "query": """
                mutation {{
                    podTerminate(input: {{ podId: "{pod_id}" }})
                }}
            """.format(pod_id=pod_id)
        }, True)

    # https://docs.runpod.io/docs/create-pod
    def create_on_demand_pod(self, pod_config):
        return self._run_query({
            "query": """
                mutation {{
                    podFindAndDeployOnDemand(input: {{ {pod_config} }}) {{
                        containerDiskInGb
                        apiKey
                        costPerHr
                        desiredStatus
                        dockerArgs
                        dockerId
                        gpuCount
                        id
                        imageName
                        machineId
                        memoryInGb
                        name
                        podType
                        ports
                        templateId
                        uptimeSeconds
                        vcpuCount
                        version
                        volumeEncrypted
                        volumeInGb
                        volumeKey
                        volumeMountPath
                        runtime {{
                            uptimeInSeconds
                            ports {{
                                ip
                                isIpPublic
                                privatePort
                                publicPort
                                type
                            }}
                            gpus {{
                                id
                                gpuUtilPercent
                                memoryUtilPercent
                            }}
                            container {{
                                cpuPercent
                                memoryPercent
                            }}
                        }}
                        machine {{
                            podHostId
                        }}
                    }}
                }}
            """.format(pod_config=pod_config)
        }, True)

    # https://docs.runpod.io/docs/create-pod
    def create_spot_pod(self, pod_config):
        return self._run_query({
            "query": """
                mutation {{
                    podRentInterruptable(input: {{ {pod_config} }}) {{
                        containerDiskInGb
                        apiKey
                        costPerHr
                        desiredStatus
                        dockerArgs
                        dockerId
                        gpuCount
                        id
                        imageName
                        machineId
                        memoryInGb
                        name
                        podType
                        ports
                        templateId
                        uptimeSeconds
                        vcpuCount
                        version
                        volumeEncrypted
                        volumeInGb
                        volumeKey
                        volumeMountPath
                        runtime {{
                            uptimeInSeconds
                            ports {{
                                ip
                                isIpPublic
                                privatePort
                                publicPort
                                type
                            }}
                            gpus {{
                                id
                                gpuUtilPercent
                                memoryUtilPercent
                            }}
                            container {{
                                cpuPercent
                                memoryPercent
                            }}
                        }}
                        machine {{
                            podHostId
                        }}
                    }}
                }}
            """.format(pod_config=pod_config)
        }, True)

    def create_template(self, template):
        return self._run_query({
            "query": """
                mutation {{
                    saveTemplate(input: {{ {template} }}) {{
                        advancedStart
                        containerDiskInGb
                        dockerArgs
                        env {{
                            key
                            value
                        }}
                        id
                        imageName
                        name
                        ports
                        readme
                        startJupyter
                        startScript
                        startSsh
                        volumeInGb
                        volumeMountPath
                    }}
                }}
            """.format(template=template)
        }, True)


class Endpoints(object):
    def __init__(self):
        env = dotenv_values('.env')
        self.API_KEY = env['RUNPOD_API_KEY']
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': self.API_KEY
        }

    def get_dreambooth_health(self):
        url = 'https://api.runpod.ai/v2/dream-booth-v1/health'

        return httpx.get(
            url,
            headers=self.headers
        )

    # https://docs.runpod.io/reference/dreambooth-sd-v15
    def train_dreambooth(self, payload):
        url = 'https://api.runpod.ai/v2/dream-booth-v1/run'

        return httpx.post(
            url,
            json=payload,
            headers=self.headers
        )

    def cancel_dreambooth_training(self, job_id):
        url = f'https://api.runpod.ai/v2/dream-booth-v1/cancel/{job_id}'

        return httpx.post(url, headers=self.headers)

    # https://docs.runpod.io/reference/status
    def get_status(self, job_id):
        url = f'https://api.runpod.ai/v2/dream-booth-v1/status/{job_id}'

        return httpx.get(url, headers=self.headers)
