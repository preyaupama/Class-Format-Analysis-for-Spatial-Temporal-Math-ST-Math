import pandas
import iso8601
import datetime
import sys


file_path_to_process = sys.argv[1] # path to the level attempt file that will be analyzed. we will rewrite this file

# read the csv file into a data frame
df = pandas.read_csv(file_path_to_process)
df['python_time'] = pandas.to_datetime(df['python_time'])

output_file = file_path_to_process
    

session_num_ssws = [0] * len(df)
session_day_number = [0] * len(df)

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
        # note:also there are data where puzzles count is zero
        grade_df = iid_df[iid_df.gcd == grade]
    
        # list down teachers/classrooms in that grade
        teachers = grade_df.teacher_entity_id.unique()
        # for each classroom
        for teacher in teachers:
            # feature 5
            teacher_entity_id = teacher
            # seperate the data
            grade_teacher_df = grade_df[grade_df.teacher_entity_id == teacher]
        
            # seperate data using day and time
            session_days = pandas.to_datetime(grade_teacher_df['python_time']).dt.date
            session_days = session_days.unique()
            session_days.sort()

            session_number = 1
            day = 1
            # last_session_data_count = 0
            for session_day in session_days:
                session_day_data = grade_teacher_df[pandas.to_datetime(grade_teacher_df['python_time']).dt.date == session_day]
                session_day_data = session_day_data.sort_values(by='python_time')
                
                # write the logic here
                # start with a level attempt - next level attempt made within 10 minutes by same or different student..if gap more than 10 minutes-
                # prevuously encountered student playing same session - same class , playing new session - it'll be defined as a new class
                # keep track of student session under which new session number
                # all level attempts within 45 minutes are same session
                ###########################################################################
                start_time_curr_session = None
                ###########################################################################
                student_session_info = dict()
                ###########################################################################
                for row in session_day_data.itertuples():
                    session_day_number[row.X1-1] = day

                    if student_session_info.get((row.student_entity_id,row.session_number)) is not None:
                        session_num_ssws[row.X1-1] = student_session_info.get((row.student_entity_id,row.session_number))

                    elif student_session_info.get((row.student_entity_id,row.session_number)) is None:
                        if start_time_curr_session is None:
                            session_num_ssws[row.X1-1] =  session_number
                            start_time_curr_session = row.python_time
                        else:
                            if (row.python_time - start_time_curr_session).total_seconds() > 2700:
                                session_number = session_number + 1
                                session_num_ssws[row.X1-1] =  session_number
                                start_time_curr_session = row.python_time
                            else:
                                session_num_ssws[row.X1-1] =  session_number
                        student_session_info[(row.student_entity_id,row.session_number)] = session_number 
                ###########################################################################
                session_number = session_number + 1 # increase session number on a new day
                day = day + 1
            
            
df['session_num_ssws'] = session_num_ssws
df['session_day_number'] = session_day_number

df.to_csv(output_file,index=False)


            
            

        