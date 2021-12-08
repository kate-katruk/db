import sys
sys.path.append('../')
import math
from controllers.readerController import ReaderController
from models.readers import Reader
from cui import CUI

class ReaderView:
    def __init__(self):
        self.currentMenu = [None, None]
        self.page = 1
        self.per_page = 10

        self.CUI = CUI("Reader model menu")
        self.readerController = ReaderController()
        self.CUI.addField('Add Reader', lambda: self.__addReaders())
        self.CUI.addField('Generate rows', lambda: self.__generateRows())
        self.CUI.addField('Readers', lambda: self.__getReaders())

    def run(self):
        self.CUI.run()

    def __generateRows(self):
        try:
            rowsNum = int(input('Enter rows num: '))
            if not (isinstance(rowsNum, int) and rowsNum > 0):
                raise Exception('Invalid input')
            self.CUI.setError('   Please wait! Rows are generating...   ')
            time = self.readerController.generateRows(rowsNum)
            self.CUI.setError('   Rows generated! Elapsed time: ' + time)
        except Exception as error:
            self.CUI.setError(str(error))

    def __addReaders(self):
        try:
            result = self.readerController.add()
            if isinstance(result, bool) and not result: raise Exception('Inccorect values')
            else: self.CUI.setError('New Reader id: ' + str(result))
        except Exception as err:
            self.CUI.setError(str(err))

    def __changePageParams(self, page: int, per_page: int):
        self.page = page
        self.per_page = per_page
        self.currentMenu[0].stop()
        self.__getReaders()

    def __getReaders(self):
        readersMenu = CUI('Readers')
        self.currentMenu[0] = readersMenu
        try:
            if self.page < math.ceil(self.readerController.getCount() / self.per_page):
                readersMenu.addField('NEXT', lambda: self.__changePageParams(self.page + 1, self.per_page))
            if self.page > 1:
                readersMenu.addField('PREV', lambda: self.__changePageParams(self.page - 1, self.per_page))
            readers = self.readerController.getAll(self.page, self.per_page)
            for reader in readers:
                readersMenu.addField(f"<{reader.reader_id}>{reader.name}", lambda reader_id=reader.reader_id: self.__getReader(reader_id))

        except Exception as err:
            readersMenu.setError(str(err))
        readersMenu.run('Return to main menu')

    def __updateReader(self, id: int):
        if self.readerController.update(id):
            self.currentMenu[1].stop()
            self.__getReader(id)
        else:
            self.currentMenu[1].setError('Incorrect update values')

    def __deleteReader(self, id: int):
        self.readerController.delete(id)
        self.currentMenu[1].stop()
        self.__supportCUIFunc()

    def __supportCUIFunc(self):
        self.currentMenu[1].stop()
        self.__changePageParams(self.page, self.per_page)

    def __getReader(self, id: int):
        readerMenu = CUI('Reader menu')
        self.currentMenu[1] = readerMenu
        try:
            reader: Reader = self.readerController.getById(id)
            values = reader.getValues().split(',')
            keys = reader.getKeys().split(',')
            for i in range(len(keys)):
                if i == 0:
                    continue
                readerMenu.addField(keys[i] + ' : ' + values[i])

            readerMenu.addField('DELETE', lambda: self.__deleteReader(reader.reader_id))
            readerMenu.addField('UPDATE', lambda: self.__updateReader(reader.reader_id))
            readerMenu.addField('Return to prev menu', lambda: self.__supportCUIFunc())
        except Exception as err:
            readerMenu.setError(str(err))
        readerMenu.run(False)