import json

import jsonschema
import yaml


def main():
    with open("docker_daemon.yaml", "r") as yaml_file:
        yaml_conf = yaml.safe_load(yaml_file.read())
    print(yaml_conf)

    with open("docker_daemon.schema.json") as schema_file:
        schema = json.load(schema_file)

    jsonschema.validate(instance=yaml_conf, schema=schema)

    with open("docker_daemon_2.json", "w") as json_file:
        json.dump(yaml_conf, json_file, indent=4)

    with open("docker_daemon_2.yaml", "w") as yaml_file:
        yaml.safe_dump(yaml_conf, yaml_file, explicit_start=True)


if __name__ == '__main__':
    main()

