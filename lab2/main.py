
import sys
from cui import CUI
from views.bookView import BookView
from views.exemplarView import ExemplarView
from views.readerView import ReaderView
from views.searchView import SearchView
if __name__ == '__main__':
    main = CUI()
    main.addField('Books', lambda: BookView().run())
    main.addField('Exemplar', lambda: ExemplarView().run())
    main.addField('Reader', lambda: ReaderView().run())
    main.addField('Search', lambda: SearchView().run())
   # main.addField('Search ', lambda: SearchView().run())
    main.run()
#from consolemenu import *
#from consolemenu.items import *
# con = psycopg2.connect(
#         database="library",
#         user="postgres",
#         password="12316c")
# cur = con.cursor()
# cur.execute("insert into public.\"Books\"(name, author,year,publishing,place) values('north','Tor',1999,'Time','Dnipro')")
# cur.execute("select book_id, name, author, year, publishing, place from public.\"Books\"")
# rows = cur.fetchall()
#for r in rows:
 #   print(f"book_id: {r[0]}, name: {r[1]}, author: {r[2]}, year: {r[3]}, publishing: {r[4]} , place: {r[5]} " )
# con.commit()
# cur.close()
# con.close()

