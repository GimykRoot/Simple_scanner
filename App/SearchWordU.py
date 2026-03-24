import os
import re
import pypdf
from docx import Document
import img2pdf
from PIL import Image

class FileAnalise():
    def __init__(self):
        self.task_list_universal = {
            0: [
            'Search specific links',
            'What site do you want to search:',
            'reddit, gmail',
            ['File name:', 'List of links:'],
            'Search specific links error',
            'Search links'
            ],
            1: [
            'Search word',
            'What word do you want to search:',
            'traum, root',
            ['Files with this word:'],
            'Search word error',
            'Search word'
            ],
            2: [
            'Image to PDF',
            'Enter the name of the future file:',
            'Scan08.11.2025, Photo_pass',
            ['The following file has been created:'],
            'No one image in current directory',
            'Img2PDF'
            ]
        }
        self.number_of_tasks = len(self.task_list_universal)
        self.current_path = os.getcwd()
        

    def work(self, task_index, path, item):
        self.item = item
        self.task_index = task_index
        self.task = self.task_list_universal[self.task_index][0]
        self.result_list = []
        self.error_list = []
        self.image_paths = []
        self.current_path = path
        self.extract_all_names()
        for docs_name in self.list_of_all_files:
            if docs_name.name.startswith("~$"):
                continue
            self.file_name = docs_name.name
            self.current_file_path = docs_name
            self.file_format_coordinate()
        match self.task_index:
            case 2:
                if self.image_paths:
                    self.pic_to_pdf(os.path.join(self.current_path, item))
                else:
                    self.error_list.append(( 'execution error', 'No one image in current directory'))
    
    #func to get a list of files
    def extract_all_names(self):
        self.list_of_all_files = list(self.current_path.rglob('*'))

    #func to get types of current file and directs to the appropriate function for working with each format
    def file_format_coordinate(self):
        self.file_type = self.current_file_path.suffix
        match self.task_index:
            case 0 | 1:
                match self.file_type:
                    case '.txt':
                        self.work_with_txt_file()
                    case '.pdf':
                        self.work_with_pdf_file()
                    case '.docx':
                        self.work_with_docx_file()
                    case _:
                        self.error_list.append((self.file_name, 'Unsupported format error'))
                        return
            case 2:
                if self.file_type.lower() in ('.png', '.jpg', '.jpeg'):
                   self.image_paths.append(self.current_file_path)
            case _:
                return

    #that func get text from file and then go to main task
    def work_with_txt_file(self):
        with open(self.current_file_path, 'r', encoding='utf-8') as workFile:
            self.content_text = workFile.read()
            self.execute_the_search_task()

    def work_with_docx_file(self):
        doc = Document(self.current_file_path)
        for par in doc.paragraphs:
            raw_text = par.text
            if raw_text:
                normalized_text = ' '.join(raw_text.split()).lower()
                self.content_text = normalized_text
                self.execute_the_search_task()
                self.hollow_check = False

    def work_with_pdf_file(self):
        try:
            self.content_all_pages = pypdf.PdfReader(self.current_file_path)
        except Exception as e:
            self.error_list.append((self.file_name, 'PDF reading error'))
            return
        for page in self.content_all_pages.pages:
            raw_text = page.extract_text()
            if raw_text:
                normalized_text = ' '.join(raw_text.split()).lower()
                self.content_text = normalized_text
                self.execute_the_search_task()
                self.hollow_check = False
    
    def execute_the_search_task(self):
        #coordinates text/link search in file
        match self.task_index:
            case 0:
                self.search_specific_link()
            case 1:
                self.search_word()
            case _:
                return
                
    def search_specific_link(self):
        url = rf"https?://\S*{re.escape(self.item)}\S*"
        list_of_link = list(re.findall(url, self.content_text))
        if list_of_link:
            self.result_list.append((self.current_file_path.relative_to(self.current_path), list_of_link)) 

    def search_word(self):
        if self.item in self.content_text and self.file_name not in self.result_list:
            self.result_list.append(self.current_file_path.relative_to(self.current_path))
            return

    def pic_to_pdf(self, output_pdf_path):
        #adding a file format
        if not output_pdf_path.lower().endswith('.pdf'):
                output_pdf_path += '.pdf'
        valid_images = [img for img in self.image_paths if img.lower().endswith(('.png', '.jpg', '.jpeg'))] #checking image format
        try:
            sorted_paths = sorted(valid_images) #sorting
            #convertation
            with open(output_pdf_path, 'wb') as f:
                print (f"End list: {sorted_paths}")
                f.write(img2pdf.convert(sorted_paths))
                self.result_list.append(output_pdf_path)
        except Exception as e:
            self.error_list.append(( 'execution error', f'Error creating PDF-file:{e}'))
