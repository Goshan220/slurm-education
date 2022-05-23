import json
import jsonschema

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["graph", "live-restore", "iptables"],
    "properties": {
        "graph": {"type": "string"},
        "live-restore": {"type": "boolean"},
        "log-driver": {"type": "string"},
        "log-opts": {
            "type": "object",
            "properties": {
                "max-file": {"type": "string"},
                "max-size": {"type": "string"},
            }
        },
        "storage-driver": {"type": "string"},
        "iptables": {"type": "boolean"},
        "insecure-registries": {
            "type": "array",
            "items": {
                "type": "string",
            }
        },
        "dns": {
            "type": "array",
            "items": {
                "type": "string",
            }
        },
        "dns-search": {
            "type": "array",
            "items": {
                "type": "string",
            }
        },
    }
}


def main():
    with open("docker_daemon.json") as json_file:
        print(type(json_file))
        my_json = json.load(json_file)
    print(my_json)
    print(my_json.get("graph"))
    with open("docker_daemon.json") as json_file:
        json_string = json_file.read()
        print(type(json_string))
        my_json = json.loads(json_string)
    print(my_json)
    print(my_json.get("graph"))

    print(jsonschema.validate(instance=my_json, schema=SCHEMA))

    print(json.dumps(my_json, sort_keys=False, indent=2))

    with open("docker_daemon_2.json", "a") as json_file:
        json.dump(my_json, json_file, sort_keys=False, indent=2)8


if __name__ == '__main__':
    main()
