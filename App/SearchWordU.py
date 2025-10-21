import os
import re
import pypdf
from docx import Document

class FileAnalise():
    def __init__(self):
        self.list_of_functions_name = ['List of all links', 'Search specific links', 'Search word'] #list of all tasks
        self.current_path = os.getcwd()
        

    def work(self, task_index, path, item):
        self.item = item
        self.task_index = task_index
        self.task = self.list_of_functions_name[self.task_index]
        self.result_list = []
        self.error_list = []
        self.current_path = path
        self.extract_all_names()
        for docs_name in self.list_of_all_files:
            self.file_name = docs_name
            self.current_file_path = os.path.join(self.current_path, docs_name)
            self.file_format_coordinate()
    
    #func to get a list of files
    def extract_all_names(self):
        self.list_of_all_files = os.listdir(self.current_path)

    #func to get types of current file and directs to the appropriate function for working with each format
    def file_format_coordinate(self):
        self.file_type = ".".join(self.file_name.split(".")[-1:])
        match self.file_type:
            case 'txt':
                self.work_with_txt_file()
            case 'pdf':
                self.work_with_pdf_file()
            case 'docx':
                self.work_with_docx_file()
            case _:
                self.error_list.append((self.file_name, 'Unsupported format error'))
                return

    #that func get text from file and then go to main task
    def work_with_txt_file(self):
        with open(self.current_file_path, 'r', encoding='utf-8') as workFile:
            self.content_text = workFile.read()
            self.execute_the_task()

    def work_with_docx_file(self):
        doc = Document(self.current_file_path)
        for par in doc.paragraphs:
            raw_text = par.text
            if raw_text:
                normalized_text = ' '.join(raw_text.split()).lower()
                self.content_text = normalized_text
                self.execute_the_task()
                self.hollow_check = False

    def work_with_pdf_file(self):
        try:
            self.content_all_pages = pypdf.PdfReader(self.current_file_path)
        except Exception as e:
            self.error_list.append((self.file_name, 'PDF reading error'))
            return
        self.hollow_check = True
        for page in self.content_all_pages.pages:
            raw_text = page.extract_text()
            if raw_text:
                normalized_text = ' '.join(raw_text.split()).lower()
                self.content_text = normalized_text
                self.execute_the_task()
                self.hollow_check = False
    
    def execute_the_task(self):
        
        match self.task_index:
            case 0:
                self.search_link()
            case 1:
                self.search_specific_link()
            case 2:
                self.search_word()
            case _:
                return

    def search_link(self):
        url = r'https?://\S+(?<!\.)'
        list_of_link = list(re.findall(url, self.content_text))
        if list_of_link:
            self.result_list.append((self.file_name, list_of_link))

    def search_specific_link(self):
        url = rf"https?://\S*{re.escape(self.item)}\S*"
        list_of_link = list(re.findall(url, self.content_text))
        if list_of_link:
            self.result_list.append((self.file_name, list_of_link)) 

    def search_word(self):
        if self.item in self.content_text and self.file_name not in self.result_list:
            self.result_list.append(self.file_name)
            return
