# -*- coding: utf-8 -*-

import unicodecsv
from datetime import datetime as dt
import datetime
import numpy as np
import time
import matplotlib.pyplot as plt
import seaborn as sns
start_time = time.time()

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
        return dt.strptime(date , '%Y-%m-%d')
    
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
            
#I will use these tables from now on
non_udacity_enrollments = remove_test_accounts(enrollments)
non_udacity_engagements = remove_test_accounts(daily_engagement)
non_udacity_submissions = remove_test_accounts(project_submissions)


#find the paid students in the enrollment table if they have not cancelled or 
#have been enrolled more than 7 days
paid_student = {}
for student in non_udacity_enrollments:
    if student["days_to_cancel"] == None or student["days_to_cancel"] >7:
        if student["account_key"] not in paid_student.keys():
            paid_student[student["account_key"]] = student["join_date"]
#to make sure that the enrollment date is the most recent one
        elif student["join_date"] > paid_student[student["account_key"]]:
            paid_student[student["account_key"]] = student["join_date"]

#add another column in engagement table for the days that student has visited
for account in non_udacity_engagements:
    if account["num_courses_visited"]>0:
        account["day_visited"] = 1
    else:
        account["day_visited"] = 0      
        
        
#find dates within one week of a date 
def within_one_week(enrollment_date, engagement_date):
    margin = datetime.timedelta(days = 7)
    if enrollment_date <= engagement_date < enrollment_date + margin:
        return True
        
paid_engagement_in_first_week = []  
#data from engagement tabel for duration of one week where the student was a paid student 
for engagement in non_udacity_engagements:
    if engagement["account_key"] in paid_student.keys():
        if within_one_week(paid_student[engagement["account_key"]] ,engagement["utc_date"]):
            paid_engagement_in_first_week.append(engagement)
#print (len(paid_engagement_in_first_week))
        
account_key_paid_first_week = set()
for student in paid_engagement_in_first_week:
    account_key_paid_first_week.add(student["account_key"])
    
passing_engagement_accounts = set()
for submission in non_udacity_submissions:
    if submission["account_key"] in account_key_paid_first_week \
    and submission["lesson_key"] in ["746169184", "3176718735"]:
        if submission["assigned_rating"] in ["PASSED", "DISTINCTION"]:
            passing_engagement_accounts.add(submission["account_key"])
             
passing_engagement = []
non_passing_engagement = []
for engagement in paid_engagement_in_first_week:
    if engagement["account_key"] in passing_engagement_accounts:
        passing_engagement.append(engagement)
    elif engagement["account_key"] not in passing_engagement_accounts:
        non_passing_engagement.append(engagement)  
           
#find average minutes spent in classroom during the first week of engagement with 3 functions
def engagement_dicts(column_in_engagement, which_engagement):
    dict_name = {}
    for key in paid_student.keys():
        list_name = []
        for engagement in which_engagement:
            if engagement["account_key"] == key:
                list_name.append(engagement[column_in_engagement])
        if len(list_name) > 0:
            dict_name[key] = list_name
    return dict_name

def total_engagement_dicts(dict_name):
    total_dict_name = {}
    for account_key in dict_name.keys():
        total_dict_name[account_key]= sum(dict_name[account_key])
    return total_dict_name

def average_engagement(total_engagement_dict):
    total = list(total_engagement_dict.values())
    average = np.mean(total)
    standard_dev = np.std(total)
    minimum = np.min(total)
    maximum = np.max(total)
    return ("%.2f"%average, "%.2f" %standard_dev, "%.2f" % minimum, "%.2f"% maximum)

minutes_passed_stats = average_engagement(total_engagement_dicts(engagement_dicts("total_minutes_visited", passing_engagement)))
days_stats = average_engagement(total_engagement_dicts(engagement_dicts("day_visited", passing_engagement)))
lessons_passed_stats = average_engagement(total_engagement_dicts(engagement_dicts("lessons_completed", passing_engagement)))
minutes_nonpassed_stats = average_engagement(total_engagement_dicts(engagement_dicts("total_minutes_visited", non_passing_engagement)))
days_stats = average_engagement(total_engagement_dicts(engagement_dicts("day_visited", non_passing_engagement)))
lessons_nonpassed_stats = average_engagement(total_engagement_dicts(engagement_dicts("lessons_completed", non_passing_engagement)))
minutes_stats = average_engagement(total_engagement_dicts(engagement_dicts("total_minutes_visited", paid_engagement_in_first_week)))
days_stats = average_engagement(total_engagement_dicts(engagement_dicts("day_visited", paid_engagement_in_first_week)))
lessons_passed = average_engagement(total_engagement_dicts(engagement_dicts("lessons_completed", paid_engagement_in_first_week)))

def hist_plotting(column_in_engagement, which_engagement, title):
    data = (total_engagement_dicts(engagement_dicts(column_in_engagement, which_engagement))).values()
    plt.figure() 
    plt.hist(data)
    plt.title(title)
    plt.xlabel(column_in_engagement)
    

#plotting the histograms
hist_plotting("total_minutes_visited", passing_engagement, "students who passed the project")   
hist_plotting("total_minutes_visited", non_passing_engagement, "students who didn't pass the project") 
hist_plotting("lessons_completed", passing_engagement, "students who passed the project") 
hist_plotting("lessons_completed", non_passing_engagement, "students who didn't pass the project")
hist_plotting("day_visited", passing_engagement, "students who passed the project") 
hist_plotting("day_visited", non_passing_engagement, "students who didn't pass the project")
  

print ("My program took {} seconds to run".format(time.time() - start_time))