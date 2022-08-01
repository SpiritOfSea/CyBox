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
                self.global_params[key] = [None, "", ""]
                raise TypeError

    def get_global(self, key):
        if key in self.global_params:
            return self.global_params[key][1:2]
        else:
            raise KeyError

    def get_all_globals(self):
        return self.global_params

    def load_global_configuration(self, configuration: dict):
        for key in configuration:
            try:
                val_type, value, descr = configuration[key]
                self.set_global(key, val_type, value, descr)
            except Exception as e:
                pass


class AppConfiguration(Configuration):

    def __init__(self):
        super().__init__()

        self.default_configuration = {
            "local_ip": [str, "127.0.0.1", "Local IP"],
            "target_ip": [str, "127.0.0.1", "Target IP"],
            "workdir": [str, "~/", "Workdir"],
            "user": [str, self.get_user(), "Current user"]
        }

    def get_user(self):
        return "kali"

    def load_default_configuration(self):
        self.load_global_configuration(self.default_configuration)


class ModuleConfiguration(Configuration):

    def __init__(self):
        super().__init__()
