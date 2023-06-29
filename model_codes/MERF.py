import statsmodels.api as sm
import statsmodels.formula.api as smf
import pandas
import sys
# percentile
# from numpy import percentile
# from numpy import std
# from numpy import mean
# from numpy import random
import numpy
from sklearn.metrics import mean_squared_error
# for decision tree and regression models
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier,AdaBoostClassifier,GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.feature_selection import RFE
from sklearn.svm import SVC
from merf.merf import MERF
from sklearn.externals import joblib
# to draw decision tree
from sklearn.externals.six import StringIO  
from IPython.display import Image  
from sklearn.tree import export_graphviz
import pydotplus

# utilities
import datetime

# read dataframe
data = pandas.read_csv("final_features_revised.csv")


################################################################################################################################
# perf_rank_bin = list()
# group = list()
# # fix other features
# # 1. prev session days
# # 2. prev sessions
# # 3. same day session
# # 4. percentage
# prev_st_math_days = list()
# num_prev_sessions = list()
# same_day_prev_session = list()
# common_students_percent = list()
# for row in data.itertuples():
#     print(row.Index)
    # g = row.gcd + "_" + row.teacher_entity_id
    # group.append(g)
    
    # 1. prev session days
    # prev_session_days = data[(data.year == row.year) & (data.gcd == row.gcd) & (data.teacher_entity_id == row.teacher_entity_id) & (data.prev_st_math_days < row.prev_st_math_days)]
    # prev_st_math_days.append(len(prev_session_days.prev_st_math_days.unique()))
    # # 2. prev sessions
    # prev_sessions = data[(data.year == row.year) & (data.gcd == row.gcd) & (data.teacher_entity_id == row.teacher_entity_id) & (data.session < row.session)]
    # num_prev_sessions.append(len(prev_session_days.session.unique()))
    # # # 3. same day session
    # if row.same_day_prev_session == 1:
    #     same_day_prev_session.append(1)
    #     common_students_percent.append(row.common_students/row.class_size)
    # else:
    #     same_day_prev_session.append(0)
    #     common_students_percent.append(0)
    # # 4. percentage
    # if row.perf_rank == 1 or row.perf_rank == 2:
    #     perf_rank_bin.append(0)
    # else:
    #     perf_rank_bin.append(1)
# data['perf_rank_bin'] = perf_rank_bin
# data['group'] = group
# data['prev_st_math_days'] = prev_st_math_days
# data['num_prev_sessions'] = num_prev_sessions
# data['same_day_prev_session'] = same_day_prev_session
# data['common_students_percent'] = common_students_percent

# data.to_csv("final_features_revised.csv",index=False)
# sys.exit(0)

# group_id = list()
# group_id_dict = dict()
# id = 1
# for row in data.itertuples():
#     print(row.Index)
#     if group_id_dict.get(row.group) is None:
#         group_id_dict[row.group] = id
#         group_id.append(id)
#         id = id + 1
#     else:
#         group_id.append(group_id_dict[row.group])
        
# data["group_id"] = group_id
# data.to_csv("final_features_revised.csv",index=False)

###################################################################################################################################
# outlier removal
# features = ['disjointedness','num_level_attempts','mp_percent','class_size','gameplay_duration','class_length','start_time_variance','finish_time_variance', 'common_students_percent']
# for feature in features:
#     print("\n\n")
#     print(feature)
#     print("Interquartile cutoff range:")
#     q25, q75 = percentile(data[feature], 25), percentile(data[feature], 75)
#     iqr = q75 - q25
#     print('Percentiles: 25th=%.3f, 75th=%.3f, IQR=%.3f' % (q25, q75, iqr))
#     cut_off = iqr * 1.5
#     lower, upper = q25 - cut_off, q75 + cut_off
#     print("lower:"+str(lower)+" upper:"+str(upper))

#     print("Cutoff using standard deviation:")
#     data_mean, data_std = mean(data[feature]), std(data[feature])
#     print("mean:"+str(data_mean)+" std:"+str(data_std))
#     cut_off = data_std * 3
#     lower, upper = data_mean - cut_off, data_mean + cut_off
#     print("lower:"+str(lower)+" upper:"+str(upper))
######################################################################################################################################
# revise session days and session numbers
# revised_session_days = list()
# revised_num_sessions = list()

# for row in data.itertuples():
#     print(row.Index)
#     # 1. prev session days
#     prev_session_days = data[(data.year == row.year) & (data.gcd == row.gcd) & (data.teacher_entity_id == row.teacher_entity_id) & (data.prev_st_math_days < row.prev_st_math_days)]
#     revised_session_days.append(len(prev_session_days.prev_st_math_days.unique()))
#     # 2. prev sessions
#     prev_sessions = data[(data.year == row.year) & (data.gcd == row.gcd) & (data.teacher_entity_id == row.teacher_entity_id) & (data.session < row.session)]
#     revised_num_sessions.append(len(prev_session_days.session.unique()))
# data['revised_session_days'] = revised_session_days
# data['revised_num_sessions'] = revised_num_sessions

# data.to_csv("final_features_revised.csv",index=False)
######################################################################################################################################
# revise groups
# group_id = list()
# group_id_dict = dict()
# id = 0
# for row in data.itertuples():
#     print(row.Index)
#     if group_id_dict.get(row.group) is None:
#         group_id_dict[row.group] = id
#         group_id.append(id)
#         id = id + 1
#     else:
#         group_id.append(group_id_dict[row.group])
        
