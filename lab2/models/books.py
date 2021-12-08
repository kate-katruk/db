from models.dbModel import DbModel

class Book(DbModel):
    def __init__(self):
        self.book_id = {
            'type': 'number',
            'value': "DEFAULT",
            'not null': False
        }

        self.name = {
            'type': 'string',
            'value': None
        }

        self.author = {
            'type': 'string',
            'value': None
        }

        self.year = {
            'type': 'number',
            'value': None
        }
        self.publishing = {
            'type': 'string',
            'value': None
        }
        self.place = {
            'type': 'string',
            'value': None
        }