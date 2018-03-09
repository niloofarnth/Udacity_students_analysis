# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import unicodecsv
from datetime import datetime

#to read the csv files as a dictionary
def file_reader(file_name):
    with open (path + file_name , "rb") as file:
        reader = unicodecsv.DictReader(file)
        return list(reader)
    
path = "/Users/niloofartehrani/google drive/programming/data-analysis/"
daily_engagement = file_reader("daily_engagement.csv")
project_submissions = file_reader("project_submissions.csv")
enrollments = file_reader("enrollments.csv")

#to change the data types


def change_time_type(date):
    if date == '':
        return None
    else: 
        return datetime.strptime(date , '%Y-%m-%d')
    
def change_number_type(number):
    if number == '':
        return None
    else:
        return int(number)


for row in enrollments:
    row["join_date"] = change_time_type(row["join_date"])
    row["cancel_date"] = change_time_type(row["cancel_date"])
    row["days_to_cancel"] = change_number_type(row["days_to_cancel"])
    row["is_udacity"] = row["is_udacity"] == "True"
    row["is_canceled"] = row["is_canceled"] == "True"
    
for row in daily_engagement:
    row["utc_date"] = change_time_type(row["utc_date"])
    row["num_courses_visited"] = int(float(row["num_courses_visited"]))
    row["total_minutes_visited"] = float(row["total_minutes_visited"])
    row["lessons_completed"] = int(float(row["lessons_completed"]))
    row["projects_completed"] = int(float(row["projects_completed"]))
    
for row in project_submissions:
    row["creation_date"] = change_time_type(row["creation_date"])
    row["completion_date"] = change_time_type(row["completion_date"])
  
    
