import yaml


def read_config():
    with open("config.yaml", 'r') as stream:
        return yaml.safe_load(stream)


config = read_config()


def write_config():
    with open("config.yaml", 'w') as stream:
        yaml.safe_dump(config, stream)


def roles():
    return config['roles']


def profile():
    return config['profile']


def thanks_list():
    return ['thanks', 'ty', 'thank you']
