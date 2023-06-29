# what are the students playing

# mark rotation only in class held sessions
# 6.00 AM - 4.00 PM - school hours

import pandas
import iso8601
import datetime
import sys
import numpy
import statistics

file_path_to_process = sys.argv[1] # path to the level attempt file that will be analyzed
# feature 1
district = sys.argv[2] # district which the file belongs to
# feature 2
year = sys.argv[3] # year to which the file belongs to
file_name = sys.argv[4] # name of the file that will be processed

# read the csv file into a data frame
df = pandas.read_csv(file_path_to_process)
df['python_time'] = pandas.to_datetime(df['python_time'])
df = df[df.home_or_lab_login == 1]

# generate result file name
result_file_play = 'D:\\upama_desktop\\Summer_2019\\scripts\\analysis\\results\\extended\\' + district + '_play_Class_Session_Formats.csv'
result_file_rotation = 'D:\\upama_desktop\\Summer_2019\\scripts\\analysis\\results\\extended\\' + district + '_rotation_Class_Session_Formats.csv'

# feature 3
iid = ''
iid_list_temp = df.iid.unique()
iid_list = [iids for iids in iid_list_temp if str(iids) != 'nan']
if len(iid_list) != 1:
    print(iid_list)
    sys.exit("ERROR:"+file_path_to_process+" contains data from multiple institutes!!!")
else:
    iid = iid_list[0]

