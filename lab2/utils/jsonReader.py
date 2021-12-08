import json
import os

class JsonReader(object):
    """read any JSON"""

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, path = ''):

        if (len(path) != 0):
            if (os.path.isdir(path)):
                self.ROOT_DIR = path
            else:
                print(f'ERROR!   {path} doesn\'t exists')

    def getJsonObject(self, fileName):
        try:
            if (fileName.startswith('/')):
                with open(fileName, "r") as read_file:
                    return json.load(read_file)
            else:
                with open(self.ROOT_DIR + '/' + fileName, "r") as read_file:
                    return json.load(read_file)
        except Exception as err:
            print(f'ERROR! {err}')
            return {}