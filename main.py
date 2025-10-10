from re import search
from SearchWordU import FileAnalise
import os

Works1 = FileAnalise()
task_list = ['List of all links', 'Search specific links', 'Search word']
task_number = int(input("What do you want to do? You can write only number of function:"))
if task_number!=1:
    item = input("Word:")
else:
    item = ''
Works1.work(task_list[task_number-1],item)

