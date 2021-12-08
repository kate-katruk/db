from .out import *

import os


class TermSizeSkeleton:

    def __init__(self):
        self.Update()

    def Update(self):
        self.RowsInt, self.ColumnsInt = map(int, os.popen('stty size', 'r').read().split())

    def Rows(self, Update=True):
        if Update: self.Update()
        return self.RowsInt

    def Columns(self, Update=True):
        if Update: self.Update()
        return self.ColumnsInt


TermSize = TermSizeSkeleton()
