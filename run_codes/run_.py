import os
import pandas
import iso8601
import sys
import csv

districts = ['DC'] # list of districts we want to include in our analysis
years = ['2014','2015','2016','2017'] # list of years we want to include in our analysis

root = 'D:\\upama_desktop\\Summer_2019\\MIND_Data\\class_format_data' # folder that will contain data from all the district and years

# get student level data(iid, grade, stmath_user_id)
student_info_dict = dict()
# read the student level data
print("Getting student info...")
csv_file = 'D:\\upama_desktop\\Summer_2019\\MIND_Data\\cleaned_merged_student_info.csv' # path to student info file
student_info_df = pandas.read_csv(csv_file, index_col="student_entity_id")
# for chunk in pandas.read_csv(csv_file, chunksize=1000, iterator=True, index_col='student_entity_id'):
for row in student_info_df.itertuples():
    student_info_dict[row.Index] = (row.iid, row.gcd, row.stmath_user_id, row.teacher_entity_id)
del student_info_df


def preprocessing(file_path, district, year, file_name):
    print("Initializing...")
    new_df = pandas.read_csv(file_path, index_col="student_entity_id") # read the data in a dataframe
    # dictionaries to keep necessary info in memory
    level_attempt_count_dict = dict() # this dictionary will contain the count for each unique student_entity_id and timestamp pair occurances
    attempt_number_dict = dict() # this dictionary keeps count for attempts taken for a particular level by a student

    # new features
    failed = list() # if the current row contains data for a failed level attempt
    performance = list() # performance in the level attempt
    X1 = list() # X1 will be used to sort the data if the data is jumbled for some reason 
    python_time = list() # the time_level_attempt_started is converted to python_time for ease of sortimg 
    attempt_number_checked = list() # stores the new attempt count
    iid = list() # institution id of a student
    gcd = list() # grade of a student
    stmath_user_id = list() # stmath_user_id of a student
    teacher_entity_id = list() # teacher entity id for a student

    missing_students_list = list() # contain a list of students whose basic info is missing

    missing_student_info_file = open('info\\missing_student_info.txt', 'a') # list down students whose basic info are missing
    inconsistent_data_file = open('info\\inconsistent_data.txt', 'a') #  list down inconsistent data
    duplicate_info_file = open('info\\duplicate_info.txt','a') # list down the percentage of duplicates found in a file

    # write the name of the file under consideration
    missing_student_info_file.write("\nFile name:"+file_name+"\n")
    inconsistent_data_file.write("\nFile name:"+file_name+"\n")
    duplicate_info_file.write("\nFile name:"+file_name+"\n")


    # 1. check for duplicates
    # row_count = 0
    # for row in new_df.itertuples(): # this loop runs for each row
    #     if level_attempt_count_dict.get(row.Index) is None: # index must be student_entity_id and time_level_attempt_started
    #         level_attempt_count_dict[row.Index] = (1, row) # first occurance of the student-timestamp pair
        
    #     else:         
    #         level_attempt_count_dict[row.Index] = (level_attempt_count_dict[row.Index][0] + 1, level_attempt_count_dict[row.Index][1]) # increment the count
    
    #     if level_attempt_count_dict[row.Index][0] > 1:
    #         print("Duplicate found!!!")
    #         print(row)
    #         print(level_attempt_count_dict[row.Index][1])
    #         print("\n")
        
    #     else:
    #         print(row_count)

    #     row_count = row_count + 1  
    # ask Dr. Rutherford what to do about duplicates

    # 2. remove duplicates
    print("Removing Duplicates...")
    prev_len = len(new_df)
    ##################################drop_duplicates has bug - using alternate############################################
    # new_df = new_df.drop_duplicates(keep = 'first', inplace=False)
    seen_data = dict()
    drop = list()
    for row in new_df.itertuples():
        if seen_data.get(row) is None:
            drop.append(0)
            seen_data[row] = 1
        else:
            drop.append(1)
    del seen_data
    new_df['drop'] = drop
    new_df=new_df.loc[new_df['drop'] == 0]
    del new_df['drop']
    #######################################################################################################################
    new_len = len(new_df)
    dup_percnt = ((prev_len-new_len)/prev_len)
    dup_info = "Duplicate:"+str(dup_percnt)+"%\n"
    duplicate_info_file.write(dup_info)

    # 3. check again for duplicates
    # row_count = 0
    # for row in new_df.itertuples(): # this loop runs for each row
    #     if level_attempt_count_dict.get(row.Index) is None:
    #         level_attempt_count_dict[row.Index] = (1, row) # first occurance of the student-timestamp pair
        
    #     else:         
    #         level_attempt_count_dict[row.Index] = (level_attempt_count_dict[row.Index][0] + 1, level_attempt_count_dict[row.Index][1]) # increment the count
    
    #     if level_attempt_count_dict[row.Index][0] > 1:
    #         print("Duplicate found!!!")
    #         print(row)
    #         print(level_attempt_count_dict[row.Index][1])
    #         print("\n")
        
    #     else:
    #         print(row_count)

    #     row_count = row_count + 1
    
    # 4. check and count micellaneous duplicates
    print("Checking Cleaning Process...")
    mic_duplicates = len(new_df.pivot_table(index=['student_entity_id','time_level_attempt_started'], aggfunc='size'))
    mic_dup_info = "Other duplicates:"+str(((len(new_df)-mic_duplicates)/len(new_df))*100)+"%\n"
    duplicate_info_file.write(mic_dup_info)


    # 6. failed flag , timestamp, X1 and performance
    print("Creating new features...")
    row_number = 0
    inconsistent_row_count = 0
    for row in new_df.itertuples(): # this loop runs for each row
        row_number = row_number + 1 # increment row number
        X1.append(row_number) # store the row number
        if row.puzzles_passed != row.puzzles_total:
            failed.append(1) # if the number of puzzles passes is not equals to number of total puzzles, the student has failed
        else:
            failed.append(0)
        if row.puzzles_total != 0:
            performance.append(round(row.puzzles_passed/row.puzzles_total, 3)) # performance rounded to 3 digits
        else:
            inconsistent_row_count = inconsistent_row_count + 1
            inconsistent_data_file.write(str(row) + "\n")
            performance.append(0)

        # timezone conversion- converted time_level_attempt_started will be stored in a new column named python_time
        python_time.append(iso8601.parse_date(row.time_level_attempt_started))

        if student_info_dict.get(row.Index) is None: # if student info is not found append the student_entity_id to missing_students_list and assign None to corresponding columns
            if row.Index not in missing_students_list:
                missing_students_list.append(row.Index)
            iid.append(None)
            gcd.append(None)
            stmath_user_id.append(None)
            teacher_entity_id.append(None)
        else: # if student info is found assign them to corresponding columns
            iid.append(student_info_dict[row.Index][0])
            gcd.append(student_info_dict[row.Index][1])
            stmath_user_id.append(student_info_dict[row.Index][2])
            teacher_entity_id.append(student_info_dict[row.Index][3])

    
    # write the files and close them
    inconsistent_info = "Inconsistency in cleaned file:"+str((inconsistent_row_count/len(new_df))*100)+"%\n"
    duplicate_info_file.write(inconsistent_info)
    missing_student_info_file.write(str(missing_students_list) + "\n")
    missing_student_info_file.close()
    inconsistent_data_file.close()
    duplicate_info_file.close()

    # add the features to the dataframe
    new_df['failed'] = failed
    new_df['performance'] = performance
    new_df['X1'] = X1
    new_df['python_time'] = python_time
    new_df['iid'] = iid
    new_df['gcd'] = gcd
    new_df['stmath_user_id'] = stmath_user_id
    new_df['teacher_entity_id'] = teacher_entity_id


    # 7. do this after duplicate removal
    ######################################################################################################################################
    # check number of attempts
    print("Checking number of attempts...")
    # sort on the basis of timestamp
    new_df.sort_values('python_time')
    # count attempt number
    for row in new_df.itertuples(): # this loop runs for each row
        attempt_key = row.Index + str(row.objective_index) + str(row.game_number_in_objective) + str(row.level_number_in_objective)
        if attempt_number_dict.get(attempt_key) is None:
            attempt_number_dict[attempt_key] = 1
            attempt_number_checked.append(1)
        else:
            attempt_number_dict[attempt_key] = attempt_number_dict[attempt_key] + 1
            attempt_number_checked.append(attempt_number_dict[attempt_key])
    # sort on the basis of x1
    new_df.sort_values('X1') # retain original sequence
    # append thr column attempt_number_checked
    new_df['attempt_number_checked'] = attempt_number_checked

    # 8. Save the data to a new csv with same name
    print("Saving data to csv...")
    output_filename = 'preprocessed_data\\' + district + '\\' + year +'\\' + file_name
    new_df.to_csv(output_filename)
    print("Done...")
    #######################################################################################################################################    


