import gi, os
from gi.repository import Gtk

from database import *

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

        self.search_result = Gtk.Label("\n"*NO_OF_RESULTS)
        self.box.pack_start(self.search_result, True, True, 0)

        self.edit_button = Gtk.Button("Edit them!")
        self.edit_button.connect_after('clicked', self.on_edit_clicked)
        self.box.pack_start(self.edit_button, True, True, 0)


        self.show_all()


    def destroy(window, self):
        Gtk.main_quit()

    def on_key_event(self, widget, event):
        results = [1,1,1,1,1,1]
        self.search_result.set_label("\n\n".join([ "\t| ".join([str(e) for e in list(r)]) for r in self.database_browser.do_search(self.search_entry.get_text(), event.keyval)[:NO_OF_RESULTS]]))
        self.show_all()

    def on_add_clicked(self, _):
        AddAlbum(self.data)

    def on_edit_clicked(self, _):
        pass

    def on_clicked_event(self, *args):
        pass

class AddAlbum(Gtk.Window):
    def __init__(self,data):
        self.data = data
        Gtk.Window.__init__(self, title="Album Manager")
        self.set_size_request(400, 200)
        self.connect_after('destroy', self.destroy)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.box)

        self.labels = [Gtk.Label(label) for label in ["id", "Title", "Authors", "Year", "Is lend?", "To who"]]
        self.entries = [Gtk.Entry() for _ in range(6)]

        for label, entry in zip(self.labels, self.entries):
            self.box.pack_start(label, True, True, 0)
            self.box.pack_start(entry, True, True, 0)

        self.discard = Gtk.Button("Discard")
        self.discard.connect_after('clicked', self.destroy)
        self.box.pack_start(self.discard, True, True, 0)

        self.add = Gtk.Button("Add")
        self.add.connect_after('clicked', self.add_album)
        self.box.pack_start(self.add, True, True, 0)
        self.show_all()

    def add_album(self, _):
        self.data.insert_one(Album(*[entry.get_text() for entry in self.entries]))

    def destroy(window, self):
        Gtk.main_quit()

class SearchResults(Gtk.Window):
    def __init__(self, ):
        Gtk.Window.__init__(self, title="Edit search results")


class AlbumEditor(Gtk.Window):
    pass

class App:
    def main():
        GUI()
        Gtk.main()

if __name__ == "__main__":
    App.main()
