import os
import pandas
import iso8601
import sys
import csv

districts = ['DC'] # list of districts we want to include in our analysis
years = ['2014','2015','2016','2017'] # list of years we want to include in our analysis


# setup the results directory-run only once
output_directory = 'D:\\upama_desktop\\Summer_2019\\scripts\\analysis\\results\\extended\\'
fields_play = ['district','year','iid','gcd','teacher_entity_id', 'old_session_num','session','date','session_hour','playing_same_levels','count_same_levels','median']
fields_rotation = ['district','year','iid','gcd','teacher_entity_id', 'old_session_num','session','date','session_hour','rotation']

print("Preparing result files...")
for district in districts:
    # path_play = output_directory+district+'_play_Class_Session_Formats.csv'
    path_rotation = output_directory+district+'_rotation_Class_Session_Formats.csv' 
    # with open(path_play, mode='a') as car:
    #     writer = csv.writer(car)
    #     writer.writerow(fields_play)
    with open(path_rotation, mode='a') as car:
        writer = csv.writer(car)
        writer.writerow(fields_rotation)


print("Starting Analysis...")
root_ = 'D:\\upama_desktop\\Summer_2019\\scripts\\analysis\\preprocessed_data'
for district in districts:
    for year in years:
        path = root_ + '\\'+district+'\\'+year+'\\' # a folder is needed to store the data from different institutions of each district and year
        files = os.listdir(path) # get the list of files under district and year folder
        for file in files:
            print(file)
            file_path = path + file # set the path to corresponding institution file
            command = 'python analysis_extended.py ' + file_path + ' ' + district + ' ' + year + ' ' + file
            os.system(command)
            
print("Done**************************************************************************")