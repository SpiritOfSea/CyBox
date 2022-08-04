import main


class CommandHandler():

    def __init__(self, app: main.MainApp):
        self.app = app

        # Syntax: "command": [function, desription, takesArgument, minArg, maxArg]
        self.command_list = {
            "exit": [exit, "exit a program", False],
            "updateconf": [self.app.update_infoPad, "update app configuration display", False],
            "help": [self.help_menu, "show help menu", True, 0, 1],
            "setglob": [self.update_global, "'VARIABLE VALUE' set global variable to specified value", True, 2, 2],
            "resetconf": [self.reset_configuration, "set configuration to default", False],
            "clear": [self.clear_pad, "clear display", False]
        }

    def padprint(self, text: str):
        self.app.write_pad(self.app.mainPad, text)

    def process_command(self, command: str):
        main_command, arguments = command.split()[0].lower(), command.split()[1:]
        if main_command in self.command_list:
            if self.command_list[main_command][2] and arguments:
                if self.command_list[main_command][3] <= len(arguments) <= self.command_list[main_command][4]:
                    self.command_list[main_command][0](arguments)
                else:
                    self.padprint(f"Provided {len(arguments)} arguments, needed [{self.command_list[main_command][3]}:{self.command_list[main_command][4]}]")
            elif self.command_list[main_command][2] and not arguments:
                if self.command_list[main_command][3] == 0:
                    self.command_list[main_command][0]()
                else:
                    self.padprint("Please, provide arguments")
            elif not self.command_list[main_command][2] and arguments:
                self.padprint("Provided unknown arguments")
            else:
                self.command_list[main_command][0]()
        else:
            self.padprint(f"Unknown command: {main_command}")

    def help_menu(self, item=None):
        if item is None:
            self.padprint("Available commands:")
            for key in sorted(self.command_list):
                self.padprint(key+" - "+self.command_list[key][1])
        elif item == ['glob']:
            self.padprint("Global variables:")
            for key in self.app.AppConfig.global_params:
                self.padprint(key + " - "+self.app.AppConfig.global_params[key][2])

    def update_global(self, arguments: [str, str]):
        self.padprint(self.app.AppConfig.update_global(arguments[0], arguments[1])[1])
        self.app.update_infoPad()

    def reset_configuration(self):
        self.padprint(self.app.AppConfig.load_default_configuration()[1])
        self.app.update_infoPad()

    def clear_pad(self):
        self.app.mainPad.clear()
        self.app.mainPad.refresh()