##########################################################################################################################################
# Run preprocessing Tasks
# for district in districts:
#     for year in years:
#         path = root + '\\'+district+'\\'+year+'\\' # a folder is needed to store the data from different institutions of each district and year
#         files = os.listdir(path) # get the list of files under district and year folder
#         for file in files:
#             file_path = path + file # set the path to corresponding institution file
#             # command = 'python preprocess.py ' + file_path + ' ' + district + ' ' + year + ' ' + file
#             # os.system(command)
#             preprocessing(file_path,district,year,file)
            
#########################################################################################################################################
# setup the results directory-run only once
# print("preparing output file...")
# output_directory_ssws = 'D:\\upama_desktop\\Summer_2019\\scripts\\analysis\\results\\DC_Final_Class_Session_Formats_ssws.csv'
# output_directory_laws = 'D:\\upama_desktop\\Summer_2019\\scripts\\analysis\\results\\DC_Final_Class_Session_Formats_laws.csv'
# fields = ['district','year','iid','gcd','teacher_entity_id','session','date','session_start','session_finish','class_length','num_students_class','participation','lab_seating','free_seating','segmented_class','session_duration','session_len','performance','max_participent','same_day_session','time_difference','common_students']
# with open(output_directory_ssws, mode='a') as ssws:
#     writer = csv.writer(ssws)
#     writer.writerow(fields)
# with open(output_directory_laws, mode='a') as laws:
#     writer = csv.writer(laws)
#     writer.writerow(fields)
##########################################################################################################################################    
# Mark new sessions
# print("Marking New Sessions...")
# root_ = 'D:\\upama_desktop\\Summer_2019\\scripts\\analysis\\preprocessed_data'
# for district in districts:
#     for year in years:
#         path = root_ + '\\'+district+'\\'+year+'\\' # a folder is needed to store the data from different institutions of each district and year
#         files = os.listdir(path) # get the list of files under district and year folder
#         for file in files:
#             print(file)
#             file_path = path + file # set the path to corresponding institution file
#             command = 'python mark_new_session.py ' + file_path
#             os.system(command)
            