# data["group_id"] = group_id
# data.to_csv("final_features_revised.csv",index=False)
######################################################################################################################################
# add feature sessions per week
# print("Start:")
# input_file = pandas.read_csv("number_of_times_each_classroom_played_stmath_in_a_month.csv")

# input_data_dict = dict()
# for row in input_file.itertuples():
#     key = str(row.year) + "_" + str(row.iid) + "_" + str(row.teacher_entity_id)
#     value = dict()
#     value['1'] = row.January
#     value['2'] = row.February
#     value['3'] = row. March
#     value['4'] = row.April
#     value['5'] = row.May
#     value['6'] = row.June
#     value['7'] = row.July
#     value['8'] = row.August
#     value['9'] = row.September
#     value['10'] = row.October
#     value['11'] = row.November
#     value['12'] = row.December
#     input_data_dict[key] = value
# st_math_per_week = list()
# data['date'] = pandas.to_datetime(data['date'])
# print("Start")
# for row in data.itertuples():
#     key = str(row.year) + "_" + str(row.iid) + "_" + str(row.teacher_entity_id)
#     if input_data_dict.get(key) is not None:
#         st_math_per_week.append(input_data_dict[key][str(row.date.month)])
#     else:
#         st_math_per_week.append(-1)
    
# data['ST_MATH_per_week'] = st_math_per_week
# data.to_csv("final_features_revised.csv",index=False)
# print("Done")
####################################################################################################################
# generate summary statistics for the features
# unit for each feature - specially the time related features
####################################################################################################################

         
# Features
# district, year, iid, gcd, teacher_entity_id, session, date, session_start, session_finish, num_week_session,
# total_students, num_students_grade, num_prev_sessions, prev_st_math_days, class_size, start_time_variance, finish_time_variance,
# disjointedness, class_length, gameplay_duration, num_level_attempts, same_day_prev_session, common_students, time_difference, max_participent,
# performance, perf_rank

# train and test set generation
data['Z'] = [1] * len(data)
feature_list_str = "num_prev_sessions + prev_st_math_days + class_size +  start_time_variance + finish_time_variance + disjointedness + class_length + gameplay_duration + num_level_attempts + did_students_practised + practiced_students_frac + max_participant_frac"
feature_list = ["num_prev_sessions", "prev_st_math_days", "class_size", "start_time_variance", "finish_time_variance", "disjointedness", "class_length", "gameplay_duration", "num_level_attempts", "did_students_practised", "practiced_students_frac", "max_participant_frac"]

feature_list_melr = ["num_prev_sessions", "prev_st_math_days", "class_size", "start_time_variance", "finish_time_variance", "disjointedness", "class_length", "gameplay_duration", "num_level_attempts", "did_students_practised", "practiced_students_frac", "max_participant_frac", "performance", "final_group", "Z"] 
X=data[feature_list_melr] # Features

y=data['performance'] # for mixed effect random forest

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
x_train = X_train[["num_prev_sessions", "prev_st_math_days", "class_size", "start_time_variance", "finish_time_variance", "disjointedness", "class_length", "gameplay_duration", "num_level_attempts", "did_students_practised", "practiced_students_frac", "max_participant_frac"]]
Z_train = X_train[["Z"]]
clusters_train = X_train["final_group"]

x_test = X_test[["num_prev_sessions", "prev_st_math_days", "class_size", "start_time_variance", "finish_time_variance", "disjointedness", "class_length", "gameplay_duration", "num_level_attempts", "did_students_practised", "practiced_students_frac", "max_participant_frac"]]
Z_test = X_test[["Z"]]
clusters_test = X_test["final_group"]
X_test.to_csv("test.csv",index=False)

# mixed effect linear regression
# formula = "performance ~ " + feature_list_str
# md = smf.mixedlm(formula, X, groups=X["final_group"])
# mdf = md.fit()

# print(mdf.summary())

# predictions = mdf.predict(X_test)
# print("MELR MSE:"+str(mean_squared_error(y_test,predictions)))


# HIGHER P-Value than 0.05 means insignificant\n

# mixed effect random forest

mrf = MERF()
mrf_model = mrf.fit(x_train, Z_train, clusters_train, y_train)

mrf_predictions = mrf.predict(x_test, Z_test, clusters_test)
print("MERF MSE:"+str(mean_squared_error(y_test,mrf_predictions)))
joblib.dump(mrf_model,'Data/fs_model-lr.pkl')


orig_mse = mean_squared_error(y_test,mrf_predictions)
for i in range(len(feature_list)):
    dup_x_test = x_test
    feature_name = feature_list[i]
    x = x_test[feature_name]
    mu = numpy.mean(x)
    sigma = numpy.std(x)
    noise = numpy.random.normal(mu, sigma, x.shape[0]).reshape(x.shape)
    dup_x_test[feature_name] = noise
    y_pred = mrf.predict(dup_x_test, Z_test, clusters_test)
    mse = mean_squared_error(y_test, y_pred)
    percent_inc = (mse - orig_mse)/orig_mse
    print(feature_name)
    print(percent_inc)