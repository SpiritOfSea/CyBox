import os


class Configuration:

    def __init__(self):
        self.global_params = {}
        self.local_params = {}

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
                return [False, f"Error while loading global conf: {e.with_traceback()}"]
        return [True, "Loaded global configuration successfully"]


class AppConfiguration(Configuration):

    def __init__(self):
        super().__init__()

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
