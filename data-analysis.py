# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import unicodecsv
def file_reader(file_name):
    with open (path + file_name , "rb") as file:
        reader = unicodecsv.DictReader(file)
        return list(reader)
    
path = "/Users/niloofartehrani/google drive/programming/data-analysis/"
daily_engagement = file_reader("daily_engagement.csv")
project_submissions = file_reader("project_submissions.csv")

print (daily_engagement[0])