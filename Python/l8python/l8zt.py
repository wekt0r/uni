import gi, os
from gi.repository import Gtk

class GUI(Gtk.Window):
    def __init__(self):
        self.a = [None for i in range(5)]
        Gtk.Window.__init__(self, title="Album Manager")
        self.set_size_request(400, 200)

        self.connect("key-press-event", self.on_key_event)
        self.connect_after('destroy', self.destroy)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.box)

        self.label = Gtk.Label("Find album:")
        self.box.pack_start(self.label, True, True, 0)

        self.search_entry = Gtk.Entry()
        self.box.pack_start(self.search_entry, True, True, 0)

        self.search_result = Gtk.Label("")
        self.box.pack_start(self.search_result, True, True, 0)

        self.show_all()


    def destroy(window, self):
        Gtk.main_quit()

    def on_key_event(self, widget, event):

        self.search_result.set_label("\n\n".join([ContactBrowser._input_handler(self.search_entry.get_text(), event.keyval) for _ in range(5)]))
        self.show_all()

    def on_clicked_event(self, *args):
        pass

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
        c.commit()
        c.close()


class ContactBrowser:
    def __init__(self):
        pass

    def _input_handler(search_entry, new_key):
        if new_key == 65288:
            return search_entry[:-1]
        return search_entry + chr(new_key) if new_key <= 128 else search_entry

    def do_search(self, ):
        pass


if __name__ == "__main__":
    GUI()
    Gtk.main()