##########################################################################################################################################
# mark new session version 4
# print("Marking New Sessions...")
# root_ = 'D:\\upama_desktop\\Summer_2019\\scripts\\analysis\\preprocessed_data\\'
# files = os.listdir(root_) # get the list of files under district and year folder
# for file in files:
#     print(file)
#     file_path = root_ + file # set the path to corresponding institution file
#     command = 'python mark_session_v4.py ' + file_path
#     os.system(command)

##########################################################################################################################################

# print("Starting Analysis...")
# root_ = 'D:\\upama_desktop\\Summer_2019\\scripts\\analysis\\preprocessed_data'

# years = ['2014','2015','2016','2017']
# for year in years:
#     file = 'laws_lab_DC_' + year + '.csv' 
#     print(file)
#     path = root_ + '\\'+ file # a folder is needed to store the data from different institutions of each district and year
#     df = pandas.read_csv(path)

#     iid = ''
#     iid_list_temp = df.iid.unique()
#     iid_list = [iids for iids in iid_list_temp if str(iids) != 'nan']

#     del df

#     for iid in iid_list:
#         command = 'python analysis_final_laws.py ' + path + ' ' + 'DC' + ' ' + year + ' ' + file + ' ' + iid
#         os.system(command)


#     file_ssws = 'ssws_lab_DC_' + year + '_45' + '.csv' 
#     print(file_ssws)
#     path = root_ + '\\'+ file_ssws # a folder is needed to store the data from different institutions of each district and year
#     df = pandas.read_csv(path)

#     iid = ''
#     iid_list_temp = df.iid.unique()
#     iid_list = [iids for iids in iid_list_temp if str(iids) != 'nan']

#     del df

#     for iid in iid_list:
#         command = 'python analysis_final_ssws.py ' + path + ' ' + 'DC' + ' ' + year + ' ' + file_ssws + ' ' + iid
#         os.system(command)
##########################################################################################################################################            
# print("Checking marked session to ensure the soundness of the method...")
# file = 'D:\\upama_desktop\\Summer_2019\\scripts\\analysis\\results\\checked_DC.csv'
# fields = ['district','year','iid','gcd','teacher_entity_id','old_session_num','session','num_students_class','participation','session_day','start_time','finish_time','class_length','session_duration','session_len','performance','same_day_session','common_students','time_difference']
            
