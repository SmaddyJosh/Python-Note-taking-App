from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.screen import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.list import OneLineListItem
import pytesseract
from PIL import Image
from kivy.uix.filechooser import FileChooserIconView
import cv2

from db_handler import initialize_db,add_note,get_all_notes,delete_notes
from kivymd.uix.list import OneLineListItem


screen_helper="""
Screen:
    MDBoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            left_action_items: [["menu", lambda x: nav_drawer.set_state("toggle")]]
            title: "All Notes"
            elevation: 5
        
        MDNavigationDrawer:
            id: nav_drawer

            MDNavigationDrawerMenu:

                MDNavigationDrawerHeader:
                    title: "Navigation Menu"
                    text: "User: Josh"
                    spacing: "4dp"
                    padding: "8dp"

                MDNavigationDrawerLabel:
                    text: "Options"
    
                MDNavigationDrawerItem:
                    icon: "note"
                    text: "Notes"
                    on_release: app.Load_Notes()
                    
    
                MDNavigationDrawerItem:
                    icon: "settings"
                    text: "Settings"
                    on_release: app.show_content("Settings")
    
                MDNavigationDrawerItem:
                    icon: "logout"
                    text: "Logout"
                    on_release: app.show_content("Logout")
            
        MDTextField:
            id: note_input
            hint_text: "Write your notes here..."
            mode: "rectangle"
            multiline: True
            size_hint_y: 0.8
        
        ScrollView:
            size_hint_y: 0.3
            MDList:
                id: notes_list

        MDBoxLayout:
            orientation:'horizontal'
            size_hint_y: None
            height: "50dp"  
            spacing: "10dp"
            
            
            MDRaisedButton:
                text: "Save Note"
                pos_hint: {"center_x": 0.5}
                on_press: app.save_note()
                
            MDRaisedButton:
                text: "Upload Image"
                pos_hint: {"center_x": 0.5}
                on_press: app.select_image()
    
            MDRaisedButton:
                text: "Extract Text"
                pos_hint: {"center_x": 0.5}
                on_press: app.extract_text()
    
            MDRaisedButton:
                text: "Get Notes"
                pos_hint: {"center_x": 0.5}
                on_press: app.Load_Notes()
            
            MDRaisedButton:
                text: "Delete All Notes!"
                pos_hint: {"center_x": 0.5}
                on_press: app.Del_Notes()
                
        MDLabel:
            id: message_label
            text: ""
            halign: "center"
            theme_text_color: "Hint"
            size_hint_y: None
            height: "40dp"



"""

class NotesApp(MDApp):
    def build(self):
        initialize_db()
        self.theme_cls.primary_palette = "Red"
        self.selected_image_path = None
        screen=Builder.load_string(screen_helper)
        return screen

    def save_note(self):
        note_text = self.root.ids.note_input.text
        image_path = self.selected_image_path
        title = note_text.strip().split('\n')[0][:30] or "Untitled"

        add_note(title, image_path, note_text)
        self.root.ids.message_label.text="Note has been saved to DB"
        print(f"Note saved to DB: {note_text}")
        self.root.ids.note_input.text = ""  # Clear after saving

    def show_content(self, name):
        print(f"Selected: {name}")
        Clock.schedule_once(lambda dt: self.root.ids.nav_drawer.set_state("close"), 0.5)


    def select_image(self):
        filechooser=FileChooserIconView()
        filechooser.bind(on_selection=self.image_selected)
        self.root.add_widget(filechooser)

    def image_selected(self,filechooser,selection):
        if selection:
            self.selected_image_path = selection[0]
            self.root.remove_widget(filechooser)

    def Load_Notes(self):
        self.root.ids.notes_list.clear_widgets()  # Clear previous notes from the list

        try:
            # Fetch all notes from the database
            notes = get_all_notes()

            for note in notes:
                note_id, title, image_path, ocr_text, created_at = note

                # Create a list item for each note
                note_item = OneLineListItem(text=f"{title} - {created_at}")
                self.root.ids.notes_list.add_widget(note_item)  # Add the note to the list
        except Exception as e:
            print("Could not fetch notes:", e)

    def Del_Notes(self):
        delete_notes()
        self.root.ids.message_label.text="All notes have been deleted"
        print("ALl notes have been deleted")





NotesApp().run()



