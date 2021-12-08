import sys
import time
sys.path.append('../')
from models.books import Book
from database import db

class BookController(object):

    def __init__(self):
        try:
            self.db = db()

            if db is None: raise Exception('No connection. Please, check your config.json or Postgre server')

        except Exception as err:
            print("Connection error! ", err)
            exit(1)

    def getAll(self, page: int, per_page: int):
        items = []
        try:
            page -= 1
            self.db.cursor.execute(
                f'SELECT {Book().getKeys()} FROM public.\"Books\" ORDER BY book_id LIMIT {per_page} OFFSET {page * per_page}')
            records = self.db.cursor.fetchall()
            for record in records:
                tmpItem = Book()
                tmpItem.parse(record)
                items.append(tmpItem)
        except Exception as err:
            print("Get error! ", err)
        return items

    def add(self, *args):
        try:
            newEntity: Book = Book()
            if len(args) > 0 and isinstance(args[0], Book):
                newEntity = args[0]
            else:
                newEntity.fill()

            if newEntity.isFull():
                self.db.cursor.execute(f'INSERT INTO public.\"Books\" ({newEntity.getKeys()}) '
                                    f'VALUES ({newEntity.getValues()}) RETURNING book_id')
                self.db.connect.commit()
                return int(self.db.cursor.fetchone()[0])
        except Exception as err:
            print("Add error! ", err)
        return False

    def getById(self, bookId):
        book = Book()
        try:
            if isinstance(bookId, int): bookId = str(bookId)
            if not isinstance(bookId, str): raise Exception('Incorrect arguments')
            self.db.cursor.execute(f'SELECT {book.getKeys()} from public.\"Books\" WHERE book_id = {bookId}')
            record = self.db.cursor.fetchone()
            if record is not None:
                book.parse(record)
            else:
                raise Exception(f'No entry with ID {bookId} found')
        except Exception as err:
            print("Get by id error! ", err)
        return book

    def delete(self, bookId):
        try:
            if isinstance(bookId, int): bookId = str(bookId)
            if not isinstance(bookId, str): raise Exception('Incorrect arguments')
            book = self.getById(bookId)
            self.db.cursor.execute(f'UPDATE "Exemplar" SET book_fk = 0 WHERE book_fk = {bookId}')
            self.db.connect.commit()
            self.db.cursor.execute(f'DELETE from public.\"Books\" WHERE book_id = {bookId}')
            self.db.connect.commit()
            return book
        except Exception as err:
            print("Delete error! ", err)
            return False

    def update(self, *args):
        try:
            book: Book = Book()
            if len(args) == 0:
                raise Exception('Invalid arguments')
            if isinstance(args[0], int) or isinstance(int(args[0]), int):
                book.fill()
                book.book_id = args[0]
                values = book.getValues().split(',')
                old_values = self.getById(args[0]).getValues().split(',')
                keys = book.getKeys().split(',')
                for i in range(len(keys)):
                    if values[i] == 'null':
                        book.__setattr__(keys[i], old_values[i])

            if isinstance(args[0], Book):
                book = args[0]

            if not book.isFull():
                raise Exception('Invalid input')

            queryStr = ''
            keys = book.getKeys().split(',')
            values = book.getValues().split(',')
            for i in range(len(keys)):
                if i == 0:
                    continue
                queryStr += keys[i] + ' = ' + values[i] + ', '
            str = f'Update public.\"Books\" Set {queryStr[:-2]} Where book_id = {book.book_id}'
            self.db.cursor.execute(str)
            self.db.connect.commit()
            return True
        except Exception as err:
            print("Update error! ", err)
            return False

    def getCount(self):
        try:
            self.db.cursor.execute(f'SELECT count(*)  from public.\"Books\"')
            return int(self.db.cursor.fetchone()[0])
        except Exception as err:
            print("Get count error! ", err)

    def generateRows(self, entitiesNum: int):
        startTime = time.time()
        try:
            self.db.cursor.execute(f"INSERT  INTO public.\"Books\"  (name, author,year,publishing,place) "
                                   f"SELECT generatestring(15),"
                                   f"generatestring(15),"
                                   f"generateint(2000)::int,"
                                   f"generatestring(15),"
                                 f"generatestring(15) "
                                   f"FROM generate_series(1, {entitiesNum})")
            self.db.connect.commit()
        except Exception as err:
            print("Generate Rows error! ", err)
            exit(1)
        endTime = time.time()
        return str(endTime - startTime)[:9] + 's'