import sys
import time
sys.path.append('../')
from models.readers import Reader
from database import db


class ReaderController(object):

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
                f'SELECT {Reader().getKeys()} FROM "Reader" ORDER BY reader_id LIMIT {per_page} OFFSET {page * per_page}')
            records = self.db.cursor.fetchall()
            for record in records:
                tmpItem = Reader()
                tmpItem.parse(record)
                items.append(tmpItem)
        except Exception as err:
            print("Get error! ", err)
            exit(1)
        return items

    def add(self, *args):
        try:
            newEntity: Reader = Reader()
            if len(args) > 0 and isinstance(args[0], Reader):
                newEntity = args[0]
            else:
                newEntity.fill()

            if newEntity.isFull():
                self.db.cursor.execute(f'INSERT INTO public."Reader" ({newEntity.getKeys()}) '
                                    f'VALUES ({newEntity.getValues()}) RETURNING reader_id')
                self.db.connect.commit()
                return int(self.db.cursor.fetchone()[0])
        except Exception as err:
            print("Add error! ", err)
        return False

    def getById(self, readerId):
        reader = Reader()
        try:
            if isinstance(readerId, int): readerId = str(readerId)
            if not isinstance(readerId, str): raise Exception('Incorrect arguments')
            self.db.cursor.execute(f'SELECT {reader.getKeys()} from "Reader" WHERE reader_id = {readerId}')
            record = self.db.cursor.fetchone()
            if record is not None:
                reader.parse(record)
            else:
                raise Exception(f'No entry with ID {readerId} found')
        except Exception as err:
            print("Get by id error! ", err)
        return reader

    def delete(self, readerId):
        try:
            if isinstance(readerId, int): readerId = str(readerId)
            if not isinstance(readerId, str): raise Exception('Incorrect arguments')
            reader = self.getById(readerId)
            self.db.cursor.execute(f'UPDATE "Exemplar" SET reader_fk = 0 WHERE reader_fk = {readerId}')
            self.db.connect.commit()
            self.db.cursor.execute(f'DELETE from "Reader" WHERE reader_id = {readerId}')
            self.db.connect.commit()
            return reader
        except Exception as err:
            print("Delete error! ", err)
            return False

    def update(self, *args):
        try:
            reader : Reader = Reader()
            if len(args) is 0: raise Exception('Invalid arguments')
            if isinstance(args[0], int) or isinstance(int(args[0]), int):
                reader.fill()
                reader.reader_id = args[0]
                values = reader.getValues().split(',')
                old_values = self.getById(args[0]).getValues().split(',')
                keys = reader.getKeys().split(',')
                for i in range(len(keys)):
                    if values[i] == 'null':
                        reader.__setattr__(keys[i], old_values[i])

            if isinstance(args[0], Reader):
                order = args[0]

            if not reader.isFull():
                raise Exception('Invalid input')

            queryStr = ''
            keys = reader.getKeys().split(',')
            values = reader.getValues().split(',')
            for i in range(len(keys)):
                queryStr += keys[i] + ' = ' + values[i] + ', '
            self.db.cursor.execute(f'Update "Reader" Set {queryStr[:-2]} Where reader_id = {reader.reader_id}')
            self.db.connect.commit()
            return True
        except Exception as err:
            print("Update error! ", err)
            return False

    def getCount(self):
        try:
            self.db.cursor.execute(f'SELECT count(*)  from "Reader"')
            return int(self.db.cursor.fetchone()[0])
        except Exception as err:
            print("Get count error! ", err)

    def generateRows(self, entitiesNum: int):
        startTime = time.time()
        try:
            self.db.cursor.execute(f"INSERT  INTO \"Reader\" (name, surname, phone)"
                                   f"SELECT generatestring(15),"
                                   f"generatestring(15),"
                                   f"generateint(100)::int "
                                   f"FROM generate_series(1, {entitiesNum})" )
            self.db.connect.commit()
        except Exception as err:
            print("Generate Rows error! ", err)
        endTime = time.time()
        return str(endTime - startTime)[:9] + 's'