# with open(file, mode='a') as cms:
#     writer = csv.writer(cms)
#     writer.writerow(fields)
    
# root_ = 'D:\\upama_desktop\\Summer_2019\\scripts\\analysis\\preprocessed_data\\'
# years = ['2014','2015','2016','2017'] # get the list of files under district and year folder
# for year in years:
#     file = 'lab_DC_' + year + '.csv'
#     print(file)
#     file_path = root_ + file # set the path to corresponding institution file
#     command = 'python checking_marked_sessions.py ' + file_path + ' ' + year + ' ' + file
#     os.system(command)
##########################################################################################################################################
# # set up output files for session length and duration analysis
# print("preparing output file...")
# output_directory_1 = 'D:\\upama_desktop\\Summer_2019\\scripts\\analysis\\results\\home_length_duration_analysis_1.csv'
# output_directory_2 = 'D:\\upama_desktop\\Summer_2019\\scripts\\analysis\\results\\lab_length_duration_analysis_1.csv'
# # output_directory_3 = 'D:\\upama_desktop\\Summer_2019\\scripts\\analysis\\results\\lab_length_duration_analysis_2.csv'
# fields = ['district','year','month','date','iid','gcd','teacher_entity_id','student_entity_id','session','start','end','length','duration','performance']
# with open(output_directory_1, mode='a') as hsdla:
#     writer = csv.writer(hsdla)
#     writer.writerow(fields)
# with open(output_directory_2, mode='a') as lsdla:
#     writer = csv.writer(lsdla)
#     writer.writerow(fields)
# # with open(output_directory_3, mode='a') as lsdla:
# #     writer = csv.writer(lsdla)
# #     writer.writerow(fields)

# # # run session_duration_analysis
# print("Starting Analysis...")
# root_ = 'D:\\upama_desktop\\Summer_2019\\scripts\\analysis\\preprocessed_data'
# # places = ['home','lab']
# # years = ['2014','2015','2016','2017']
# files = ['laws_lab_DC_2014.csv','laws_lab_DC_2015.csv','laws_lab_DC_2016.csv','laws_lab_DC_2017.csv']
# for file in files: 
#     print(file)
#     path = root_ + '\\'+ file # a folder is needed to store the data from different institutions of each district and year
#     command = 'python session_duration_session_length.py ' + path + ' ' + output_directory_2
#     os.system(command)
# files = ['home_DC_2014.csv','home_DC_2015.csv','home_DC_2016.csv','home_DC_2017.csv']
# for file in files: 
#     print(file)
#     path = root_ + '\\'+ file # a folder is needed to store the data from different institutions of each district and year
#     command = 'python session_duration_session_length.py ' + path + ' ' + output_directory_1
#     os.system(command)
# files = ['ssws_lab_DC_2014_45.csv','ssws_lab_DC_2015_45.csv','ssws_lab_DC_2016_45.csv','ssws_lab_DC_2017_45.csv']
# for file in files: 
#     print(file)
#     path = root_ + '\\'+ file # a folder is needed to store the data from different institutions of each district and year
#     command = 'python session_duration_session_length.py ' + path + ' ' + output_directory_3
#     os.system(command)
#####################################################################################################################################
# revise X1
# os.system('python time_change_home_login_remove.py')
# set up output files for school hour analysis
######################################################################################################################################
# print("preparing output file...")
# output_directory_1 = 'D:\\upama_desktop\\Summer_2019\\scripts\\analysis\\results\\DC_school_hour_validation.csv'
# fields = ['district','year','iid','gcd','teacher_entity_id','session','date','session_time','curr_session_students']
# with open(output_directory_1, mode='a') as dshv:
#     writer = csv.writer(dshv)
#     writer.writerow(fields)
# run school hour validation task
#print("Starting Analysis...")
# root_ = 'D:\\upama_desktop\\Summer_2019\\scripts\\analysis\\preprocessed_data'
# files = os.listdir(root_)
# for file in files:
#     print(file)
#     path = root_ + '\\'+ file # a folder is needed to store the data from different institutions of each district and year
#     command = 'python validate_school_hours.py ' + path
#     os.system(command)



# root_ = 'D:\\upama_desktop\\Summer_2019\\scripts\\analysis\\preprocessed_data'

