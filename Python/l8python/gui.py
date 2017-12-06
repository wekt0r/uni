import gi, os
from gi.repository import Gtk

from database import *

NO_OF_RESULTS = 10

class GUI(Gtk.Window):

    def __init__(self, data):
        self.data = data
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

        self.search_result = Gtk.Label("\n"*NO_OF_RESULTS)
        self.box.pack_start(self.search_result, True, True, 0)

        self.edit_button = Gtk.Button("Edit them!")
        self.edit_button.connect_after('clicked', self.on_edit_clicked)


        self.show_all()


    def destroy(window, self):
        Gtk.main_quit()

    def on_key_event(self, widget, event):
        self.search_result.set_label("\n\n".join([DatabaseBrowser.do_search(self.search_entry.get_text(), event.keyval) for _ in range(5)]) + "\nand {} more.".format(len(results) - NO_OF_RESULTS))
        self.show_all()

    def on_edit_clicked(self):
        pass

    def on_clicked_event(self, *args):
        pass

class SearchResults(Gtk.Window):
    pass

class AlbumEditor(Gtk.Window):
    pass

class App:
    def main():
        data = Data()
        GUI(data)
        Gtk.main()

if __name__ == "__main__":
    App.main()
