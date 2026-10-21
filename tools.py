
import json

from kubernetes import client, config
from kubernetes.client.exceptions import ApiException
from kubernetes.config.config_exception import ConfigException
from langchain_core.tools import tool


def get_core_v1():
    """Load the local Kubernetes configuration and return the Core API."""
    config.load_kube_config()
    return client.CoreV1Api()


@tool
def get_nodes() -> str:
    """Get Kubernetes worker nodes, their readiness status, and resource capacity."""
    try:
        v1 = get_core_v1()
        nodes = v1.list_node()

        results = []

        for node in nodes.items:
            conditions = node.status.conditions or []

            ready_status = next(
                (
                    condition.status
                    for condition in conditions
                    if condition.type == "Ready"
                ),
                "Unknown",
            )

            results.append({
                "name": node.metadata.name,
                "ready": ready_status,
                "kubernetes_version": node.status.node_info.kubelet_version,
                "capacity": node.status.capacity,
                "pod_capacity": node.status.allocatable.get("pods"),
            })

        return json.dumps(results, indent=2)

    except (ConfigException, ApiException) as exc:
        return f"Could not retrieve nodes: {exc}"


@tool
def get_pods(namespace: str = "all") -> str:
    """Get pod status, container states, and restart counts.
    Use namespace='all' to inspect every namespace.
    """
    try:
        v1 = get_core_v1()

        if namespace.lower() == "all":
            pods = v1.list_pod_for_all_namespaces()
        else:
            pods = v1.list_namespaced_pod(namespace=namespace)

        results = []

        for pod in pods.items:
            container_statuses = []

            for status in pod.status.container_statuses or []:
                state = "unknown"

                if status.state.waiting:
                    state = status.state.waiting.reason or "waiting"
                elif status.state.running:
                    state = "running"
                elif status.state.terminated:
                    state = status.state.terminated.reason or "terminated"

                container_statuses.append({
                    "name": status.name,
                    "state": state,
                    "restart_count": status.restart_count,
                })

            results.append({
                "namespace": pod.metadata.namespace,
                "name": pod.metadata.name,
                "phase": pod.status.phase,
                "node": pod.spec.node_name,
                "pod_ip": pod.status.pod_ip,
                "containers": container_statuses,
            })

        return json.dumps(results, indent=2)

    except (ConfigException, ApiException) as exc:
        return f"Could not retrieve pods: {exc}"


@tool
def get_pod_logs(
    pod_name: str,
    namespace: str = "default",
    container: str = "",
    tail_lines: int = 100,
) -> str:
    """Retrieve recent logs from a pod.
    Supply the pod name and namespace. Specify container if the pod has
    multiple containers. tail_lines controls how many recent lines to read.
    """
    try:
        if not 1 <= tail_lines <= 500:
            return "tail_lines must be between 1 and 500."

        v1 = get_core_v1()

        options = {
            "name": pod_name,
            "namespace": namespace,
            "tail_lines": tail_lines,
            "timestamps": True,
        }

        if container.strip():
            options["container"] = container.strip()

        logs = v1.read_namespaced_pod_log(**options)

        return logs or "No logs returned for this pod."

    except (ConfigException, ApiException) as exc:
        return f"Could not retrieve pod logs: {exc}"


@tool
def get_events(namespace: str = "all") -> str:
    """Get recent Kubernetes events to help diagnose scheduling,
    image-pull, container, and other cluster problems.
    Use namespace='all' to inspect every namespace.
    """
    try:
        v1 = get_core_v1()

        if namespace.lower() == "all":
            events = v1.list_event_for_all_namespaces(limit=50)
        else:
            events = v1.list_namespaced_event(
                namespace=namespace,
                limit=50,
            )

        results = []

        for event in events.items:
            results.append({
                "namespace": event.metadata.namespace,
                "object": (
                    f"{event.involved_object.kind}/"
                    f"{event.involved_object.name}"
                ),
                "type": event.type,
                "reason": event.reason,
                "message": event.message,
                "count": event.count,
                "last_seen": str(
                    event.last_timestamp or event.event_time or ""
                ),
            })

        return json.dumps(results, indent=2)

    except (ConfigException, ApiException) as exc:
        return f"Could not retrieve events: {exc}"


TOOLS = [
    get_nodes,
    get_pods,
    get_pod_logs,
    get_events,
]
