import os
import re
import pypdf

class FileAnalise():
    def __init__(self,carr_path):               #take a path to work dir
        self.curr_path= carr_path
        self.error_result_files=[]
        self.task_list = ['list of links','specific link search','search for a word']
        print(f'The program has 3 operating modes: {self.task_list} \n ')

    def make(self, task, item):
        self.task = task
        self.item = item

        self.result_works_with_word = []
        self.result_works_with_spec_link = []
        self.result_link_list = []

        self.extract_all_names()
        for works_name in self.file_list:
            self.check_file_or_subdir(works_name)
            self.file_name = os.path.basename(self.curr_file_path)
            self.file_format_coordinate()

        self.result_output()
        self.result_in_file_output()

    def extract_all_names(self):                #create list with all subdir names
        self.file_list = os.listdir(self.curr_path)

    def change_dir(self, old_dir, new_dir):     #func to change work subdir
        try:
            os.chdir(new_dir)
        except:
            return
        finally:
            os.chdir(old_dir)

    def check_file_or_subdir(self, file_name):               #func to check is work subdir the file or not
        self.curr_file_path = os.path.join(self.curr_path, file_name)
        if not os.path.isfile(self.curr_file_path):
            print(f'CurrFile:{self.file_name} is not file')
            self.change_dir(self.curr_path,self.curr_file_path)

    def file_format_coordinate(self):                       # take a format of the file
        self.file_format = ".".join(self.file_name.split(".")[-1:])
        match self.file_format:
            case 'txt':
                self.work_with_txt_file()
            case 'pdf': #dont work jet
                self.work_with_pdf_file()
            case _:
                self.error_result_files.append((self.file_name, "Invalid file format"))


    def work_with_txt_file(self):                #func that open txt-file and tries to work with it
        with open(self.curr_file_path, 'r', encoding='utf-8') as workFile:
            self.content= workFile.read()
            self.choise_the_task()

    def work_with_pdf_file(self):                # func that open pdf-file and tries to work with it
        self.content_all_pages= pypdf.PdfReader(self.curr_file_path)
        self.hollow_check = True
        self.list_of_page = []
        for page in self.content_all_pages.pages:
            self.content = page.extract_text()
            if self.content:
                self.choise_the_task()
                self.hollow_check = False
            if self.file_name in self.result_works_with_word:
                return
        if self.list_of_page:
            self.result_works_with_spec_link.append((self.file_name, self.list_of_page))
        if self.hollow_check:
            self.error_result_files.append((self.file_name, "PDF without text"))
            return

    def search_links(self):                           #will search all link in file
        url = r'https?://\S+(?<!\.)'
        list_of_link = list(re.findall(url, self.content))
        if list_of_link:
            self.result_link_list.append( (self.file_name,list_of_link) )

    def search_specific_link(self):
        url = rf"https?://\S*{re.escape(self.item)}\S*"
        list_of_link = list(re.findall(url, self.content))
        if list_of_link:
            if self.file_format == 'txt':
                self.result_works_with_spec_link.append((self.file_name, list_of_link))
            else:
                self.list_of_page.append(list_of_link)


    def search_word(self):
        if self.item in self.content:
            self.result_works_with_word.append(self.file_name)
            return

    def choise_the_task(self):
        match self.task:
            case task if task==self.task_list[0]:
                self.search_links()
            case task if task==self.task_list[1]:
                self.search_specific_link()
            case task if task==self.task_list[2]:
                self.search_word()
            case _:
                print("Task error")

    def result_output(self):
        print('Results of work: \n')
        match self.task:
            case task if task == self.task_list[0]:
                for result in self.result_link_list:
                    print(f'File name:{result[0]} || List of links:{result[1]} \n')
            case task if task == self.task_list[1]:
                print(f'Files with correspond links:{self.result_works_with_spec_link} \n')
            case task if task==self.task_list[2]:
                print(f'Files with this word:{self.result_works_with_word} \n')
        print("Files with errors: \n ")
        for error_file in self.error_result_files:
            print (f'File name:{error_file[0]} || Error type: {error_file[1]}')

    def result_in_file_output(self):
        with open("Result.txt", "w", encoding="utf-8") as output:
            output.write('Results of work: \n')
            match self.task:
                case task if task == self.task_list[0]:
                    for result in self.result_link_list:
                        output.write(f'File name:{result[0]} || List of links:{result[1]} \n')
                case task if task == self.task_list[1]:
                    for result in self.result_works_with_spec_link:
                        output.write(f'File name:{result[0]} || List of links:{result[1]}\n')
                case task if task == self.task_list[2]:
                    output.write(f'Files with this word:{self.result_works_with_word} \n')
            output.write("Files with errors: \n")
            for error_file in self.error_result_files:
                output.write(f'File name:{error_file[0]} || Error type: {error_file[1]}')
