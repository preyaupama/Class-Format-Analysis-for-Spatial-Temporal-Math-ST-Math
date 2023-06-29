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
result_file = 'D:\\upama_desktop\\Summer_2019\\scripts\\analysis\\results\\prediction_features.csv'
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
    grade_df = df[df.gcd == grade]
    
    # list down teachers/classrooms in that grade
    teachers = grade_df.teacher_entity_id.unique()
    # for each classroom
    for teacher in teachers:
        # feature 5
        teacher_entity_id = teacher
        # seperate the data
        grade_teacher_df = grade_df[grade_df.teacher_entity_id == teacher]
        
         # list down the session numbers conducted on that class
        sessions = grade_teacher_df.session_num_laws.unique()
        sessions.sort()
        
        # indicate if previous session was a rotation or not
        prev_session = 0 # assume prev session is not rotation
        # for each session we find out the following: lab(1/0), free seating(1/0), Rotation(1/0), others(1/0), teacher_helping(1/0), session_len, session_duration, performance_increasing(1/0-???), performance_decreasing(1/0-???), performance(avg. performance for the student)
        for i in range(len(sessions)):
            # feature 7
            session = sessions[i]
            # separate data for this particular class/teacher
            grade_session_teacher_df = grade_teacher_df[grade_teacher_df.session_num_laws == session]

            # feature list
            # - How many times a week the particular class(same grade, same teacher) attends a ST Math session - Ruth
            # - How many students the teacher handle in that grade
            # - How many students were handled by that teacher in that academic year
            # - How many sessions are conducted before the current session
            # - How many ST Math days were found before current session
            # - class size
            # - variance in start time
            # - variance in finish time
            # - disjointedness(boolean)
            # - class duration
            # - gameplay session duration
            # - number of level attempts
            # - performance (double)
            # - performance (catetgorical)
            # - was there any other session in that day
            # - what was the gap
            # - How many common students


            # start and finish times for each student
            start_finish_times = grade_session_teacher_df.groupby("student_entity_id").python_time.agg(['min', 'max']).reset_index() # min is the start time and max is the end time 
            # convert the start and finish times to datetime object
            start_times = pandas.to_datetime(start_finish_times['min'])
            finish_times = pandas.to_datetime(start_finish_times['max'])
            # range of start and finish times
            start_time_diff =  (start_times.max() - start_times.min()).total_seconds()
            finish_times_diff = (finish_times.max() - finish_times.min()).total_seconds()

            # feature 8
            date = start_times.min().date()
            # feature 9
            session_start = start_times.min().time()
            # feature 10
            session_finish = finish_times.max().time()
            

            #######################################CODE FOR FEATURES#################################################
            # 1. How many times a week the particular class(same grade, same teacher) attends a ST Math session - Ruth
            num_week_session = 2
            # 2. How many students in that grade were handled by the teacher who conducted the session
            students = grade_teacher_df.student_entity_id.unique()
            num_students_grade = len(students)
            # 3. How many students were handled by that teacher in that academic year from all grades ??? possible feature
            teacher_data = df[df.teacher_entity_id == teacher]
            total_students = len(teacher_data.student_entity_id.unique())
            # 4. How many sessions are conducted before the current session
            num_prev_sessions = session - 1
            # 5. How many ST Math days were found before current session
            prev_st_math_days = grade_session_teacher_df.session_day_number.unique()[0]-1
            # 6. class size
            class_size = grade_session_teacher_df.student_entity_id.unique()
            # 7. variance in start times
            start_time_variance = 0
            start_times.sort()
            mid_start_time = None
            half_way = int(len(start_times)/2)
            if len(start_times) == 1:
                start_time_variance = 0
            else:
                if len(start_times)%2 == 1:
                    mid_start_time = start_times[half_way]
                else:
                    diff = (start_times[half_way]-start_times[half_way-1]).total_seconds()
                    mid_start_time = start_times[half_way-1]-datetime.timedelta(0,diff)
                X = 0
                for time in start_times:
                    time_diff = 0
                    if time >= mid_start_time:
                        time_diff = (time - mid_start_time).total_seconds()
                    elif mid_start_time > time:
                        time_diff = (mid_start_time - time).total_seconds()
                    X = X + time_diff*time_diff
                start_time_variance = start_time_variance/len(start_times)



            # 8. variance in finish times
            finish_time_variance = 0
            finish_times.sort()
            mid_finish_time = None
            half_way = int(len(finish_times)/2)
            if len(finish_times) == 1:
                finish_time_variance = 0
            else:
                if len(finish_times)%2 == 1:
                    mid_finish_time = finish_times[half_way]
                else:
                    diff = (finish_times[half_way]-finish_times[half_way-1]).total_seconds()
                    mid_start_time = finish_times[half_way-1]-datetime.timedelta(0,diff)
                X = 0
                for time in finish_times:
                    time_diff = 0
                    if time >= mid_finish_time:
                        time_diff = (time - mid_finish_time).total_seconds()
                    elif mid_finish_time > time:
                        time_diff = (mid_finish_time - time).total_seconds()
                    X = X + time_diff*time_diff
                finish_time_variance = finish_time_variance/len(finish_times)
            # 9. disjointedness(boolean)
            # identify simultaneous plays in the order of time
            segmented_class = 0
            start_finish_times = start_finish_times.sort_values(by='min')
            simultaneous_players = list()
            for student in start_finish_times.itertuples():
                matched_lists = list() # lists which have matched
                if len(simultaneous_players) == 0: # there is no list. create a new list with single element
                    simul_players_list = list()
                    simul_players_list.append(student.Index)
                    simultaneous_players.append(simul_players_list)
                else:
                    # check with every list if the student fits with any list
                    new_player_lists = list() # new lists to be appended
                    no_match = 1 # indicates if any of the lists has matched
                    for simul_players_list in simultaneous_players: # for each list
                        flag = 0 # indicates if the list has matched or not
                        new_player_list = list() # this list stores players who have matched
                        new_player_list.append(student.Index)
                        for player in simul_players_list: # for each player in the list
                            player_data = start_finish_times.loc[player] # get player data
                            if not((player_data['max'] < student.min) or (player_data['min'] > student.max)): # check if it has overlapped time range with current student
                                new_player_list.append(player) # if true append it
                            else:
                                flag = 1 # if false indicate that the list has not fully matched
                        if flag == 0: # if the list has fully matched
                            simul_players_list.append(student.Index) # append student to the list
                            simul_players_list.sort() # sort the list
                            matched_lists.append(simul_players_list) # append the list to matched_lists
                            no_match = 0 # no_match becomes zero which indicates atleast 1 matching list found
                        else:
                            subset_match_flag = 0 # this flag indicates if the new_player_list is a subset of previously matched list
                            temp = list()
                            for x in new_player_lists:
                                if set(x) != set(new_player_list):
                                    if set(new_player_list).issubset(set(x)):
                                        subset_match_flag = 1
                                        break 
                                    elif not(set(x).issubset(set(new_player_list))):
                                        temp.append(x)
                                else:
                                    temp.append(x)
                            new_player_lists=temp

                            for p_list in matched_lists:
                                if set(new_player_list).issubset(set(p_list)):
                                    subset_match_flag = 1
                            # if new_player_list is not a subset of previously matched list and it doesn't contain only current student, sort the list and append it to new_player_lists
                            if not(len(new_player_list) == 1 and new_player_list[0] == student.Index) and subset_match_flag != 1:
                                new_player_list.sort()
                                if new_player_list not in new_player_lists: 
                                    new_player_lists.append(new_player_list)
                    if no_match == 1 and len(new_player_lists)==0: # if no partial or complete match found for the current student create a list of lists containg the current student
                        curr_student = list()
                        curr_student.append(student.Index)
                        new_player_lists.append(curr_student)

                    for new_player_list in new_player_lists: # add the lists
                        if new_player_list not in simultaneous_players:
                            simultaneous_players.append(new_player_list)
            # end identifying simultaneous play

            # analyze simultaneous plays
            length_list = list()
            for play in simultaneous_players:
                length_list.append(len(play))
            
            # maximum students played at the same time? - possible feature??
            max_participent = max(length_list)
            # segmented class
            if len(simultaneous_players) == 1:
                segmented_class = 0
            else:
                disjoint = 0
                for x in range(len(simultaneous_players)-2):
                    curr_stud = simultaneous_players[x] 
                    next_stud = simultaneous_players[x+1]
                    common_stud = set(curr_stud).intersection(set(next_stud))
                    if set(curr_stud).isdisjoint(set(next_stud)) or (len(common_stud)/len(curr_stud) <= 0.5 and len(common_stud)/len(next_stud) <= 0.5):
                        disjoint = disjoint + 1
                if disjoint/len(simultaneous_players) >= 0.5:
                    segmented_class = 1
            disjointedness = segmented_class     
            # end analyzing simultaneous plays
            # 10. class duration
            class_length = (session_finish - session_start).total_seconds()
            # 11. gameplay session duration
            student_list = grade_session_teacher_df.student_entity_id.unique()
            total_gameplay_duration = 0
            total_gameplay = 0
            for student in student_list:
                grade_session_teacher_student_df = grade_session_teacher_df[grade_session_teacher_df.student_entity_id == student]
                session_list =  grade_session_teacher_student_df.session_number.unique()
                for a_session in session_list:
                    total_gameplay = total_gameplay + 1 
                    a_session_data =  grade_session_teacher_student_df[grade_session_teacher_student_df.session_number == a_session]
                    start_time = a_session_data.python_time.min()
                    finish_time = a_session_data.python_time.max()
                    play_time = (finish_time-start_time).total_seconds
                    total_gameplay_duration = total_gameplay_duration + play_time
            gameplay_duration = total_gameplay_duration/total_gameplay
            # 12. number of level attempts
            level_attempt_count = grade_session_teacher_df.groupby("student_entity_id").python_time.agg(['count'])
            num_level_attempts = list(level_attempt_count.mean())[0]
            # 13. performance (double)
            performance = grade_session_teacher_df['performance'].mean()
            # 14. performance rank(catetgorical)
            perf_rank = 1
            if performance <= 0.5:
                perf_rank = 1
            elif performance > 0.5 and performance <= 0.7:
                perf_rank = 2
            elif performance > 0.7 and performance <= 1.0:
                perf_rank = 3
            # 15. was there any other session in that day
            # 16. what was the gap from previous sessions
            # 17. How many common students
            # feature 15
            same_day_prev_session = 0
            # feature 16
            time_difference = 0
            # feature 17
            common_students = 0
            if i > 0:
                    prev_session = sessions[i-1]
                    prev_session_data = grade_teacher_df[grade_teacher_df.session_num_laws == prev_session]
                    same_day_prev_session = 0
                    session_day = grade_session_teacher_df.session_day_number.unique()[0]
                    if session_day == prev_session_data.session_day_number.unique()[0]:
                        same_day_prev_session = 1
                    common_students = len(set(grade_session_teacher_df.student_entity_id.unique()).intersection(set(prev_session_data.student_entity_id.unique())))
                    time_difference = (session_start-prev_session_data.python_time.max()).total_seconds()
            else:
                same_day_prev_session = 2 # first session conducted by a teacher in a grade
                common_students = 0
                time_difference = 0
            ########################################################################################################

            # save the features for the current session in the output csv
            # 'district','year','iid','gcd','teacher_entity_id','session','date','session_start','session_finish','num_week_session','total_students','num_students_grade','num_prev_sessions','prev_st_math_days','class_size','start_time_variance','finish_time_variance','disjointedness','class_length','gameplay_duration','num_level_attempts','same_day_prev_session','common_students','time_difference','performance','perf_rank'
            data = [[district,year,iid,gcd,teacher_entity_id,session,date,session_start,session_finish,num_week_session,total_students,num_students_grade,num_prev_sessions,prev_st_math_days,class_size,start_time_variance,finish_time_variance,disjointedness,class_length,gameplay_duration,num_level_attempts,same_day_prev_session,common_students,time_difference,performance,perf_rank]]
            result_df = pandas.DataFrame(data)
            result_df.to_csv(result_file,mode='a',header=None,index=False)

