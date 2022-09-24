import base64

from kubernetes import config, client


class K8sClient:
    def __init__(self):
        # config.load_kube_config('/home/rsysoev/.kube/config')
        config.load_incluster_config()
        self.api = client.CoreV1Api()

    def add_secret(self, secret_name: str, secret_key: str, secret_value: str, namespace: str) -> None:
        secret_value_bytes = secret_value.encode("ascii")
        base64_bytes = base64.b64encode(secret_value_bytes)
        base64_string = base64_bytes.decode("ascii")

        api_version = 'v1'
        kind = 'Secret'
        metadata = {'name': secret_name}
        data = {secret_key: base64_string}

        body = client.V1Secret(api_version=api_version, data=data, kind=kind, metadata=metadata)
        self.api.create_namespaced_secret(namespace, body)
