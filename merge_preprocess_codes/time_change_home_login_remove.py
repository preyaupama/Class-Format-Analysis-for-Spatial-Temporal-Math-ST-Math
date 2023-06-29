import pandas
import os
import sys
import datetime

directory = 'D:\\upama_desktop\\Summer_2019\\scripts\\analysis\\preprocessed_data\\'
files = os.listdir(directory)

# Removed the duplicates
# Each year includes data from August-July
# seperates lab login from home login
# GRADE 1- GRADE 6
# Remove inconsistencies
# After verifying the school hours exclude them in two different ways(added 12 hours on that basis) 
for file in files:
    print(file)
    path = directory + file
    df = pandas.read_csv(path, index_col=[0,1]) # read the data in a dataframe
    df['python_time'] = pandas.to_datetime(df['python_time'])
    df['python_time'] = df['python_time'] + pandas.Timedelta('12:00:00')

    lab_df = df[df.home_or_lab_login == 1]
    home_df = df[df.home_or_lab_login == 0]
    lab_df.to_csv(directory+'lab_'+file)
    home_df.to_csv(directory+'home_'+file)

    # exclude irrelevant grades
    df = df[(df.gcd == 'GRADE1') | (df.gcd == 'GRADE2') | (df.gcd == 'GRADE3') | (df.gcd == 'GRADE4') | (df.gcd == 'GRADE5') | (df.gcd == 'GRADE6')]
    df.to_csv(path)

    # exclude inconsistencies
    consistent_data = df[df.puzzles_total != 0] 

    # update X1
    X1 = list()
    row_number = 1
    for row in df.itertuples():
        X1.append(row_number)
        row_number = row_number+1
    df['X1'] = X1
    df.to_csv(path)
    