from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from pathlib import Path
from kivy.uix.image import Image

from SearchWordU import FileAnalise
from FuncManager import FunctionalDialog

try:
    from plyer import filechooser
    HAS_PLYER = True
except ImportError:
    HAS_PLYER = False

class FileManagerApp(App):

    def build(self):
        Window.size = (600, 800)
        Window.clearcolor = (0.61, 0.61, 0.71, 1)
        self.titel = 'InFile Searcher'
        return FileManagerGUI()

class FileItem(BoxLayout):      #widget for every file
    def __init__(self, path, name, file_type, size, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 40
        self.padding = 5
        self.spacing = 10
        # icon
        icon = Image(
            source=path,
            size_hint=(None, None),
            size=(32, 32)
        )
        self.add_widget(icon)
        #name
        name_label = Label(
            text=name,
            size_hint_x=0.5,
            halign='left',
            valign='middle'
        )
        name_label.bind(size=name_label.setter('text_size'))
        self.add_widget(name_label)
        #file type
        type_label = Label(
            text=file_type,
            size_hint_x=0.25,
            halign='center',
            valign='middle'
        )
        self.add_widget(type_label)
        #size
        size_label = Label(
            text=size,
            size_hint_x=0.25,
            halign='right',
            valign='middle'
        )
        size_label.bind(size=size_label.setter('text_size'))
        self.add_widget(size_label)

class FileManagerGUI(BoxLayout, FileAnalise):
  
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        self.current_path= None
        self.file_types = {
            "folder": 'icon/folder.png',
            ".txt": 'icon/text.png',
            ".py": 'icon/python.png',
            ".pdf": 'icon/pdf.png',
            ".doc": 'icon/doc.png',
            "default": 'icon/default.png'
        }
        self.setup_ui()

    def setup_ui(self):
        #Top panel
        top_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1, spacing=10)
        #Place for specified directory
        select_btn = Button(text='Specify the path \n to the directory', size_hint_x=0.25)
        select_btn.bind(on_press=self.select_directory)
        top_layout.add_widget(select_btn)
        #Label for path
        self.path_label = Label(
            text='Path not specified',
            size_hint_x=0.55,
            halign='left',
            valign='middle'
        )
        self.path_label.bind(size=self.path_label.setter('text_size'))
        top_layout.add_widget(self.path_label)
        #Button for the fuction menu
        menu_btn = Button(text='Function menu', size_hint_x=0.2)
        menu_btn.bind(on_press=self.show_function_menu)
        top_layout.add_widget(menu_btn)
        self.add_widget(top_layout)
        # Names of labels
        header_layout = BoxLayout(orientation='horizontal', size_hint_y=0.05, spacing=10)
        header_layout.add_widget(Label(text='Name', size_hint_x=0.5, bold=True))
        header_layout.add_widget(Label(text='Type', size_hint_x=0.25, bold=True))
        header_layout.add_widget(Label(text='Size', size_hint_x=0.25, bold=True))
        self.add_widget(header_layout)
        # Scroll of files
        scroll_view = ScrollView(size_hint=(1, 0.85))
        self.file_list = GridLayout(cols=1, size_hint_y=None, spacing=5)
        self.file_list.bind(minimum_height=self.file_list.setter('height'))
        scroll_view.add_widget(self.file_list)
        self.add_widget(scroll_view)

    def display_content(self):
        self.file_list.clear_widgets()
        if not self.current_path:
            return
        try:
            items = list(self.current_path.iterdir())
            # Folder first, done then files
            folders = sorted([x for x in items if x.is_dir()], key=lambda x: x.name.lower())
            files = sorted([x for x in items if x.is_file()], key=lambda x: x.name.lower())
            # Folders
            for folder in folders:
                icon = self.file_types["folder"]
                file_item = FileItem(
                    name=f"{icon} {folder.name}",
                    file_type="Folder",
                    size=""
                )
                self.file_list.add_widget(file_item)
            # Files
            for file in files:
                ext = file.suffix.lower()
                icon = self.file_types.get(ext, self.file_types["default"])
                size = self.format_size(file.stat().st_size)
                file_type = ext if ext else "File"

                file_item = FileItem(
                    path=icon,
                    name=f"{file.name}",
                    file_type=file_type,
                    size=size
                )
                self.file_list.add_widget(file_item)
        except PermissionError:
            self.show_error("No access to directory")
        except Exception:
            self.show_error(f"An Error occurred: {str(Exception)}")
    
    def format_size(self, size):
        #Size of files
        for unit in ['B', 'KiB', 'MiB', 'GiB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TeB"

    def show_function_menu(self, instance):
        #Menu with func
        dropdown = DropDown()
        for func_name in ['List of all links', 'Search specific links', 'Search word']:
            btn = Button(text=func_name, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn, name=func_name: self.open_function_dialog(name, dropdown))
            dropdown.add_widget(btn)
        dropdown.open(instance)

    def open_function_dialog(self, function_name, dropdown):
        #Functions dialog menu
        dropdown.dismiss()
        task_index = self.list_of_functions_name.index(function_name)
        dialog = FunctionDialog(task_index, self.current_path)
        dialog.open()

    def select_directory(self, instance):
        if HAS_PLYER:
            try:
                path = filechooser.choose_dir(title="Select a directory")
                if path:
                    self.current_path = Path(path[0])
                    self.path_label.text = str(self.current_path)
                    self.display_contents()
            except Exception as e:
                self.show_error(f"Path error: {str(e)}")
        else:
            #if without plyr
            content = BoxLayout(orientation='vertical', padding=10, spacing=10)
            content.add_widget(Label(text='Enter the path to the directory:'))
            path_input = TextInput(multiline=False, size_hint_y=0.3)
            content.add_widget(path_input)
            btn_layout = BoxLayout(size_hint_y=0.3, spacing=10)

            def confirm_path(instance):
                path_text = path_input.text
                if path_text and Path(path_text).exists():
                    self.current_path = Path(path_text)
                    self.path_label.text = str(self.current_path)
                    self.display_content()
                    popup.dismiss()
                else:
                    self.show_error("This path doesn't exist")

            ok_btn = Button(text='OK')
            ok_btn.bind(on_press=confirm_path)
            btn_layout.add_widget(ok_btn)

            cancel_btn = Button(text='Cancel')
            cancel_btn.bind(on_press=lambda x: popup.dismiss())
            btn_layout.add_widget(cancel_btn)

            content.add_widget(btn_layout)

            popup = Popup(
                title='Directory selection',
                content=content,
                size_hint=(0.8, 0.4)
            )
            popup.open()

    def show_error(self, message):
        #correct Error return
        popup = Popup(
            title='Error',
            content=Label(text=message) 
            size_hint=(0.6, 0.4)
        )
        popup.open()
