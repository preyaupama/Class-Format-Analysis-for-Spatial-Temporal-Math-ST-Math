import pandas
import iso8601
import datetime
import sys


file_path_to_process = sys.argv[1] # path to the level attempt file that will be analyzed. we will rewrite this file

# read the csv file into a data frame
df = pandas.read_csv(file_path_to_process)
df['python_time'] = pandas.to_datetime(df['python_time'])

output_file = file_path_to_process

# temp
X1 = list()
row_number = 1
for row in df.itertuples():
    X1.append(row_number)
    row_number = row_number+1
df['X1'] = X1
    

session_num_v4 = [0] * len(df)
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
                
                row_number = 0
                prev_row = None
                # Session: 45 minutes
                ###########################################################################
                all_session_info = dict()
                session_list = list()
                session_list_copy = list()
                ###########################################################################
                for row in session_day_data.itertuples():
                    session_day_number[row.X1-1] = day    
                    if row_number == 0:
                        session_num_v4[row.X1-1] = session_number
                    else:
                        time_difference = (row.python_time - prev_row.python_time).total_seconds()
                        if time_difference > 600:
                            session_number = session_number + 1
                        session_num_v4[row.X1-1] = session_number
                    #######################################################################
                    if session_number not in session_list:
                        session_list.append(session_number)
                        session_list_copy.append(session_number)
                    #######################################################################
                    if all_session_info.get(session_number) is None:
                        if prev_row is not None:
                            all_session_info[session_num_v4[prev_row.X1-1]]['finish_time'] = prev_row.python_time
                        all_session_info[session_number] = dict()
                        all_session_info[session_number]['students'] = list()
                        all_session_info[session_number]['start_time'] = row.python_time
                    if row.student_entity_id not in all_session_info[session_number]['students']:
                        all_session_info[session_number]['students'].append(row.student_entity_id)
                    if row_number == len(session_day_data)-1:
                        all_session_info[session_number]['finish_time'] = row.python_time
                    #######################################################################
                    
                    row_number = row_number + 1
                    prev_row = row
                

                ###########################################################################
                # revise
                # merge only if it's within class time
                # merge if same students are playing again
                # merge if consecutive sessions are found within 45 minute
                # merge only if the gap is reasonable
                print(session_list)
                revised = 0
                for i in range(len(session_list)):
                    school_start = datetime.datetime.strptime('08:00:00', "%H:%M:%S").time()
                    school_finish = datetime.datetime.strptime('16:00:00', "%H:%M:%S").time() 
                    if all_session_info[session_list_copy[i]]['start_time'].time() >= school_start and all_session_info[session_list_copy[i]]['finish_time'].time() <= school_finish:
                        if i != len(session_list) - 1:
                            if all_session_info[session_list[i+1]]['finish_time'].time() <= school_finish:
                                num_common_students = len(set(all_session_info[session_list_copy[i]]['students']).intersection(set(all_session_info[session_list[i+1]]['students'])))
                                time_gap = (all_session_info[session_list[i+1]]['start_time'] - all_session_info[session_list_copy[i]]['finish_time']).total_seconds()
                                time_span = (all_session_info[session_list[i+1]]['finish_time'] - all_session_info[session_list[i]]['start_time']).total_seconds()
                                if i == 4:
                                    print(time_gap)
                                    print(time_span)
                                    print(num_common_students)
                                    print(len(set(all_session_info[session_list_copy[i]]['students']).intersection(set(all_session_info[session_list[i+2]]['students']))))
                                if time_span <= 2700:
                                    all_session_info[session_list[i+1]]['students'].extend(all_session_info[session_list[i]]['students'])
                                    all_session_info[session_list[i+1]]['students'] = list(set(all_session_info[session_list[i+1]]['students']))
                                    session_list[i+1] = session_list[i]
                                    revised = 1
                                else:
                                    if num_common_students != 0 and time_gap <= 1800:
                                        all_session_info[session_list[i+1]]['students'].extend(all_session_info[session_list[i]]['students'])
                                        all_session_info[session_list[i+1]]['students'] = list(set(all_session_info[session_list[i+1]]['students']))
                                        session_list[i+1] = session_list[i]
                                        revised = 1
                # revised session number mapping
                print(session_list)
                if revised == 1:
                    unique_sessions = list(set(session_list))
                    unique_sessions.sort()
                    mapping = list()
                    for x in range(len(unique_sessions)):
                        if x == 0:
                            mapping.append(unique_sessions[x])
                        else:
                            mapping.append(mapping[x-1] + 1) 
                    for i in range(len(session_list)):
                        index = unique_sessions.index(session_list[i])
                        session_list[i] = mapping[index]
                    session_number = session_list[len(session_list)-1]
                print(session_list)
                sys.exit(0)
                # update session number
                if revised == 1:
                    for row in session_day_data.itertuples():
                        session_num_v4[row.X1-1] = session_list[session_list_copy.index(session_num_v4[row.X1-1])] 
                ###########################################################################
                session_number = session_number + 1
                day = day + 1
            
            
df['session_num_v4'] = session_num_v4
df['session_day_number'] = session_day_number

df.to_csv(output_file,index=False)


            
            

        