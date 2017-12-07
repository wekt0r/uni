import gi, os
from gi.repository import Gtk

from database import *
from functools import partial

NO_OF_RESULTS = 10

class GUI(Gtk.Window):

    def __init__(self):
        self.data = Data()
        self.database_browser = DatabaseBrowser(self.data)
        Gtk.Window.__init__(self, title="Album Manager")
        self.set_size_request(400, 200)

        self.connect("key-press-event", self.on_key_event)
        self.connect_after('destroy', self.destroy)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.box)

        self.add_album = Gtk.Button("Add Album")
        self.add_album.connect_after('clicked', self.on_add_clicked)
        self.box.pack_start(self.add_album, True, True, 0)

        self.label = Gtk.Label("Find album:")
        self.box.pack_start(self.label, True, True, 0)

        self.search_entry = Gtk.Entry()
        self.box.pack_start(self.search_entry, True, True, 0)

        self.edit_button = Gtk.Button("Edit them!")
        self.edit_button.connect_after('clicked', self.on_edit_clicked)
        self.box.pack_start(self.edit_button, True, True, 0)

        self.search_result = Gtk.Table(rows=NO_OF_RESULTS, columns=6, homogeneous=True)
        self._create_table_row(self.search_result,0, "Id", "Title", "Authors", "Year", "Is lend?", "To who?")
        #self.search_result = Gtk.Label("\n"*NO_OF_RESULTS)
        self.box.pack_start(self.search_result, True, True, 0)

        self.show_all()


    def destroy(window, self):
        Gtk.main_quit()

    def on_key_event(self, widget, event):
        self.box.remove(self.search_result)
        self.search_result = Gtk.Table(rows=NO_OF_RESULTS, columns=6, homogeneous=True)
        self._create_table_row(self.search_result,0, "Id", "Title", "Authors", "Year", "Is lend?", "To who?")
        for row, res in enumerate(self.database_browser.do_search(self.search_entry.get_text(), event.keyval)[:NO_OF_RESULTS]):
            self._create_table_row(self.search_result, row+1, *res)
        self.box.pack_start(self.search_result, True, True, 0)
        self.show_all()

    def on_add_clicked(self, _):
        AddAlbum(self.data)

    def on_edit_clicked(self, _):
        EditSearchResults(self.data)

    def _create_table_row(self, table, row, id, title, authors, year, is_lend, to_who):
        table.attach(Gtk.Label(str(id)),
                     0,1,
                     row,row+1)
        table.attach(Gtk.Label(str(title)),
                     1,2,
                     row,row+1)
        table.attach(Gtk.Label(str(authors)),
                     2,3,
                     row,row+1)
        table.attach(Gtk.Label(str(year)),
                     3,4,
                     row,row+1)
        table.attach(Gtk.Label(str(is_lend)),
                     4,5,
                     row,row+1)
        table.attach(Gtk.Label(str(to_who)),
                     5,6,
                     row,row+1)
        return table

class AddAlbum(Gtk.Window):
    def __init__(self,data):
        self.data = data
        Gtk.Window.__init__(self, title="Add Album")
        self.set_size_request(400, 200)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.box)

        self.labels = [Gtk.Label(label) for label in ["id", "Title", "Authors", "Year", "Is lend?", "To who"]]
        self.entries = [Gtk.Entry() for _ in range(6)]

        for label, entry in zip(self.labels, self.entries):
            self.box.pack_start(label, True, True, 0)
            self.box.pack_start(entry, True, True, 0)

        self.add = Gtk.Button("Add")
        self.add.connect_after('clicked', self.add_album)
        self.box.pack_start(self.add, True, True, 0)
        self.show_all()

    def add_album(self, _):
        self.data.insert_one(Album(*[entry.get_text() for entry in self.entries]))

class UpdateAlbum(Gtk.Window):
    def __init__(self, data, album):
        self.data = data
        self.album = album
        Gtk.Window.__init__(self, title="Update Album")
        self.set_size_request(400, 200)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.box)

        self.labels = [Gtk.Label(label) for label in ["id", "Title", "Authors", "Year", "Is lend?", "To who"]]
        self.entries = [Gtk.Entry() for _ in [album.id, album.title, album.authors, album.year, album.is_lend, album.to_who]]

        for label, entry, value in zip(self.labels, self.entries, [album.id, album.title, album.authors, album.year, album.is_lend, album.to_who]):
            self.box.pack_start(label, True, True, 0)
            entry.set_text(str(value))
            self.box.pack_start(entry, True, True, 0)

        self.add = Gtk.Button("Remove")
        self.add.connect_after('clicked', self.remove_album)
        self.box.pack_start(self.add, True, True, 0)

        self.add = Gtk.Button("Update")
        self.add.connect_after('clicked', self.update_album)
        self.box.pack_start(self.add, True, True, 0)
        self.show_all()

    def remove_album(self, _):
        self.data.remove_one(self.album)

    def update_album(self, _):
        self.data.remove_one(self.album)
        self.data.insert_one(Album(*[entry.get_text() for entry in self.entries]))

class EditSearchResults(Gtk.Window):
    def __init__(self, data):
        self.data = data
        Gtk.Window.__init__(self, title="Edit Search Results")
        self.set_size_request(400, 200)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.box)
        self.buttons = []

        for album_tuple in self.data.results:
            self.buttons.append(Gtk.Button("\t| ".join([str(e) for e in album_tuple])))
            update_album = partial(self.update_album, Album(*album_tuple))
            self.buttons[-1].connect_after('clicked', update_album)
            self.box.pack_start(self.buttons[-1], True, True, 0)

        self.show_all()
    def update_album(self, album, _):
        UpdateAlbum(self.data, album)

class App:
    def main():
        GUI()
        Gtk.main()

if __name__ == "__main__":
    App.main()
