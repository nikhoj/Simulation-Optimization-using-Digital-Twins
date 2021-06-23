'''
Rules:
    1. All Raw Dataframe name will be CAPITALIZED
    2. All Column value will be withour space and start with capital letter
    3. Everyother variable will name small letter.
'''

import pandas as pd
import os
import numpy as np

global SPLIT_PERCENT

root = ""

#function to read the files from directory
def read_files(root, name):
    directory = os.path.join(root, name)
    data = pd.read_csv(directory)
    
    return data


global data

#Reading the Raw files from the directory
RMI = read_files(root, name= 'X_edited.csv')
RMI = RMI.iloc[:,0:-1]
RMI = RMI.dropna()
RMI = RMI.rename(columns={"Location Name": "Site", "RMI Drum": "Drum", "Qty in pounds" : "Level"})
#RMI['Capacity'] = RMI['Capacity'].str.replace(',', '').astype(int)
for i in range(len(RMI)):
    if len(RMI.iloc[i,1]) == 9:
        RMI.iloc[i,1] = RMI.iloc[i,1].replace(RMI.iloc[i,1][8:],'0'+ RMI.iloc[i,1][8:])

for i in range(len(RMI)):
    if len(RMI.iloc[i,2]) == 15:
        RMI.iloc[i,2] = RMI.iloc[i,2].replace(RMI.iloc[i,2][14:],'0'+ RMI.iloc[i,2][14:])

SPLIT_PERCENT = read_files(root, name = 'Classifier Split.csv')
SPLIT_PERCENT = SPLIT_PERCENT.rename(columns={"Color ": "Color", "Percentage ": "Percentage"})
for i in range(len(SPLIT_PERCENT)):
    if len(SPLIT_PERCENT.iloc[i,0]) == 15:
        SPLIT_PERCENT.iloc[i,0] = SPLIT_PERCENT.iloc[i,0].replace(SPLIT_PERCENT.iloc[i,0][14:],'0'+ SPLIT_PERCENT.iloc[i,0][14:])



CLASSIFIER = read_files(root, name = 'Classifier.csv')
CLASSIFIER = CLASSIFIER.rename(columns = {"Processing_Rate" : "Rate"})
CLASSIFIER = list(CLASSIFIER['Rate'])

PFI = read_files(root, name = 'Pre-finish Inventory Drum.csv')
PFI = PFI.rename(columns = {"Drum Number" : "Drum", "Capacity In pounds": "Capacity"})
PFI['Capacity'] = PFI['Capacity'].str.replace(',', '').astype(int)
PFI['Color'],PFI['Size'], PFI['Flavor'], PFI['Level'] = np.NaN,np.NaN, np.NaN, 0
for i in range(len(PFI)):
    if len(PFI.iloc[i,1]) == 9:
        PFI.iloc[i,1] = PFI.iloc[i,1].replace(PFI.iloc[i,1][8:],'0'+ PFI.iloc[i,1][8:])

PI = read_files(root, name = 'Pack inventory Drum.csv')
PI = PI.rename(columns= {"Drum Number" : "Drum"})
PI['Capacity'] = PI['Capacity'].str.replace(',', '').astype(int)
PI['Color'], PI['Size'], PI['Flavor'], PI['Level'] = np.NaN, 0, np.NaN, 0
for i in range(len(PI)):
    if len(PI.iloc[i,1]) == 9:
        PI.iloc[i,1] = PI.iloc[i,1].replace(PI.iloc[i,1][8:],'0'+ PI.iloc[i,1][8:])

data = [RMI, PFI, PI]
#Data Structure for only one site
sitelist = ['Detroit, MI', 'Columbus, OH', 'Springfield, MO', 'Green Bay, WI', 'Omaha, NE']


global f1
global f2
global f3
global classifier_pr
global site
global num_of_PFO
global rmi
global pfi
global pi


def site_data(data, site):
    global rmi
    global pfi
    global pi
    
    RMI, PFI, PI = data
    rmi = RMI[RMI['Site'] == site].dropna().reset_index(drop=True)
    rmi = rmi.sort_values(by = ['Color', 'Drum']).reset_index(drop = True)
    pfi = PFI[PFI['Site'] == site].reset_index(drop=True)
    pi = PI[PI['Site'] == site].reset_index(drop=True)
    
    
    return rmi, pfi, pi

site = sitelist[0]    #Change 1
rmi, pfi, pi = site_data(data, site = site )


#call for the rate
classifier_pr = CLASSIFIER[0]   #Change 2
#num_of_PFO = 2
#f1, f2, f3 = ['F14', 'F15', 'F16']
    




    