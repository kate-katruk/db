from models.dbModel import DbModel

class Reader(DbModel):
    def __init__(self):
        self.reader_id = {
            'type': 'number',
            'value': "DEFAULT",
            'not null': False
        }

        self.name = {
            'type': 'string',
            'value': None
        }

        self.surname = {
            'type': 'string',
            'value': None
        }

        self.phone = {
            'type': 'number',
            'value': None
        }