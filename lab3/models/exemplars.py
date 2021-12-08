from sqlalchemy import Column, Integer, String, Date, func, ForeignKey
from sqlalchemy.orm import relationship, backref
from bases import Base

class Exemplar(Base):
    __tablename__ = 'Exemplar'

    id = Column(Integer, primary_key=True)
    book_fk = Column(Integer, ForeignKey('Book.id'))
    reader_fk = Column(Integer, ForeignKey('Reader.id'))
    date_from = Column(Date, default=func.now())
    date_to = Column(Date, default=func.now())

    Book = relationship("Book", backref=backref("Reader", uselist=False))
    Reader = relationship("Reader", backref=backref("Book", uselist=False))

    def __repr__(self):
      return "<Exemplar(book_fk='%i',reader_fk='%i', date_from='%s', date_to='%s')>" % \
             (self.book_fk, self.reader_fk, self.date_from, self.date_to)

    def __init__(self,
                 book_fk: int,
                 reader_fk: int,
                 date_from: str,
                 date_to: str):
        self.book_fk = book_fk
        self.reader_fk = reader_fk
        self.date_from = date_from
        self.date_to = date_to
