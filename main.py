import curses
from curses.textpad import Textbox, rectangle
import time
from ConfigHandler import *
import CommandHandler


class MainApp:
    def __init__(self):
        self.infocol_width = 24
        self.infocol_div_height = 9
        self.logo = """
  ___  _  _  ____
 / __)( \/ )(  _ \     
( (__  \  /  ) _ <     
 \___) (__) (____/     
     ____  _____  _  _ 
    (  _ \(  _  )( \/ )
     ) _ < )(_)(  )  ( 
    (____/(_____)(_/\_)
"""
        self.AppConfig = AppConfiguration()
        self.AppConfig.load_default_configuration()
        self.CurrentModuleConfig = ModuleConfiguration()
        self.CommandHandler = CommandHandler.CommandHandler(self)

    def initialize(self):
        curses.wrapper(self.main_routine)

    def prepare_pads(self):
        curses.echo()

        # Initialize colors
        curses.start_color()
        curses.use_default_colors()
        for i in range(0, curses.COLORS):
            curses.init_pair(i + 1, i, -1)

        # Initialize pads
        self.mainPad = curses.newwin(curses.LINES-2, curses.COLS-2-self.infocol_width, 0, 0)
        self.logoPad = curses.newwin(self.infocol_div_height, self.infocol_width,
                                     0, curses.COLS-1-self.infocol_width)
        self.infoPad = curses.newwin(curses.LINES-self.infocol_div_height, self.infocol_width,
                                     self.infocol_div_height, curses.COLS-1-self.infocol_width)
        self.inputPad = curses.newwin(2, curses.COLS-1-self.infocol_width, curses.LINES-2, 0)

        # Allow scroll
        self.infoPad.scrollok(True)
        self.mainPad.scrollok(True)
        self.logoPad.scrollok(True)
        self.inputPad.scrollok(True)

        # Prepare default content
        self.rewrite_pad(self.logoPad, self.logo)
        self.rewrite_pad(self.inputPad, "> ")
        self.list_configuration()

        # Place cursor to inputPad
        self.inputPad.move(0, 2)


        # self.mainPad.border(1,"#",1,1,1,1,1,1)
        # self.mainPad.refresh()

        # self.infoPad.box()
        # self.infoPad.refresh()
        # self.logoPad.box()
        # self.logoPad.refresh()

    def main_routine(self, screen):
        self.mainWindow = screen
        self.prepare_pads()

        while True:
            self.wait_for_command()

    def wait_for_command(self):
        command = self.inputPad.getstr().decode()
        self.rewrite_pad(self.inputPad, "> ")
        self.CommandHandler.process_command(command)
        self.inputPad.move(0, 2)

    def write_pad(self, pad, text, sameline=False, color=0):
        if sameline:
            pad.addstr(str(text), curses.color_pair(color))
        else:
            pad.addstr(str(text)+"\n", curses.color_pair(color))
        pad.refresh()

    def rewrite_pad(self, pad, text):
        pad.clear()
        pad.addstr(str(text))
        pad.refresh()

    def list_configuration(self):
        current_app_config = self.AppConfig.get_all_globals()
        current_module_config = self.CurrentModuleConfig.get_all_globals()
        self.infoPad.clear()
        self.write_pad(self.infoPad, "=====")
        for key in current_app_config:
            self.write_pad(self.infoPad, current_app_config[key][2]+": ", True, 2)
            self.write_pad(self.infoPad, str(current_app_config[key][1]))
        self.write_pad(self.infoPad, "=====")
        for key in current_module_config:
            self.write_pad(self.infoPad, current_module_config[key][2] + ": " + str(current_module_config[key][1]))
        # self.infoPad.box()
        # self.infoPad.refresh()


if __name__ == "__main__":
    app = MainApp()
    app.initialize()
