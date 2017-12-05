import sqlite3

class Album:
    def __init__(self, id, title, authors, year, is_lend, to_who):
        self.id = id
        self.title = title
        self.authors = authors
        self.year = year
        self.is_lend = is_lend
        self.to_who = to_who

    def lend_to(self, to_who):
        self.is_lend = True
        self.to_who = to_who
    def accept_back(self):
        self.is_lend = False
        self.to_who = None

class Data:
    def __init__(self):
        try:
            with open("albums.db") as f:
                self.db_connection = sqlite3.connect('albums.db')
        except OSError:
            self.db_connection = sqlite3.connect('albums.db')
            c.execute("""CREATE TABLE albums (id, title, authors, year, is_lend, to_who)""")

    def insert_one(self, album):
        c = self.db_connection.cursor()
        c.execute("""INSERT INTO albums VALUES ({},{},{},{},{},{})""".format(album.id, album.title, album.authors,
                                                                             album.year, album.is_lend, album.to_who))
    def remove_one(self, album):
        c = self.db_connection.cursor()
        c.execute("""DELETE FROM albums WHERE id={} AND title={} AND authors={} AND year={}""".format(album.id, album.title,
                                                                                                      album.authors, album.year))

    def find_all(self, query):
        c = self.db_connection.cursor()
        c.execute("""SELECT * FROM albums WHERE id LIKE '%{0}%' OR title LIKE '%{0}%' OR authors LIKE '%{0}%'
                     OR year LIKE '%{0}%' OR is_lend LIKE '%{0}%' OR to_who LIKE '%{0}%';""")
        return c.fetchall()

class ContactBrowser:
    def __init__(self):
        pass

    def input_handler(search_entry, new_key):
        if new_key == 65288:
            return search_entry[:-1]
        return search_entry + chr(new_key) if new_key <= 128 else search_entry

    def do_search(self):
        pass
