from sqlalchemy import func, select
from sqlalchemy.orm.attributes import InstrumentedAttribute

from bases import session


class ModelController(object):

    def __init__(self, instance):
        self.instance = instance

    def getRange(self, page: int, per_page: int):
        items = []
        try:
            page -= 1
            items = session.query(self.instance) \
                .order_by(self.instance.id.asc()) \
                .offset(page * per_page) \
                .limit(per_page) \
                .all()
        except Exception as err:
            print("Get error! ", err)
            raise err
        return items

    def add(self, item):
        try:
            if not isinstance(item, self.instance):
                raise Exception('Invalid arguments')

            session.add(item)
            session.commit()
            session.refresh(item)
            return item.id
        except Exception as err:
            print("Add error! ", err)
            raise err

    def getById(self, itemId):
        try:
            return session.query(self.instance).get(itemId)
        except Exception as err:
            print("Get by id error! ", err)
            raise err

    def delete(self, itemId):
        try:
            deletedItem = self.getById(itemId)
            if deletedItem is None: raise Exception('This id doesn\'t exists')
            session.query(self.instance).filter(self.instance.id == itemId).delete()
            session.commit()
            return deletedItem
        except Exception as err:
            print("Delete error! ", err)
            raise err

    def update(self, item):
        try:
            if not isinstance(item, self.instance):
                raise Exception('Invalid arguments')

            session.query(self.instance) \
                .filter(self.instance.id == item.id) \
                .update(self.getModelEntityMappedKeys(item))
            session.commit()
            return True
        except Exception as err:
            print("Update error! ", err)
            raise err

    def getCount(self):
        try:
            return session.execute(select([func.count()]).select_from(self.instance)).scalar()
        except Exception as err:
            print("Get count error! ", err)
            raise err

    def getModelKeys(self):
        keys = []
        for entity in self.instance.__dict__.items():
            key = entity[0]
            key_type = entity[1]
            if type(key_type) is InstrumentedAttribute and key is not 'id' and not key[0].isupper():
                keys.append(key)
        return keys

    def getModelEntityMappedKeys(self, item):
        mapped_values = {}
        for entity in item.__dict__.items():
            key = entity[0]
            value = entity[1]
            if key is not '_sa_instance_state':
                mapped_values[key] = value
        return mapped_values