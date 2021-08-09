''' 
name: selene_ods.py

location:  /Users/dkm/Documents/Talmy_research/biological_replicates_project/scripts/selene_ods.py 

author: DKM

working to read in data from excel via pandas and hopefully work on looking at biological/technical replicate data varience

'''


import pandas as pd
import numpy as np
from matplotlib import *
import matplotlib.pyplot as plt 


#############################

   # Data Input   

#############################

IV_1_df = pd.read_excel('../../biological_replicates_project/data/Selene_data_reconfigured.xlsx', sheet_name = "IV_1-OD", header = 2, keep_default_na = True)
  #keep_default_na -> gets rid of missing values in the data frame, convert_float -> makes all numbers a float in the dataframe   #Have header set at 4 because Selene said the 0 time points weren't accurarte for OD and that they were probs back-calculated anyway

#IV_1_df.dropna(how='all', axis=1, inplace=False)


IV_2_df = pd.read_excel('../../biological_replicates_project/data/Selene_data_reconfigured.xlsx', sheet_name = "IV_2-OD", header = 2, keep_default_na = True)
IV_3_df = pd.read_excel('../../biological_replicates_project/data/Selene_data_reconfigured.xlsx', sheet_name = "IV_3-OD", header = 2, keep_default_na = True)
IV_4_df = pd.read_excel('../../biological_replicates_project/data/Selene_data_reconfigured.xlsx', sheet_name = "IV_4-OD" , header = 2, keep_default_na = True) 




#print( IV_1_df, IV_2_df, IV_3_df, IV_4_df) 




###############################

#   Graphing Data  

###############################


#IV_1_df = IV_1_df.fillna(0)
#IV_1_df.astype(float)
ax = IV_1_df.plot( x = "Time (min)",  y = ['OD_1'], kind = 'scatter')
ax.set(title = 'Seperate OD runs over different Time sets', xlabel = 'Time (min)', ylabel = 'Optical Density of E.coli')
IV_1_df["OD_3"] = IV_1_df['OD_3'].replace(' ',np.nan)

for odname in IV_1_df.columns[1:]:
	IV_1_df[odname] = IV_1_df[odname].replace(' ',np.nan)   #replacing any stray spaces in a 'blank' excel cell with a nan in the df
	IV_1_df.plot(x="Time (min)", y=odname, ax=ax, kind = 'scatter')    #plotting each OD column vs Time :-) 
#IV_1_df.plot(x="Time (min)", y="OD_3", kind="scatter", ax=ax, color = 'r')
#IV_1_df.plot(x="Time (min)", y="OD_4", kind="scatter", ax=ax, color = 'y')






#plt.semilogy()
#ax.legend()

plt.show()









