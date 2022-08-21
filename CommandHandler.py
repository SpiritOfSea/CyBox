import main
import os


class CommandHandler:

    def __init__(self, app: main.MainApp):
        self.app = app

        # Syntax: "command": [function, description, takesArgument, minArg, maxArg]
        self.command_list = {
            "exit": [exit, "exit a program", False],
            "help": [self.help_menu, "show help menu; 'help ARTICLE' to get specified help", True, 0, 1],
            "set": [self.update_param, "'VARIABLE VALUE' set global variable to specified value", True, 2, 2],
            "conf": [self.conf_handler, "'reset|ls|save|load CONFNAME' configuration handler", True, 1, 2],
            "save": [self.save_module, "'CONFNAME' save module state to CONFNAME", True, 1, 1],
            "load": [self.load_module, "'CONFNAME' load module", True, 1, 1],
            "clear": [self.clear_pad, "clear display", False],
            "watch": [self.watch, "'add|del TARGET KEY', add param to watchlist", True, 3, 3],
        }

    def padprint(self, text: str):
        self.app.write_pad(self.app.mainPad, text)

    def process_command(self, command: str):
        main_command, arguments = command.split()[0].lower(), command.split()[1:]
        if main_command in self.command_list:
            if self.command_list[main_command][2] and arguments:
                if self.command_list[main_command][3] <= len(arguments) <= self.command_list[main_command][4]:
                    return self.command_list[main_command][0](arguments)
                else:
                    return f"Provided {len(arguments)} arguments, needed [{self.command_list[main_command][3]}:{self.command_list[main_command][4]}]"
            elif self.command_list[main_command][2] and not arguments:
                if self.command_list[main_command][3] == 0:
                    return self.command_list[main_command][0]()
                else:
                    return "Please, provide arguments"
            elif not self.command_list[main_command][2] and arguments:
                return "Provided unknown arguments"
            else:
                return self.command_list[main_command][0]()
        elif main_command in self.app.CurrentModule.get_command_list():
            return self.app.CurrentModule.process_command(main_command, arguments)
        elif main_command in self.app.CurrentModule.get_pipe_list():
            return self.app.CurrentModule.process_pipe(main_command)
        else:
            return f"Unknown command: {main_command}"

    def help_menu(self, item=None) -> str:
        if item == ['params']:
            output = "List of app parameters:\n"
            for key in self.app.AppConfig.param_list:
                output += key + " - " + self.app.AppConfig.param_list[key][2]+"\n"
            output += "===========\n"
            output += "List of module parameters:\n"
            for key in self.app.CurrentModule.ModConfig.param_list:
                output += key + " - " + self.app.CurrentModule.ModConfig.param_list[key][2]+"\n"
        else:
            output = "Available app commands:\n"
            for key in sorted(self.command_list):
                output += key + " - " + self.command_list[key][1] + "\n"
            output += "===========\n"
            output += "Available module commands:\n"
            for key in sorted(self.app.CurrentModule.get_command_list()):
                output += key + " - " + self.app.CurrentModule.get_command_list()[key]['description'] + "\n"
            output += "===========\n"
            output += "Available pipes:"
            for key in sorted(self.app.CurrentModule.get_pipe_list()):
                output += "\n" + key + ":"
                for cmd in self.app.CurrentModule.get_pipe_list()[key]:
                    output += "\n    - " + cmd[1]
            output += "\n"
        return output

    def update_param(self, arguments: [str, str]) -> str:
        result, output = self.app.AppConfig.update_param(arguments[0], arguments[1])
        if not result:
            output = self.app.CurrentModule.ModConfig.update_param(arguments[0], arguments[1])[1]
        self.app.update_infopad()
        return output

    def conf_handler(self, arguments) -> str:
        if arguments[0] == "reset":
            output = self.app.AppConfig.load_default_configuration()[1]
            self.app.update_infopad()
        elif arguments[0] == "load":
            if len(arguments) == 2:
                output = self.app.AppConfig.load_configuration_from_json(arguments[1])[1]
                self.app.update_infopad()
            else:
                output = "Please, provide CONFNAME to load"
        elif arguments[0] == "save":
            if len(arguments) == 2:
                output = self.app.AppConfig.save_configuration_to_json(arguments[1])[1]
            else:
                output = "Please, provide CONFNAME to save"
        elif arguments[0] == "ls":
            output = "Configuration files in 'configurations/application' directory:"
            for file in os.listdir("configurations/application"):
                output += file + "\n"
        else:
            output = "Please, use 'reset', 'ls', 'load' or 'save' methods"

        return output

    def save_module(self, arguments) -> str:
        if len(arguments) == 1:
            output = self.app.CurrentModule.save_module(arguments[0])[1]
        else:
            output = "Please, provide correct CONFNAME to save"
        return output

    def load_module(self, arguments) -> str:
        if len(arguments) == 1:
            output = self.app.CurrentModule.load_module(arguments[0])[1]
            self.app.update_infopad()
        else:
            output = "Please, provide CONFNAME to load"
        return output

    def clear_pad(self)->str:
        self.app.mainPad.clear()
        self.app.mainPad.refresh()

        return ""

    def watch(self, arguments: [str, str, str]) -> str:
        mode = arguments[0]
        if not mode == "add" and not mode == "del":
            return "Please, use 'add' or 'del' methods"
        target = arguments[1]
        key = arguments[2]
        if target == "app":
            if mode == "add":
                output = self.app.AppConfig.add_watch(key)[1]
            else:
                output = self.app.AppConfig.delete_watch(key)[1]
            self.app.update_infopad()
        elif target == "module":
            if mode == "add":
                output = self.app.CurrentModule.add_watch(key)[1]
            else:
                output = self.app.CurrentModule.delete_watch(key)[1]
            self.app.update_infopad()
        else:
            output = "Please, provide correct target: 'app' or 'module'"

        return output
