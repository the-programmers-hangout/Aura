import yaml


class ConfigManager:
    def __init__(self):
        with open("config.yaml", 'r') as stream:
            self._config = yaml.safe_load(stream)
        self._categories = ['helpful', 'funny', 'informative', 'kind', 'creative']

    @property
    def config(self):
        return self._config

    @property
    def karma_categories(self):
        return self._categories
