import psycopg2
import os
import sys
sys.path.append('../')
from utils.jsonReader import JsonReader

class db:
    def __init__(self):
        config = JsonReader(os.getcwd()).getJsonObject('./config.json')
        self.connect = psycopg2.connect(
        database="library",
        user="postgres",
        password="12316c")
        self.cursor = self.connect.cursor()


    #define custom sql functions
    def defineGenerateStringFunc(self):
        self.cursor.execute('create or replace function generatestring(length int) '
                            'returns text '
                            'language plpgsql '
                            'as '
                            '$$ '
                            'declare '
                            'outputString text; '
                            'begin '
                            'select string_agg(chr(trunc(97 + random()*25)::int), '') '
                            'from generate_series(1, length) '
                            'into outputString; '
                            'return outputString; '
                            'end; '
                            '$$; ')
        self.connect.commit()

    def defineGenerateDateFunc(self):
        self.cursor.execute('create function generatedate() returns text '
                            'language plpgsql '
                            'as '
                            '$$ '
                            'declare '
                            'outputDate text; '
                            'begin '
                            'select concat((1990 + trunc(random() * 30 + 1)::int)::text, '
                            '"-0", trunc(random() * 9 + 1)::text, "-", '
                            '(8 + trunc(random() * 20 + 1)::int)::text) '
                            'into outputDate; '
                            'return outputDate; '
                            'end; '
                            '$$; ')
        self.connect.commit()

    def defineGenerateIntFunc(self):
        self.cursor.execute('create function generateint(max integer) returns text '
                            'language plpgsql '
                            'as '
                            '$$ '
                            'declare '
                            'outputInt int; '
                            'begin '
                            'select trunc(random() * max + 1) '
                            'into outputInt; '
                            'return outputInt; '
                            'end; '
                            '$$; ')
        self.connect.commit()

    def init(self):
        self.defineGenerateStringFunc()
        self.defineGenerateDateFunc()
        self.defineGenerateIntFunc()