from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView, FileChooser
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget


class FileSelector(GridLayout):
    def __init__(self):
        GridLayout.__init__(self)
        self.overview_layout = GridLayout(rows=2)
        self.selected_file = 'No file selected'
        self.placeholder_file = Label(text='No file selected', font_size=24)
        #self.instrument_holder = Button(text='Instrument')
        file_upload_btn = Button(text='Choose a file', font_size=24, size_hint_y=0.5)

        popup_layout = GridLayout(cols=1)
        self.file_chooser = FileChooserListView(path='/home/tho/Dropbox (MIT)/MIT_IHTFP/MEng/6.835/FP/midi_files/',
                                                on_entry_added=self.update_file_list_entry,
                                                on_subentry_to_entry=self.update_file_list_entry)

        boxlayout_children = self.file_chooser.children[0].children[0].children[-1].children
        for child in boxlayout_children:
            if isinstance(child, Label):
                child.font_size = 24

        # create content and add to the popup
        close_button = Button(text='Done!', font_size=24, size_hint_y=0.2)

        popup_layout.add_widget(self.file_chooser)
        popup_layout.add_widget(close_button)
        self.popup = Popup(title='Directories', title_size=26,
                      content=popup_layout,)
                      #size_hint=(None, None), size=(500, 500))
        close_button.bind(on_press=self.off_button_press)
        file_upload_btn.bind(on_press=self.on_button_press)

        self.overview_layout.add_widget(self.placeholder_file)
        #self.overview_layout.add_widget(self.instrument_holder)
        self.overview_layout.add_widget(file_upload_btn)

    def update_file_list_entry(self, file_chooser, file_list_entry, *args):
        file_list_entry.ids['filename'].font_size = 24
        size_label = file_list_entry.children[0].children[0]
        size_label.font_size = 24


    def off_button_press(self, *args):
        if len(self.file_chooser.selection) > 0:
            self.placeholder_file.text = self.file_chooser.selection[0].split('/')[-1]
            self.selected_file = self.file_chooser.selection[0]
        else:
            self.placeholder_file.text = 'No file selected'
            self.selected_file = 'No file selected'
        self.popup.dismiss()
    def on_button_press(self, *args):
        self.popup.open()

class TestApp(App):
    def build(self):
        return FileSelector().overview_layout


if __name__ == '__main__':
    TestApp().run()