import pandas
import ast
import csv
import os

output_file = 'info\\missing_students.csv'
fields = ['student_entity_id','source']
with open(output_file, mode='a') as of:
    writer = csv.writer(of)
    writer.writerow(fields)


# version 1
districts = ['DC']
years = ['2014','2015','2016','2017']
print("Getting student info...")
csv_file = 'D:\\upama_desktop\\Summer_2019\\MIND_Data\\cleaned_merged_student_info.csv' # path to student info file
student_info_df = pandas.read_csv(csv_file, index_col="student_entity_id")
student_info_dict = dict()
for row in student_info_df.itertuples():
    student_info_dict[row.Index] = (row.iid, row.gcd, row.stmath_user_id, row.teacher_entity_id)
del student_info_df

print("Listing missing data...")
root = 'C:\\DAST_data\\class_format_data'
missing_students_list = list()
for district in districts:
    for year in years:
        path = root + '\\'+district+'\\'+year+'\\' # a folder is needed to store the data from different institutions of each district and year
        files = os.listdir(path) # get the list of files under district and year folder
        for file in files:
            file_path = path + file # set the path to corresponding institution file
            new_df = pandas.read_csv(file_path, index_col="student_entity_id") # read the data in a dataframe
            for row in new_df.itertuples():
                if student_info_dict.get(row.Index) is None: # if student info is not found append the student_entity_id to missing_students_list and assign None to corresponding columns
                    if row.Index not in missing_students_list:
                        missing_students_list.append(row.Index)
                        data = [[row.Index,file]]
                        result_df = pandas.DataFrame(data)
                        result_df.to_csv(output_file,mode='a',header=None,index=False)
print("Done...")



# version 2
# lines = open('info/missing_student_info.txt').readlines()
# curr_file = ''
# for line in lines:
#     if 'File name:' in line:
#         line = line.replace('File name:','')
#         curr_file = line.strip()
#         print(line)
#     elif line == '\n':
#         continue
#     else:
#         print(line)
#         line = line.strip()
#         missing_students = ast.literal_eval(line)
#         print(missing_students)
#         for student in missing_students:
#             data = [[student,curr_file]]
#             result_df = pandas.DataFrame(data)
#             result_df.to_csv(output_file,mode='a',header=None,index=False)
