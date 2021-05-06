# import kivy module
import kivy

# base Class of your App inherits from the App class.
# app:always refers to the instance of your application
from kivy.app import App

# this restrict the kivy version i.e
# below this kivy version you cannot
# use the app or software
kivy.require('1.9.0')

# to  use this must have to import it
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.label import Label
from animation import MetronomeWidget, CustomDropDown
#TabbedPanelItem,
# Floatlayout allows us to place the elements
# relatively based on the current window
# size and height especially in mobiles
from kivy.uix.floatlayout import FloatLayout

# Create Tabbed class
class Tab(TabbedPanel):
    def __init__(self):
        TabbedPanel.__init__(self)
    @property
    def create_menu(self):
        tabs = TabbedPanel()
        # Settings for the Tab Panel
        tabs.tab_width *= 2
        tabs.tab_height *= 2
        # Metronome Tab
        tabs.default_tab_text = 'Metronome1'
        tabs.default_tab.font_size = 24
        tabs.default_tab_content = MetronomeWidget(1, False, dropdown=CustomDropDown())
        # Different Visual Tab
        tab0 = TabbedPanelHeader(text='Metronome2', font_size=24)
        tab0.content = MetronomeWidget(1, True, dropdown=CustomDropDown())
        # Accompaniment Tab
        tab1 = TabbedPanelHeader(text='Accompaniment', font_size=24)
        tab1.content = CustomDropDown().mainbutton

        tabs.add_widget(tab0)
        tabs.add_widget(tab1)
        return tabs


# create App class
class TabbedPanelApp(App):
    def build(self):
        tabs = Tab()
        return tabs.create_menu


# run the App
if __name__ == '__main__':
    TabbedPanelApp().run()