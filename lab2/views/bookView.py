import sys
sys.path.append("../")
import math
from controllers.bookController import BookController
from models.books import Book
from cui import CUI

class BookView:
    def __init__(self):
        self.currentMenu = [None, None]
        self.page = 1
        self.per_page = 10

        self.CUI = CUI("Book model menu")
        self.bookController = BookController()
        self.CUI.addField('Add Book', lambda: self.__addBooks())
        self.CUI.addField('Generate rows', lambda: self.__generateRows())
        self.CUI.addField('Books', lambda: self.__getBooks())

    def run(self):
        self.CUI.run()

    def __generateRows(self):
        try:
            rowsNum = int(input('Enter rows num: '))
            if not (isinstance(rowsNum, int) and rowsNum > 0):
                raise Exception('Invalid input')
            self.CUI.setError('   Please wait! Rows are generating...   ')
            time = self.bookController.generateRows(rowsNum)
            self.CUI.setError('   Rows generated! Elapsed time: ' + time)
        except Exception as error:
            self.CUI.setError(str(error))

    def __addBooks(self):
        try:
            result = self.bookController.add()
            self.CUI.setError('New Book id: ' + str(result))
            if isinstance(result, bool) and not result: raise Exception('Inccorect values')
            else: self.CUI.setError('New Book id: ' + str(result))
        except Exception as err:
            self.CUI.setError(str(err))

    def __changePageParams(self, page: int, per_page: int):
        self.page = page
        self.per_page = per_page
        self.currentMenu[0].stop()
        self.__getBooks()

    def __getBooks(self):
        booksMenu = CUI('Books')
        self.currentMenu[0] = booksMenu
        try:
            if self.page < math.ceil(self.bookController.getCount() / self.per_page):
                booksMenu.addField('NEXT', lambda: self.__changePageParams(self.page + 1, self.per_page))
            if self.page > 1:
                booksMenu.addField('PREV', lambda: self.__changePageParams(self.page - 1, self.per_page))
            books = self.bookController.getAll(self.page, self.per_page)
            for book in books:
                booksMenu.addField(f"<{book.book_id}>{book.name}", lambda book_id=book.book_id: self.__getBook(book_id))

        except Exception as err:
            booksMenu.setError(str(err))
        booksMenu.run('Return to main menu')

    def __updateBook(self, id: int):
        if self.bookController.update(id):
            self.currentMenu[1].stop()
            self.__getBook(id)
        else:
            self.currentMenu[1].setError('Incorrect update values')

    def __deleteBook(self, id: int):
        self.bookController.delete(id)
        self.currentMenu[1].stop()
        self.__supportCUIFunc()

    def __supportCUIFunc(self):
        self.currentMenu[1].stop()
        self.__changePageParams(self.page, self.per_page)

    def __getBook(self, id: int):
        bookMenu = CUI('Book menu')
        self.currentMenu[1] = bookMenu
        try:
            book: Book = self.bookController.getById(id)
            values = book.getValues().split(',')
            keys = book.getKeys().split(',')
            for i in range(len(keys)):
                bookMenu.addField(keys[i] + ' : ' + values[i])

            bookMenu.addField('DELETE', lambda: self.__deleteBook(book.book_id))
            bookMenu.addField('UPDATE', lambda: self.__updateBook(book.book_id))
            bookMenu.addField('Return to prev menu', lambda: self.__supportCUIFunc())
        except Exception as err:
            bookMenu.setError(str(err))
        bookMenu.run(False)