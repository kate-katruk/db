import sys
sys.path.append('../')
from database import db

class SearchController(object):

    def __init__(self):
        try:
            self.db = db()

            if db is None: raise Exception('No connection. Please, check your config.json or Postgre server')

        except Exception as err:
            print("Connection error! ", err)
            exit(1)

    def getBooksByReader(self, reader_id):
        try:
                self.db.cursor.execute('SELECT b.book_id, b.name, b.publishing, b.year as book from "Books" as b'
                                       f' inner join "Reader" r on r.reader_id=b.book_id where r.reader_id={reader_id}')
                return self.db.cursor.fetchall()
        except Exception as err:
            print("Get error! ", err)

    def getReadersByBook(self, book_id):
        try:
            self.db.cursor.execute(
                'SELECT r.reader_id, r.name, r.surname as reader from "Reader" as r'         
                f' inner join "Books" b on b.book_id=r.reader_id where b.book_id={book_id}')
            return self.db.cursor.fetchall()
        except Exception as err:
            raise str(err)
    def getSomeExemplars(self, exemplar_id):
        try:
            self.db.cursor.execute(
                'SELECT e.exemplar_id, e.book_fk, e.reader_fk as exemplar from "Exemplar" as e'                        
                f'  where e.exemplar_id<{exemplar_id}')
            return self.db.cursor.fetchall()
        except Exception as err:
                raise str(err)