import pandas
import os
import sys
import datetime

def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end

directory = 'D:\\upama_desktop\\Summer_2019\\scripts\\analysis\\preprocessed_data\\'
files = ['lab_DC_2017.csv']

output_directory = 'D:\\upama_desktop\\Summer_2019\\scripts\\analysis\\preprocessed_data\\school_hour_data\\'

prefix_1 = "laws_" # level attempts within school time
prefix_2 = "ssws_" # student session within school time


for file in files:
    print(file)
    path = directory + file
    
    
    # filtering 1
    # df = pandas.read_csv(path, index_col=[0,1]) # read the data in a dataframe
    # df['python_time'] = pandas.to_datetime(df['python_time'])
    # output_file = output_directory + prefix_1 + file
    # filtered_data = df[df.python_time.dt.strftime('%H:%M:%S').between('08:00:00','16:00:00')]
    # filtered_data.to_csv(output_file)
    # del df

    # filtering 2
    # df = pandas.read_csv(path) # read the data in a dataframe
    # df['python_time'] = pandas.to_datetime(df['python_time'])

    # drop = [0] * len(df)
    # output_file = output_directory + prefix_2 + file
    # start = datetime.time(8, 0, 0)
    # end = datetime.time(16, 0, 0)

    # students = df.student_entity_id.unique()

    # for student in students:
    #     student_df = df[df.student_entity_id == student]
    #     sessions = student_df.session_number.unique()
    #     sessions.sort()


    #     for session in sessions:
    #         session_data = student_df[student_df.session_number == session]
    #         session_start_time =  session_data.python_time.min()
    #         session_end_time = session_data.python_time.max()
    #         session_duration = (session_end_time - session_start_time).total_seconds()
    #         drop_var = 0 # 0 - don't drop, 2 - don't drop (session longer than 45 minutes), 1 - drop
    #         if session_start_time.date() == session_end_time.date():
    #             if time_in_range(start, end, session_start_time.time()) and time_in_range(start, end, session_end_time.time()):
    #                 if session_duration <= 2700:
    #                     drop_var = 0
    #                 else:
    #                     drop_var = 2
    #             else:
    #                 drop_var = 1 
    #         else:
    #             drop_var = 1
    #         for row in session_data.itertuples():
    #             drop[row.X1-1] = drop_var
    # df['drop'] = drop
    # filtered_data=df.loc[df['drop'] != 1]
    # filtered_data.to_csv(output_file,index = False)

    ###########################################################################################



files = os.listdir(output_directory)
for file in files:
    print(output_directory+file)
    path = output_directory + file
    df = pandas.read_csv(path, index_col=[0,1]) # read the data in a dataframe
    # update X1
    X1 = list()
    row_number = 1
    for row in df.itertuples():
        X1.append(row_number)
        row_number = row_number+1
    df['X1'] = X1
    df.to_csv(path)


