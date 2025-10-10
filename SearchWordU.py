import os
import re
import pypdf

class FileAnalise():
    def __init__(self):
        self.list_of_functions_name = ['List of all links', 'Search specific links', 'Search word'] #list of all tasks
        self.current_path = os.getcwd()
        

    def work(self, task, item):
        self.task = task
        self.item = item
        self.task_index = self.list_of_functions_name.index(self.task)
        self.result_list = []
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
            case _:
                print(f'File:{self.file_name}| Type Error')

    #that func get text from file and then go to main task
    def work_with_txt_file(self):
        with open(self.current_file_path, 'r', encoding='utf-8') as workFile:
            self.content = workFile.read()
            self.execute_the_task()

    def work_with_pdf_file(self):
        self.content_all_pages = pypdf.PdfReader(self.current_file_path)
        self.hollow_check = True #check for text in pdf file
        for page in self.content_all_pages.pages:
            self.content = page.extract_text()
            if self.content:
                self.execute_the_task()
                self.hollow_check = False

        if self.hollow_check:
            print(f'File:{self.file_name}| PDF without text')
    
    def execute_the_task(self):
        
        match self.task_index:
            case 0:
                self.search_link()
            case 1:
                self.search_specific_link()
            case 2:
                self.search_word()
            case _:
                print("Task error")

    def search_link(self):
        url = r'https?://\S+(?<!\.)'
        list_of_link = list(re.findall(url, self.content)
        if list_of_link:
            self.result_list.append((self.file_name, list_of_link))

    def search_specific_link(self):
        url = rf"https?://\S*{re.escape(self.item)}\S*"
        list_of_link = list(re.findall(url, self.content)
        if list_of_link:
            self.result_list.append((self.file_name, list_of_link)) 

    def search_word(self):
        if self.item in self.content and self.name not in self.result_list:
            self.result_list.append(self.file_name)
            return

    def print_results(self):
        print('RESULTS:')
        match self.task_index:
            case 0 | 1:
                for names in self.result_list:
                    print(f'File name:{self.result_list[0]}| Result of search:{self.result_list[0]}')
            case 2:
                for names in self.result_list:
                    print(f'File name:{self.result_list[0]}')
            
        
