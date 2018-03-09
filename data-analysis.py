# -*- coding: utf-8 -*-

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
    row["account_key"] = row.pop("acct")
    
for row in project_submissions:
    row["creation_date"] = change_time_type(row["creation_date"])
    row["completion_date"] = change_time_type(row["completion_date"])
  
    
#find the total number of the rows in each file
enrollment_num_rows = len(enrollments)
engagement_num_rows = len(daily_engagement)
submission_num_rows = len(project_submissions)


#find unique students
def find_unique_students(table_name):
    unique_students= set()
    for row in table_name:
        unique_students.add(row["account_key"])
    return unique_students
        

enrollment_unique_students = find_unique_students(enrollments)
engagement_unique_students = find_unique_students(daily_engagement)
submission_unique_students= find_unique_students(project_submissions)

enrollment_num_unique_students = len(enrollment_unique_students )
engagement_num_unique_students = len(engagement_unique_students )
submission_num_unique_students= len(submission_unique_students)

#find the students who are in enrollment but not in engagement
not_in_engagement = set()
for student in enrollment_unique_students:
    if student not in engagement_unique_students:
        not_in_engagement.add(student)
    else:
        continue
#print (not_in_engagement)

#find the odd students among who are not in engagement  
problem_students = []
for student in not_in_engagement:
    for row in enrollments:
        if student == row["account_key"]:
            if row["days_to_cancel"] != 0:
                problem_students.append(row)
#print (problem_students)


#find the udacity test accounts which means students whose is_udacity is true
test_accounts = set()
for student in enrollments:
    if student["is_udacity"]:
        test_accounts.add(student["account_key"])
#print (test_accounts)

#function to remove udacity test_accounts form the all tables
def remove_test_accounts(table_name):
    new_table = []
    for student in table_name:
        if student["account_key"] not in test_accounts:
            new_table.append(student)
    return new_table
            
non_udacity_enrollments = remove_test_accounts(enrollments)
non_udacity_engagements = remove_test_accounts(daily_engagement)
non_udacity_engagements = remove_test_accounts(project_submissions)


            
            

