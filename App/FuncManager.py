from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
import os

from App.SearchWordU import FileAnalise

class FunctionDialog(Popup, FileAnalise):
    """Functional menu of app"""
    def __init__(self, function_index, path, callback=None, **kwargs):
        super().__init__(**kwargs)
        self.path = path
        self.function_index = function_index
        self.title = self.task_list_universal[self.function_index][0]
        self.size_hint = (0.6, 0.4)
        self.callback = callback
        # Main container
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Title
        title_label = Label(
            text=self.task_list_universal[self.function_index][5],
            size_hint_y=0.2,
            font_size='20sp',
            bold=True
        )
        layout.add_widget(title_label)
        #text
        top_label = Label(
            text=self.task_list_universal[self.function_index][1],
            size_hint_y=0.6,
            halign='center',
            valign='middle'
        )
        top_label.bind(size=top_label.setter('text_size'))
        layout.add_widget(top_label)
        # Input field
        input_layout = GridLayout(cols=2, size_hint_y=0.3, spacing=10)
        self.entry1 = TextInput(
            multiline=False,
            hint_text=self.task_list_universal[self.function_index][2], #example of input text
            size_hint_y=None,
            size_hint_x=0.3,
            height=40
        )
        input_layout.add_widget(self.entry1)

        layout.add_widget(input_layout)

        # Buttons
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=0.2, spacing=10)

        execute_btn = Button(text='Execute')
        execute_btn.bind(on_press=self.execute_function)
        button_layout.add_widget(execute_btn)

        cancel_btn = Button(text='Cancel')
        cancel_btn.bind(on_press=self.dismiss)
        button_layout.add_widget(cancel_btn)

        layout.add_widget(button_layout)
        self.content = layout

    def execute_function(self, instance):

        item = self.entry1.text
        self.work(self.function_index, self.path, item)
        text_content=''
        # Print results"""self.function_index != 2 and"""
        if self.result_list:
            match self.function_index:
                case 0:
                    text_content = '\n'.join(
                        f"{self.task_list_universal[self.function_index][3][0]} {item[0]} \n {self.task_list_universal[self.function_index][3][1]} {item[1]}"
                        for item in self.result_list
                    )
                case 1:
                    text_content = '\n'.join(
                        f"{self.task_list_universal[self.function_index][3][0]} {item}"
                        for item in self.result_list
                        )
                case 2:
                    if not item.lower().endswith('.pdf'):
                        item += '.pdf'
                    text_content = f"File {item} has been created successfully. \n Full path to the file: {os.path.join(self.path, item)} "
        else:
            text_content = 'No results'
        result_popup = Popup(
            title='Result:',
            content=TextInput(
                text=text_content,
                readonly=True,     
                background_color=(0, 0, 0, 0), 
                foreground_color=(1, 1, 1, 1), 
                border=(0, 0, 0, 0) 
            ),
            size_hint=(0.9, 0.5)
        )
        result_popup.open()

        if self.callback:
            self.callback(self.task_list_universal[self.function_index][4])
        self.dismiss()
