import ConfigHandler
import ConfigHandler
import subprocess


class Module:
    def __init__(self, app, module="None"):
        self.app = app
        if module == "None":
            self.ModConfig = ConfigHandler.ModuleConfiguration()
            self.ModConfig.load_default_configuration()
        else:
            self.load_module(module)

    def process_command(self, action, arguments) -> str:
        action = self.ModConfig.action_list[action]

        command = action["command"]

        for key in action["arguments"]:
            if action["arguments"][key][0] == "appconf":
                command = command.replace(key, self.app.AppConfig.get_param(action["arguments"][key][1])[1])
            elif action["arguments"][key][0] == "modconf":
                command = command.replace(key, self.ModConfig.get_param(action["arguments"][key][1])[1])

        if action["type"] == "os":
            output = subprocess.check_output(command.split()).decode()
        else:
            output = "NO OUTPUT"

        return output

    def get_command_list(self):
        return self.ModConfig.action_list

    def load_module(self, module: str):
        pass

    def padprint(self, text: str):
        self.app.write_pad(self.app.mainPad, text)

    def clear_pad(self):
        self.app.mainPad.clear()
        self.app.mainPad.refresh()
