import yaml


class ConfigStore:
    def __init__(self):
        self._config = self.read_config()

    @property
    def config(self):
        return self._config

    @property
    def roles(self):
        return self.config['roles']

    @staticmethod
    def read_config():
        with open("config.yaml", 'r') as stream:
            return yaml.safe_load(stream)

    def write_config(self):
        with open("config.yaml", 'w') as stream:
            yaml.dump(self.config, stream)
