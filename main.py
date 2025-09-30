from re import search

from SearchWordU import FileAnalise
import os

actual_path = os.path.join(os.getcwd(),'Test')
print(f'Actual path: {actual_path}')
Works1 = FileAnalise(actual_path)
task_list = ['list of links','specific link search','search for a word']
task_number = int(input("What do you want to do? You can write only number of function:"))
if task_number!=1:
    item = input("Word:")
else:
    item = ''
Works1.make(task_list[task_number-1],item)

