import pandas
import iso8601
import datetime
import sys
import numpy

# start time, finish time, difference, num student, common student, time difference between two sessions, same day session, session duration


file_path_to_process = sys.argv[1] # path to the level attempt file that will be analyzed
# feature 1
district = 'DC' # district which the file belongs to
# feature 2
year = sys.argv[2] # year to which the file belongs to
file_name = sys.argv[3] # name of the file that will be processed

# read the csv file into a data frame
df = pandas.read_csv(file_path_to_process)
df['python_time'] = pandas.to_datetime(df['python_time'])

# generate result file name
result_file = 'D:\\upama_desktop\\Summer_2019\\scripts\\analysis\\results\\checked_DC.csv'

# feature 3
iid_list = df.iid.unique()
iid_list = [iids for iids in iid_list if str(iids) != 'nan']
for iid in iid_list:
    iid_df = df[df.iid == iid]

    # list down unique grades
    grades = iid_df.gcd.unique()
    grades = [grade for grade in grades if str(grade) != 'nan']
    # for each grade run the session analysis
    for grade in grades:
        # feature 4
        gcd = grade
        # sepearate data for the grade
        # note:there are students whose grades we don't know. They are excluded from the analysis
        # note:also there are data where puzzles count is zero. percentage is really low. so including or excluding them doesn't impact the analysis
        grade_df = iid_df[iid_df.gcd == grade]
    
        # list down teachers/classrooms in that grade
        teachers = grade_df.teacher_entity_id.unique()
        # for each classroom
        for teacher in teachers:
            # feature 5
            teacher_entity_id = teacher
            # seperate the data
            grade_teacher_df = grade_df[grade_df.teacher_entity_id == teacher]
            # list down students of that grade handled by the teacher/the students that belong to the same classroom
            students = grade_teacher_df.student_entity_id.unique()
            # feature 10
            num_students_class = len(students)
            # this file is temporary***********************************************************************************************
            # grade_session_df.to_csv("grade_session_df.csv")
            # group using hours, keep track of previous and next sessions
                # within school hours(7.30-3.30) + no home-login
                # within school hours + home-login
                # outside school hours + lab-login
                # outside school hours + home-login
            
            # *********************************************************************************************************************
            # list down the session numbers conducted on that class
            sessions = grade_teacher_df.session_num_v4.unique()
            sessions.sort()
        
            # indicate if previous session was a rotation or not
            prev_session = 0 # assume prev session is not rotation
            # for each session we find out the following: lab(1/0), free seating(1/0), Rotation(1/0), others(1/0), teacher_helping(1/0), session_len, session_duration, performance_increasing(1/0-???), performance_decreasing(1/0-???), performance(avg. performance for the student)
            for i in range(len(sessions)):
                # feature 7
                session = sessions[i]

                # separate data for this particular class/teacher
                grade_session_teacher_df = grade_teacher_df[grade_teacher_df.session_num_v4 == session]

                # feature 6
                old_session_num = str(grade_session_teacher_df.session_number.unique())

                # start and finish times for each student
                start_finish_times = grade_session_teacher_df.groupby("student_entity_id").python_time.agg(['min', 'max']).reset_index() # min is the start time and max is the end time 
                # convert the start and finish times to datetime object
                start_times = pandas.to_datetime(start_finish_times['min'])
                finish_times = pandas.to_datetime(start_finish_times['max'])
                # range of start and finish times
                start_time_diff =  (start_times.max() - start_times.min()).total_seconds()
                finish_times_diff = (finish_times.max() - finish_times.min()).total_seconds()
            
                session_day = grade_session_teacher_df.session_day_number.unique()[0]
                start_time = start_times.min()
                finish_time = finish_times.max()
                class_length = (finish_time - start_time).total_seconds()

                if i > 0:
                    prev_session = sessions[i-1]
                    prev_session_data = grade_teacher_df[grade_teacher_df.session_num_v4 == prev_session]
                    same_day_session = 0
                    if session_day == prev_session_data.session_day_number.unique()[0]:
                        same_day_session = 1
                    common_students = len(set(grade_session_teacher_df.student_entity_id.unique()).intersection(set(prev_session_data.student_entity_id.unique())))
                    time_difference = (start_time-prev_session_data.python_time.max()).total_seconds()
                else:
                    same_day_session = 2 # first session conducted by a teacher in a grade
                    common_students = 0
                    time_difference = 0


            
                # feature 19
                session_duration = 0
                # feature 20
                session_len = 0
                # feature 21
                performance = 0
            
                # feature 11
                curr_session_students = grade_session_teacher_df.student_entity_id.unique()
                participation = len(curr_session_students)

                # session duration
                session_duration_col = finish_times - start_times
                session_duration = session_duration_col.mean().total_seconds()
        
                # session length
                level_attempt_count = grade_session_teacher_df.groupby("student_entity_id").python_time.agg(['count'])
                session_len = list(level_attempt_count.mean())[0]
        
                # performance
                performance = grade_session_teacher_df['performance'].mean()
        
                # save the features for the current session in the output csv
                # 'district','year','iid','gcd','teacher_entity_id', 'old_session_num','session','date','session_hour','num_students_class','participation', 'lab_seating','free_seating','rotation','others','session_duration','session_len','performance'
                data = [[district,year,iid,gcd,teacher_entity_id,old_session_num,session,num_students_class,participation,session_day,start_time,finish_time,class_length,session_duration,session_len,performance,same_day_session,common_students,time_difference]]
                result_df = pandas.DataFrame(data)
                result_df.to_csv(result_file,mode='a',header=None,index=False)

            
        #         break
        #     break

        # break
