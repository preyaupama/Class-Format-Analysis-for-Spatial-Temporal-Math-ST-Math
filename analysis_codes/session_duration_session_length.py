import pandas
import iso8601
import datetime
import sys

file_path_to_process = sys.argv[1] # path to the level attempt file that will be analyzed. we will rewrite this file



# read the csv file into a data frame
df = pandas.read_csv(file_path_to_process)
df['python_time'] = pandas.to_datetime(df['python_time'])

output_file = sys.argv[2]


# year, month, iid, grade, teacher, student, session, start, end, length, duratuion, performance    



students = df.student_entity_id.unique()
# for each student run the session analysis

for student in students:
    student_df = df[df.student_entity_id == student]
    

    session_days = pandas.to_datetime(student_df['python_time']).dt.date
    session_days = session_days.unique()
    session_days.sort()

    for session_day in session_days:
        session_day_data = student_df[pandas.to_datetime(student_df['python_time']).dt.date == session_day]
        session_day_data = session_day_data.sort_values(by='python_time')


        sessions = session_day_data.session_number.unique()
        sessions.sort()

        for session in sessions:
            session_data = session_day_data[session_day_data.session_number == session]
        
        
            year = session_data.year.unique()[0]
            month = session_data.month.unique()[0]
        
            iid = session_data.iid.unique()[0]
            grade = session_data.gcd.unique()[0]
            teacher = session_data.teacher_entity_id.unique()[0]
            student_entity_id = student
            start = session_data.python_time.min()
            end = session_data.python_time.max()
            length = len(session_data)
            duration = (end-start).total_seconds()
            performance = session_data.performance.mean()

            data = [['DC',year,month,session_day,iid,grade,teacher,student_entity_id,session,start,end,length,duration,performance]]
            result_df = pandas.DataFrame(data)
            result_df.to_csv(output_file,mode='a',header=None,index=False)
