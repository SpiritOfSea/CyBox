import curses
from curses.textpad import Textbox, rectangle
import time


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

    def initialize(self):
        curses.wrapper(self.main_routine)

    def prepare_pads(self):
        curses.echo()

        self.mainPad = curses.newwin(curses.LINES-2, curses.COLS-2-self.infocol_width, 0, 0)
        self.logoPad = curses.newwin(self.infocol_div_height+1, self.infocol_width,
                                     0, curses.COLS-1-self.infocol_width)
        self.infoPad = curses.newwin(curses.LINES-self.infocol_div_height, self.infocol_width,
                                     self.infocol_div_height, curses.COLS-1-self.infocol_width)
        self.inputPad = curses.newwin(2, curses.COLS-1-self.infocol_width, curses.LINES-2, 0)

        self.infoPad.scrollok(True)
        self.mainPad.scrollok(True)
        self.logoPad.scrollok(True)
        self.inputPad.scrollok(True)

        self.rewrite_pad(self.logoPad, self.logo)
        self.rewrite_pad(self.inputPad, "> ")

        self.infoPad.box()
        self.infoPad.refresh()
        self.logoPad.box()
        self.logoPad.refresh()

    def main_routine(self, screen):
        self.mainWindow = screen
        self.prepare_pads()

        while True:
            self.wait_for_command()
            # for i in range(1, 10):
            #     self.write_pad(self.mainPad, i*10)
            #     self.write_pad(self.infoPad, i*10)
            #     time.sleep(0.01)
            # self.wait_for_input()

    def wait_for_command(self):
        s = self.inputPad.getstr().decode()
        self.rewrite_pad(self.inputPad, "> ")
        if s == "exit" or s == b'exit':
            exit()
        self.write_pad(self.mainPad, s)
        self.inputPad.move(0, 2)

    def write_pad(self, pad, text):
        pad.addstr(str(text))
        pad.refresh()

    def rewrite_pad(self, pad, text):
        pad.clear()
        pad.addstr(str(text))
        pad.refresh()


if __name__ == "__main__":
    app = MainApp()
    app.initialize()
