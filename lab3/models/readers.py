from sqlalchemy import Column, Integer, String, Date, func, ForeignKey
from sqlalchemy.orm import relationship, backref
from models.links import links_books_association
from bases import Base

class Reader(Base):
    __tablename__ = 'Reader'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    phone = Column(Integer)
    def __repr__(self):
      return "<Reader(name='%s',surname='%s', phone='%i')>" %\
             (self.name, self.surname, self.phone)

    Books = relationship("Book", secondary=links_books_association)

    def __init__(self,
                 name: str,
                 surname: str,
                 phone: int):
        self.name = name
        self.surname = surname
        self.phone = phone