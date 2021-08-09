'''

name:   ben_odelib_test.py 

location: /Users/dkm/Documents/Talmy_research?biological_replicates_project/src

author: DKM


goal:  import and graph Pro cell count data from 2 different days of growth in 0nm HOOH (MIT9215 + 0nM HOOH on 2/5/20 and 1/31/20) 


'''



import pandas as pd
import numpy as np
from matplotlib import *
import matplotlib.pyplot as plt 
from openpyxl import *
import ODElib
import scipy
import pylab as py





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

'''
jan_hooh_df = jan_df.loc[jan_df['HOOH treatment'] == 400]
#print(jan_hooh_df)


feb_hooh_df = feb_df.loc[feb_df['HOOH treatment'] == 400]
#print(feb_hooh_df)


#feb_control_df = feb_df.loc[feb_df['control'] == 'True']
#print(feb_control_df)



'''




####################################

#from katiedemo/src/example.py 

###################################



###################################################
# read in data
###################################################

# read whole dataset
master_df = feb_df
single = master_df


##################################################
# define model
###################################################

def holling_one(y,t,ps):
    alpha=ps[0]
    N,H = y[0],y[1]
    dNdt = -alpha*N*H
    dHdt = alpha*N*H
    return [dNdt,dHdt]

###################################################
# initialize model
###################################################

# define initial conditions
#H0 = single[single['organism']=='H']['abundance'].iloc[0]
#N0 = single[single['organism']=='H']['abundance'].iloc[-1] - H0

H0 = single[single['organism']=='H']['rep1'].iloc[0]
N0 = single[single['organism']=='H']['rep1'].iloc[-1] - H0



# log-transformed priors
alpha_prior=ODElib.parameter(stats_gen=scipy.stats.lognorm,
                      hyperparameters={'s':1,'scale':1e-6})

N0_prior=ODElib.parameter(stats_gen=scipy.stats.lognorm,
                      hyperparameters={'s':1,'scale':N0})

# initialize the class for fitting
H1=ODElib.ModelFramework(ODE=holling_one,
                          parameter_names=['alpha','N0'],
                          state_names = ['N','H'],
                          dataframe=single,
                          alpha = alpha_prior.copy(),
                          N0 = N0_prior.copy(),
                          t_steps=288,
                          H = H0,
                          N = N0
                         )


###################################################
# visualize initial parameter guess
###################################################

# setup figure
f,ax = py.subplots(1,2,figsize=[9,4.5])
ax[0].set_xlabel('Time (days)')
ax[1].set_xlabel('Time (days)')
ax[0].set_ylabel('Nutrients (cellular equivalents ml$^{-1}$)')
ax[1].set_ylabel('Cells ml$^{-1}$')
ax[0].semilogy()
ax[1].semilogy()

# plot data
ax[1].errorbar(H1.df.loc['H']['time'],
                            H1.df.loc['H']['abundance'],
                            yerr=H1._calc_stds('H')
                            )

# integrate the model once with initial parameter guess
mod = H1.integrate()

# plot model initial guess
ax[0].plot(H1.times,mod['N'],label='initial guess',c='r')
ax[1].plot(H1.times,mod['H'],label='initial guess',c='r')

###################################################
# do fitting and plot fitted model
###################################################

# provide reasonable guesses for the mcmc algorithm
chain_inits = pd.DataFrame({'alpha':[1e-6]*2,'N0':[N0]*2})

# call the MCMC algorithm to fit parameters
posteriors = H1.MCMC(chain_inits=chain_inits,iterations_per_chain=1000,
                       cpu_cores=2,fitsurvey_samples=1000,sd_fitdistance=20.0)

# set optimal parameters
im = posteriors.loc[posteriors.chi==min(posteriors.chi)].index[0]
H1.set_parameters(**posteriors.loc[im][H1.get_pnames()].to_dict())
H1.set_inits(**{'N':posteriors.loc[im][H1.get_pnames()].to_dict()['N0']})

# run the model again, now with fitted parameters
mod = H1.integrate()

# plot fitted model
ax[0].plot(H1.times,mod['N'],label='fitted',c='g')
ax[1].plot(H1.times,mod['H'],label='fitted',c='g')

# legend
l = ax[1].legend()
l.draw_frame(False)

py.show()

# save output
#f.savefig('../figures/batch_curve_fitting')



