import tkinter as tk
from database import Database

class BrowseLibrary:
    def __init__(self, root, username):
        self.name = username
        self.root = root

        #