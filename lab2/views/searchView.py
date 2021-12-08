import sys
import math
import time
sys.path.append('../')

from controllers.searchController import SearchController
from cui import CUI

class SearchView:
    def __init__(self):
        self.currentMenu = None
        self.page = 1
        self.per_page = 10
        self.reader_id = None
        self.book_id = None
        self.exemplar_id = None

        self.CUI = CUI("Search menu")
        self.searchController = SearchController()
        self.CUI.addField('Search all books of the reader', lambda: self.__getBooksByReader())
        self.CUI.addField('Search readers of the book', lambda: self.__getReadersByBook())
        self.CUI.addField('Search all exemplars which id less than input value:', lambda: self.__getSomeExemplars())

    def run(self):
        self.CUI.run()

    def __changePageParams(self, page: int, per_page: int):
        self.page = page
        self.per_page = per_page
        self.currentMenu.stop()
        self.__getBooksByReader()

    def __exitMenu(self):
        self.reader_id = None
        self.book_id = None
        self.exemplar_id = None
        self.page = 1
        self.per_page = 10
        self.currentMenu.stop()

    def __getBooksByReader(self):
        searchMenu = CUI('Books which read by reader')
        self.currentMenu = searchMenu
        try:
            reader_id = int(input('Enter book id: '))
            if not (isinstance(reader_id, int) and reader_id > 0):
                    raise Exception('Invalid input')

            startTime = time.time()
            allRecords = self.searchController.getBooksByReader(reader_id)
            endTime = time.time()

            searchMenu.setError('\nElapsed time: ' + str(endTime - startTime)[:9] + 's'
                                '\nRows num: ' + str(len(allRecords)))

            if self.page < math.ceil(len(allRecords) / self.per_page):
                searchMenu.addField('NEXT', lambda: self.__changePageParams(self.page + 1, self.per_page))
            if self.page > 1:
                searchMenu.addField('PREV', lambda: self.__changePageParams(self.page - 1, self.per_page))

            searchMenu.addField('<ID> | Book name | Publishing | Year')
            for record in allRecords:
                searchMenu.addField(f"<{record[0]}> {record[1]} {record[2]} {record[3]}")

        except Exception as err:
            searchMenu.setError(str(err))

        searchMenu.addField('Return to prev menu', lambda: self.__exitMenu())
        searchMenu.run(False)

    def __getReadersByBook(self):
        searchMenu = CUI('Readers of the book')
        self.currentMenu = searchMenu
        try:
            book_id = int(input('Enter book id: '))

            if not (isinstance(book_id, int) and book_id > 0):
                raise Exception('Invalid input')

            startTime = time.time()
            allRecords = self.searchController.getReadersByBook(book_id)
            endTime = time.time()

            searchMenu.setError('\nElapsed time: ' + str(endTime - startTime)[:9] + 's'
                                '\nRows num: ' + str(len(allRecords)))

            searchMenu.addField('<Book id> | Reader name | Reader surname')
            for record in allRecords:
                searchMenu.addField(f"<{record[0]}> {record[1]} {record[2]}")

        except Exception as err:
            searchMenu.setError(str(err))

        searchMenu.run('Return to prev menu')

    def __getSomeExemplars(self):
        searchMenu = CUI('Exemplars which id less than input value')
        self.currentMenu = searchMenu
        try:
            exemplar_id = int(input('Input value of id: '))

            if not (isinstance(exemplar_id, int) and exemplar_id > 0):
                raise Exception('Invalid input')

            startTime = time.time()
            allRecords = self.searchController.getSomeExemplars(exemplar_id)
            endTime = time.time()

            searchMenu.setError('\nElapsed time: ' + str(endTime - startTime)[:9] + 's'
                                '\nRows num: ' + str(len(allRecords)))

            searchMenu.addField('<Exemplar id> | Book id | Reader id ')
            for record in allRecords:
                searchMenu.addField(f"<{record[0]}> {record[1]} {record[2]} ")

        except Exception as err:
            searchMenu.setError(str(err))

        searchMenu.run('Return to prev menu')