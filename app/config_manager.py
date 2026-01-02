import yaml

class ConfigManager:
    def __init__(self, filepath = 'config.yaml'):
        self.filepath = filepath

        with open(self.filepath) as file:
            self.config = yaml.safe_load(file)
    
    def get(self, key):
        return self.config[key]