# years = ['2014','2015','2016','2017']
# for year in years:
#     file = 'lab_DC_' + year + '.csv' 
#     print(file)
#     path = root_ + '\\'+ file # a folder is needed to store the data from different institutions of each district and year
#     df = pandas.read_csv(path)

#     iid = ''
#     iid_list_temp = df.iid.unique()
#     iid_list = [iids for iids in iid_list_temp if str(iids) != 'nan']

#     del df

#     for iid in iid_list:
#         command = 'python analysis_school_hours.py ' + path + ' ' + 'DC' + ' ' + year + ' ' + file + ' ' + iid
#         os.system(command)
##########################################################################################################################################
# mark session ssws
# print("Marking New Sessions...")
# root_ = 'D:\\upama_desktop\\Summer_2019\\scripts\\analysis\\preprocessed_data\\'
# files = ['ssws_lab_DC_2014_45.csv', 'ssws_lab_DC_2015_45.csv', 'ssws_lab_DC_2016_45.csv','ssws_lab_DC_2017_45.csv'] # get the list of files under district and year folder
# for file in files:
#     print(file)
#     file_path = root_ + file # set the path to corresponding institution file
#     command = 'python mark_session_ssws.py ' + file_path
#     os.system(command)
##########################################################################################################################################
# mark session lsws
# print("Marking New Sessions...")
# root_ = 'D:\\upama_desktop\\Summer_2019\\scripts\\analysis\\preprocessed_data\\'
# files = ['laws_lab_DC_2014.csv', 'laws_lab_DC_2015.csv', 'laws_lab_DC_2016.csv','laws_lab_DC_2017.csv'] # get the list of files under district and year folder
# for file in files:
#     print(file)
#     file_path = root_ + file # set the path to corresponding institution file
#     command = 'python mark_session_laws.py ' + file_path
#     os.system(command)
##########################################################################################################################################             
##########################################################################################################################################
# seperating scatter plot data
# print("Seperating scatter plot data...")
# root_ = 'D:\\upama_desktop\\Summer_2019\\scripts\\analysis\\preprocessed_data\\'
# files = ['laws_lab_DC_2014.csv','laws_lab_DC_2015.csv','laws_lab_DC_2016.csv','laws_lab_DC_2017.csv'] # get the list of files under district and year folder
# for file in files:
#     print(file)
#     fields = ['year','iid','gcd','teacher_entity_id', 'session_day', 'session','class_length','session_duration','session_start','session_finish','student_entity_id','student_start','student_finish','performance']
#     output_file_path = root_ + 'plot_' + file
#     with open(output_file_path, mode='a') as ofp:
#         writer = csv.writer(ofp)
#         writer.writerow(fields)
#     file_path = root_ + file # set the path to corresponding institution file
#     command = 'python scatter_plot_data.py ' + file_path + ' ' + output_file_path
#     os.system(command)
#########################################################################################################################################
# prepare session feature file
# print("preparing output file...")
# output_directory = 'D:\\upama_desktop\\Summer_2019\\scripts\\analysis\\results\\prediction_features.csv'

# fields = ['district','year','iid','gcd','teacher_entity_id','session','date','session_start','session_finish','num_week_session','total_students','num_students_grade','num_prev_sessions','prev_st_math_days','class_size','start_time_variance','finish_time_variance','disjointedness','class_length','gameplay_duration','num_level_attempts','same_day_prev_session','common_students','time_difference','max_participent','performance','perf_rank']
# with open(output_directory, mode='a') as pff:
#     writer = csv.writer(pff)
#     writer.writerow(fields)

# create the features
# root_ = 'D:\\upama_desktop\\Summer_2019\\scripts\\analysis\\preprocessed_data'
years = ['2014','2015','2016','2017']
for year in years:
    file = 'laws_lab_DC_' + year + '.csv' 
    print(file)
    # path = root_ + '\\'+ file # a folder is needed to store the data from different institutions of each district and year
    path = file
    df = pandas.read_csv(path)

    iid = ''
    iid_list_temp = df.iid.unique()
    iid_list = [iids for iids in iid_list_temp if str(iids) != 'nan']

    del df

    for iid in iid_list:
        command = 'python prediction_model_features.py ' + path + ' ' + 'DC' + ' ' + year + ' ' + file + ' ' + iid
        os.system(command)
        # sys.exit(0)
print("Done**************************************************************************")