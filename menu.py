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
    #     self.metro = None
    #     Clock.schedule_once(self.on_update, 5)
    #
    # def on_update(self, *args):
    #     if 'Pulsing' in self.mainbutton.text:
    #         self.metro = MetronomeWidget(1, True)
    #     else:
    #         self.metro = MetronomeWidget(1, False)
class Tab(Widget):
    def __init__(self):
        Widget.__init__(self)
        self.tabs = TabbedPanel()
        # Settings for the Tab Panel
        self.tabs.tab_width *= 2.7
        self.tabs.tab_height *= 2
        # Metronome Tab
        self.tabs.default_tab_text = 'IM: Moving Block'
        self.tabs.default_tab.font_size = 24
        self.tabs.default_tab_content = CustomDropDown()
        #MetronomeWidget(1, False, dropdown=CustomDropDown())
        # Different Visual Tab
        #tab0 = TabbedPanelHeader(text='IM: Pulsing', font_size=24)
        #tab0.content = MetronomeWidget(1, True)
        # Accompaniment Tab
        self.tab1 = TabbedPanelHeader(text='IM: Accompaniment', font_size=24)
        self.tab1.content = CustomDropDown().mainbutton

        #tabs.add_widget(tab0)
        self.tabs.add_widget(self.tab1)
        self.add_widget(self.tabs)


# create App class
class TabbedPanelApp(App):
    def __init__(self):
        App.__init__(self)
        self.metronome = MetronomeWidget(1, False)
        self.config_button = Button(text='Tempo Visual', size_hint=(None, None))
        self.title = 'Intuitive Metronome (IM)'
        self.layout = GridLayout(cols=1, padding=10)
        self.button = Button(text="Configure", font_size=24, size_hint_x=0.35)
        self.mode = 'Moving Block'
        self.accomp = False
        self.viz_feedback = None
        self.accomp_feedback = None
    def build(self):
        # Add a button
        top_row = GridLayout(cols=3, size_hint_y=0.2)
        self.viz_feedback = Label(text='Tempo Viz: %s' % self.mode, font_size=24)
        top_row.add_widget(self.viz_feedback)
        self.accomp_feedback = Label(text='Accomp: %s' % self.accomp, font_size=24)
        top_row.add_widget(self.accomp_feedback)
        top_row.add_widget(self.button)
        self.layout.add_widget(top_row)
        #self.layout.add_widget(self.button)
        # Attach a callback for the button press event
        self.button.bind(on_press=self.onButtonPress)
        self.layout.add_widget(self.metronome)
        Clock.schedule_interval(self.update, 1)
        return self.layout

    def update(self, *args):
        self.mode = self.config_button.text

        def is_pulsing(x):
            if x == 'Pulsing':
                return True, 'Tempo Viz: Pulsing'
            elif x == 'Moving Block' or x == 'Tempo Visual':
                return False, 'Tempo Viz: Moving Block'

        is_pulsed, vis_text = is_pulsing(self.mode)
        self.metronome.pulsing = is_pulsed
        self.viz_feedback.text = vis_text

        print('Pulsing:', is_pulsing(self.mode))

    # On button press - Create a popup dialog with a label and a close button
    def onButtonPress(self, button):
        popup_layout = GridLayout(cols=1, padding=5)
        close_button = Button(text="Close")

        config_layout = GridLayout(cols=2)
        # Add dropdown
        vis_opts = AnchorLayout(anchor_x='center', anchor_y='center')
        #vis_opts.add_widget(Label(text='Tempo'))

        vis_dropdown = DropDown()
        for vis_opt in ['Moving Block', 'Pulsing']:
            btn = Button(text=vis_opt, height=40, size_hint_y=None)
            btn.bind(on_release=lambda b: vis_dropdown.select(b.text))
            vis_dropdown.add_widget(btn)
        # create a big main button

        self.config_button.bind(on_release=vis_dropdown.open)
        vis_dropdown.bind(on_select=lambda instance, x: setattr(self.config_button, 'text', x))

        vis_opts.add_widget(self.config_button)
        config_layout.add_widget(vis_opts)
        # Add checkbox, Label and Widget
        acc_check = GridLayout(cols=1)
        checkbox_label = Label(text='Accompaniment')
        checkbox = CheckBox(active=True)
        acc_check.add_widget(checkbox_label)
        acc_check.add_widget(checkbox)
        config_layout.add_widget(acc_check)
        # Add 2nd and third item
        popup_layout.add_widget(config_layout)
        popup_layout.add_widget(close_button)
        # Instantiate the modal popup and display
        popup = Popup(title='Metronome Settings',
                      content=popup_layout,
                      size_hint=(None, None), size=(500, 500))
        popup.open()
        # Attach close button press with popup.dismiss action
        close_button.bind(on_press=popup.dismiss)

    # run the App
if __name__ == '__main__':
    TabbedPanelApp().run()