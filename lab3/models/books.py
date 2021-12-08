from sqlalchemy import Column, Integer, String, Date, func, ForeignKey
from sqlalchemy.orm import relationship, backref
from models.links import links_books_association
from bases import Base

class Book(Base):
    __tablename__ = 'Book'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    author = Column(String)
    year = Column(Integer)
    publishing = Column(String)
    place = Column(String)

    Readers = relationship("Reader", secondary=links_books_association)
    def __repr__(self):
      return "<Book(name='%s',author='%s', year='%i',publishing='%s',place='%s')>" %\
             (self.name, self.author, self.year, self.publishing, self.place)

    def __init__(self,
                 name: str,
                 author: str,
                 year: int,
                 publishing: str,
                 place: str):
        self.name = name
        self.author = author
        self.year = year
        self.publishing = publishing
        self.place = place