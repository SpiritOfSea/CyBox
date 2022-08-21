import os
import json
from pydoc import locate


class Configuration:

    def __init__(self):
        self.param_list = {
            "_WATCHLIST": [list, [], "watchlist"]
        }
        self.type = "DefaultConfig"
        self.json_config = {}

    def set_param(self, key: str, val_type: type, value, description="") -> bool:
        if isinstance(value, val_type):
            self.param_list[key] = [val_type, value, description]
            return True
        else:
            try:
                self.param_list[key] = [val_type, val_type(value), description]
                return True
            except Exception as e:
                return False

    def update_param(self, key: str, value) -> [bool, str]:
        if key in self.param_list:
            try:
                self.param_list[key][1] = self.param_list[key][0](value)
                return [True, f"Successfully set {key} to {value}"]
            except Exception as e:
                return [False, f"'{value}' is not {self.param_list[key][0]} type"]
        else:
            return [False, f"There is no {key} global variable available"]

    def get_param(self, key):
        if key in self.param_list:
            return self.param_list[key]
        else:
            raise KeyError

    def get_all_params(self):
        return self.param_list

    def add_watch(self, key: str) -> [bool, str]:
        if not key.startswith("_"):
            if key in self.param_list:
                self.param_list["_WATCHLIST"][1].append(key)
                return [True, f"Successfully added {key} to watchlist"]
            else:
                return [False, f"No such key in configuration: {key}"]
        else:
            return [False, "You cannot watch private params"]

    def delete_watch(self, key: str) -> [bool, str]:
        if key in self.param_list:
            self.param_list["_WATCHLIST"][1].remove(key)
            return [True, f"Successfully deleted {key} from watchlist"]
        else:
            return [False, f"No such key in configuration: {key}"]

    def load_param_list(self, param_list: dict) -> [bool, str]:
        for key in param_list:
            try:
                val_type, value, descr = param_list[key]
                self.set_param(key, val_type, value, descr)
            except Exception as e:
                return [False, f"Error while loading global configuration"]
        return [True, "Loaded global configuration successfully"]

    def save_configuration_to_json(self, filepath: str) -> [bool, str]:
        try:
            if '/' not in filepath:
                if '.json' not in filepath:
                    filepath = f"configurations/{self.type}/" + filepath + ".json"
                else:
                    filepath = f"configurations/{self.type}/" + filepath
            with open(filepath, "w") as file:
                json.dump(self.json_config, file, indent=4)
            return [True, f"Successfully saved configuration to {filepath}"]
        except:
            return [False, f"Failed while saving configuration to {filepath}"]

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
            "USER": [str, self.get_user(), "current user"],
            "_WATCHLIST": [list, ["LIP", "TIP", "WORKDIR", "USER"], "watchlist"]
        }

    def get_workdir(self):
        workdir = os.path.abspath(os.getcwd())
        return workdir

    def get_user(self):
        username = os.environ.get('USER', os.environ.get('USERNAME'))
        return username

    def load_default_configuration(self) -> [bool, str]:
        if self.load_param_list(self.default_configuration)[0]:
            return [True, "Successfully loaded default configuration"]
        else:
            return [False, "Error occurred while loading default configuration"]

    def load_configuration_from_json(self, filepath: str) -> [bool, str]:
        try:
            if '/' not in filepath:
                if '.json' not in filepath:
                    filepath = f"configurations/{self.type}/" + filepath + ".json"
                else:
                    filepath = f"configurations/{self.type}/" + filepath
            with open(filepath, "r") as file:
                json_config = json.load(file)
            if json_config['type'] == self.type:
                if self.load_param_list(self.deserialize_config(json_config['params']))[0]:
                    return [True, f"Successfully loaded configuration from {filepath}"]
                else:
                    return [False, f"Failed while loading configuration from {filepath}"]
            else:
                return [False, f"You're trying to load {json_config['type']} config to {self.type}"]
        except:
            return [False, f"Unexpected error occurred while loading {filepath}"]

    def save_configuration_to_json(self, filepath: str) -> [bool, str]:
        self.json_config = {"type": self.type,
                            "params": self.serialize_config(self.param_list)}
        return super().save_configuration_to_json(filepath)


class ModuleConfiguration(Configuration):

    def __init__(self):
        super().__init__()
        self.type = "ModuleConfig"
        self.action_list = {}
        self.pipe_list = {}
        self.default_configuration = {
            # "params": {},
            # "actions": {
            #     # "test": {"type": "os",
            #     #          "command": "echo '%USER% %NAME%'",
            #     #          "description": "echo random info",
            #     #          "arguments": {     # %placeholder%: [%conf_type%, %param_name%, %can_be_piped%]
            #     #              "%USER%": ["appconf", "USER", False],
            #     #          }
            # },
            # "pipes": {
            #     # "test_pipe": [     # [%target_module%, %command%, %print_result%, %takes_pipe%, ~%piped_param%
            #     #     ["self", "lswdir", False, False],
            #     #     ["self", "test", True, True, "%NAME%"]
            #     # ]
            # }
        }

    def load_default_configuration(self):
        self.load_param_list(self.default_configuration["params"])
        self.action_list = self.default_configuration["actions"]
        self.pipe_list = self.default_configuration["pipes"]

    def save_configuration_to_json(self, filepath: str) -> [bool, str]:
        self.json_config = {"type": self.type,
                            "params": self.serialize_config(self.param_list),
                            "actions": self.action_list,
                            "pipes": self.pipe_list}
        return super().save_configuration_to_json(filepath)

    def load_configuration_from_json(self, filepath: str) -> [bool, str]:
        try:
            if '/' not in filepath:
                if '.json' not in filepath:
                    filepath = f"configurations/{self.type}/" + filepath + ".json"
                else:
                    filepath = f"configurations/{self.type}/" + filepath
            with open(filepath, "r") as file:
                json_config = json.load(file)
            if json_config['type'] == self.type:
                self.load_param_list(self.deserialize_config(json_config['params']))
                self.action_list = json_config["actions"]
                self.pipe_list = json_config["pipes"]
                return [True, f"Module {self.get_param('NAME')[1]} successfully loaded"]
            else:
                return [False, f"You're trying to load {json_config['type']} config to {self.type}"]
        except:
            return [False, f"Unexpected error occurred while loading {filepath}"]

