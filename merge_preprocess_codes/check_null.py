import pandas
# remove duplicates
# student_time_pair = list()
# dup = list()
csv_file = "D:\\upama_desktop\\Summer_2019\\MIND_Data\\class_format_data\\DC.csv"
chunk_num = 0
for chunk in pandas.read_csv(csv_file, chunksize=10000, iterator=True, index_col='student_entity_id'):
    chunk_num = chunk_num + 1
    if chunk.isnull().values.any():
        print("NA exists!!!")
        break
    print(chunk_num)
    # for row in new_chunk.itertuples():
    #     val_list = [row.student_entity_id,row.time_level_attempt_started,row.session_number,row.home_or_lab_login,row.objective_index,row.game_number_in_objective,row.level_number_in_objective,row.attempt_number,row.level_passed_before,row.puzzles_passed,row.puzzles_total]
    #     with open('cleaned_merged_level_attempt.csv', mode='a') as cmla:
    #         writer = csv.writer(cmla)
    #         writer.writerow(fields)
        # if row.Index not in student_time_pair:
        #     student_time_pair.append(row.Index)
        #     dup.append(0)
        # else:
        #     dup.append(1)

# failed flag
# check attempt count