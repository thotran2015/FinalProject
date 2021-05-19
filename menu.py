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
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from animation import MetronomeWidget
from kivy.uix.dropdown import DropDown
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
from kivy.clock import Clock
from testing_filechooser import FileSelector
from kivy.core.window import Window
from animation import BG_COLOR, TEXT_COLOR
#(249, 56, 0)
#CONFIGURE_COLOR = (249/255, 56/255, 0/255, 1)
CONFIGURE_COLOR = (1, 0, 0, 1)
#TabbedPanelItem,
# Floatlayout allows us to place the elements
# relatively based on the current window
# size and height especially in mobiles
from kivy.uix.floatlayout import FloatLayout


# Create Tabbed class
class CustomDropDown(Widget):
    # Dropdown Variables
    def __init__(self, options=['Moving Block', 'Pulsing']):
        Widget.__init__(self)
        self.vis_dropdown = DropDown()
        for vis_opt in options:
            btn = Button(text=vis_opt, height=40, size_hint_y=None)
            btn.bind(on_release=lambda b: self.vis_dropdown.select(b.text))
            self.vis_dropdown.add_widget(btn)
        # create a big main button
        self.mainbutton = Button(text='Tempo Visual', size_hint=(None, None))
        self.mainbutton.bind(on_release=self.vis_dropdown.open)
        self.vis_dropdown.bind(on_select=lambda instance, x: setattr(self.mainbutton, 'text', x))
        self.add_widget(self.mainbutton)


# create App class
class TabbedPanelApp(App):
    def __init__(self):
        App.__init__(self)
        Window.clearcolor = BG_COLOR
        self.metronome = MetronomeWidget(1, False)
        self.title = 'Intuitive Metronome (IM)'
        self.layout = GridLayout(cols=1, padding=10)
        self.config_button = Button(text="Configure", font_size=24, size_hint_x=0.35, bold=True, color=TEXT_COLOR,
                                    background_color=CONFIGURE_COLOR)
        self.mode = 'Moving Block'
        self.accomp = False
        self.selected_file = None
        self.viz_feedback = None
        self.accomp_feedback = None
        self.file_chooser = FileSelector()
        Clock.schedule_interval(self.update, 1)


    def build(self):
        # Add a button
        #self.build_app_layout()
        self.vis_dropdown = DropDown()
        popup_layout = self.build_popup_layout(self.vis_dropdown)
        self.config_popup = Popup(title='Metronome Settings', content=popup_layout,
                      size_hint=(None, None), size=(700, 500), title_size=24)
        # Attach close button press with popup.dismiss action
        self.close_button.bind(on_press=self.config_popup.dismiss)
        self.build_app_layout()

        # Clock.schedule_interval(self.update, 0.2)
        return self.layout

    def update(self, *args):
        self.mode = self.tempo_vis_button.text
        self.selected_file = self.file_chooser.selected_file

        if self.selected_file == 'No file selected':
            self.accomp = False
        else:
            self.accomp = True

        if 'midi' in self.selected_file:
            self.metronome.accomp_file = self.selected_file
        self.accomp_feedback.text = 'Accompaniment: %s' % self.accomp

        def is_pulsing(x):
            if x == 'Pulsing':
                return True, 'Tempo Vis.: Pulsing'
            elif x == 'Moving Block' or x == 'Tempo Visual':
                return False, 'Tempo Vis.: Moving Block'

        is_pulsed, vis_text = is_pulsing(self.mode)
        self.metronome.pulsing = is_pulsed
        self.viz_feedback.text = vis_text


    def build_app_layout(self):
        top_row = GridLayout(cols=3, size_hint_y=0.2)
        self.viz_feedback = Label(text='Tempo Vis.: %s' % self.mode, font_size=24, bold=True, color=TEXT_COLOR)
        self.accomp_feedback = Label(text='Accompaniment: %s' % self.accomp, font_size=24, bold=True, color=TEXT_COLOR)

        # Attach a callback for the button press event
        self.config_button.bind(on_press=self.onButtonPress)

        top_row.add_widget(self.viz_feedback)
        top_row.add_widget(self.accomp_feedback)
        top_row.add_widget(self.config_button)
        self.layout.add_widget(top_row)

        self.layout.add_widget(self.metronome)

    def build_popup_layout(self, vis_dropdown):
        # Configuration Feature
        popup_layout = GridLayout(cols=1, padding=5)
        self.close_button = Button(text="Close", size_hint_y=0.2, font_size=24)
        config_layout = GridLayout(cols=2)
        # Add dropdown
        vis_opts = GridLayout(cols=1, padding=(30, 0, 30, 95))
        for vis_opt in ['Moving Block', 'Pulsing']:
            btn = Button(text=vis_opt, height=40, size_hint_y=None, font_size=24)
            btn.bind(on_release=lambda b: vis_dropdown.select(b.text))
            vis_dropdown.add_widget(btn)
        # create a big main button
        self.tempo_vis_button = Button(text='Moving Block', font_size=24, size_hint=(0.7, None))
        self.tempo_vis_button.bind(on_release=vis_dropdown.open)
        vis_dropdown.bind(on_select=lambda instance, x: setattr(self.tempo_vis_button, 'text', x))

        vis_opts.add_widget(Label(text='Select Tempo Visual Below', font_size=24))
        vis_opts.add_widget(self.tempo_vis_button)
        config_layout.add_widget(vis_opts)

        # Add checkbox, Label and Widget
        acc_check = GridLayout(cols=1, padding=(20, 15, 20, 95))
        selector_label = Label(text='Accompaniment', font_size=25)
        file_selector = self.file_chooser.overview_layout

        acc_check.add_widget(selector_label)
        acc_check.add_widget(file_selector)
        config_layout.add_widget(acc_check)
        # Add 1st and 2nd item
        popup_layout.add_widget(config_layout)
        popup_layout.add_widget(self.close_button)
        return popup_layout
        # Instantiate the modal popup and display

    # On button press - Create a popup dialog with a label and a close button
    def onButtonPress(self, button):
        self.config_popup.open()

    # run the App
if __name__ == '__main__':
    TabbedPanelApp().run()
