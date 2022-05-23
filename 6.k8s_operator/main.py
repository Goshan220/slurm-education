from contextlib import suppress
import kopf
import kubernetes as k8s
from k8soperator.envs.env_factory import create_env

RESOURCE_GROUP = "example.org"
RESOURCE_VERSION = "v1"
RESOURCE_TYPE = "testenv"


@kopf.on.create(RESOURCE_GROUP, RESOURCE_VERSION, RESOURCE_TYPE)
def create_custom_resource(body, spec, logger, **kwargs):
    name = body["metadata"]["name"]
    host_user = spec["hostUser"]

    env = create_env(spec["type"], name, host_user)
    create_k8s_object(spec["namespace"], env, logger)


@kopf.on.delete(RESOURCE_GROUP, RESOURCE_VERSION, RESOURCE_TYPE)
def delete_custom_resource(body, spec, logger, **kwargs):
    api = k8s.client.CoreV1Api()
    ext_api = k8s.client.ExtensionsV1beta1Api()

    name = body["metadata"]["name"]
    namespace = spec["namespace"]
    host_user = spec["hostUser"]

    env = create_env(spec["type"], name, host_user)
    pod_name = env.pod.metadata.name
    with suppress(k8s.client.exceptions.ApiException):
        api.delete_namespaced_pod(pod_name, namespace)

    svc_name = env.svc["metadata"]["name"]
    with suppress(k8s.client.exceptions.ApiException):
        api.delete_namespaced_service(svc_name, namespace)

    ingress_name = env.ingress["metadata"]["name"]
    with suppress(k8s.client.exceptions.ApiException):
        ext_api.delete_namespaced_ingress(ingress_name, namespace)

    with suppress(k8s.client.exceptions.ApiException):
        api.delete_namespace(namespace)

    message = f"Namespace {namespace} and it's resources deleted"
    logger.info(message)
    return {"message": message}


def create_k8s_object(namespace, env, logger):
    api = k8s.client.CoreV1Api()
    ext_api = k8s.client.ExtensionsV1beta1Api()

    if not any(cluster_ns.metadata.name == namespace for cluster_ns in api.list_namespace().items):
        logger.info(f"{namespace} not found in cluster, creating")
        api.create_namespace(k8s.client.V1Namespace(metadata=k8s.client.V1ObjectMeta(
            name=namespace
        )))

    pod = api.create_namespaced_pod(namespace, env.pod)
    logger.info(f"Pod {pod.metadata.name} created")

    svc = api.create_namespaced_service(namespace, env.svc)
    logger.info(f"Service {pod.metadata.name} created")

    ingress = ext_api.create_namespaced_ingress(namespace, env.ingress)
    logger.info(f"Ingress {pod.metadata.name} created")
