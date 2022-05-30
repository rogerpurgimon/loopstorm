#!/usr/bin/python3
# -*- encoding: latin-1 -*-

import os
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication

# A venv was created in the file env in the leonardbalm file,
# this is where the pip and the python3 is located


class LoopStormGUI(QMainWindow):
    loops = []

    def __init__(self):
        super().__init__()
        uic.loadUi("LoopStormInterface.ui", self)
        self.importLoops.clicked.connect(lambda: self.import_loops(self.loops, 3))
        self.deleteLoop.clicked.connect(lambda: self.remove_loop())
        self.exportMaster.clicked.connect(lambda: self.export_master())
        self.selectMaster.clicked.connect(lambda: self.select_loop(0))
        self.selectLoop1.clicked.connect(lambda: self.select_loop(1))
        self.selectLoop2.clicked.connect(lambda: self.select_loop(2))
        self.leftArrow.clicked.connect(lambda: self.arrow("left"))
        self.rightArrow.clicked.connect(lambda: self.arrow("right"))
        self.playButton.clicked.connect(lambda: self.play_button())

    def import_loops(self, loops, limit):
        """
        Loops only come from the loops folder. Modify that folder if we want to use different loops.
        1. Check amount of loop slots available (this should be represented in a list somewhere)
        2. Check amount of loops to import in the loops folder.
        3. If not enough slots pop-up window with a warning and import amount of loops possible.
        """
        current_file_loops = []
        directory = '../loops'

        # Filling an auxiliary list with all the loops in the loops file
        for filename in os.listdir(directory):
            arg = directory + "/" + filename
            loop = MonoLoader(filename=arg)
            current_file_loops.append(loop)

        # Checking if there are enough available slots
        if len(loops) + len(current_file_loops) > limit:
            raise ValueError("Not enough slots available! Remove some loops from LoopStorm or from the loops folder.")
        else:
            loops.append(current_file_loops)

        self.represent_loops()

    def represent_loops(self):
        """
        1. Check if a loop is selected.
        2. Erase loop data from the loops list somewhere.
        """
        self.generate_image()

    def generate_image(self):
        """
        1. Check if a loop is selected.
        2. Erase loop data from the loops list somewhere.
        """

    def remove_loop(self):
        """
        1. Check if a loop is selected.
        2. Erase loop data from the loops list somewhere.
        """

    def export_master(self):
        """
        1. Check if a loop is selected.
        2. Erase loop data from the loops list somewhere.
        """

    def select_loop(self, number):
        """
        1. Check if a loop is selected.
        2. Erase loop data from the loops list somewhere.
        """

    def arrow(self, direction):
        """
        1. Check if a loop is selected.
        2. Erase loop data from the loops list somewhere.
        """

    def play_button(self):
        """
        1. Check if a loop is selected.
        2. Erase loop data from the loops list somewhere.
        """


if __name__ == "__main__":
    app = QApplication(sys.argv)
    GUI = LoopStormGUI()
    GUI.show()
    sys.exit(app.exec_())
