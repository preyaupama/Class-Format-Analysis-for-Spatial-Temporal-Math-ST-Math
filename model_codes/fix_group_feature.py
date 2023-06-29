years = [2014, 2015, 2016, 2017]
import pandas
import sys

# retrieve the data
session_data = pandas.read_csv("final_features_revised.csv")

# assign a serial number
X1 = list()
serial_num = 0
for row in session_data.itertuples():
    X1.append(serial_num)
    serial_num = serial_num + 1
session_data['X1'] = X1


student_group = [0]*len(session_data)
content_group = [0]*len(session_data)

student_dict = dict()
content_dict = dict()

student_group_num = 1
content_group_num = 1
for year in years:
    print(year)
    # open corresponding file
    year_all_data_path = "D:\\upama_desktop\\Summer_2019\\scripts\\analysis\\preprocessed_data\\" + "laws_lab_DC_" + str(year) + ".csv"
    year_all_data = pandas.read_csv(year_all_data_path)
    
    # get data for that year
    session_data_year = session_data[session_data.year == year]
    print(len(session_data_year))
    
    for row in session_data_year.itertuples():
        level_attempts_session = year_all_data[(year_all_data.iid == row.iid) & (year_all_data.gcd == row.gcd) & (year_all_data.teacher_entity_id == row.teacher_entity_id) & (year_all_data.session_num_laws == row.session)]
        # get the students group
        # CODE HERE ######
        student_list = level_attempts_session.student_entity_id.unique()
        student_list.sort()
        students = ""
        for student in student_list:
            students = students + "_" + student

        if student_dict.get(students) is None:
            student_dict[students] = student_group_num
            student_group[row.X1] = student_group_num
            student_group_num = student_group_num + 1
        else:
            student_group[row.X1] = student_dict[students]
        ####################
        # get the contents group
        level_list = list()
        for r in level_attempts_session.itertuples():
            level = str(r.objective_index) + "_" + str(r.game_number_in_objective) + "_" + str(r.level_number_in_objective)
            level_list.append(level)
        level_list.sort()

        levels = ""
        for level in level_list:
            levels = levels + "#" + level
        # CODE HERE ######
        if content_dict.get(levels) is None:
            content_dict[levels] = content_group_num
            content_group[row.X1] = content_group_num
            content_group_num = content_group_num + 1
        else:
            content_group[row.X1] = content_dict[levels]
        ####################

session_data['student_group'] = student_group
session_data['content_group'] = content_group

print("Assign final group number...")
final_group = [0]*len(session_data)
# final grouping
final_group_dict = dict()
final_group_num = 0
# CODE HERE ######
for row in session_data.itertuples():
    group_num = str(row.group_id) + "_" + str(row.student_group) + "_" + str(row.content_group)
    if final_group_dict.get(group_num) is None:
        final_group_dict[group_num] = final_group_num
        final_group[row.X1] = final_group_num
        final_group_num = final_group_num + 1
    else:
        final_group[row.X1] = final_group_dict.get(group_num)
####################
session_data['final_group'] = final_group
print("done")


# do later if possible
# session_per_ymw = [0]*len(session_data)
# info_file = pandas.read_csv("number_of_times_each_classroom_played_stmath_in_a_month.csv")
# # add sessions per month
# # CODE HERE ######
# ####################
# session_data['session_per_ymw'] = session_per_ymw


# save after fixing
session_data.to_csv("final_features_revised.csv",index=False)