import pandas
import csv

root = 'D:\\upama_desktop\\Summer_2019\\MIND_Data\\class_format_data' # folder that will contain data from all the district and years

# get student level data(iid, grade, stmath_user_id)
student_info_dict = dict()
# read the student level data
print("Getting student info...")
csv_file = 'D:\\upama_desktop\\Summer_2019\\MIND_Data\\cleaned_merged_student_info.csv' # path to student info file
student_info_df = pandas.read_csv(csv_file, index_col="student_entity_id")
# for chunk in pandas.read_csv(csv_file, chunksize=1000, iterator=True, index_col='student_entity_id'):
for row in student_info_df.itertuples():
    student_info_dict[row.Index] = (row.iid, row.gcd, row.teacher_entity_id,row.first_login_date,row.first_progress_date,row.date_of_last_login, row.content_progress_june, 
                                   row.num_lab_logins_june, row.num_home_logins_june, row.num_minutes_june, row.content_progress_april,
                                   row.num_lab_logins_april, row.num_home_logins_april, row.num_minutes_april)
del student_info_df

print("Creating new datasets for basic stats...")
result_file = 'D:\\upama_desktop\\Summer_2019\\scripts\\analysis\\results\\basic_stats_final.csv'
fields = ['year','student_entity_id','iid','gcd','teacher_entity_id','first_login_date','first_progress_date','date_of_last_login','content_progress_june','num_lab_logins_june','num_home_logins_june','num_minutes_june','content_progress_april','num_lab_logins_april','num_home_logins_april','num_minutes_april']
            
with open(result_file, mode='a') as cms:
    writer = csv.writer(cms)
    writer.writerow(fields)
###########
total_level_attempts = 0
passed_level_attempts = 0
failed_level_attempts = 0

###########
root_ = 'D:\\upama_desktop\\Summer_2019\\scripts\\analysis\\preprocessed_data\\'
years = ['2014','2015','2016','2017'] # get the list of files under district and year folder
student_list_dict = dict()
for year in years:
    file = 'laws_lab_DC_' + year + '.csv'
    print(file)
    file_path = root_ + file # set the path to corresponding institution file
    new_df = pandas.read_csv(file_path)
    new_df = new_df[new_df.gcd != "GRADE6"]
    total_level_attempts = total_level_attempts + len(new_df)
    passed_level_attempts = passed_level_attempts + len(new_df[new_df.failed == 0])
    failed_level_attempts = failed_level_attempts + len(new_df[new_df.failed == 1])
    
    students = new_df.student_entity_id.unique()
    for student in students:
        if student_info_dict.get(student) is not None:
            if student_list_dict.get(student) is None:
                student_list_dict[student] = 1
                student_info = student_info_dict[student]
                data = [[year,student,student_info[0],student_info[1],student_info[2],student_info[3],student_info[4],student_info[5],student_info[6],student_info[7],student_info[8],student_info[9],student_info[10],student_info[11],student_info[12],student_info[13]]]
                result_df = pandas.DataFrame(data)
                result_df.to_csv(result_file,mode='a',header=None,index=False)
print(total_level_attempts)
print(passed_level_attempts)
print(failed_level_attempts)


# don't need it right now
# for year in years:
#     file = 'home_DC_' + year + '.csv'
#     print(file)
#     file_path = root_ + file # set the path to corresponding institution file
#     new_df = pandas.read_csv(file_path)

#     students = new_df.student_entity_id.unique()
#     for student in students:
#         if student_info_dict.get(student) is not None:
#             if student_list_dict.get(student) is None:
#                 student_list_dict[student] = 1
#                 student_info = student_info_dict[student]
#                 data = [[year,student,student_info[0],student_info[1],student_info[2],student_info[3],student_info[4],student_info[5],student_info[6],student_info[7],student_info[8],student_info[9],student_info[10],student_info[11],student_info[12],student_info[13]]]
#                 result_df = pandas.DataFrame(data)
#                 result_df.to_csv(result_file,mode='a',header=None,index=False)

             



