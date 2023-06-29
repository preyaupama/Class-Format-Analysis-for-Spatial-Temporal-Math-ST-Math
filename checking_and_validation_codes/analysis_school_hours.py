import pandas
import iso8601
import datetime
import sys
import numpy




file_path_to_process = sys.argv[1] # path to the level attempt file that will be analyzed
# feature 1
district = sys.argv[2] # district which the file belongs to
# feature 2
year = sys.argv[3] # year to which the file belongs to
file_name = sys.argv[4] # name of the file that will be processed

# read the csv file into a data frame
df = pandas.read_csv(file_path_to_process)
df['python_time'] = pandas.to_datetime(df['python_time'])


# generate result file name
result_file = 'D:\\upama_desktop\\Summer_2019\\scripts\\analysis\\results\\DC_school_hour_validation.csv'
# feature 3
iid = sys.argv[5] 
df = df[df.iid == iid]

# list down unique grades
grades = df.gcd.unique()
grades = [grade for grade in grades if str(grade) != 'nan']
# for each grade run the session analysis
for grade in grades:
    # feature 4
    gcd = grade
    # sepearate data for the grade
    # note:there are students whose grades we don't know. They are excluded from the analysis
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
        # group using hours, keep track of previous and next sessions
            # within school hours(7.30-3.30) + no home-login
            # within school hours + home-login
            # outside school hours + lab-login
            # outside school hours + home-login
            
        # *********************************************************************************************************************
        # list down the session numbers conducted on that class
        sessions = grade_teacher_df.validate_s_hours.unique()
        sessions.sort()
        
        # find all in_class sessions
        # in_class_sessions = list()
        # for i in range(len(sessions)):
        #     s_data = grade_teacher_df[grade_teacher_df.original_session_num == sessions[i]]
        #     sample_time = s_data.iloc[0]['python_time'].time()
        #     if (sample_time >= datetime.time(19,30,0) and sample_time <= datetime.time(23,59,59)) or (sample_time >= datetime.time(0,0,0) and sample_time <= datetime.time(3,30,0)):
        #         in_class_sessions.append(sessions[i]) 

        # indicate if previous session was a rotation or not
        prev_session = 0 # assume prev session is not rotation
        # for each session we find out the following: lab(1/0), free seating(1/0), Rotation(1/0), others(1/0), teacher_helping(1/0), session_len, session_duration, performance_increasing(1/0-???), performance_decreasing(1/0-???), performance(avg. performance for the student)
        for i in range(len(sessions)):
            # feature 7
            session = sessions[i]

            # separate data for this particular class/teacher
            grade_session_teacher_df = grade_teacher_df[grade_teacher_df.validate_s_hours == session]

            
            # start and finish times for each student
            start_finish_times = grade_session_teacher_df.groupby("student_entity_id").python_time.agg(['min', 'max']).reset_index() # min is the start time and max is the end time 
            # convert the start and finish times to datetime object
            start_times = pandas.to_datetime(start_finish_times['min'])
            


            # feature 8
            date = start_times.min().date()
            
            # feature 9
            # minutes = start_times.min().minute
            hour = start_times.min().hour
            # if minutes >= 1 and minutes <= 30:
            #     if hour == 0:
            #         hour = 23
            #         date = date-datetime.timedelta(days=1)
            #     else:
            #         hour = hour -1
            session_time = datetime.time(hour,0,0)
            
            

            # determine rotation
            # check the previous and next sessions and the participants list in those session
            curr_session_students = len(grade_session_teacher_df.student_entity_id.unique())
            data = [[district,year,iid,gcd,teacher_entity_id,session,date,session_time,curr_session_students]]
            result_df = pandas.DataFrame(data)
            result_df.to_csv(result_file,mode='a',header=None,index=False)

            
    #         break
    #     break

    # break
