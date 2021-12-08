from models.dbModel import DbModel

class Exemplar(DbModel):
    def __init__(self):
        self.exemplar_id = {
            'type': 'number',
            'value': "DEFAULT",
            'not null': False
        }

        self.book_fk = {
            'type': 'number',
            'value': None
        }

        self.reader_fk = {
            'type': 'number',
            'value': None
        }

        self.date_from = {
            'type': 'date',
            'value': None
        }
        self.date_to = {
            'type': 'date',
            'value': None
        }