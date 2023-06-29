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
result_file = 'D:\\upama_desktop\\Summer_2019\\scripts\\analysis\\results\\DC_Final_Class_Session_Formats_ssws.csv'
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
        # feature 6
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
        sessions = grade_teacher_df.session_num_ssws.unique()
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
            grade_session_teacher_df = grade_teacher_df[grade_teacher_df.session_num_ssws == session]

        

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

            # compare with the previous session - how well the sessions are separated 
            # feature 11
            same_day_session = 0
            # feature 12
            time_difference = 0
            # feature 13
            common_students = 0
            if i > 0:
                    prev_session = sessions[i-1]
                    prev_session_data = grade_teacher_df[grade_teacher_df.session_num_ssws == prev_session]
                    same_day_session = 0
                    if session_day == prev_session_data.session_day_number.unique()[0]:
                        same_day_session = 1
                    common_students = len(set(grade_session_teacher_df.student_entity_id.unique()).intersection(set(prev_session_data.student_entity_id.unique())))
                    time_difference = (start_time-prev_session_data.python_time.max()).total_seconds()
                else:
                    same_day_session = 2 # first session conducted by a teacher in a grade
                    common_students = 0
                    time_difference = 0
            # how long is the class
            # feature 14
            class_length = (session_finish - session_start).total_seconds()
            
            # feature 15
            lab_seating = 0
            # feature 16
            free_seating = 0
            
            # feature 17
            segmented_class = 0
            
            # feature 18
            session_duration = 0
            # feature 19
            session_len = 0
            # feature 20
            performance = 0
            
            
            

        
            # determine lab seating and free seating (need to examine free seating more)
            # and if the start and finish times varies within 30 minutes
            # and if there is no home login it's a lab_seating

            
            # and if the start and finish times do not varies within 10 minutes
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
            
            # feature 21
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
            
            
            if start_time_diff < 600 and finish_times_diff < 600:
                lab_seating = 1
                free_seating = 0
                
            else:
                lab_seating = 0
                free_seating = 1
            

            
            # number of students in this session
            curr_session_students = grade_session_teacher_df.student_entity_id.unique()
            # feature 22
            participation = len(curr_session_students)/len(students)
            
            
            

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
            data = [[district,year,iid,gcd,teacher_entity_id,session,date,session_start,session_finish,class_length,num_students_class,participation,lab_seating,free_seating,segmented_class, session_duration,session_len,performance,max_participent,same_day_session,time_difference,common_students]]
            result_df = pandas.DataFrame(data)
            result_df.to_csv(result_file,mode='a',header=None,index=False)

            
    #         break
    #     break

    # break
