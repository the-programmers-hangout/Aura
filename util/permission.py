import yaml


def load_permissions():
    with open("resources/permission.yaml", 'r') as stream:
        return yaml.safe_load(stream)


def write_permissions():
    with open("resources/permission.yaml", 'w') as stream:
        yaml.safe_dump(permission_map, stream)


permission_map = load_permissions()  # command name to role name
