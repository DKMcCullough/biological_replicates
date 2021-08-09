'''

name:   ben_all.py 

location: /Users/dkm/Documents/Talmy_research?biological_replicates_project/src

author: DKM


goal:  import and graph Pro cell count data from 2 different days of growth in 0nm HOOH (MIT9215 + 0nM HOOH on 2/5/20 and 1/31/20) 


'''



import pandas as pd
import numpy as np
from matplotlib import *
import matplotlib.pyplot as plt 
from openpyxl import *







############################

#  Data Import from csv   

############################


df_all = pd.read_excel('../../biological_replicates_project/data/ben_vol_1_multi_data.xlsx', engine = 'openpyxl', sheet_name = "ODElib_format_reps", header = 0, keep_default_na = True) 

#using openpyxl because of xlrd version issues
df_all.columns = df_all.iloc[0]
#print(df_all.columns)


#Grabbing just data from Feb experiment or Jan experiment

feb_df = df_all.loc[df_all['oriSource'] == 'Calfee raw data 2-5-2020']
#print(feb_df)

jan_df = df_all.loc[df_all['oriSource'] == 'Calfee raw data 1-31-2020']
#print(jan_df)


jan_hooh_df = jan_df.loc[jan_df['HOOH treatment'] == 400]
#print(jan_hooh_df)


feb_hooh_df = feb_df.loc[feb_df['HOOH treatment'] == 400]
#print(feb_hooh_df)


feb_control_df = feb_df.loc[feb_df['control'] == 'True']
print(feb_control_df)




'''




######################################

# graphing 

#####################################


'''








