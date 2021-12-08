from sqlalchemy import Column, Integer, Table, ForeignKey
from  bases import Base

links_books_association= Table(
    'Link_Book-Reader', Base.metadata,
    Column('book_id', Integer, ForeignKey('Book.id')),
    Column('reader_id', Integer, ForeignKey('Reader.id'))
)