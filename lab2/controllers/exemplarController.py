import sys
import time
sys.path.append('../')
from models.exemplars import Exemplar
from database import db


class ExemplarController(object):

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
                f'SELECT {Exemplar().getKeys()} FROM "Exemplar" ORDER BY exemplar_id LIMIT {per_page} OFFSET {page * per_page}')
            records = self.db.cursor.fetchall()
            for record in records:
                tmpItem = Exemplar()
                tmpItem.parse(record)
                items.append(tmpItem)
        except Exception as err:
            print("Get error! ", err)
            exit(1)
        return items

    def add(self, *args):
        try:
            newEntity: Exemplar = Exemplar()
            if len(args) > 0 and isinstance(args[0], Exemplar):
                newEntity = args[0]
            else:
                newEntity.fill()

            if newEntity.isFull():
                str = f'INSERT INTO public."Exemplar" ({newEntity.getKeys()}) VALUES ({newEntity.getValues()}) RETURNING exemplar_id'
                self.db.cursor.execute(str)
                self.db.connect.commit()
                return int(self.db.cursor.fetchone()[0])
        except Exception as err:
            print("Add error! ", err)
        return False

    def getById(self, exemplarId):
        exemplar = Exemplar()
        try:
            if isinstance(exemplarId, int): exemplarId = str(exemplarId)
            if not isinstance(exemplarId, str): raise Exception('Incorrect arguments')
            self.db.cursor.execute(f'SELECT {exemplar.getKeys()} from "Exemplar" WHERE exemplar_id = {exemplarId}')
            record = self.db.cursor.fetchone()
            if record is not None:
                exemplar.parse(record)
            else:
                raise Exception(f'No entry with ID {exemplarId} found')
        except Exception as err:
            print("Get by id error! ", err)
        return exemplar

    def delete(self, exemplarId):
        try:
            if isinstance(exemplarId, int): exemplarId = str(exemplarId)
            if not isinstance(exemplarId, str): raise Exception('Incorrect arguments')
            exemplar = self.getById(exemplarId)
            self.db.cursor.execute(f'DELETE from "Exemplar" WHERE exemplar_id = {exemplarId}')
            self.db.connect.commit()
            return exemplar
        except Exception as err:
            print("Delete error! ", err)
            return False

    def update(self, *args):
        try:
            exemplar: Exemplar = Exemplar()
            if len(args) == 0: raise Exception('Invalid arguments')
            if isinstance(args[0], int) or isinstance(int(args[0]), int):
                exemplar.fill()
                exemplar.exemplar_id = args[0]
                values = exemplar.getValues().split(',')
                old_values = self.getById(args[0]).getValues().split(',')
                keys = exemplar.getKeys().split(',')
                for i in range(len(keys)):
                    if values[i] == 'null':
                        exemplar.__setattr__(keys[i], old_values[i])

            if isinstance(args[0], Exemplar):
                order = args[0]

            if not exemplar.isFull():
                raise Exception('Invalid input')

            queryStr = ''
            keys = exemplar.getKeys().split(',')
            values = exemplar.getValues().split(',')
            for i in range(len(keys)):
                if i == 0:
                    continue
                queryStr += keys[i] + ' = ' + values[i] + ', '
            str=f'Update "Exemplar" Set {queryStr[:-2]} Where exemplar_id = {exemplar.exemplar_id}'
            self.db.cursor.execute(str)
            self.db.connect.commit()
            return True
        except Exception as err:
            print("Update error! ", err)
            return False

    def getCount(self):
        try:
            self.db.cursor.execute(f'SELECT count(*)  from "Exemplar"')
            return int(self.db.cursor.fetchone()[0])
        except Exception as err:
            print("Get count error! ", err)

    def generateRows(self, entitiesNum: int):
        startTime = time.time()
        try:
            self.db.cursor.execute(f"INSERT  INTO \"Exemplar\" (book_fk, reader_fk, date_from, date_to)"
                                   f"SELECT randomb_fk()::int,"
                                   f"randomr_fk()::int,"
                                   f"generatedate()::date,"
                                   f"generatedate()::date "
                                   f"FROM generate_series(1, {entitiesNum})")
            self.db.connect.commit()
        except Exception as err:
            print("Generate Rows error! ", err)
        endTime = time.time()
        return str(endTime - startTime)[:9] + 's'