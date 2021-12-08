import math
from modelController import ModelController
from CUI.cui import CUI

exec_bad_chars = set('{}()[],;.\'\"')


class EntityView:
    def __init__(self, instance):
        self.instance = instance
        self.page = 1
        self.itemsCurrentMenu = [None, None]
        self.per_page = 10
        self.CUI = CUI(f"{self.instance.__name__} model menu")
        self.Controller = ModelController(instance)

        self.CUI.addField(f'Add {self.instance.__name__}', lambda: self.__addItem())
        self.CUI.addField(f'{self.instance.__name__}s', lambda: self.__getItems())

    def __supportFillItemFunc(self, key, value, item):
        try:
            new_value = input(f'Enter new {key} value: ')
            if isinstance(new_value, str) and len(new_value) > 0:
                if new_value.isdigit():
                    setattr(item, key, int(new_value))
                else:
                    setattr(item, key, new_value)
            else:
                raise Exception('Incorrect input')
            self.currentMenu.renameField(f'{key}:        <{value}>', f'{key}:        <{new_value}>')
        except Exception as err:
            self.currentMenu.setError(str(err))

    def __supportFillFunc(self, key, mapped):
        try:
            value = input(f'Enter new {key} value: ')
            old_value = None
            if key in mapped and mapped[key] is not None: old_value = mapped[key]
            if isinstance(value, str) and len(value) > 0:
                if value.isdigit():
                    mapped[key] = int(value)
                else:
                    mapped[key] = value
            else:
                raise Exception('Incorrect input')

            if old_value is None:
                self.currentMenu.renameField(f'{key}', f'{key}:        <{value}>')
            else:
                self.currentMenu.renameField(f'{key}:        <{old_value}>', f'{key}:        <{value}>')
        except Exception as err:
            self.currentMenu.setError(str(err))

    def __fillEntityMenu(self, *args):
        self.currentMenu = CUI(f'{self.instance.__name__} fill menu')
        try:
            if len(args) > 0 and isinstance(args[0], self.instance):
                item = args[0]
                for (key, value) in self.Controller.getModelEntityMappedKeys(item).items():
                    self.currentMenu.addField(f'{key}:        <{value}>',
                                              lambda key=key, value=value: self.__supportFillItemFunc(key, value, item))
            elif len(args) > 0 and isinstance(args[0], dict):
                mapped = args[0]
                for key in self.Controller.getModelKeys():
                    mapped[key] = None
                    self.currentMenu.addField(f'{key}', lambda key=key: self.__supportFillFunc(key, mapped))
            else:
                raise Exception('Invalid arguments')

        except Exception as err:
            self.currentMenu.setError(str(err))
        self.currentMenu.run('Save and Return')

    def run(self):
        self.CUI.run()

    def __addItem(self):
        try:
            mapped = {}
            self.__fillEntityMenu(mapped)
            exec_str = ''
            for value in mapped.values():
                if value is None or \
                        (isinstance(value, str) and
                         any((char in exec_bad_chars) for char in value)) \
                        : raise Exception('Invalid entity fill')
                if isinstance(value, str):
                    exec_str += f"'{value}', "
                else: exec_str += f"{value}, "

            exec("self.entity = self.instance(%s)" % exec_str[:-1])

            entityId = self.Controller.add(self.entity)
            self.CUI.setError(f'New Entity created! Id: {entityId}')
        except Exception as err:
            self.CUI.setError(str(err))

    def __changePageParams(self, page: int, per_page: int):
        self.page = page
        self.per_page = per_page
        self.itemsCurrentMenu[0].stop()
        self.__getItems()

    def __getItems(self):
        itemsMenu = CUI(self.instance.__name__ + 's')
        self.itemsCurrentMenu[0] = itemsMenu
        try:
            if self.page < math.ceil(self.Controller.getCount() / self.per_page):
                itemsMenu.addField('NEXT', lambda: self.__changePageParams(self.page + 1, self.per_page))
            if self.page > 1:
                itemsMenu.addField('PREV', lambda: self.__changePageParams(self.page - 1, self.per_page))
            entities = self.Controller.getRange(self.page, self.per_page)
            for entity in entities:
                if 'name' in self.Controller.getModelKeys():
                    itemsMenu.addField(f"<{entity.id}> {entity.name}", lambda id=entity.id: self.__getItem(id))
                else:
                    itemsMenu.addField(f"<{entity.id}>", lambda id=entity.id: self.__getItem(id))

        except Exception as err:
            itemsMenu.setError(str(err))
        itemsMenu.run('Return to main menu')

    def __updateItem(self, item):
        self.__fillEntityMenu(item)
        self.Controller.update(item)
        self.itemsCurrentMenu[1].stop()
        self.__getItem(item.id)

    def __deleteItem(self, id: int):
        self.Controller.delete(id)
        self.itemsCurrentMenu[1].stop()
        self.__supportCUIFunc()

    def __supportCUIFunc(self):
        self.itemsCurrentMenu[1].stop()
        self.__changePageParams(self.page, self.per_page)

    def __getItem(self, id: int):
        itemMenu = CUI(f'{self.instance.__name__} menu')
        self.itemsCurrentMenu[1] = itemMenu
        try:
            item = self.Controller.getById(id)
            for (key, value) in self.Controller.getModelEntityMappedKeys(item).items():
                itemMenu.addField(str(key) + ' : ' + str(value))

            itemMenu.addField('DELETE', lambda: self.__deleteItem(item.id))
            itemMenu.addField('UPDATE', lambda: self.__updateItem(item))
            itemMenu.addField('Return to prev menu', lambda: self.__supportCUIFunc())
        except Exception as err:
            itemMenu.setError(str(err))
        itemMenu.run(False)