# list down unique grades
grades = df.gcd.unique()
grades = [grade for grade in grades if str(grade) != 'nan']
# for each grade run the session analysis
for grade in grades:
    # feature 4
    gcd = grade
    # sepearate data for the grade
    # note:there are students whose grades we don't know. They are excluded from the analysis
    # note: there are level attempts with same time stamp and student_entity_id. But the count for this type of level attempt is very low
    # note:also there are data where puzzles count is zero. percentage is really low. so including or excluding them doesn't impact the analysis
    grade_df = df[df.gcd == grade]
    
    # list down teachers/classrooms in that grade
    teachers = grade_df.teacher_entity_id.unique()
    # for each classroom
    for teacher in teachers:
        # feature 5
        teacher_entity_id = teacher
        # seperate the data
        grade_teacher_df = grade_df[grade_df.teacher_entity_id == teacher]
        
        # this file is temporary***********************************************************************************************
        # grade_session_df.to_csv("grade_session_df.csv")
        # *********************************************************************************************************************
        # list down the session numbers conducted on that class
        sessions = grade_teacher_df.original_session_num.unique()
        sessions.sort()
        
        # for each session we find out the following: lab(1/0), free seating(1/0), Rotation(1/0), others(1/0), teacher_helping(1/0), session_len, session_duration, performance_increasing(1/0-???), performance_decreasing(1/0-???), performance(avg. performance for the student)
        # for i in range(len(sessions)):
        #     # feature 7
        #     session = sessions[i]

        #     # separate data for this particular class/teacher
        #     grade_session_teacher_df = grade_teacher_df[grade_teacher_df.original_session_num == session]

        #     # feature 6 - what this old_session_num means
        #     old_session_num = str(grade_session_teacher_df.session_number.unique())

        #     # start and finish times for each student
        #     start_finish_times = grade_session_teacher_df.groupby("student_entity_id").python_time.agg(['min', 'max']).reset_index() # min is the start time and max is the end time 
        #     # convert the start and finish times to datetime object
        #     start_times = pandas.to_datetime(start_finish_times['min'])
            
        #     # feature 8
        #     date = start_times.min().date()
            
        #     # feature 9
        #     # minutes = start_times.min().minute
        #     hour = start_times.min().hour
        #     session_time = datetime.time(hour,0,0)

        #     # feature 10
        #     playing_same_levels = 0
        #     count_same_levels = 0
        #     levels_played = list()
        #     # write code here
        #     for student in start_finish_times.itertuples():
        #         student_data = grade_session_teacher_df[grade_session_teacher_df.student_entity_id == student.student_entity_id]
        #         stud_levels_played = list()
        #         for l_attempt in student_data.itertuples():
        #             level = str(l_attempt.objective_index) + '_' + str(l_attempt.game_number_in_objective) + '_' + str(l_attempt.level_number_in_objective)
        #             if level not in stud_levels_played:
        #                 stud_levels_played.append(level)
        #         levels_played.append(stud_levels_played)
            
        #     forward_pass = list()
        #     backward_pass = list()

        #     forward_intersection = set(levels_played[0])
        #     backward_intersection = set(levels_played[len(levels_played)-1])
        #     for i in range(1,len(levels_played)):
        #         forward_intersection = forward_intersection.intersection(set(levels_played[i]))
        #         forward_pass.append(len(forward_intersection))
        #         backward_intersection = backward_intersection.intersection(set(levels_played[len(levels_played)-(i+1)]))
        #         backward_pass.append(len(backward_intersection))
        #     backward_pass.reverse()
        #     final_pass = list()
        #     for i in range(len(forward_pass)):
        #         final_pass.append(max(forward_pass[i],backward_pass[i]))
        #     if len(forward_intersection) > 0:
        #         playing_same_levels = 1 
        #     count_same_levels = len(forward_intersection)
        #     med = -1
        #     if len(final_pass) != 0:
        #         med = statistics.median(final_pass)
            
        #     # end
            
        #     # save the features for the current session in the output csv
        #     data = [[district,year,iid,gcd,teacher_entity_id,old_session_num,session,date,session_time,playing_same_levels,count_same_levels,med]]
        #     result_df = pandas.DataFrame(data)
        #     result_df.to_csv(result_file_play,mode='a',header=None,index=False)
            
    

        # find all in_class sessions
        in_class_sessions = sessions
        # in_class_sessions = list()
        # for i in range(len(sessions)):
        #     s_data = grade_teacher_df[grade_teacher_df.original_session_num == sessions[i]]
        #     sample_time = s_data.iloc[0]['python_time'].time()
        #     # change the time here
        #     if (sample_time >= datetime.time(23,0,0) and sample_time <= datetime.time(23,59,59)) or (sample_time >= datetime.time(0,0,0) and sample_time <= datetime.time(9,0,0)):
        #         in_class_sessions.append(sessions[i]) 

        # indicate if previous session was a rotation or not
        prev_session = 0 # assume prev session is not rotation
        in_class_sessions.sort()
        for i in range(len(in_class_sessions)):
            # feature 7
            session = in_class_sessions[i]

            # separate data for this particular class/teacher
            grade_session_teacher_df = grade_teacher_df[grade_teacher_df.original_session_num == session]

            # feature 6
            old_session_num = str(grade_session_teacher_df.session_number.unique())

            # start and finish times for each student
            start_finish_times = grade_session_teacher_df.groupby("student_entity_id").python_time.agg(['min', 'max']).reset_index() # min is the start time and max is the end time 
            # convert the start and finish times to datetime object
            start_times = pandas.to_datetime(start_finish_times['min'])

            # feature 8
            date = start_times.min().date()
            
            # feature 9
            hour = start_times.min().hour
            session_time = datetime.time(hour,0,0)
            
            # feature 10
            rotation = 0
            # determine rotation
            # check the previous and next sessions and the participants list in those session
            curr_session_students = grade_session_teacher_df.student_entity_id.unique()
            
            if len(in_class_sessions) == 1: # the teacher conducted only one session
                rotation = 0
            elif i == 0: # first session conducted by the teacher
                prev_session_students = None 
                next_session_students = grade_teacher_df[grade_teacher_df.session_number == in_class_sessions[i+1]].student_entity_id.unique()
                if set(curr_session_students).isdisjoint(set(next_session_students)):
                    rotation = 1
                else:
                    common_students = set(curr_session_students).intersection(set(next_session_students))
                    if len(common_students)/len(curr_session_students) <= 0.5 and len(common_students)/len(next_session_students) <= 0.5:
                        rotation = 2
            elif i == len(in_class_sessions)-1: # last session conducted by the teacher
                next_session_students = None
                prev_session_students = grade_teacher_df[grade_teacher_df.session_number == in_class_sessions[i-1]].student_entity_id.unique()
                if set(curr_session_students).isdisjoint(set(prev_session_students)):
                    rotation = 1
                else:
                    common_students = set(curr_session_students).intersection(set(prev_session_students))
                    if len(common_students)/len(curr_session_students) <= 0.5 and len(common_students)/len(prev_session_students) <= 0.5:
                        rotation = 2
            else: # other session
                next_session_students = grade_teacher_df[grade_teacher_df.session_number == in_class_sessions[i+1]].student_entity_id.unique()
                prev_session_students = grade_teacher_df[grade_teacher_df.session_number == in_class_sessions[i-1]].student_entity_id.unique()
                if set(prev_session_students).isdisjoint(set(curr_session_students)) or set(curr_session_students).isdisjoint(set(next_session_students)):
                    rotation = 1
                
                else:
                    common_students_pc = set(curr_session_students).intersection(set(prev_session_students))
                    common_students_cn = set(curr_session_students).intersection(set(next_session_students)) 
                    if len(common_students_cn)/len(curr_session_students) <= 0.5 and len(common_students_cn)/len(next_session_students) <= 0.5 and len(common_students_pc)/len(curr_session_students) <= 0.5 and len(common_students_pc)/len(prev_session_students) <= 0.5:
                        rotation = 2
                    # next session is a rotation
                    elif len(common_students_cn)/len(curr_session_students) <= 0.5 and len(common_students_cn)/len(next_session_students) <= 0.5:
                        if i+2 == len(in_class_sessions):
                            rotation = 2
                        else:
                            more_next_session_students = grade_teacher_df[grade_teacher_df.session_number == in_class_sessions[i+2]].student_entity_id.unique()
                            common_students_cn_mnss = set(more_next_session_students).intersection(set(next_session_students))
                            if len(common_students_cn_mnss) == 0 or (len(common_students_cn_mnss)/len(more_next_session_students) <= 0.5 and len(common_students_cn_mnss)/len(next_session_students) <= 0.5):
                                rotation = 2
                    # prev session is a rotation
                    elif len(common_students_pc)/len(curr_session_students) <= 0.5 and len(common_students_pc)/len(prev_session_students) <= 0.5:
                        if prev_session == 1 or prev_session == 2:
                            rotation = 2
            prev_session = rotation


            data = [[district,year,iid,gcd,teacher_entity_id,old_session_num,session,date,session_time,rotation]]
            result_df = pandas.DataFrame(data)
            result_df.to_csv(result_file_rotation,mode='a',header=None,index=False)

            
    #         break
    #     break
    # break

