from bases import session
from entityView import EntityView
from CUI.cui import CUI
from models.books import Book
from models.exemplars import Exemplar
from models.readers import Reader


if __name__ == '__main__':
    cui = CUI('lab3')
    cui.addField('Books', lambda: EntityView(Book).run())
    cui.addField('Exemplars', lambda: EntityView(Exemplar).run())
    cui.addField('Readers', lambda: EntityView(Reader).run())
    cui.run()
    session.close()