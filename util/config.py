import yaml


def read_config():
    with open("config.yaml", 'r') as stream:
        return yaml.safe_load(stream)


config = read_config()


def write_config():
    with open("config.yaml", 'w') as stream:
        yaml.safe_dump(config, stream)


# shorthand for roles configuration
def roles():
    return config['roles']


# shorthand for profile configurations
def profile():
    return config['profile']


# shorthand for blacklist configuration
def blacklist():
    return config['blacklist']


# shorthand for karma configuration
def karma():
    return config['karma']


# split the karma keywords
def thanks_list():
    return config['karma']['keywords'].split(",")


# version dict
def version():
    return dict(aura_version='1.3.1', python_version='3.8.2', discord_version='1.3.3')


# return the discord tag of the author of this bot
def author_discord():
    return 'arkencl#5579'


# return the link to the repository
def repository():
    return '[[Github]](https://github.com/arkencl/aura)'


class ConfigDescription:
    def __init__(self, keys, description, values):
        self.keys: str = keys  # 'channel log'
        self.description: str = description  # 'which channel aura should log karma gain, removals and other messages'
        self.values: [] = values  # possible values
