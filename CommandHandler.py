import main


class CommandHandler():

    def __init__(self, app: main.MainApp):
        self.app = app
        self.command_list = {
            "exit": [exit, "exit a program"],
            "updateconf": [app.list_configuration, "update app configuration display"],
            "help": [self.help_menu, "show help menu"]
        }

    def process_command(self, command: str):
        # self.app.write_pad(self.app.mainPad, command)
        if command in self.command_list:
            self.command_list[command][0]()
        else:
            self.app.write_pad(self.app.mainPad, f"Unknown command: {command}")

    def help_menu(self):
        self.app.write_pad(self.app.mainPad, "Available commands: \n")
        for key in self.command_list:
            self.app.write_pad(self.app.mainPad, key+" - "+self.command_list[key][1])
