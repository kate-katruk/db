import os
import sys

# custom import
sys.path.append("../venv/Scripts/python.exe")
import utils.console as console
import cui.menuTree as tree


class CUI(object):

    def __setBreakStatus(self, status: bool):
        self.__isBreakON = status

    def __init__(self, mainMenuTitle='Main menu'):
        self.root = tree.Node(mainMenuTitle, lambda: 0)
        self.__currentNode = self.root

        # support:
        self.__BREAK_NODE = tree.Node("BREAK", lambda: self.__setBreakStatus(False))
        self.__EMPTY_NODE = tree.Node("", lambda: 0)

        # private fields:
        self.__currentPos = 1
        self.__isBreakON = True
        self.__error = ''

    def __print(self):
        console.clear()
        # custom items
        print(f'-------{self.__currentNode.title}------- ' + self.__error)
        for i in range(len(self.__currentNode.childs)):
            if i == self.__currentPos - 1:
                console.printBold(f'[{self.__currentNode.childs[i].title}]')
            else:
                print(f'[{self.__currentNode.childs[i].title}]')

    def __inputController(self):
        return console.getch()

    def __stepController(self, char):
        upperLimit: int = len(self.__currentNode.childs)
        charCode: int = ord(char.lower())
        if (charCode == 119 or charCode == 97) and self.__currentPos > 1: self.__currentPos += -1
        if (charCode == 115 or charCode == 98) and self.__currentPos < upperLimit: self.__currentPos += 1
        if charCode == 10 or charCode == 13:  self.__currentNode.childs[self.__currentPos - 1].on_press()

    def __goToCurrentNode(self):
        self.__currentNode = self.__currentNode.childs[self.__currentPos - 1]
        self.__currentPos = 1

    def __goToParent(self):
        self.__currentNode = self.__currentNode.root
        self.__currentPos = 1

    # public fields:
    def run(self, *args):
        self.__currentNode = self.root
        exit_str = "EXIT"
        if len(args) > 0 and isinstance(args[0], str): exit_str = args[0]
        if not (len(args) > 0 and isinstance(args[0], bool) and args[0] is False):
            self.__currentNode.append(exit_str, lambda: self.__setBreakStatus(False))

        while (self.__isBreakON):
            self.__print()
            self.__stepController(self.__inputController())
        console.clear()

    def addField(self, title, *args):
        if len(args) > 0:
            self.__currentNode.append(title, args[0])
        else:
            self.__currentNode.append(title, lambda: 0)

    def addMenu(self, title):
        newNode = tree.Node(title, lambda: self.__goToCurrentNode())
        newNode.append("Return to prev Menu", lambda: self.__goToParent())
        self.__currentNode.append(newNode)
        self.__currentNode = newNode

    def finishMenu(self):
        if self.__currentNode.root != None:
            self.__goToParent()

    def renameField(self, current: str, new: str):
        try:
            if len(current) > 0 and len(new) > 0:
                if self.__currentNode.title == current:
                    self.__currentNode.title = new

                for i in range(len(self.__currentNode.childs)):
                    if self.__currentNode.childs[i].title == current:
                        self.__currentNode.childs[i].title = new
            else:
                raise Exception('Invalid title')
        except Exception as err:
            print("Error! ", err)

    def deleteField(self, title: str):
        try:
            if len(title) > 0:

                for i in range(len(self.__currentNode.childs)):
                    if self.__currentNode.childs[i].title == title:
                        del self.__currentNode.childs[i]
            else:
                raise Exception('Invalid title')
        except Exception as err:
            print("Error! ", err)

    def setError(self, err: str):
        self.__error = err

    def stop(self):
        self.__setBreakStatus(False)
