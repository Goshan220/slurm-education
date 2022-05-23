import kopf
from k8soperator.envs.env import Environment

__envs_conf = {
    'nginx': (80, 'nginx:stable'),
    'apache': (8080, 'tomcat:10.0.8-jdk8-openjdk-buster')
}


def create_env(env_type, name, host_user):
    if env_type in __envs_conf:
        port, image = __envs_conf[env_type]
        return Environment(name, port, env_type, image, host_user)

    raise kopf.HandlerFatalError(f"Type must be one of {list(__envs_conf.keys())}")