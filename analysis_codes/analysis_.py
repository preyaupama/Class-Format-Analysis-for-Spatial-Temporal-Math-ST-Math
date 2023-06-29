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
result_file = 'D:\\upama_desktop\\Summer_2019\\scripts\\analysis\\results\\DC_Final_Class_Session_Formats.csv'
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
        # list down students of that grade handled by the teacher/the students that belong to the same classroom
        students = grade_teacher_df.student_entity_id.unique()
        # feature 10
        num_students_class = len(students)
            
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


            # feature 8
            date = start_times.min().date()
            
            # feature 9
            # minutes = start_times.min().minute
            hour = start_times.min().hour
            session_time = datetime.time(hour,0,0)
            
            # feature 12
            lab_seating = 0
            # feature 13
            free_seating = 0
            # feature 14
            home_login_exist = 1
            # feature 15
            high_time_variance = 0
            # feature 16
            segmented_class = 0
            # feature 17
            rotation = 0
            # feature 18
            others = 0
            # feature 19
            session_duration = 0
            # feature 20
            session_len = 0
            # feature 21
            performance = 0
            
            
            # determine lab seating and free seating
            # and if the start and finish times varies within 30 minutes
            # and if there is no home login it's a lab_seating

            
            # and if the start and finish times do not varies within 30 minutes
            # or if there are home login then it's a free_seating

            # each sesssion is either a lab seating or free seating

            # identify simultaneous plays in the order of time
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
            
            # feature 22
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
            # end analyzing simultaneous plays
            
            login_types = grade_session_teacher_df.home_or_lab_login.unique() 
            if len(login_types) == 1 and login_types[0] == 1:
                home_login_exist = 0
            if len(login_types) == 1 and login_types[0] == 0:
                home_login_exist = 2

            if start_time_diff < 300 and finish_times_diff < 300:
                if home_login_exist == 0:
                    lab_seating = 1
                    free_seating = 0
                else:
                    lab_seating = 0
                    free_seating = 1
            else:
                high_time_variance = 1

                lab_seating = 0
                free_seating = 1
            

            # determine rotation
            # check the previous and next sessions and the participants list in those session
            curr_session_students = grade_session_teacher_df.student_entity_id.unique()
            # feature 11
            participation = len(curr_session_students)/len(students)
            
            # end
            if len(sessions) == 1: # the teacher conducted only one session
                rotation = 0
            elif i == 0: # first session conducted by the teacher
                prev_session_students = None 
                next_session_students = grade_teacher_df[grade_teacher_df.session_number == sessions[i+1]].student_entity_id.unique()
                if set(curr_session_students).isdisjoint(set(next_session_students)):
                    rotation = 1
                else:
                    common_students = set(curr_session_students).intersection(set(next_session_students))
                    if len(common_students)/len(curr_session_students) <= 0.5 and len(common_students)/len(next_session_students) <= 0.5:
                        rotation = 2
            elif i == len(sessions)-1: # last session conducted by the teacher
                next_session_students = None
                prev_session_students = grade_teacher_df[grade_teacher_df.session_number == sessions[i-1]].student_entity_id.unique()
                if set(curr_session_students).isdisjoint(set(prev_session_students)):
                    rotation = 1
                else:
                    common_students = set(curr_session_students).intersection(set(prev_session_students))
                    if len(common_students)/len(curr_session_students) <= 0.5 and len(common_students)/len(prev_session_students) <= 0.5:
                        rotation = 2
            else: # other session
                next_session_students = grade_teacher_df[grade_teacher_df.session_number == sessions[i+1]].student_entity_id.unique()
                prev_session_students = grade_teacher_df[grade_teacher_df.session_number == sessions[i-1]].student_entity_id.unique()
                if set(prev_session_students).isdisjoint(set(curr_session_students)) or set(curr_session_students).isdisjoint(set(next_session_students)):
                    rotation = 1
                
                else:
                    common_students_pc = set(curr_session_students).intersection(set(prev_session_students))
                    common_students_cn = set(curr_session_students).intersection(set(next_session_students)) 
                    if len(common_students_cn)/len(curr_session_students) <= 0.5 and len(common_students_cn)/len(next_session_students) <= 0.5 and len(common_students_pc)/len(curr_session_students) <= 0.5 and len(common_students_pc)/len(prev_session_students) <= 0.5:
                        rotation = 2
                    # next session is a rotation
                    elif len(common_students_cn)/len(curr_session_students) <= 0.5 and len(common_students_cn)/len(next_session_students) <= 0.5:
                        if i+2 == len(sessions):
                            rotation = 2
                        else:
                            more_next_session_students = grade_teacher_df[grade_teacher_df.session_number == sessions[i+2]].student_entity_id.unique()
                            common_students_cn_mnss = set(more_next_session_students).intersection(set(next_session_students))
                            if len(common_students_cn_mnss) == 0 or (len(common_students_cn_mnss)/len(more_next_session_students) <= 0.5 and len(common_students_cn_mnss)/len(next_session_students) <= 0.5):
                                rotation = 2
                    # prev session is a rotation
                    elif len(common_students_pc)/len(curr_session_students) <= 0.5 and len(common_students_pc)/len(prev_session_students) <= 0.5:
                        if prev_session == 1 or prev_session == 2:
                            rotation = 2
            prev_session = rotation


            # determine others (low participation and not rotation)
            if len(start_finish_times)/len(students) < 0.7 and rotation == 0:
                others = 1

            # session duration
            session_duration_col = finish_times - start_times
            session_duration = session_duration_col.mean().total_seconds()
        
            # session length
            level_attempt_count = grade_session_teacher_df.groupby("student_entity_id").python_time.agg(['count'])
            session_len = list(level_attempt_count.mean())[0]
        
            # performance
            performance = grade_session_teacher_df['performance'].mean()
        
            # save the features for the current session in the output csv
            data = [[district,year,iid,gcd,teacher_entity_id,old_session_num,session,date,session_time,num_students_class,participation,lab_seating,free_seating,home_login_exist,high_time_variance,segmented_class,rotation,others, session_duration,session_len,performance,max_participent]]
            result_df = pandas.DataFrame(data)
            result_df.to_csv(result_file,mode='a',header=None,index=False)

        