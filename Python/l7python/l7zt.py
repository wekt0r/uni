import gi, os, sys
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class GUI(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Image Viewer")
        self.set_size_request(400, 200)

        self.connect_after('destroy', self.destroy)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(box)

        self.label = Gtk.Label("Enter directory to image(s):")
        box.pack_start(self.label, True, True, 0)

        self.images_dir = Gtk.Entry()
        self.images_dir.set_text(os.getcwd())
        box.pack_start(self.images_dir, True, True, 0)

        self.show_button = Gtk.Button("Show images")
        self.show_button.connect_after('clicked', self.on_show_clicked)
        box.pack_start(self.show_button, True, True, 0)

        self.show_all()

    def destroy(window, self):
        Gtk.main_quit()

    def _is_graphic_file(directory):
        return any((directory.endswith(extension) for extension in [".jpg", ".png", ".jpeg", ".bmp"]))

    def on_show_clicked(self, button):
        my_dir_or_image = self.images_dir.get_text()
        try:
            if GUI._is_graphic_file(my_dir_or_image):
                Images(Gtk.Image.new_from_file(my_dir_or_image))
            else:
                Images(*[Gtk.Image.new_from_file(my_dir_or_image + file_dir if my_dir_or_image.endswith("/") else my_dir_or_image + "/" + file_dir)
                         for file_dir in os.listdir(my_dir_or_image) if GUI._is_graphic_file(file_dir)])
        except Exception as e:
            exception_window = Gtk.Window(title="Error occured!")
            exception_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            exception_window.add(exception_box)
            exception_label = Gtk.Label("""Unfortunately, something went wrong! Probably the file isn't an image, or the directory doesn't exist""")
            exception_code = Gtk.Label(str(e))
            exception_box.pack_start(exception_label, True, True, 0)
            exception_box.pack_start(exception_code, True, True, 0)
            exception_window.show_all()

class Images(Gtk.Window):
    def __init__(self, *images):
        self.images = images
        Gtk.Window.__init__(self, title="Images")
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.add(box)
        for image in images:
            box.pack_start(image, True, True, 0)
        self.show_all()

def main():
    app = GUI()
    Gtk.main()

if __name__ == "__main__":
    sys.exit(main())
