import pandas
import iso8601
import datetime
import sys


file_path_to_process = sys.argv[1] # path to the level attempt file that will be analyzed. we will rewrite this file

# read the csv file into a data frame
df = pandas.read_csv(file_path_to_process)
df['python_time'] = pandas.to_datetime(df['python_time'])

output_file = sys.argv[2]

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
        
            sessions = grade_teacher_df.session_num_laws.unique()
            sessions.sort()

            for i in range(len(sessions)):
                # feature 7
                session = sessions[i]

                # separate data for this particular class/teacher
                grade_session_teacher_df = grade_teacher_df[grade_teacher_df.session_num_laws == session]

                # start and finish times for each student
                # start_finish_times = grade_session_teacher_df.groupby("student_entity_id").python_time.agg(['min', 'max']).reset_index() # min is the start time and max is the end time
                group_by_data = grade_session_teacher_df.groupby("student_entity_id", as_index = False).agg({'python_time': [min,max], 'performance':'mean','year':'first'}) 
                start_times = pandas.to_datetime(group_by_data['python_time'].min())
                finish_times = pandas.to_datetime(group_by_data['python_time'].max())
                
                
                session_day = grade_session_teacher_df.session_day_number.unique()[0]

                start_time = start_times.min()
                finish_time = finish_times.max()
                class_length = (finish_time - start_time).total_seconds()

                session_duration_col = finish_times - start_times
                session_duration = session_duration_col.mean().total_seconds()

                for level_attempt in group_by_data.itertuples():
                    data = [[level_attempt._5,iid,gcd,teacher_entity_id,session_day,session,class_length,session_duration,start_time,finish_time,level_attempt._1,level_attempt._2,level_attempt._3,level_attempt._4]]
                    result_df = pandas.DataFrame(data)
                    result_df.to_csv(output_file,mode='a',header=None,index=False)
                