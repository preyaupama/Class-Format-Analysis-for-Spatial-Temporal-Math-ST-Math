import os
import pandas
import csv

#########################################################################################################
# merge the data
directory_in_str = 'D:\\upama_desktop\\Summer_2019\\scripts\\analysis\\preprocessed_data' # directory that contains the files
file_list = ['lab_DC_2014.csv','lab_DC_2015.csv','lab_DC_2016.csv','lab_DC_2017.csv']

file_number = 1
for file in file_list: # this loop runs for each file in the directory
    print(file_number)
    filename = file # get the filename
    if filename.endswith(".csv"): # input files must be csv files
        filename_with_path  = directory_in_str + "\\" + filename # get the full file path
        df = pandas.read_csv(filename_with_path, index_col=[0,1]) # read the csv with student_entity_id and time_level_attempt_started
        if file_number == 1:
            df.to_csv('merged_DC.csv') # if it is the first file read along with field name
            file_number = file_number + 1
        else:
            df.to_csv('merged_DC.csv', mode='a', header=False) # else read only the data
        continue
    else:
        continue

########################################################################################################
