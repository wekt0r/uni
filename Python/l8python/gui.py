import gi, os
from gi.repository import Gtk

from database import *

NO_OF_RESULTS = 10

class GUI(Gtk.Window):

    def __init__(self):
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

        self.buttons = [Gtk.Button("") for i in range(NO_OF_RESULTS)]
        for button in self.buttons:
            self.box.pack_start(button, True, True, 0)

        #self.search_result = Gtk.Label("")
        #self.box.pack_start(self.search_result, True, True, 0)
        #for
        self.show_all()


    def destroy(window, self):
        Gtk.main_quit()

    def on_key_event(self, widget, event):
        results = [ContactBrowser.input_handler(self.search_entry.get_text(), event.keyval) for _ in range(10)]
        for i, result in enumerate(results):
            if result:
                self.buttons[i] = Gtk.Button("result")
                #button.set_label(result)
        self.show_all()

    def on_clicked_event(self, *args):
        pass

class SearchResults(Gtk.Window):
    pass

class AlbumEditor(Gtk.Window):
    pass


if __name__ == "__main__":
    GUI()
    Gtk.main()
