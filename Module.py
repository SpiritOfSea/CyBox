import ConfigHandler
import subprocess


class Module:
    def __init__(self, app, module="None"):
        self.app = app
        self.ModConfig = ConfigHandler.ModuleConfiguration()
        self.load_module(module)

    def process_command(self, action, arguments=None) -> str:
        action = self.ModConfig.action_list[action]
        output = ""
        command = action["command"]
        for key in action["arguments"]:
            if action["arguments"][key][2] and arguments and key in arguments:
                command = command.replace(key, arguments[key])
            elif action["arguments"][key][0] == "appconf":
                command = command.replace(key, self.app.AppConfig.get_param(action["arguments"][key][1])[1])
            elif action["arguments"][key][0] == "modconf":
                command = command.replace(key, self.ModConfig.get_param(action["arguments"][key][1])[1])

        if action["type"] == "os":
            output += subprocess.check_output(command, shell=True).decode()
        else:
            output += "NO OUTPUT"
        return output

    def process_pipe(self, pipename) -> str:
        if pipename not in self.ModConfig.pipe_list:
            return f"No such pipe: {pipename}"

        output = ""
        last_output = ""
        pipe_stdout = ""

        for action in self.ModConfig.pipe_list[pipename]:
            if action[0] == "self":
                if action[3]:
                    pipe_stdout = self.process_command(action[1], {action[4]: pipe_stdout})
                else:
                    pipe_stdout = self.process_command(action[1])
            elif action[0] == "app":
                if action[3]:
                    command = action[1].replace("%PIPE%", pipe_stdout)
                else:
                    command = action[1]
                pipe_stdout = self.app.CommandHandler.process_command(command)
            if action[2] and last_output != pipe_stdout:
                output += pipe_stdout
                last_output = pipe_stdout
        return output.strip()+"\n"

    def get_command_list(self):
        return self.ModConfig.action_list

    def get_pipe_list(self):
        return self.ModConfig.pipe_list

    def load_module(self, module: str) -> [bool, str]:
        return self.ModConfig.load_configuration_from_json(module)

    def save_module(self, module: str) -> [bool, str]:
        return self.ModConfig.save_configuration_to_json(module)

    def padprint(self, text: str):
        self.app.write_pad(self.app.mainPad, text)

    def clear_pad(self):
        self.app.mainPad.clear()
        self.app.mainPad.refresh()
