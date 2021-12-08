import sys
sys.path.append('../')
import math
from controllers.exemplarController import ExemplarController
from models.exemplars import Exemplar
from cui import CUI

class ExemplarView:
    def __init__(self):
        self.currentMenu = [None, None]
        self.page = 1
        self.per_page = 10

        self.CUI = CUI("Exemplar model menu")
        self.exemplarController = ExemplarController()
        self.CUI.addField('Add Exemplar', lambda: self.__addExemplars())
        self.CUI.addField('Generate rows', lambda: self.__generateRows())
        self.CUI.addField('Exemplars', lambda: self.__getExemplars())

    def run(self):
        self.CUI.run()

    def __generateRows(self):
        try:
            rowsNum = int(input('Enter rows num: '))
            if not (isinstance(rowsNum, int) and rowsNum > 0):
                raise Exception('Invalid input')
            self.CUI.setError('   Please wait! Rows are generating...   ')
            time = self.exemplarController.generateRows(rowsNum)
            self.CUI.setError('   Rows generated! Elapsed time: ' + time)
        except Exception as error:
            self.CUI.setError(str(error))

    def __addExemplars(self):
        try:
            result = self.exemplarController.add()
            if isinstance(result, bool) and not result: raise Exception('Inccorect values')
            else: self.CUI.setError('New Exemplar id: ' + str(result))
        except Exception as err:
            self.CUI.setError(str(err))

    def __changePageParams(self, page: int, per_page: int):
        self.page = page
        self.per_page = per_page
        self.currentMenu[0].stop()
        self.__getExemplars()

    def __getExemplars(self):
        exemplarsMenu = CUI('Exemplar')
        self.currentMenu[0] = exemplarsMenu
        try:
            if self.page < math.ceil(self.exemplarController.getCount() / self.per_page):
                exemplarsMenu.addField('NEXT', lambda: self.__changePageParams(self.page + 1, self.per_page))
            if self.page > 1:
                exemplarsMenu.addField('PREV', lambda: self.__changePageParams(self.page - 1, self.per_page))
            exemplars = self.exemplarController.getAll(self.page, self.per_page)
            for exemplar in exemplars:
                exemplarsMenu.addField(f"<{exemplar.exemplar_id}>", lambda exemplar_id=exemplar.exemplar_id: self.__getExemplar(exemplar_id))

        except Exception as err:
            exemplarsMenu.setError(str(err))
        exemplarsMenu.run('Return to main menu')

    def __updateExemplar(self, id: int):
        if self.exemplarController.update(id):
            self.currentMenu[1].stop()
            self.__getExemplar(id)
        else:
            self.currentMenu[1].setError('Incorrect update values')

    def __deleteExemplar(self, id: int):
        self.exemplarController.delete(id)
        self.currentMenu[1].stop()
        self.__supportCUIFunc()

    def __supportCUIFunc(self):
        self.currentMenu[1].stop()
        self.__changePageParams(self.page, self.per_page)

    def __getExemplar(self, id: int):
        exemplarMenu = CUI('Exemplar menu')
        self.currentMenu[1] = exemplarMenu
        try:
            exemplar: Exemplar = self.exemplarController.getById(id)
            values = exemplar.getValues().split(',')
            keys = exemplar.getKeys().split(',')
            for i in range(len(keys)):
                exemplarMenu.addField(keys[i] + ' : ' + values[i])

            exemplarMenu.addField('DELETE', lambda: self.__deleteExemplar(exemplar.exemplar_id))
            exemplarMenu.addField('UPDATE', lambda: self.__updateExemplar(exemplar.exemplar_id))
            exemplarMenu.addField('Return to prev menu', lambda: self.__supportCUIFunc())
        except Exception as err:
            exemplarMenu.setError(str(err))
        exemplarMenu.run(False)