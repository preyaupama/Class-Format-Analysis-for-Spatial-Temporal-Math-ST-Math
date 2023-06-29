import pandas
import iso8601
import datetime
import sys

file_path_to_process = sys.argv[1] # path to the level attempt file that will be analyzed. we will rewrite this file

# read the csv file into a data frame
df = pandas.read_csv(file_path_to_process)
df['python_time'] = pandas.to_datetime(df['python_time'])

output_file = file_path_to_process

X1 = list()
row_number = 1
for row in df.itertuples():
    X1.append(row_number)
    row_number = row_number+1
df['X1'] = X1
    

original_session_num = [0] * len(df)
session_day_number = [0] * len(df)

students = df.student_entity_id.unique()
# for each student run the session analysis
for student in students:
    student_df = df[df.student_entity_id == student]
    # seperate data using day and time
    session_days = pandas.to_datetime(student_df['python_time']).dt.date
    session_days = session_days.unique()

    session_number = 0
    day = 1
    
    for session_day in session_days:
        session_number = session_number + 1
        session_day_data = student_df[pandas.to_datetime(student_df['python_time']).dt.date == session_day]
        session_day_data = session_day_data.sort_values(by='python_time')

        row_number = 0
        prev_row = None
            
        for row in session_day_data.itertuples():
            session_day_number[row.X1-1] = day
            if row_number == 0:
                original_session_num[row.X1-1] = session_number
                
            else:
                time_difference = (row.python_time - prev_row.python_time).total_seconds()
                if time_difference > 1200:
                    session_number = session_number + 1
                original_session_num[row.X1-1] = session_number
                    
            row_number = row_number + 1
            prev_row = row
        day = day + 1


df['session_num_v4'] = original_session_num
df['session_day_number'] = session_day_number

df.to_csv(output_file,index=False)


            
            

        