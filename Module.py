import ConfigHandler
import subprocess
from pathlib import Path


class Module:
    def __init__(self, app, module="None"):
        self.app = app
        self.ModConfig = ConfigHandler.ModuleConfiguration()
        self.load_module(module)

    def process_command(self, action_key, arguments=None) -> str:
        action = self.ModConfig.action_list[action_key]
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

        if action["loggable"]:
            self.write_log(action_key, output)

        return output

    def process_pipe(self, pipename) -> str:
        if pipename not in self.ModConfig.pipe_list:
            return f"No such pipe: {pipename}"

        output = ""
        last_output = ""
        pipe_stdout = ""

        for action in self.ModConfig.pipe_list[pipename]:
            if action["target"] == "self":
                if action["takes_pipe"]:
                    pipe_stdout = self.process_command(action["command"], {action["piped_param"]: pipe_stdout})
                else:
                    pipe_stdout = self.process_command(action["command"])
            elif action["target"] == "app":
                if action["takes_pipe"]:
                    command = action["command"].replace("%PIPE%", pipe_stdout)
                else:
                    command = action["command"]
                pipe_stdout = self.app.CommandHandler.process_command(command)
            if action["printable"] and last_output != pipe_stdout:
                output += pipe_stdout
                last_output = pipe_stdout
        return output.strip()+"\n"

    def get_command_list(self):
        return self.ModConfig.action_list

    def get_pipe_list(self):
        return self.ModConfig.pipe_list

    def load_module(self, module: str) -> [bool, str]:
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
        return self.ModConfig.load_configuration_from_json(module)

    def save_module(self, module: str) -> [bool, str]:
        return self.ModConfig.save_configuration_to_json(module)

    def padprint(self, text: str):
        self.app.write_pad(self.app.mainPad, text)

    def clear_pad(self):
        self.app.mainPad.clear()
        self.app.mainPad.refresh()

    def write_log(self, target, content) -> bool:
        wdir = self.app.AppConfig.get_workdir()
        file = Path(wdir+"/"+target)
        counter = 0
        while file.is_file():
            file=Path(wdir+"/"+target+"_"+str(counter))
            counter += 1
        with open(file, "w") as file:
            file.write(content)

        return True
