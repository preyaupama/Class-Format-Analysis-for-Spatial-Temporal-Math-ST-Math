
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as n
from sklearn import linear_model
from sklearn.feature_selection import SelectFromModel


# In[ ]:


ds = pd.read_csv('final_features_revised.csv')
print(ds.shape)
ds_subset = ds.iloc[:,  ds.columns.isin(["perf_rank_bin","performance","num_prev_sessions",
"prev_st_math_days", 
"class_size", 
"start_time_variance", 
"finish_time_variance", 
"disjointedness", 
"class_length", 
"gameplay_duration", 
"num_level_attempts", 
"did_students_practised",
"practiced_students_frac", 
"max_participant_frac"])]
print(ds_subset.shape)


# In[9]:


fs_y_1 = ds.ix[:,'performance']
fs_y_2 = ds.ix[:,'perf_rank_bin']

fs_x = ds_subset.iloc[:,  ds_subset.columns.isin(["num_prev_sessions",
"prev_st_math_days", 
"class_size", 
"start_time_variance", 
"finish_time_variance", 
"disjointedness", 
"class_length", 
"gameplay_duration", 
"num_level_attempts", 
"did_students_practised",
"practiced_students_frac", 
"max_participant_frac"])]


# In[33]:


#clf = linear_model.Lasso(alpha=0.1)
# Lasso(alpha=0.1, copy_X=True, fit_intercept=True, max_iter=1000,
#    normalize=False, positive=False, precompute=False, random_state=None,
#    selection='cyclic', tol=0.0001, warm_start=False)
clf_1 = linear_model.Lasso(alpha=0.01,max_iter=1000,selection='cyclic').fit(fs_x, fs_y_1)

model_1 = SelectFromModel(clf_1, prefit=True)

# print(model_1.transform(fs_x))
features = fs_x.columns.values
print(features[model_1.get_support()])

clf_2 = linear_model.Lasso(alpha=0.01).fit(fs_x, fs_y_2)

model_2 = SelectFromModel(clf_2, prefit=True)

# print(model_2.transform(fs_x))
features = fs_x.columns.values
print(features[model_2.get_support()])


# In[22]:


print(clf_1.get_params)

