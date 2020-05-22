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
    return config['thanks'].split(",")


def version():
    return dict(aura_version='1.3.1', python_version='3.8.2', discord_version='1.3.3')


def author_discord():
    return 'arkencl#5579'


def repository():
    return '[[Github]](https://github.com/arkencl)'
