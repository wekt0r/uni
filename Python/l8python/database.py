import sqlite3

class Album:
    def __init__(self, id, title, authors, year, is_lent, to_who):
        self.id = id
        self.title = title
        self.authors = authors
        self.year = year
        self.is_lent = is_lent
        self.to_who = to_who

def setup_connection(func):
    def setup_decorator(self, *args, **kwargs):
        c = self._make_conn()
        func(self, c, *args, **kwargs)
        self._commit_conn()
    return setup_decorator

class Data:

    def _make_conn(self):
        c = self.conn.cursor()
        return c

    def _commit_conn(self):
        self.conn.commit()

    def __init__(self):
        try:
            with open("albums.db") as f:
                pass
        except OSError:
            self.setup_table()
        finally:
            self.conn = sqlite3.connect("albums.db")


    @setup_connection
    def setup_table(self, c):
        c.execute("""CREATE TABLE albums (id, title, authors, year, is_lent, to_who)""")

    @setup_connection
    def insert_one(self, c, album):
        c.execute("""INSERT INTO albums VALUES (?,?,?,?,?,?)""", (album.id, album.title, album.authors,
                                                                 album.year, album.is_lent, album.to_who))
    @setup_connection
    def remove_one(self, c, album):
        c.execute("""DELETE FROM albums WHERE id=? AND title=? AND authors=? AND year=?""", (album.id, album.title,
                                                                                                      album.authors, album.year))
    @setup_connection
    def find_all(self, c, query):
        c.execute("""SELECT * FROM albums WHERE id LIKE '%{}%' OR title LIKE '%{}%' OR authors LIKE '%{}%'
                     OR year LIKE '%{}%' OR is_lent LIKE '%{}%' OR to_who LIKE '%{}%'""".format( *([query]*6)))
        self.results = c.fetchall()

class DatabaseBrowser:
    def __init__(self, data):
        self.data = data

    @staticmethod
    def _input_handler(search_entry, new_key):
        if new_key == 65288:
            return search_entry[:-1]
        return search_entry + chr(new_key) if new_key <= 128 else search_entry

    def do_search(self, search_entry, new_key):
        self.data.find_all(self._input_handler(search_entry, new_key))
        return self.data.results
