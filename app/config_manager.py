import yaml
import os

class ConfigManager:
    def __init__(self, filepath = 'config.yaml'):
        self.filepath = filepath

        with open(self.filepath) as file:
            self.config = yaml.safe_load(file)
    
    def get(self, key_path, default=None):
        env_key = key_path.replace('.', '_').upper() 
        env_value = os.getenv(env_key)
        
        if env_value:
            return env_value
        
        keys = key_path.split('.')
        value = self.config

        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
