import pandas
import iso8601
import datetime
import sys

file_path_to_process = sys.argv[1] # path to the level attempt file that will be analyzed. we will rewrite this file

# read the csv file into a data frame
df = pandas.read_csv(file_path_to_process)
df['python_time'] = pandas.to_datetime(df['python_time'])

output_file = file_path_to_process

original_session_num = [0] * len(df)
session_day_number = [0] * len(df)

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
    # note:also there are data where puzzles count is zero
    grade_df = df[df.gcd == grade]
    
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

        session_number = 0
        day = 1
        # last_session_data_count = 0
        for session_day in session_days:
            session_number = session_number + 1
            session_day_data = grade_teacher_df[pandas.to_datetime(grade_teacher_df['python_time']).dt.date == session_day]
            session_day_data = session_day_data.sort_values(by='python_time')

            row_number = 0
            prev_row = None
            # temp = list()
            for row in session_day_data.itertuples():
                session_day_number[row.X1-1] = day
                if row_number == 0:
                    original_session_num[row.X1-1] = session_number
                    # temp.append(session_number)
                else:
                    time_difference = (row.python_time - prev_row.python_time).total_seconds()
                    if time_difference > 600:
                        session_number = session_number + 1
                    original_session_num[row.X1-1] = session_number
                    # temp.append(session_number)
                    
                row_number = row_number + 1
                prev_row = row
            day = day + 1

            # session_day_data.to_csv('single_day_data.csv')
            # hours_in_day = session_day_data['python_time'].dt.hour
            # print(len(hours_in_day.unique()))

            # start_finish_times = session_day_data.groupby("student_entity_id").python_time.agg(['min', 'max']).reset_index() # min is the start time and max is the end time 
            # # range of start and finish times
            # start_finish_times['play_time'] =  pandas.Timedelta(start_finish_times['max'] - start_finish_times['min']).seconds
            # print(start_finish_times)

            # sys.exit(1)

            
            # session_day_data.index=pandas.to_datetime(session_day_data['python_time'])

            # time_ranges = [('00:00:00', '00:59:59'),('01:00:00','01:59:59'),('02:00:00','02:59:59'),
            #                ('03:00:00', '03:59:59'),('04:00:00','04:59:59'),('05:00:00','05:59:59'),
            #                ('06:00:00', '06:59:59'),('07:00:00','07:59:59'),('08:00:00','08:59:59'),
            #                ('09:00:00', '09:59:59'),('10:00:00','10:59:59'),('11:00:00','11:59:59'),
            #                ('12:00:00', '12:59:59'),('13:00:00','13:59:59'),('14:00:00','14:59:59'),
            #                ('15:00:00', '15:59:59'),('16:00:00','16:59:59'),('17:00:00','17:59:59'),
            #                ('18:00:00', '18:59:59'),('19:00:00','19:59:59'),('20:00:00','20:59:59'),
            #                ('21:00:00', '21:59:59'),('22:00:00','22:59:59'),('23:00:00','23:59:59'),]

            
            # for i in range(len(time_ranges)):
            #     session_data = session_day_data.between_time(time_ranges[i][0],time_ranges[i][1])
                
            #     if len(session_data) != 0:
            #         for row in session_data.itertuples():
            #             original_session_num[row.X1-1] = session_number
            #             session_day[row.X1-1] = day
            #         session_number = session_number + 1
            # day = day + 1

df['session_num_v3'] = original_session_num
df['session_day_number'] = session_day_number

df.to_csv(output_file,index=False)


            
            

        