import os
import json
from pydoc import locate

class Configuration:

    def __init__(self):
        self.global_params = {}
        self.local_params = {}
        self.type = "DefaultConfig"

    def set_global(self, key: str, val_type: type, value, description="") -> bool:
        if isinstance(value, val_type):
            self.global_params[key] = [val_type, value, description]
            return True
        else:
            try:
                self.global_params[key] = [val_type, val_type(value), description]
                return True
            except Exception as e:
                return False

    def update_global(self, key: str, value) -> [bool, str]:
        if key in self.global_params:
            try:
                self.global_params[key][1] = self.global_params[key][0](value)
                return [True, f"Successfully set {key} to {value}"]
            except Exception as e:
                return [False, f"'{value}' is not {self.global_params[key][0]} type"]
        else:
            return [False, f"There is no {key} global variable available"]

    def get_global(self, key):
        if key in self.global_params:
            return self.global_params[key][1:2]
        else:
            raise KeyError

    def get_all_globals(self):
        return self.global_params

    def load_global_configuration(self, configuration: dict) -> [bool, str]:
        for key in configuration:
            try:
                val_type, value, descr = configuration[key]
                self.set_global(key, val_type, value, descr)
            except Exception as e:
                return [False, f"Error while loading global configuration"]
        return [True, "Loaded global configuration successfully"]

    def save_configuration_to_json(self, filepath: str) -> [bool, str]:
        try:
            if '/' not in filepath:
                if '.json' not in filepath:
                    filepath = "configurations/application/"+filepath+".json"
                else:
                    filepath = "configurations/application/" + filepath
            json_config = {"type": self.type,
                           "global_config": self.serialize_config(self.global_params)}
            with open(filepath, "w") as file:
                json.dump(json_config, file, indent=4)
            return [True, f"Successfully saved configuration to {filepath}"]
        except:
            return [False, f"Failed while saving configuration to {filepath}"]

    def load_configuration_from_json(self, filepath: str) -> [bool, str]:
        try:
            if '/' not in filepath:
                if '.json' not in filepath:
                    filepath = "configurations/application/"+filepath+".json"
                else:
                    filepath = "configurations/application/" + filepath
            with open(filepath, "r") as file:
                json_config = json.load(file)
            if json_config['type'] == self.type:
                if self.load_global_configuration(self.deserialize_config(json_config['global_config']))[0]:
                    return [True, f"Successfully loaded configuration from {filepath}"]
                else:
                    return [False, f"Failed while loading configuration from {filepath}"]
            else:
                return [False, f"You're trying to load {json_config['type']} config to {self.type}"]
        except:
            return [False, f"Unexpected error occured while loading {filepath}"]

    def serialize_config(self, config: dict):
        serialized_config = {}
        for key in config:
            pre_arr = config[key]
            pre_arr[0] = config[key][0].__name__
            serialized_config[key] = pre_arr
        return serialized_config

    def deserialize_config(self, config: dict):
        deserialized_config = {}
        for key in config:
            pre_arr = config[key]
            pre_arr[0] = locate(config[key][0])
            deserialized_config[key] = pre_arr
        return deserialized_config


class AppConfiguration(Configuration):

    def __init__(self):
        super().__init__()
        self.type = "AppConfig"

        self.default_configuration = {
            "LIP": [str, "127.0.0.1", "local machine IP"],
            "TIP": [str, "127.0.0.1", "target machine IP"],
            "WORKDIR": [str, self.get_workdir(), "current workdir"],
            "USER": [str, self.get_user(), "current user"]
        }

    def get_workdir(self):
        workdir = os.path.abspath(os.getcwd())
        return workdir

    def get_user(self):
        username = os.environ.get('USER', os.environ.get('USERNAME'))
        return username

    def load_default_configuration(self) -> [bool, str]:
        if self.load_global_configuration(self.default_configuration)[0]:
            return [True, "Successfully loaded default configuration"]
        else:
            return [False, "Error occurred while loading default configuration"]


class ModuleConfiguration(Configuration):

    def __init__(self):
        super().__init__()
        self.type = "ModuleConfig"
