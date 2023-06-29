import pandas

input_data = pandas.read_csv("final_features_revised.csv")

input_data_dict = dict()
for row in input_data.itertuples():
    key = str(row.year) + "_" + str(row.iid) + "_" + str(row.gcd) + "_" + str(row.teacher_entity_id) + "_" + str(row.session)
    input_data_dict[key] = 1
del input_data

data_to_be_filtered = pandas.read_csv("DC_Final_Class_Session_Formats_laws.csv")
result_file = "filtered_class_format_data.csv"
for row in data_to_be_filtered.itertuples():
    key = key = str(row.year) + "_" + str(row.iid) + "_" + str(row.gcd) + "_" + str(row.teacher_entity_id) + "_" + str(row.session)
    if input_data_dict.get(key) is not None:
        data = [[row.district,row.year,row.iid,row.gcd,row.teacher_entity_id,row.session,row.date,row.session_start,row.session_finish,row.class_length,row.num_students_class,row.participation,row.lab_seating,row.free_seating,row.segmented_class,row.session_duration,row.session_len,row.performance,row.max_participent,row.same_day_session,row.time_difference,row.common_students]]
        result_df = pandas.DataFrame(data)
        result_df.to_csv(result_file,mode='a',header=None,index=False) 