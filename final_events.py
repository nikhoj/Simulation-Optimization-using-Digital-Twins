from Data_structure import *
from Demand_dist import *
from bin_segmentor import *
from Distribution import df1, df2
import pandas as pd
import numpy as np
import random

#some global variable
global color_of_rmi
global level_of_rmi
global Y
global time

global L #classifier busy or not 
global FEL
global tank_que
global I1
global I2
global I3
global tank1_mtl
global tank2_mtl
global tank3_mtl
global color_wise_demand #when a drum opens it create a chart of color, size, flavor combination
global empty_pi_que
global box1
global bag1
global bag2
global box_que
global production1
global production2
global bag_que
global num_of_bag
global flavoring_rate
global pack_rate
global R
global last_color
global pfi_cap
global pi_cap

pfi_cap , pi_cap = 1 , 1
last_color = 0

R = 0
#initialize

flavoring_rate = df1[df1['Site'] == site[0:-4]]
pack_rate = df2[df2['Site'] == site[0:-4]]
time = 0
num_of_bag = 2
empty_pi_que = pi

color_of_rmi = 1
level_of_rmi = 0

I1, I2, I3 = 0, 0, 0
box1, bag1, bag2 = 0, 0, 0

#initialize Y , the amount of Jelly beans of color i, size j in classifier
Y = pd.DataFrame(columns=['Color' , 'Size', 'Level'])
#Y['Color'], Y['Size'], Y['Level'] = [0,0,0,0,0], ['S1','S2','S3','S4','S5'], [0,0,0,0,0]
events = ['Releasing Drum', 'Classifying', 'Flavoring in tank1','Flavoring in tank2', 'Flavoring in tank3', 'Boxing', 'Bagging in mc1', 'Bagging in mc2', 'Flavor Changing tank1', 'Flavor Changing tank2', 'Flavor Changing tank3']
FEL = pd.DataFrame(columns=['Event' , 'Time'])
tank_que = pd.DataFrame(columns=['Site', 'Drum', 'Capacity',  'Color', 'Size','Flavor',  'Level'])
tank1_mtl = pd.DataFrame(columns=['Site','Drum', 'Capacity', 'Color' ,'Size' , 'Flavor', 'Level'])
tank2_mtl = pd.DataFrame(columns=['Site','Drum', 'Capacity', 'Color' ,'Size' , 'Flavor', 'Level'])
tank3_mtl = pd.DataFrame(columns=['Site','Drum', 'Capacity', 'Color' ,'Size' , 'Flavor', 'Level'])
box_que = pd.DataFrame(columns=['Site','Drum', 'Capacity', 'Color' ,'Size' , 'Flavor', 'Level'])
bag_que = pd.DataFrame(columns=['Site','Drum', 'Capacity', 'Color' ,'Size' , 'Flavor', 'Level'])
production1 = pd.DataFrame(columns=['Site','Drum', 'Capacity', 'Color' ,'Size' , 'Flavor', 'Level'])
production2 = pd.DataFrame(columns=['Site','Drum', 'Capacity', 'Color' ,'Size' , 'Flavor', 'Level'])

#FEL = FEL.append({'Event' : 'Releasing Drum', 'Time' : time}, ignore_index=True)



def FEL_builder(event, level = None, rate = None):
    global FEL
    global time

    
    if event == 'Releasing Drum':
        FEL = FEL.append({'Event' : 'Releasing Drum', 'Time' : time}, ignore_index=True)
    elif event == 'Classifying':
        FEL = FEL.append({'Event' : 'Classifying', 'Time' : time + ( level / rate)}, ignore_index=True)
    elif event == 'Flavoring in tank1':
        FEL = FEL.append({'Event' : 'Flavoring in tank1', 'Time' : time + (level / rate)}, ignore_index=True)
    elif event == 'Flavoring in tank2':
        FEL = FEL.append({'Event' : 'Flavoring in tank2', 'Time' : time +(level / rate)}, ignore_index=True)
    elif event == 'Flavoring in tank3':
        FEL = FEL.append({'Event' : 'Flavoring in tank3', 'Time' : time +(level / rate)}, ignore_index=True)
    elif event == 'Boxing':
        FEL = FEL.append({'Event' : 'Boxing', 'Time' : time +( level / rate)}, ignore_index=True)
    elif event == 'Bagging in mc1':
        FEL = FEL.append({'Event' : 'Bagging in mc1', 'Time' : time +( level / rate)}, ignore_index=True)
    elif event == 'Bagging in mc2':
        FEL = FEL.append({'Event' : 'Bagging in mc2', 'Time' : time +( level / rate)}, ignore_index=True)
    elif event == 'Flavor Changing tank1':
        FEL = FEL.append({'Event' : 'Flavor Changing tank1', 'Time' : int(time + (5/60))}, ignore_index=True)
    elif event == 'Flavor Changing tank2':
        FEL = FEL.append({'Event' : 'Flavor Changing tank2', 'Time' : int(time + (5/60))}, ignore_index=True)
    elif event == 'Flavor Changing tank3':
        FEL = FEL.append({'Event' : 'Flavor Changing tank3', 'Time' : int(time + (5/60))}, ignore_index=True)
    else:
        print('Unknown Event')
    
       
    

def releasing_drum():
    global rmi
    global time
    global L
    global FEL
    global color_wise_demand
    global color_of_rmi
    global level_of_rmi
    global classifier_pr
    global R
    global last_color
    
    #Remove First Drum D from the RMI Queue after taking color and level
    color_of_rmi = rmi.loc[0, 'Color']
    
    level_of_rmi = rmi.loc[0, 'Level']
    rmi = rmi.drop(0).reset_index(drop=True)
        
    #Update the L : Make classifier Busy
    L = 1
    R = 1
    rate = classifier_pr
    level = level_of_rmi
    FEL_builder('Classifying', level, rate)
    if last_color != color_of_rmi:
        color_wise_demand = prepare_color_wise_demand(color_of_rmi)
    
#releasing_drum()

def excess_fill(giver_level, taker_cap, size): #helping function to fill bin
    global color_wise_demand
    global f1
    
    taker_level = 0
    #temp = color_wise_demand[(color_wise_demand['Size'] == size) & (color_wise_demand['Demand'] > 0)].reset_index(drop = True)
    flavor = f1
    X = giver_level
    #get_index = int(color_wise_demand[(color_wise_demand['Size'] == size) & (color_wise_demand['Flavor'] == flavor)].index.values)
    
    if X >= taker_cap *.95:
        Y = taker_cap *.95
    else:
        Y = X
    
    
    if giver_level >= Y:
        giver_level -= Y
        taker_level += Y
        #color_wise_demand.loc[get_index, 'Demand'] = X - Y
    elif giver_level < Y:
        taker_level += giver_level
        giver_level = 0
        #color_wise_demand.loc[get_index, 'Demand'] = X - Y
    
        
    return giver_level, taker_level, flavor


def fill(giver_level, taker_cap, size): #helping function to fill bin
    global color_wise_demand
    
    
    taker_level = 0
    temp = color_wise_demand[(color_wise_demand['Size'] == size) & (color_wise_demand['Demand'] > 0)].reset_index(drop = True)
    flavor = temp.iloc[0,2]
    X = temp.loc[0, 'Demand']
    get_index = int(color_wise_demand[(color_wise_demand['Size'] == size) & (color_wise_demand['Flavor'] == flavor)].index.values)
    
    if X >= taker_cap *.95:
        Y = taker_cap *.95
    else:
        Y = X
    
    
    
    if giver_level >= Y:
        giver_level -= Y
        taker_level += Y
        color_wise_demand.loc[get_index, 'Demand'] = X - Y
    elif giver_level < Y:
        taker_level += giver_level
        giver_level = 0
        color_wise_demand.loc[get_index, 'Demand'] = X - Y
    
        
    return giver_level, taker_level, flavor



def pfi_fill():                 #helping function to fill all sized que
    global sized_que1
    global sized_que2
    global sized_que3
    global sized_que4
    global sized_que5
    
    global Y
    global color_wise_demand
    global pfi_cap
    global pi_cap
    
    
    if len(sized_que1) > 0:
        for i in range(len(sized_que1)):    
            bin_cap = min(pfi_cap, pi_cap)
            giver_level = Y.loc[0, 'Level']
            
            temp = color_wise_demand[(color_wise_demand['Size'] == 'S1') & (color_wise_demand['Demand'] > 0)].reset_index(drop = True)
            if len(temp) > 0:
            
                Y.loc[0, 'Level'], sized_que1.loc[i,'Level'], sized_que1.loc[i,'Flavor'] = fill(giver_level = giver_level, taker_cap= bin_cap, size = 'S1')
                sized_que1.loc[i,'Color'] = Y.loc[0, 'Color']
            else:
                Y.loc[0, 'Level'], sized_que1.loc[i,'Level'], sized_que1.loc[i,'Flavor'] = excess_fill(giver_level = giver_level, taker_cap= bin_cap, size = 'S1')
                sized_que1.loc[i,'Color'] = Y.loc[0, 'Color']
    
    if len(sized_que2) > 0:
        for i in range(len(sized_que2)):    
            bin_cap = min(pfi_cap, pi_cap)
            giver_level = Y.loc[1, 'Level']
            
            temp = color_wise_demand[(color_wise_demand['Size'] == 'S2') & (color_wise_demand['Demand'] > 0)].reset_index(drop = True)
            if len(temp) > 0:
            
                Y.loc[1, 'Level'], sized_que2.loc[i,'Level'], sized_que2.loc[i,'Flavor'] = fill(giver_level = giver_level, taker_cap= bin_cap, size = 'S2')
                sized_que2.loc[i,'Color'] = Y.loc[1, 'Color']
                
            else:
                Y.loc[1, 'Level'], sized_que2.loc[i,'Level'], sized_que2.loc[i,'Flavor'] = excess_fill(giver_level = giver_level, taker_cap= bin_cap, size = 'S2')
                sized_que2.loc[i,'Color'] = Y.loc[1, 'Color']
    
    if len(sized_que3) > 0:    
        for i in range(len(sized_que3)):    
            bin_cap = min(pfi_cap, pi_cap)
            giver_level = Y.loc[2, 'Level']
            temp = color_wise_demand[(color_wise_demand['Size'] == 'S3') & (color_wise_demand['Demand'] > 0)].reset_index(drop = True)
            if len(temp) > 0:
            
                Y.loc[2, 'Level'], sized_que3.loc[i,'Level'], sized_que3.loc[i,'Flavor'] = fill(giver_level = giver_level, taker_cap= bin_cap, size = 'S3')
                sized_que3.loc[i,'Color'] = Y.loc[2, 'Color']
            else:
                Y.loc[2, 'Level'], sized_que3.loc[i,'Level'], sized_que3.loc[i,'Flavor'] = excess_fill(giver_level = giver_level, taker_cap= bin_cap, size = 'S3')
                sized_que3.loc[i,'Color'] = Y.loc[2, 'Color']
                
    if len(sized_que4) > 0:    
        for i in range(len(sized_que4)):    
            bin_cap = min(pfi_cap, pi_cap)
            giver_level = Y.loc[3, 'Level']
            
            temp = color_wise_demand[(color_wise_demand['Size'] == 'S4') & (color_wise_demand['Demand'] > 0)].reset_index(drop = True)
            if len(temp) > 0:
            
                Y.loc[3, 'Level'], sized_que4.loc[i,'Level'], sized_que4.loc[i,'Flavor'] = fill(giver_level = giver_level, taker_cap= bin_cap, size = 'S4')
                sized_que4.loc[i,'Color'] = Y.loc[3, 'Color']
            else:
                Y.loc[3, 'Level'], sized_que4.loc[i,'Level'], sized_que4.loc[i,'Flavor'] = excess_fill(giver_level = giver_level, taker_cap= bin_cap, size = 'S4')
                sized_que4.loc[i,'Color'] = Y.loc[3, 'Color']
    if len(sized_que5) > 0:    
        for i in range(len(sized_que5)):    
            bin_cap = min(pfi_cap, pi_cap)
            giver_level = Y.loc[4, 'Level']
            temp = color_wise_demand[(color_wise_demand['Size'] == 'S5') & (color_wise_demand['Demand'] > 0)].reset_index(drop = True)
            if len(temp) > 0:
            
                Y.loc[4, 'Level'], sized_que5.loc[i,'Level'], sized_que5.loc[i,'Flavor'] = fill(giver_level = giver_level, taker_cap= bin_cap, size = 'S5')
                sized_que5.loc[i,'Color'] = Y.loc[4, 'Color']
            else:
                Y.loc[4, 'Level'], sized_que5.loc[i,'Level'], sized_que5.loc[i,'Flavor'] = excess_fill(giver_level = giver_level, taker_cap= bin_cap, size = 'S5')
                sized_que5.loc[i,'Color'] = Y.loc[4, 'Color']
                
        
def sized_que_2_tank_que():         #helping function to transfer to tank que
    global sized_que1
    global sized_que2
    global sized_que3
    global sized_que4
    global sized_que5
    global tank_que
    
    loop = True
    
    while loop == True:
               
        
        if len(sized_que1[sized_que1['Level'] > 0]) != 0:
            tank_que = tank_que.append(sized_que1.loc[0]).reset_index(drop = True)
            sized_que1 = sized_que1.drop(0).reset_index(drop = True)
        if len(sized_que2[sized_que2['Level'] > 0]) != 0:
            tank_que = tank_que.append(sized_que2.loc[0]).reset_index(drop = True)
            sized_que2= sized_que2.drop(0).reset_index(drop = True)
        if len(sized_que3[sized_que3['Level'] > 0]) != 0:
            tank_que = tank_que.append(sized_que3.loc[0]).reset_index(drop = True)
            sized_que3 = sized_que3.drop(0).reset_index(drop = True)
        if len(sized_que4[sized_que4['Level'] > 0]) != 0:
            tank_que = tank_que.append(sized_que4.loc[0]).reset_index(drop = True)
            sized_que4 = sized_que4.drop(0).reset_index(drop = True)
        if len(sized_que5[sized_que5['Level'] > 0]) != 0:
            tank_que = tank_que.append(sized_que5.loc[0]).reset_index(drop = True)
            sized_que5 = sized_que5.drop(0).reset_index(drop = True)
                
                
        if len(sized_que1[sized_que1['Level'] > 0]) + len(sized_que2[sized_que2['Level'] > 0]) +len(sized_que3[sized_que3['Level'] > 0]) +len(sized_que4[sized_que4['Level'] > 0]) +len(sized_que5[sized_que5['Level'] > 0]) == 0:
            loop = False
    #print(tank_que)
#pfi_fill()        
#sized_que_2_tank_que()              
def tank_que_2_sized_que(indx):
    global sized_que1
    global sized_que2
    global sized_que3
    global sized_que4
    global sized_que5
    global tank_que
    
    temp = pd.DataFrame(columns = ['Site','Drum', 'Capacity', 'Color' ,'Size' , 'Flavor', 'Level'])
    size = tank_que.loc[indx, 'Size']
     
    
    temp = temp.append(tank_que.loc[indx] ,ignore_index = True)
    #print(temp)
    temp['Color'], temp['Flavor'], temp['Level'] = 0 , 0 , 0
    #print(temp)
       
    if size == 'S1':
        
        sized_que1 = sized_que1.append(temp).sort_values(by=['Drum']).reset_index(drop = True)
    
    elif size == 'S2':
        
        sized_que2 = sized_que2.append(temp).sort_values(by=['Drum']).reset_index(drop = True)
    
    elif size == 'S3':
        
        sized_que3 = sized_que3.append(temp).sort_values(by=['Drum']).reset_index(drop = True)
    
    elif size == 'S4':
        
        sized_que4 = sized_que4.append(temp).sort_values(by=['Drum']).reset_index(drop = True)
    
    elif size == 'S5':
        
        sized_que5 = sized_que5.append(temp).sort_values(by=['Drum']).reset_index(drop = True)
    
    tank_que = tank_que.drop(indx).reset_index(drop = True)
    pfi_fill()
    sized_que_2_tank_que()    
    
def classifier():
    global color_of_rmi
    global level_of_rmi
    global Y
    global I1
    global I2
    global I3
    global tank1_mtl
    global tank_que
    global f1
    global f2
    global f3
    global FEL
    global time
    global flavors
    global num_of_PFO
    global tank2_mtl
    global tank3_mtl
    global final_demand
    global flavoring_rate
    global pack_rate
    global num_of_PFO
    global R
    global SPLIT_PERCENT
    
    split_percent = SPLIT_PERCENT
    sp = split_percent[split_percent['Color'] == color_of_rmi]
    sp = sp.sort_values(by = ['Size'])
    sp = list(sp['Percentage'] / 100)
    for i in range(5):
        Y.loc[i,'Level'] = sp[i] * level_of_rmi
        Y.loc[i,'Color'] = color_of_rmi
    
    if len(rmi) > 0:
        R = 0
    
    
    pfi_fill()
    sized_que_2_tank_que()
    
    if len(tank_que) > 0:
        #check if the tank I1 is busy or not
        if I1 == 0:
           '''<<<<<<<<<<<Trigger point 1 start here tank 1>>>>>>>>>'''
           if f1 in tank_que['Flavor'].values:
               first_indx = tank_que[tank_que['Flavor'] == f1].index.values[0]
               tank1_mtl =  tank_que.loc[first_indx]
               
               mean = flavoring_rate[(flavoring_rate['Size'] == tank1_mtl['Size']) & (flavoring_rate['Flavor'] == tank1_mtl['Flavor'])]['Mean'].values[0]
               std = flavoring_rate[(flavoring_rate['Size'] == tank1_mtl['Size']) & (flavoring_rate['Flavor'] == tank1_mtl['Flavor'])]['Std'].values[0]
               rate = random.normalvariate(mean, std)
               level = tank1_mtl['Level']
               
               tank_que_2_sized_que(first_indx)
               I1 =1           
               
               FEL_builder('Flavoring in tank1', level, rate)
           else:
               
               for i in range(len(tank_que)):
                   current_flavor = tank_que.iloc[i,5]
                   if current_flavor not in [f1,f2,f3]:
                       f1 = current_flavor
                       I1 = 1
                       
                       FEL_builder('Flavor Changing tank1')
                       #print(FEL)
                       break
                   
           '''<<<<<<<<<<<Trigger point 1 finish here tank 1>>>>>>>>>'''     
       
#'''<<<<<<<check machine 2 and machine 3 start from here >>>>>>>>>'''
           if num_of_PFO > 1:
                                     
               
               if I2 == 0:
                                                    
                   
                   '''<<<<<<<<<<<Trigger point 1 start here for tank 2 >>>>>>>>>'''
                   if f2 in tank_que['Flavor'].values:
                              
                       #print('third check')
                       first_indx = tank_que[tank_que['Flavor'] == f2].index.values[0]
                       tank2_mtl =  tank_que.loc[first_indx]
                       
                       mean = flavoring_rate[(flavoring_rate['Size'] == tank2_mtl['Size']) & (flavoring_rate['Flavor'] == tank2_mtl['Flavor'])]['Mean'].values[0]
                       std = flavoring_rate[(flavoring_rate['Size'] == tank2_mtl['Size']) & (flavoring_rate['Flavor'] == tank2_mtl['Flavor'])]['Std'].values[0]
                       rate = random.normalvariate(mean, std)
                       level = tank2_mtl['Level']
                       
                       tank_que_2_sized_que(first_indx)
                       I2 =1           
    
                       FEL_builder('Flavoring in tank2', level, rate)
                       
                   else:
                                               
                               
                       for i in range(len(tank_que)):
                                
                           current_flavor = tank_que.iloc[i,5]
                           if current_flavor not in [f1,f2,f3]:
                               f2 = current_flavor
                               I2 = 1
                                       
                               FEL_builder('Flavor Changing tank2')
                               
                               break
                        
                       '''<<<<<<<<<<<Trigger point 1 finish here for tank 2>>>>>>>>>'''
           if num_of_PFO > 2:
               
               if I3 == 0:
                   
                   
                   '''<<<<<<<<<<<Trigger point 1 start here for tank 3>>>>>>>>>'''
                   
                   if f3 in tank_que['Flavor'].values:
                       
                       first_indx = tank_que[tank_que['Flavor'] == f3].index.values[0]
                       tank3_mtl =  tank_que.loc[first_indx]
                       
                       mean = flavoring_rate[(flavoring_rate['Size'] == tank3_mtl['Size']) & (flavoring_rate['Flavor'] == tank3_mtl['Flavor'])]['Mean'].values[0]
                       std = flavoring_rate[(flavoring_rate['Size'] == tank3_mtl['Size']) & (flavoring_rate['Flavor'] == tank3_mtl['Flavor'])]['Std'].values[0]
                       rate = random.normalvariate(mean, std)
                       level = tank3_mtl['Level']
                       
                       tank_que_2_sized_que(first_indx)
                       I3 =1           

                       FEL_builder('Flavoring in tank3', level, rate)
                
                   else:
                        
                       for i in range(len(tank_que)):
                           current_flavor = tank_que.iloc[i,5]
                           if current_flavor not in [f1,f2,f3]:
                               f3 = current_flavor
                               I3 = 1
                               
                               FEL_builder('Flavor Changing tank3')
                               
                               break
    
                       '''<<<<<<<<<<<Trigger point 1 finish here for tank 3>>>>>>>>>'''
           

'''finish flavoring start here '''

def fill_pi(tank):     
    
    global production
    global tank1_mtl
    global tank2_mtl
    global tank3_mtl
    
    global box_que
    global final_demand  
    global empty_pi_que
    
    global I1
    global I2
    global I3
    #call one by one all the pi and fill it.
    
    if len(empty_pi_que) > 0:
            
        if tank == 1 and len(tank1_mtl) > 0 and I1 == 1:
                               
            temp = empty_pi_que.iloc[:1]
            temp['Level'] = tank1_mtl['Level']
            temp['Color'] = tank1_mtl['Color']
            temp['Size'] = tank1_mtl['Size']
            temp['Flavor'] = tank1_mtl['Flavor']
            box_que = box_que.append(temp).reset_index(drop = True)
            
            tank1_mtl = tank1_mtl.iloc[:0]
            I1 = 0
            empty_pi_que = empty_pi_que.iloc[1:].reset_index(drop = True)
            empty_pi_que = empty_pi_que.sort_values(by=['Drum']).reset_index(drop = True)
        
        elif tank == 2 and len(tank2_mtl) > 0 and I2 == 1:
                     
            temp = empty_pi_que.iloc[:1]
            temp['Level'] = tank2_mtl['Level']
            temp['Color'] = tank2_mtl['Color']
            temp['Size'] = tank2_mtl['Size']
            temp['Flavor'] = tank2_mtl['Flavor']
            box_que = box_que.append(temp).reset_index(drop = True)
                      
            tank2_mtl = tank2_mtl.iloc[:0]
            I2 = 0
            empty_pi_que = empty_pi_que.iloc[1:].reset_index(drop = True)
            empty_pi_que = empty_pi_que.sort_values(by=['Drum']).reset_index(drop = True)
        
        elif tank == 3 and len(tank3_mtl) > 0 and I3 == 1:
                       
            temp = empty_pi_que.iloc[:1]
            temp['Level'] = tank3_mtl['Level']
            temp['Color'] = tank3_mtl['Color']
            temp['Size'] = tank3_mtl['Size']
            temp['Flavor'] = tank3_mtl['Flavor']
            box_que = box_que.append(temp).reset_index(drop = True)
                       
            tank3_mtl = tank3_mtl.iloc[:0]
            I3 = 0
            empty_pi_que = empty_pi_que.iloc[1:].reset_index(drop = True)
            empty_pi_que = empty_pi_que.sort_values(by=['Drum']).reset_index(drop = True)
                     

def finish_flavoring_tank1():
    global tank1_mtl
    global box_que
    global bag_que
    
    global f1
    global tank_que
    global sized_que1
    global sized_que2
    global sized_que3
    global sized_que4
    global sized_que5
    
    global L
    global FEL
    global I1
    
    global box1
    global bag2
    global bag1
    global num_of_bag
    
    global final_demand
    global production1
    global production2
    global empty_pi_que
    global time
    global num_of_PFO
    global num_of_bag
    global R
    
    
    #fill the pi all of them whatever the material
    fill_pi(tank = 1)
    
    if Y['Level'].sum() < 1:
        L = 0
    else:
        pfi_fill()
        sized_que_2_tank_que()
    
    if L == 0 and R == 0:    
        if len(sized_que1) * len(sized_que2) *len(sized_que3) *len(sized_que4) *len(sized_que5) > 0:
            if len(rmi) > 0:
                R = 1
                FEL_builder('Releasing Drum')
        
          
    
    
    if len(tank1_mtl) < 1:
        I1 = 0
    else:
        I1 = 1
        
    if I1 == 0:
        #trigger 1 start
        if len(tank_que) > 0:
            if f1 in tank_que['Flavor'].values:
                
                first_indx = tank_que[tank_que['Flavor'] == f1].index.values[0]
                tank1_mtl =  tank_que.loc[first_indx]
                mean = flavoring_rate[(flavoring_rate['Size'] == tank1_mtl['Size']) & (flavoring_rate['Flavor'] == tank1_mtl['Flavor'])]['Mean'].values[0]
                std = flavoring_rate[(flavoring_rate['Size'] == tank1_mtl['Size']) & (flavoring_rate['Flavor'] == tank1_mtl['Flavor'])]['Std'].values[0]
                rate = random.normalvariate(mean, std)
                level = tank1_mtl['Level']
               
                tank_que_2_sized_que(first_indx)
                I1 =1           
               
                FEL_builder('Flavoring in tank1', level, rate)
            else:
                for i in range(len(tank_que)):
                    
                    
                    current_flavor = tank_que.iloc[i,5]
                    if current_flavor not in [f1,f2,f3]:
                        
                        f1 = current_flavor
                        I1 = 1
                       
                        FEL_builder('Flavor Changing tank1')
                        
                        break    
            #trigger 1 stop
        
    
    
    
    if box1 == 0:
        '''<<<<<<<<<<<trigger point 3 start here>>>>>>>>>>>>>'''
        #checks first whether anyone waiting in box que
        if len(box_que) > 0:
            #if it is true then it calls that and take the amount that is required
            #to fulfill the demand of boxing
            if len(final_demand[(final_demand['Color'] == box_que.iloc[0,3]) & (final_demand['Size'] == box_que.iloc[0,4]) & (final_demand['Flavor'] == box_que.iloc[0,5]) & (final_demand['Pack'] == 'Box') & (final_demand['Demand'] > 0)]) > 0: 
                amount_needed = final_demand[(final_demand['Color'] == box_que.iloc[0,3]) & (final_demand['Size'] == box_que.iloc[0,4]) & (final_demand['Flavor'] == box_que.iloc[0,5]) & (final_demand['Pack'] == 'Box')]['Demand'].values[0] 
            
                #take the amount
                full_amount = box_que.iloc[0,6]
                
                if amount_needed > full_amount:
                    amount_needed = full_amount
                
                
                box_que.iloc[0,6] = amount_needed
                #update the production table
                production1 = production1.append(box_que.iloc[0,:]).reset_index(drop = True)
                #update the amount now
                box_que.iloc[0,6] = full_amount - amount_needed
    
                
                box1 = 1
                #finish_boxinf FEL builder
                level = amount_needed
                mean = pack_rate[(pack_rate['Size'] == box_que.iloc[0,4]) & (pack_rate['Packaging'] == 'Box')]['Mean'].values[0]
                std = pack_rate[(pack_rate['Size'] == box_que.iloc[0,4]) & (pack_rate['Packaging'] == 'Box')]['Std'].values[0]
                rate = random.normalvariate(mean, std)
                FEL_builder('Boxing', level, rate)
            else:
                #append it to the bag que
                bag_que = bag_que.append(box_que.iloc[:1]).reset_index(drop = True)
                #delete from box_que
                box_que = box_que.iloc[1:].reset_index(drop = True)
        '''<<<<<<<<<<<trigger point 3 stop here>>>>>>>>>>>>>'''    
    else:
        pass
    
    if bag1 == 0:
        '''<<<<<<<<trigger point 4 start here for bagging machine 1>>>>>>>>>'''
        if len(bag_que) > 0:
            #if it is true then it calls that and take the amount that is required
            #to fulfill the demand of bagging
            bag1 = 1
            level = bag_que.iloc[0,6]
            size = bag_que.iloc[0,4]
                                
            #update the production table
            production2 = production2.append(bag_que.iloc[:1]).reset_index(drop = True)
            #update the amount now
            bag_que.iloc[0,6] = 0
            
            
            
    
            #finish_boxinf FEL builder
            bag1 = 1
            mean = pack_rate[(pack_rate['Size'] == size) & (pack_rate['Packaging'] == 'Bag')]['Mean'].values[0]
            std = pack_rate[(pack_rate['Size'] == size) & (pack_rate['Packaging'] == 'Bag')]['Std'].values[0]
            rate = random.normalvariate(mean, std)
            FEL_builder('Bagging in mc1', level, rate)
            
        '''<<<<<<<<trigger point 4 stop here for bagging machine 1>>>>>>>>>'''
    else:
        pass
    
    
    if num_of_bag >1:
        if bag2 == 0:
            '''<<<<<<<<trigger point 4 start here but for bagging machine number 2>>>>>>>>>'''
            if len(bag_que) > 0:
                #if it is true then it calls that and take the amount that is required
                #to fulfill the demand of bagging
                bag2 = 1 
                level = bag_que.iloc[0,6]
                size = bag_que.iloc[0,4]
                    
                #update the production table
                production2 = production2.append(bag_que.iloc[:1]).reset_index(drop = True)
                #update the amount now
                bag_que.iloc[0,6] = 0
                
                
                
                
                #finish_boxinf FEL builder
                mean = pack_rate[(pack_rate['Size'] == size) & (pack_rate['Packaging'] == 'Bag')]['Mean'].values[0]
                std = pack_rate[(pack_rate['Size'] == size) & (pack_rate['Packaging'] == 'Bag')]['Std'].values[0]
                rate = random.normalvariate(mean, std)
                FEL_builder('Bagging in mc2', level, rate)
                
                '''<<<<<<<<trigger point 4 stop here but for bagging machine number 2>>>>>>>>>'''
        else:
            pass
    else:
        pass

def finish_flavoring_tank2():
    global tank2_mtl
    global box_que
    global bag_que
    
    global f2
    global tank_que
    global sized_que1
    global sized_que2
    global sized_que3
    global sized_que4
    global sized_que5
    
    global L
    global FEL
    global I2
    
    global box1
    global bag2
    global bag1
    global num_of_bag
    
    global final_demand
    global production1
    global production2
    global empty_pi_que
    global time
    global num_of_PFO
    global num_of_bag
    global R
    
    #fill the pi all of them whatever the material
    fill_pi(tank = 2)
    
    if Y['Level'].sum() < 1:
        L = 0
    else:
        pfi_fill()
        sized_que_2_tank_que()
    
    if L == 0 and R == 0:    
        if len(sized_que1) * len(sized_que2) *len(sized_que3) *len(sized_que4) *len(sized_que5) > 0:
            if len(rmi) > 1:
                R = 1
                FEL_builder('Releasing Drum')
    else:
        pfi_fill()
        sized_que_2_tank_que()
      
    if len(tank2_mtl) == 0:
        I2 = 0
    else:
        I2 = 1   
    
    if I2 == 0:
        if len(tank_que) > 0:
            #trigger 1 start
            if f2 in tank_que['Flavor'].values:
                
                first_indx = tank_que[tank_que['Flavor'] == f2].index.values[0]
                tank2_mtl =  tank_que.loc[first_indx]
                mean = flavoring_rate[(flavoring_rate['Size'] == tank2_mtl['Size']) & (flavoring_rate['Flavor'] == tank2_mtl['Flavor'])]['Mean'].values[0]
                std = flavoring_rate[(flavoring_rate['Size'] == tank2_mtl['Size']) & (flavoring_rate['Flavor'] == tank2_mtl['Flavor'])]['Std'].values[0]
                rate = random.normalvariate(mean, std)
                level = tank2_mtl['Level']
               
                tank_que_2_sized_que(first_indx)
                I2 =1           
    
                FEL_builder('Flavoring in tank2', level, rate)
           
            else:
                for i in range(len(tank_que)):
                    
                    
                    current_flavor = tank_que.iloc[i,5]
                    if current_flavor not in [f1,f2,f3]:
                        
                        f2 = current_flavor
                        I2 = 1
                       
                        FEL_builder('Flavor Changing tank2')
                        
                        break    
            #trigger 1 stop
       
    
    if box1 == 0:
        '''<<<<<<<<<<<trigger point 3 start here>>>>>>>>>>>>>'''
        #checks first whether anyone waiting in box que
        if len(box_que) > 0:
            #if it is true then it calls that and take the amount that is required
            #to fulfill the demand of boxing
            if len(final_demand[(final_demand['Color'] == box_que.iloc[0,3]) & (final_demand['Size'] == box_que.iloc[0,4]) & (final_demand['Flavor'] == box_que.iloc[0,5]) & (final_demand['Pack'] == 'Box') & (final_demand['Demand'] > 0)]) > 0: 
                amount_needed = final_demand[(final_demand['Color'] == box_que.iloc[0,3]) & (final_demand['Size'] == box_que.iloc[0,4]) & (final_demand['Flavor'] == box_que.iloc[0,5]) & (final_demand['Pack'] == 'Box')]['Demand'].values[0] 
                
                #take the amount
                full_amount = box_que.iloc[0,6]
                
                if amount_needed > full_amount:
                    amount_needed = full_amount
                                
                box_que.iloc[0,6] = amount_needed
                #update the production table
                production1 = production1.append(box_que.iloc[0,:]).reset_index(drop = True)
                #update the amount now
                box_que.iloc[0,6] = full_amount - amount_needed
    
                
                box1 = 1
                #finish_boxinf FEL builder
                level = amount_needed
                mean = pack_rate[(pack_rate['Size'] == box_que.iloc[0,4]) & (pack_rate['Packaging'] == 'Box')]['Mean'].values[0]
                std = pack_rate[(pack_rate['Size'] == box_que.iloc[0,4]) & (pack_rate['Packaging'] == 'Box')]['Std'].values[0]
                rate = random.normalvariate(mean, std)
                FEL_builder('Boxing', level, rate)
            else:
                #append it to the bag que
                bag_que = bag_que.append(box_que.iloc[:1]).reset_index(drop = True)
                #delete from box_que
                box_que = box_que.iloc[1:].reset_index(drop = True)
            
            '''<<<<<<<<<<<trigger point 3 stop here>>>>>>>>>>>>>'''    
    else:
        pass
    
    if bag1 == 0:
        '''<<<<<<<<trigger point 4 start here for bagging machine 1>>>>>>>>>'''
        if len(bag_que) > 0:
            #if it is true then it calls that and take the amount that is required
            #to fulfill the demand of bagging
            bag1 = 1
            level = bag_que.iloc[0,6]
            size = bag_que.iloc[0,4]                    
            #update the production table
            production2 = production2.append(bag_que.iloc[:1]).reset_index(drop = True)
            #update the amount now
            bag_que.iloc[0,6] = 0
            
            
            
    
            #finish_boxinf FEL builder
            mean = pack_rate[(pack_rate['Size'] == size) & (pack_rate['Packaging'] == 'Bag')]['Mean'].values[0]
            std = pack_rate[(pack_rate['Size'] == size) & (pack_rate['Packaging'] == 'Bag')]['Std'].values[0]
            rate = random.normalvariate(mean, std)
            FEL_builder('Bagging in mc1', level, rate)
        '''<<<<<<<<trigger point 4 stop here for bagging machine 1>>>>>>>>>'''
    else:
        pass
    
    
    if num_of_bag >1:
        if bag2 == 0:
            '''<<<<<<<<trigger point 4 start here but for bagging machine number 2>>>>>>>>>'''
            if len(bag_que) > 0:
                #if it is true then it calls that and take the amount that is required
                #to fulfill the demand of bagging
                bag2 = 1 
                level = bag_que.iloc[0,6]
                size =  bag_que.iloc[0,4]                    
                #update the production table
                production2 = production2.append(bag_que.iloc[:1]).reset_index(drop = True)
                #update the amount now
                bag_que.iloc[0,6] = 0
                
                
                
                
                #finish_boxinf FEL builder
                mean = pack_rate[(pack_rate['Size'] == size) & (pack_rate['Packaging'] == 'Bag')]['Mean'].values[0]
                std = pack_rate[(pack_rate['Size'] == size) & (pack_rate['Packaging'] == 'Bag')]['Std'].values[0]
                rate = random.normalvariate(mean, std)
                FEL_builder('Bagging in mc2', level, rate)
                
                '''<<<<<<<<trigger point 4 stop here but for bagging machine number 2>>>>>>>>>'''
        else:
            pass
    else:
        pass
    
def finish_flavoring_tank3():
    global tank3_mtl
    global box_que
    global bag_que
    
    global f3
    global tank_que
    global sized_que1
    global sized_que2
    global sized_que3
    global sized_que4
    global sized_que5
    
    global L
    global FEL
    global I3
    
    global box1
    global bag2
    global bag1
    global num_of_bag
    
    global final_demand
    global production1
    global production2
    global empty_pi_que
    global time
    global num_of_PFO
    global num_of_bag
    global R
    
    
    
    #fill the pi all of them whatever the material
    fill_pi(tank = 3)
    
    if Y['Level'].sum() < 1:
        L = 0
    else:
        pfi_fill()
        sized_que_2_tank_que()
    
    if L == 0 and R == 0:    
        if len(sized_que1) * len(sized_que2) *len(sized_que3) *len(sized_que4) *len(sized_que5) > 0:
            if len(rmi) > 0:
                R = 1
                FEL_builder('Releasing Drum')
    
    
    
    
    if len(tank3_mtl) == 0:
        I3 = 0
    else:
        I3 = 1
    
    
    
    if I3 == 0:
        if len(tank_que) > 0:
            #trigger 1 start
            if f3 in tank_que['Flavor'].values:
                
                first_indx = tank_que[tank_que['Flavor'] == f3].index.values[0]
                tank3_mtl =  tank_que.loc[first_indx]
                mean = flavoring_rate[(flavoring_rate['Size'] == tank3_mtl['Size']) & (flavoring_rate['Flavor'] == tank3_mtl['Flavor'])]['Mean'].values[0]
                std = flavoring_rate[(flavoring_rate['Size'] == tank3_mtl['Size']) & (flavoring_rate['Flavor'] == tank3_mtl['Flavor'])]['Std'].values[0]
                rate = random.normalvariate(mean, std)
                level = tank3_mtl['Level']
               
                tank_que_2_sized_que(first_indx)
                I3 =1           
    
                FEL_builder('Flavoring in tank3', level, rate)
           
            else:
                for i in range(len(tank_que)):
                    
                    
                    current_flavor = tank_que.iloc[i,5]
                    if current_flavor not in [f1,f2,f3]:
                        
                        f3 = current_flavor
                        I3 = 1
                       
                        FEL_builder('Flavor Changing tank3')
                        break    
            #trigger 1 stop
    

    if box1 == 0:
        '''<<<<<<<<<<<trigger point 3 start here>>>>>>>>>>>>>'''
        #checks first whether anyone waiting in box que
        if len(box_que) > 0:
            #if it is true then it calls that and take the amount that is required
            #to fulfill the demand of boxing
            if len(final_demand[(final_demand['Color'] == box_que.iloc[0,3]) & (final_demand['Size'] == box_que.iloc[0,4]) & (final_demand['Flavor'] == box_que.iloc[0,5]) & (final_demand['Pack'] == 'Box') & (final_demand['Demand'] > 0)]) > 0: 
                amount_needed = final_demand[(final_demand['Color'] == box_que.iloc[0,3]) & (final_demand['Size'] == box_que.iloc[0,4]) & (final_demand['Flavor'] == box_que.iloc[0,5]) & (final_demand['Pack'] == 'Box')]['Demand'].values[0] 
            
                #take the amount
                full_amount = box_que.iloc[0,6]
                
                if amount_needed > full_amount:
                    amount_needed = full_amount
                
                box_que.iloc[0,6] = amount_needed
                #update the production table
                production1 = production1.append(box_que.iloc[0,:]).reset_index(drop = True)
                #update the amount now
                box_que.iloc[0,6] = full_amount - amount_needed
    
                
                box1 = 1
                #finish_boxinf FEL builder
                level = amount_needed
                mean = pack_rate[(pack_rate['Size'] == box_que.iloc[0,4]) & (pack_rate['Packaging'] == 'Box')]['Mean'].values[0]
                std = pack_rate[(pack_rate['Size'] == box_que.iloc[0,4]) & (pack_rate['Packaging'] == 'Box')]['Std'].values[0]
                rate = random.normalvariate(mean, std)
                FEL_builder('Boxing', level, rate)
            else:
                #append it to the bag que
                bag_que = bag_que.append(box_que.iloc[:1]).reset_index(drop = True)
                #delete from box_que
                box_que = box_que.iloc[1:].reset_index(drop = True)
            
            '''<<<<<<<<<<<trigger point 3 stop here>>>>>>>>>>>>>'''    
    else:
        pass
    
    if bag1 == 0:
        '''<<<<<<<<trigger point 4 start here for bagging machine 1>>>>>>>>>'''
        if len(bag_que) > 0:
            #if it is true then it calls that and take the amount that is required
            #to fulfill the demand of bagging
     
            level = bag_que.iloc[0,6]
            size = bag_que.iloc[0,4]
            bag1 = 1                   
            #update the production table
            production2 = production2.append(bag_que.iloc[:1]).reset_index(drop = True)
            #update the amount now
            bag_que.iloc[0,6] = 0
            
            
            
    
            #finish_boxinf FEL builder
            mean = pack_rate[(pack_rate['Size'] == size) & (pack_rate['Packaging'] == 'Bag')]['Mean'].values[0]
            std = pack_rate[(pack_rate['Size'] == size) & (pack_rate['Packaging'] == 'Bag')]['Std'].values[0]
            rate = random.normalvariate(mean, std)
            FEL_builder('Bagging in mc1', level, rate)
        '''<<<<<<<<trigger point 4 stop here for bagging machine 1>>>>>>>>>'''
    else:
        pass
    
    
    if num_of_bag >1:
        if bag2 == 0:
            '''<<<<<<<<trigger point 4 start here but for bagging machine number 2>>>>>>>>>'''
            if len(bag_que) > 0:
                #if it is true then it calls that and take the amount that is required
                #to fulfill the demand of bagging
                 
                level = bag_que.iloc[0,6]
                size = bag_que.iloc[0,4]
                bag2 = 1                    
                #update the production table
                production2 = production2.append(bag_que.iloc[:1]).reset_index(drop = True)
                #update the amount now
                bag_que.iloc[0,6] = 0
                
                
                
                
                #finish_boxinf FEL builder
                mean = pack_rate[(pack_rate['Size'] == size) & (pack_rate['Packaging'] == 'Bag')]['Mean'].values[0]
                std = pack_rate[(pack_rate['Size'] == size) & (pack_rate['Packaging'] == 'Bag')]['Std'].values[0]
                rate = random.normalvariate(mean, std)
                FEL_builder('Bagging in mc2', level, rate)
                
                '''<<<<<<<<trigger point 4 stop here but for bagging machine number 2>>>>>>>>>'''
        else:
            pass
    else:
        pass

def finish_boxing():
    global box_que
    global bag_que
    global empty_pi_que
    global bag1
    global bag2
    global box1
    global production1
    global production2
    global FEL
    global time
    global I1
    global I2
    global I3
    global f1
    global f2
    global f3
    
    #make the machine free
    box1 = 0
    
    #check if the bin has any remaining material after boxing operation
    if len(box_que) > 0:
    
        if box_que.iloc[0,6] > 0:
            #append it to the bag que
            bag_que = bag_que.append(box_que.iloc[:1]).reset_index(drop = True)
            #delete from box_que
            box_que = box_que.iloc[1:].reset_index(drop = True)
        else:
            #send it to tank and 
            empty_pi_que = empty_pi_que.append(box_que.iloc[:1]).reset_index(drop = True)
            #delete from box_que
            box_que = box_que.iloc[1:].reset_index(drop = True)
          
    if len(box_que) > 0:
        
             
        #if it is true then it calls that and take the amount that is required
        #to fulfill the demand of boxing
        if len(final_demand[(final_demand['Color'] == box_que.iloc[0,3]) & (final_demand['Size'] == box_que.iloc[0,4]) & (final_demand['Flavor'] == box_que.iloc[0,5]) & (final_demand['Pack'] == 'Box') & (final_demand['Demand'] > 0)]) > 0: 
            amount_needed = final_demand[(final_demand['Color'] == box_que.iloc[0,3]) & (final_demand['Size'] == box_que.iloc[0,4]) & (final_demand['Flavor'] == box_que.iloc[0,5]) & (final_demand['Pack'] == 'Box')]['Demand'].values[0] 
        
            #take the amount
            full_amount = box_que.iloc[0,6]
            
            if amount_needed > full_amount:
                    amount_needed = full_amount
            
            box_que.iloc[0,6] = amount_needed
            #update the production table
            production1 = production1.append(box_que.iloc[0,:]).reset_index(drop = True)
            #update the amount now
            box_que.iloc[0,6] = full_amount - amount_needed

            
            box1 = 1
            #finish_boxinf FEL builder
            level = amount_needed
            mean = pack_rate[(pack_rate['Size'] == box_que.iloc[0,4]) & (pack_rate['Packaging'] == 'Box')]['Mean'].values[0]
            std = pack_rate[(pack_rate['Size'] == box_que.iloc[0,4]) & (pack_rate['Packaging'] == 'Box')]['Std'].values[0]
            rate = random.normalvariate(mean, std)
            FEL_builder('Boxing', level, rate)
        else:
            #append it to the bag que
            bag_que = bag_que.append(box_que.iloc[:1]).reset_index(drop = True)
            #delete from box_que
            box_que = box_que.iloc[1:].reset_index(drop = True)
        
    
    if bag1 == 0:
        '''<<<<<<<<trigger point 4 start here for bagging machine 1>>>>>>>>>'''
        if len(bag_que) > 0:
            #if it is true then it calls that and take the amount that is required
            #to fulfill the demand of bagging
     
            level = bag_que.iloc[0,6]
            size = bag_que.iloc[0,4]
            bag1 = 1                   
            #update the production table
            production2 = production2.append(bag_que.iloc[:1]).reset_index(drop = True)
            #update the amount now
            bag_que.iloc[0,6] = 0
            
            
            #finish_boxinf FEL builder
            mean = pack_rate[(pack_rate['Size'] == size) & (pack_rate['Packaging'] == 'Bag')]['Mean'].values[0]
            std = pack_rate[(pack_rate['Size'] == size) & (pack_rate['Packaging'] == 'Bag')]['Std'].values[0]
            rate = random.normalvariate(mean, std)
            FEL_builder('Bagging in mc1', level, rate)
        '''<<<<<<<<trigger point 4 stop here for bagging machine 1>>>>>>>>>'''
    else:
        pass
    
    
    if num_of_bag > 1:
        if bag2 == 0:
            '''<<<<<<<<trigger point 4 start here but for bagging machine number 2>>>>>>>>>'''
            if len(bag_que) > 0:
                #if it is true then it calls that and take the amount that is required
                #to fulfill the demand of bagging
                 
                level = bag_que.iloc[0,6]
                size = bag_que.iloc[0,4]
                bag2 = 1                    
                #update the production table
                production2 = production2.append(bag_que.iloc[:1]).reset_index(drop = True)
                #update the amount now
                bag_que.iloc[0,6] = 0
                
                
                #finish_boxinf FEL builder
                mean = pack_rate[(pack_rate['Size'] == size) & (pack_rate['Packaging'] == 'Bag')]['Mean'].values[0]
                std = pack_rate[(pack_rate['Size'] == size) & (pack_rate['Packaging'] == 'Bag')]['Std'].values[0]
                rate = random.normalvariate(mean, std)
                FEL_builder('Bagging in mc2', level, rate)
                
                '''<<<<<<<<trigger point 4 stop here but for bagging machine number 2>>>>>>>>>''' 
    
    if I1 == 0:
        #trigger 1 start
        if len(tank_que) > 0:
            if f1 in tank_que['Flavor'].values:
                
                first_indx = tank_que[tank_que['Flavor'] == f1].index.values[0]
                tank1_mtl =  tank_que.loc[first_indx]
                mean = flavoring_rate[(flavoring_rate['Size'] == tank1_mtl['Size']) & (flavoring_rate['Flavor'] == tank1_mtl['Flavor'])]['Mean'].values[0]
                std = flavoring_rate[(flavoring_rate['Size'] == tank1_mtl['Size']) & (flavoring_rate['Flavor'] == tank1_mtl['Flavor'])]['Std'].values[0]
                rate = random.normalvariate(mean, std)
                level = tank1_mtl['Level']
               
                tank_que_2_sized_que(first_indx)
                I1 =1           
               
                FEL_builder('Flavoring in tank1', level, rate)
            else:
                for i in range(len(tank_que)):
                    
                    
                    current_flavor = tank_que.iloc[i,5]
                    if current_flavor not in [f1,f2,f3]:
                        
                        f1 = current_flavor
                        I1 = 1
                       
                        FEL_builder('Flavor Changing tank1')
                        
                        break    
            #trigger 1 stop
    if I2 == 0:
        if len(tank_que) > 0:
            #trigger 1 start
            if f2 in tank_que['Flavor'].values:
                
                first_indx = tank_que[tank_que['Flavor'] == f2].index.values[0]
                tank2_mtl =  tank_que.loc[first_indx]
                mean = flavoring_rate[(flavoring_rate['Size'] == tank2_mtl['Size']) & (flavoring_rate['Flavor'] == tank2_mtl['Flavor'])]['Mean'].values[0]
                std = flavoring_rate[(flavoring_rate['Size'] == tank2_mtl['Size']) & (flavoring_rate['Flavor'] == tank2_mtl['Flavor'])]['Std'].values[0]
                rate = random.normalvariate(mean, std)
                level = tank2_mtl['Level']
               
                tank_que_2_sized_que(first_indx)
                I2 =1           
    
                FEL_builder('Flavoring in tank2', level, rate)
           
            else:
                for i in range(len(tank_que)):
                    
                    
                    current_flavor = tank_que.iloc[i,5]
                    if current_flavor not in [f1,f2,f3]:
                        
                        f2 = current_flavor
                        I2 = 1
                       
                        FEL_builder('Flavor Changing tank2')
                        
                        break    
            #trigger 1 stop
    if I3 == 0:
        if len(tank_que) > 0:
            #trigger 1 start
            if f3 in tank_que['Flavor'].values:
                
                first_indx = tank_que[tank_que['Flavor'] == f3].index.values[0]
                tank3_mtl =  tank_que.loc[first_indx]
                mean = flavoring_rate[(flavoring_rate['Size'] == tank3_mtl['Size']) & (flavoring_rate['Flavor'] == tank3_mtl['Flavor'])]['Mean'].values[0]
                std = flavoring_rate[(flavoring_rate['Size'] == tank3_mtl['Size']) & (flavoring_rate['Flavor'] == tank3_mtl['Flavor'])]['Std'].values[0]
                rate = random.normalvariate(mean, std)
                level = tank3_mtl['Level']
               
                tank_que_2_sized_que(first_indx)
                I3 =1           
    
                FEL_builder('Flavoring in tank3', level, rate)
           
            else:
                for i in range(len(tank_que)):
                    
                    
                    current_flavor = tank_que.iloc[i,5]
                    if current_flavor not in [f1,f2,f3]:
                        
                        f3 = current_flavor
                        I3 = 1
                       
                        FEL_builder('Flavor Changing tank3')
                        break    
        
    
def finish_bagging_m1():
    global box_que
    global bag_que
    global empty_pi_que
    global bag1
    global bag2
    global box1
    global production1
    global production2
    global FEL
    global time
    global I1
    global I2
    global I3
    global f1
    global f2
    global f3
    
    bag1 = 0
    
    #send it to tank
    empty_pi_que = empty_pi_que.append(bag_que.iloc[:1]).reset_index(drop = True)
    #delete from bag_que
    bag_que = bag_que.iloc[1:].reset_index(drop = True)
    
    if box1 == 0:
    
        if len(box_que) > 0:
            #if it is true then it calls that and take the amount that is required
            #to fulfill the demand of boxing
            if len(final_demand[(final_demand['Color'] == box_que.iloc[0,3]) & (final_demand['Size'] == box_que.iloc[0,4]) & (final_demand['Flavor'] == box_que.iloc[0,5]) & (final_demand['Pack'] == 'Box') & (final_demand['Demand'] > 0)]) > 0: 
                amount_needed = final_demand[(final_demand['Color'] == box_que.iloc[0,3]) & (final_demand['Size'] == box_que.iloc[0,4]) & (final_demand['Flavor'] == box_que.iloc[0,5]) & (final_demand['Pack'] == 'Box')]['Demand'].values[0] 
            
                #take the amount
                full_amount = box_que.iloc[0,6]
                
                if amount_needed > full_amount:
                    amount_needed = full_amount
                    
                box_que.iloc[0,6] = amount_needed
                #update the production table
                production1 = production1.append(box_que.iloc[0,:]).reset_index(drop = True)
                #update the amount now
                box_que.iloc[0,6] = full_amount - amount_needed
    
                
                box1 = 1
                #finish_boxinf FEL builder
                level = amount_needed
                mean = pack_rate[(pack_rate['Size'] == box_que.iloc[0,4]) & (pack_rate['Packaging'] == 'Box')]['Mean'].values[0]
                std = pack_rate[(pack_rate['Size'] == box_que.iloc[0,4]) & (pack_rate['Packaging'] == 'Box')]['Std'].values[0]
                rate = random.normalvariate(mean, std)
                FEL_builder('Boxing', level, rate)
            else:
                #append it to the bag que
                bag_que = bag_que.append(box_que.iloc[:1]).reset_index(drop = True)
                #delete from box_que
                box_que = box_que.iloc[1:].reset_index(drop = True)
        
    
    if bag1 == 0:
        '''<<<<<<<<trigger point 4 start here for bagging machine 1>>>>>>>>>'''
        if len(bag_que) > 0:
            #if it is true then it calls that and take the amount that is required
            #to fulfill the demand of bagging
     
            level = bag_que.iloc[0,6]
            size = bag_que.iloc[0,4]
            bag1 = 1                   
            #update the production table
            production2 = production2.append(bag_que.iloc[:1]).reset_index(drop = True)
            #update the amount now
            bag_que.iloc[0,6] = 0
            
            
            
    
            #finish_boxinf FEL builder
            mean = pack_rate[(pack_rate['Size'] == size) & (pack_rate['Packaging'] == 'Bag')]['Mean'].values[0]
            std = pack_rate[(pack_rate['Size'] == size) & (pack_rate['Packaging'] == 'Bag')]['Std'].values[0]
            rate = random.normalvariate(mean, std)
            FEL_builder('Bagging in mc1', level, rate)
        '''<<<<<<<<trigger point 4 stop here for bagging machine 1>>>>>>>>>'''
    else:
        pass
    
    
    if num_of_bag > 1:
        if bag2 == 0:
            '''<<<<<<<<trigger point 4 start here but for bagging machine number 2>>>>>>>>>'''
            if len(bag_que) > 0:
                #if it is true then it calls that and take the amount that is required
                #to fulfill the demand of bagging
                 
                level = bag_que.iloc[0,6]
                size = bag_que.iloc[0,4]
                bag2 = 1                    
                #update the production table
                production2 = production2.append(bag_que.iloc[:1]).reset_index(drop = True)
                #update the amount now
                bag_que.iloc[0,6] = 0
                
                
                #finish_boxinf FEL builder
                mean = pack_rate[(pack_rate['Size'] == size) & (pack_rate['Packaging'] == 'Bag')]['Mean'].values[0]
                std = pack_rate[(pack_rate['Size'] == size) & (pack_rate['Packaging'] == 'Bag')]['Std'].values[0]
                rate = random.normalvariate(mean, std)
                FEL_builder('Bagging in mc2', level, rate)
                
                '''<<<<<<<<trigger point 4 stop here but for bagging machine number 2>>>>>>>>>''' 
    
    if I1 == 0:
        #trigger 1 start
        if len(tank_que) > 0:
            if f1 in tank_que['Flavor'].values:
                
                first_indx = tank_que[tank_que['Flavor'] == f1].index.values[0]
                tank1_mtl =  tank_que.loc[first_indx]
                mean = flavoring_rate[(flavoring_rate['Size'] == tank1_mtl['Size']) & (flavoring_rate['Flavor'] == tank1_mtl['Flavor'])]['Mean'].values[0]
                std = flavoring_rate[(flavoring_rate['Size'] == tank1_mtl['Size']) & (flavoring_rate['Flavor'] == tank1_mtl['Flavor'])]['Std'].values[0]
                rate = random.normalvariate(mean, std)
                level = tank1_mtl['Level']
               
                tank_que_2_sized_que(first_indx)
                I1 =1           
               
                FEL_builder('Flavoring in tank1', level, rate)
            else:
                for i in range(len(tank_que)):
                    
                    
                    current_flavor = tank_que.iloc[i,5]
                    if current_flavor not in [f1,f2,f3]:
                        
                        f1 = current_flavor
                        I1 = 1
                       
                        FEL_builder('Flavor Changing tank1')
                        
                        break    
            #trigger 1 stop
    if I2 == 0:
        if len(tank_que) > 0:
            #trigger 1 start
            if f2 in tank_que['Flavor'].values:
                
                first_indx = tank_que[tank_que['Flavor'] == f2].index.values[0]
                tank2_mtl =  tank_que.loc[first_indx]
                mean = flavoring_rate[(flavoring_rate['Size'] == tank2_mtl['Size']) & (flavoring_rate['Flavor'] == tank2_mtl['Flavor'])]['Mean'].values[0]
                std = flavoring_rate[(flavoring_rate['Size'] == tank2_mtl['Size']) & (flavoring_rate['Flavor'] == tank2_mtl['Flavor'])]['Std'].values[0]
                rate = random.normalvariate(mean, std)
                level = tank2_mtl['Level']
               
                tank_que_2_sized_que(first_indx)
                I2 =1           
    
                FEL_builder('Flavoring in tank2', level, rate)
           
            else:
                for i in range(len(tank_que)):
                    
                    
                    current_flavor = tank_que.iloc[i,5]
                    if current_flavor not in [f1,f2,f3]:
                        
                        f2 = current_flavor
                        I2 = 1
                       
                        FEL_builder('Flavor Changing tank2')
                        
                        break    
            #trigger 1 stop
    if I3 == 0:
        if len(tank_que) > 0:
            #trigger 1 start
            if f3 in tank_que['Flavor'].values:
                
                first_indx = tank_que[tank_que['Flavor'] == f3].index.values[0]
                tank3_mtl =  tank_que.loc[first_indx]
                mean = flavoring_rate[(flavoring_rate['Size'] == tank3_mtl['Size']) & (flavoring_rate['Flavor'] == tank3_mtl['Flavor'])]['Mean'].values[0]
                std = flavoring_rate[(flavoring_rate['Size'] == tank3_mtl['Size']) & (flavoring_rate['Flavor'] == tank3_mtl['Flavor'])]['Std'].values[0]
                rate = random.normalvariate(mean, std)
                level = tank3_mtl['Level']
               
                tank_que_2_sized_que(first_indx)
                I3 =1           
    
                FEL_builder('Flavoring in tank3', level, rate)
           
            else:
                for i in range(len(tank_que)):
                    
                    
                    current_flavor = tank_que.iloc[i,5]
                    if current_flavor not in [f1,f2,f3]:
                        
                        f3 = current_flavor
                        I3 = 1
                       
                        FEL_builder('Flavor Changing tank3')
                        break 
                    


def finish_bagging_m2():
    global box_que
    global bag_que
    global empty_pi_que
    global bag1
    global bag2
    global box1
    global production1
    global production2
    global FEL
    global time
    global I1
    global I2
    global I3
    global f1
    global f2
    global f3
    
    bag2 = 0
    #send it to tank
    empty_pi_que = empty_pi_que.append(bag_que.iloc[:1]).reset_index(drop = True)
    #delete from bag_que
    bag_que = bag_que.iloc[1:].reset_index(drop = True)
  
    if box1 == 0:
    
        if len(box_que) > 0:
            #if it is true then it calls that and take the amount that is required
            #to fulfill the demand of boxing
            if len(final_demand[(final_demand['Color'] == box_que.iloc[0,3]) & (final_demand['Size'] == box_que.iloc[0,4]) & (final_demand['Flavor'] == box_que.iloc[0,5]) & (final_demand['Pack'] == 'Box') & (final_demand['Demand'] > 0)]) > 0: 
                amount_needed = final_demand[(final_demand['Color'] == box_que.iloc[0,3]) & (final_demand['Size'] == box_que.iloc[0,4]) & (final_demand['Flavor'] == box_que.iloc[0,5]) & (final_demand['Pack'] == 'Box')]['Demand'].values[0] 
            
                #take the amount
                full_amount = box_que.iloc[0,6]
                
                if amount_needed > full_amount:
                    amount_needed = full_amount
                
                box_que.iloc[0,6] = amount_needed
                #update the production table
                production1 = production1.append(box_que.iloc[0,:]).reset_index(drop = True)
                #update the amount now
                box_que.iloc[0,6] = full_amount - amount_needed
    
                
                box1 = 1
                #finish_boxinf FEL builder
                level = amount_needed
                mean = pack_rate[(pack_rate['Size'] == box_que.iloc[0,4]) & (pack_rate['Packaging'] == 'Box')]['Mean'].values[0]
                std = pack_rate[(pack_rate['Size'] == box_que.iloc[0,4]) & (pack_rate['Packaging'] == 'Box')]['Std'].values[0]
                rate = random.normalvariate(mean, std)
                FEL_builder('Boxing', level, rate)
            else:
                #append it to the bag que
                bag_que = bag_que.append(box_que.iloc[:1]).reset_index(drop = True)
                #delete from box_que
                box_que = box_que.iloc[1:].reset_index(drop = True)
        
    
    if bag1 == 0:
        '''<<<<<<<<trigger point 4 start here for bagging machine 1>>>>>>>>>'''
        if len(bag_que) > 0:
            #if it is true then it calls that and take the amount that is required
            #to fulfill the demand of bagging
     
            level = bag_que.iloc[0,6]
            size = bag_que.iloc[0,4]
            bag1 = 1                   
            #update the production table
            production2 = production2.append(bag_que.iloc[:1]).reset_index(drop = True)
            #update the amount now
            bag_que.iloc[0,6] = 0
            
            
            #finish_boxinf FEL builder
            mean = pack_rate[(pack_rate['Size'] == size) & (pack_rate['Packaging'] == 'Bag')]['Mean'].values[0]
            std = pack_rate[(pack_rate['Size'] == size) & (pack_rate['Packaging'] == 'Bag')]['Std'].values[0]
            rate = random.normalvariate(mean, std)
            FEL_builder('Bagging in mc1', level, rate)
        '''<<<<<<<<trigger point 4 stop here for bagging machine 1>>>>>>>>>'''
    else:
        pass
    
    
    if num_of_bag > 1:
        if bag2 == 0:
            '''<<<<<<<<trigger point 4 start here but for bagging machine number 2>>>>>>>>>'''
            if len(bag_que) > 0:
                #if it is true then it calls that and take the amount that is required
                #to fulfill the demand of bagging
                 
                level = bag_que.iloc[0,6]
                size = bag_que.iloc[0,4]
                bag2 = 1                    
                #update the production table
                production2 = production2.append(bag_que.iloc[:1]).reset_index(drop = True)
                #update the amount now
                bag_que.iloc[0,6] = 0
                
                
                
                #finish_boxinf FEL builder
                mean = pack_rate[(pack_rate['Size'] == size) & (pack_rate['Packaging'] == 'Bag')]['Mean'].values[0]
                std = pack_rate[(pack_rate['Size'] == size) & (pack_rate['Packaging'] == 'Bag')]['Std'].values[0]
                rate = random.normalvariate(mean, std)
                FEL_builder('Bagging in mc2', level, rate)
                
                '''<<<<<<<<trigger point 4 stop here but for bagging machine number 2>>>>>>>>>''' 
    
    if I1 == 0:
        #trigger 1 start
        if len(tank_que) > 0:
            if f1 in tank_que['Flavor'].values:
                
                first_indx = tank_que[tank_que['Flavor'] == f1].index.values[0]
                tank1_mtl =  tank_que.loc[first_indx]
                mean = flavoring_rate[(flavoring_rate['Size'] == tank1_mtl['Size']) & (flavoring_rate['Flavor'] == tank1_mtl['Flavor'])]['Mean'].values[0]
                std = flavoring_rate[(flavoring_rate['Size'] == tank1_mtl['Size']) & (flavoring_rate['Flavor'] == tank1_mtl['Flavor'])]['Std'].values[0]
                rate = random.normalvariate(mean, std)
                level = tank1_mtl['Level']
               
                tank_que_2_sized_que(first_indx)
                I1 =1           
               
                FEL_builder('Flavoring in tank1', level, rate)
            else:
                for i in range(len(tank_que)):
                    
                    
                    current_flavor = tank_que.iloc[i,5]
                    if current_flavor not in [f1,f2,f3]:
                        
                        f1 = current_flavor
                        I1 = 1
                       
                        FEL_builder('Flavor Changing tank1')
                        
                        break    
            #trigger 1 stop
    if I2 == 0:
        if len(tank_que) > 0:
            #trigger 1 start
            if f2 in tank_que['Flavor'].values:
                
                first_indx = tank_que[tank_que['Flavor'] == f2].index.values[0]
                tank2_mtl =  tank_que.loc[first_indx]
                mean = flavoring_rate[(flavoring_rate['Size'] == tank2_mtl['Size']) & (flavoring_rate['Flavor'] == tank2_mtl['Flavor'])]['Mean'].values[0]
                std = flavoring_rate[(flavoring_rate['Size'] == tank2_mtl['Size']) & (flavoring_rate['Flavor'] == tank2_mtl['Flavor'])]['Std'].values[0]
                rate = random.normalvariate(mean, std)
                level = tank2_mtl['Level']
               
                tank_que_2_sized_que(first_indx)
                I2 =1           
    
                FEL_builder('Flavoring in tank2', level, rate)
           
            else:
                for i in range(len(tank_que)):
                    
                    
                    current_flavor = tank_que.iloc[i,5]
                    if current_flavor not in [f1,f2,f3]:
                        
                        f2 = current_flavor
                        I2 = 1
                       
                        FEL_builder('Flavor Changing tank2')
                        
                        break    
            #trigger 1 stop
    if I3 == 0:
        if len(tank_que) > 0:
            #trigger 1 start
            if f3 in tank_que['Flavor'].values:
                
                first_indx = tank_que[tank_que['Flavor'] == f3].index.values[0]
                tank3_mtl =  tank_que.loc[first_indx]
                mean = flavoring_rate[(flavoring_rate['Size'] == tank3_mtl['Size']) & (flavoring_rate['Flavor'] == tank3_mtl['Flavor'])]['Mean'].values[0]
                std = flavoring_rate[(flavoring_rate['Size'] == tank3_mtl['Size']) & (flavoring_rate['Flavor'] == tank3_mtl['Flavor'])]['Std'].values[0]
                rate = random.normalvariate(mean, std)
                level = tank3_mtl['Level']
               
                tank_que_2_sized_que(first_indx)
                I3 =1           
    
                FEL_builder('Flavoring in tank3', level, rate)
           
            else:
                for i in range(len(tank_que)):
                    
                    
                    current_flavor = tank_que.iloc[i,5]
                    if current_flavor not in [f1,f2,f3]:
                        
                        f3 = current_flavor
                        I3 = 1
                       
                        FEL_builder('Flavor Changing tank3')
                        break 




def flavor_changed_tank1():
    global I1
    global I2
    global I3
    global tank_que
    global FEL
    
    global f1
    global f2
    global f3
    global tank1_mtl
    global time
    
    global bag1
    global bag2
    global box1
    global f1
    global f2
    global f3
    global tank1_mtl
    global tank2_mtl
    global box_que
    global bag_que
    global production1
    global production2
    global empty_pi_que
    
    I1 = 0
    if len(tank_que) > 0:
        '''<<<<<<trigger point 1 start here for tank 1>>>>>>>>'''
        
        if f1 in tank_que['Flavor'].values:
            first_indx = tank_que[tank_que['Flavor'] == f1].index.values[0]
            tank1_mtl =  tank_que.loc[first_indx]
           
            mean = flavoring_rate[(flavoring_rate['Size'] == tank1_mtl['Size']) & (flavoring_rate['Flavor'] == tank1_mtl['Flavor'])]['Mean'].values[0]
            std = flavoring_rate[(flavoring_rate['Size'] == tank1_mtl['Size']) & (flavoring_rate['Flavor'] == tank1_mtl['Flavor'])]['Std'].values[0]
            rate = random.normalvariate(mean, std)
            level = tank1_mtl['Level']
           
            tank_que_2_sized_que(first_indx)
            I1 =1           
           
            FEL_builder('Flavoring in tank1', level, rate)
           
        else:
           
            for i in range(len(tank_que)):
                current_flavor = tank_que.iloc[i,5]
                if current_flavor not in [f1,f2,f3]:
                    f1 = current_flavor
                    I1 = 1
                   
                    FEL_builder('Flavor Changing tank1')
                    break

            '''<<<<<<<<<<<Trigger point 1 stop here for tank 1>>>>>>>>>'''
    if box1 == 0:
    
        if len(box_que) > 0:
            #if it is true then it calls that and take the amount that is required
            #to fulfill the demand of boxing
            if len(final_demand[(final_demand['Color'] == box_que.iloc[0,3]) & (final_demand['Size'] == box_que.iloc[0,4]) & (final_demand['Flavor'] == box_que.iloc[0,5]) & (final_demand['Pack'] == 'Box') & (final_demand['Demand'] > 0)]) > 0: 
                amount_needed = final_demand[(final_demand['Color'] == box_que.iloc[0,3]) & (final_demand['Size'] == box_que.iloc[0,4]) & (final_demand['Flavor'] == box_que.iloc[0,5]) & (final_demand['Pack'] == 'Box')]['Demand'].values[0] 
            
                #take the amount
                full_amount = box_que.iloc[0,6]
                
                if amount_needed > full_amount:
                    amount_needed = full_amount
                
                
                box_que.iloc[0,6] = amount_needed
                #update the production table
                production1 = production1.append(box_que.iloc[0,:]).reset_index(drop = True)
                #update the amount now
                box_que.iloc[0,6] = full_amount - amount_needed
    
                
                box1 = 1
                #finish_boxinf FEL builder
                level = amount_needed
                mean = pack_rate[(pack_rate['Size'] == box_que.iloc[0,4]) & (pack_rate['Packaging'] == 'Box')]['Mean'].values[0]
                std = pack_rate[(pack_rate['Size'] == box_que.iloc[0,4]) & (pack_rate['Packaging'] == 'Box')]['Std'].values[0]
                rate = random.normalvariate(mean, std)
                FEL_builder('Boxing', level, rate)
            else:
                #append it to the bag que
                bag_que = bag_que.append(box_que.iloc[:1]).reset_index(drop = True)
                #delete from box_que
                box_que = box_que.iloc[1:].reset_index(drop = True)
        
    
    if bag1 == 0:
        '''<<<<<<<<trigger point 4 start here for bagging machine 1>>>>>>>>>'''
        if len(bag_que) > 0:
            #if it is true then it calls that and take the amount that is required
            #to fulfill the demand of bagging
     
            level = bag_que.iloc[0,6]
            size = bag_que.iloc[0,4]
            bag1 = 1                   
            #update the production table
            production2 = production2.append(bag_que.iloc[:1]).reset_index(drop = True)
            #update the amount now
            bag_que.iloc[0,6] = 0
            
           
    
            #finish_boxinf FEL builder
            mean = pack_rate[(pack_rate['Size'] == size) & (pack_rate['Packaging'] == 'Bag')]['Mean'].values[0]
            std = pack_rate[(pack_rate['Size'] == size) & (pack_rate['Packaging'] == 'Bag')]['Std'].values[0]
            rate = random.normalvariate(mean, std)
            FEL_builder('Bagging in mc1', level, rate)
        '''<<<<<<<<trigger point 4 stop here for bagging machine 1>>>>>>>>>'''
    else:
        pass
    
    
    if num_of_bag > 1:
        if bag2 == 0:
            '''<<<<<<<<trigger point 4 start here but for bagging machine number 2>>>>>>>>>'''
            if len(bag_que) > 0:
                #if it is true then it calls that and take the amount that is required
                #to fulfill the demand of bagging
                 
                level = bag_que.iloc[0,6]
                size = bag_que.iloc[0,4]
                bag2 = 1                    
                #update the production table
                production2 = production2.append(bag_que.iloc[:1]).reset_index(drop = True)
                #update the amount now
                bag_que.iloc[0,6] = 0
                
                
                
                #finish_boxinf FEL builder
                mean = pack_rate[(pack_rate['Size'] == size) & (pack_rate['Packaging'] == 'Bag')]['Mean'].values[0]
                std = pack_rate[(pack_rate['Size'] == size) & (pack_rate['Packaging'] == 'Bag')]['Std'].values[0]
                rate = random.normalvariate(mean, std)
                FEL_builder('Bagging in mc2', level, rate)
                
                '''<<<<<<<<trigger point 4 stop here but for bagging machine number 2>>>>>>>>>''' 
    

    if I2 == 0:
        if len(tank_que) > 0:
            #trigger 1 start
            if f2 in tank_que['Flavor'].values:
                
                first_indx = tank_que[tank_que['Flavor'] == f2].index.values[0]
                tank2_mtl =  tank_que.loc[first_indx]
                mean = flavoring_rate[(flavoring_rate['Size'] == tank2_mtl['Size']) & (flavoring_rate['Flavor'] == tank2_mtl['Flavor'])]['Mean'].values[0]
                std = flavoring_rate[(flavoring_rate['Size'] == tank2_mtl['Size']) & (flavoring_rate['Flavor'] == tank2_mtl['Flavor'])]['Std'].values[0]
                rate = random.normalvariate(mean, std)
                level = tank2_mtl['Level']
               
                tank_que_2_sized_que(first_indx)
                I2 =1           
    
                FEL_builder('Flavoring in tank2', level, rate)
           
            else:
                for i in range(len(tank_que)):
                    
                    
                    current_flavor = tank_que.iloc[i,5]
                    if current_flavor not in [f1,f2,f3]:
                        
                        f2 = current_flavor
                        I2 = 1
                       
                        FEL_builder('Flavor Changing tank2')
                        
                        break    
            #trigger 1 stop
    if I3 == 0:
        if len(tank_que) > 0:
            #trigger 1 start
            if f3 in tank_que['Flavor'].values:
                
                first_indx = tank_que[tank_que['Flavor'] == f3].index.values[0]
                tank3_mtl =  tank_que.loc[first_indx]
                mean = flavoring_rate[(flavoring_rate['Size'] == tank3_mtl['Size']) & (flavoring_rate['Flavor'] == tank3_mtl['Flavor'])]['Mean'].values[0]
                std = flavoring_rate[(flavoring_rate['Size'] == tank3_mtl['Size']) & (flavoring_rate['Flavor'] == tank3_mtl['Flavor'])]['Std'].values[0]
                rate = random.normalvariate(mean, std)
                level = tank3_mtl['Level']
               
                tank_que_2_sized_que(first_indx)
                I3 =1           
    
                FEL_builder('Flavoring in tank3', level, rate)
           
            else:
                for i in range(len(tank_que)):
                    
                    
                    current_flavor = tank_que.iloc[i,5]
                    if current_flavor not in [f1,f2,f3]:
                        
                        f3 = current_flavor
                        I3 = 1
                       
                        FEL_builder('Flavor Changing tank3')
                        break
       
def flavor_changed_tank2():
    global I1
    global I2
    global I3
    global tank_que
    global FEL
    
    global f1
    global f2
    global f3
    global tank2_mtl
    global time
    
    global bag1
    global bag2
    global box1
    global f1
    global f2
    global f3
    global tank1_mtl
    global tank2_mtl
    global box_que
    global bag_que
    global production1
    global production2
    global empty_pi_que
    
    I2 = 0
    if len(tank_que) > 0:
        '''<<<<<<trigger point 1 start here for tank 2>>>>>>>>'''
        if f2 in tank_que['Flavor'].values:
                      
                          
            #print('third check')
            first_indx = tank_que[tank_que['Flavor'] == f2].index.values[0]
            tank2_mtl =  tank_que.loc[first_indx]
            
            mean = flavoring_rate[(flavoring_rate['Size'] == tank2_mtl['Size']) & (flavoring_rate['Flavor'] == tank2_mtl['Flavor'])]['Mean'].values[0]
            std = flavoring_rate[(flavoring_rate['Size'] == tank2_mtl['Size']) & (flavoring_rate['Flavor'] == tank2_mtl['Flavor'])]['Std'].values[0]
            rate = random.normalvariate(mean, std)
            level = tank2_mtl['Level']
           
            tank_que_2_sized_que(first_indx)
            I2 =1           

            FEL_builder('Flavoring in tank2', level, rate)
        else:
                                   
                   
            for i in range(len(tank_que)):
                    
                current_flavor = tank_que.iloc[i,5]
                if current_flavor not in [f1,f2,f3]:
                    f2 = current_flavor
                    I2 = 1
                           
                    FEL_builder('Flavor Changing tank2')
                    break
      

        '''<<<<<<<<<<<Trigger point 1 stop here for tank 2>>>>>>>>>'''    
    if box1 == 0:

        if len(box_que) > 0:
            #if it is true then it calls that and take the amount that is required
            #to fulfill the demand of boxing
            if len(final_demand[(final_demand['Color'] == box_que.iloc[0,3]) & (final_demand['Size'] == box_que.iloc[0,4]) & (final_demand['Flavor'] == box_que.iloc[0,5]) & (final_demand['Pack'] == 'Box') & (final_demand['Demand'] > 0)]) > 0: 
                amount_needed = final_demand[(final_demand['Color'] == box_que.iloc[0,3]) & (final_demand['Size'] == box_que.iloc[0,4]) & (final_demand['Flavor'] == box_que.iloc[0,5]) & (final_demand['Pack'] == 'Box')]['Demand'].values[0] 
            
                #take the amount
                full_amount = box_que.iloc[0,6]
                
                if amount_needed > full_amount:
                    amount_needed = full_amount
                
                box_que.iloc[0,6] = amount_needed
                #update the production table
                production1 = production1.append(box_que.iloc[0,:]).reset_index(drop = True)
                #update the amount now
                box_que.iloc[0,6] = full_amount - amount_needed
    
                
                box1 = 1
                #finish_boxinf FEL builder
                level = amount_needed
                mean = pack_rate[(pack_rate['Size'] == box_que.iloc[0,4]) & (pack_rate['Packaging'] == 'Box')]['Mean'].values[0]
                std = pack_rate[(pack_rate['Size'] == box_que.iloc[0,4]) & (pack_rate['Packaging'] == 'Box')]['Std'].values[0]
                rate = random.normalvariate(mean, std)
                FEL_builder('Boxing', level, rate)
            else:
                #append it to the bag que
                bag_que = bag_que.append(box_que.iloc[:1]).reset_index(drop = True)
                #delete from box_que
                box_que = box_que.iloc[1:].reset_index(drop = True)
        
    
    if bag1 == 0:
        '''<<<<<<<<trigger point 4 start here for bagging machine 1>>>>>>>>>'''
        if len(bag_que) > 0:
            #if it is true then it calls that and take the amount that is required
            #to fulfill the demand of bagging
     
            level = bag_que.iloc[0,6]
            size = bag_que.iloc[0,4]
            bag1 = 1                   
            #update the production table
            production2 = production2.append(bag_que.iloc[:1]).reset_index(drop = True)
            #update the amount now
            bag_que.iloc[0,6] = 0
            
            
            
    
            #finish_boxinf FEL builder
            mean = pack_rate[(pack_rate['Size'] == size) & (pack_rate['Packaging'] == 'Bag')]['Mean'].values[0]
            std = pack_rate[(pack_rate['Size'] == size) & (pack_rate['Packaging'] == 'Bag')]['Std'].values[0]
            rate = random.normalvariate(mean, std)
            FEL_builder('Bagging in mc1', level, rate)
        '''<<<<<<<<trigger point 4 stop here for bagging machine 1>>>>>>>>>'''
    else:
        pass
    
    
    if num_of_bag > 1:
        if bag2 == 0:
            '''<<<<<<<<trigger point 4 start here but for bagging machine number 2>>>>>>>>>'''
            if len(bag_que) > 0:
                #if it is true then it calls that and take the amount that is required
                #to fulfill the demand of bagging
                 
                level = bag_que.iloc[0,6]
                size = bag_que.iloc[0,4]
                bag2 = 1                    
                #update the production table
                production2 = production2.append(bag_que.iloc[:1]).reset_index(drop = True)
                #update the amount now
                bag_que.iloc[0,6] = 0
                
                
                
                
                #finish_boxinf FEL builder
                mean = pack_rate[(pack_rate['Size'] == size) & (pack_rate['Packaging'] == 'Bag')]['Mean'].values[0]
                std = pack_rate[(pack_rate['Size'] == size) & (pack_rate['Packaging'] == 'Bag')]['Std'].values[0]
                rate = random.normalvariate(mean, std)
                FEL_builder('Bagging in mc2', level, rate)
                
                '''<<<<<<<<trigger point 4 stop here but for bagging machine number 2>>>>>>>>>''' 
    
    if I1 == 0:
        #trigger 1 start
        if len(tank_que) > 0:
            if f1 in tank_que['Flavor'].values:
                
                first_indx = tank_que[tank_que['Flavor'] == f1].index.values[0]
                tank1_mtl =  tank_que.loc[first_indx]
                mean = flavoring_rate[(flavoring_rate['Size'] == tank1_mtl['Size']) & (flavoring_rate['Flavor'] == tank1_mtl['Flavor'])]['Mean'].values[0]
                std = flavoring_rate[(flavoring_rate['Size'] == tank1_mtl['Size']) & (flavoring_rate['Flavor'] == tank1_mtl['Flavor'])]['Std'].values[0]
                rate = random.normalvariate(mean, std)
                level = tank1_mtl['Level']
               
                tank_que_2_sized_que(first_indx)
                I1 =1           
               
                FEL_builder('Flavoring in tank1', level, rate)
            else:
                for i in range(len(tank_que)):
                    
                    
                    current_flavor = tank_que.iloc[i,5]
                    if current_flavor not in [f1,f2,f3]:
                        
                        f1 = current_flavor
                        I1 = 1
                       
                        FEL_builder('Flavor Changing tank1')
                        
                        break    
            #trigger 1 stop

    if I3 == 0:
        if len(tank_que) > 0:
            #trigger 1 start
            if f3 in tank_que['Flavor'].values:
                
                first_indx = tank_que[tank_que['Flavor'] == f3].index.values[0]
                tank3_mtl =  tank_que.loc[first_indx]
                mean = flavoring_rate[(flavoring_rate['Size'] == tank3_mtl['Size']) & (flavoring_rate['Flavor'] == tank3_mtl['Flavor'])]['Mean'].values[0]
                std = flavoring_rate[(flavoring_rate['Size'] == tank3_mtl['Size']) & (flavoring_rate['Flavor'] == tank3_mtl['Flavor'])]['Std'].values[0]
                rate = random.normalvariate(mean, std)
                level = tank3_mtl['Level']
               
                tank_que_2_sized_que(first_indx)
                I3 =1           
    
                FEL_builder('Flavoring in tank3', level, rate)
           
            else:
                for i in range(len(tank_que)):
                    
                    
                    current_flavor = tank_que.iloc[i,5]
                    if current_flavor not in [f1,f2,f3]:
                        
                        f3 = current_flavor
                        I3 = 1
                       
                        FEL_builder('Flavor Changing tank3')
                        break
        
        
        
def flavor_changed_tank3():
    global I1
    global I2
    global I3
    global tank_que
    global FEL
    
    global f1
    global f2
    global f3
    global tank3_mtl
    global time
    
    global bag1
    global bag2
    global box1
    global f1
    global f2
    global f3
    global tank1_mtl
    global tank2_mtl
    global box_que
    global bag_que
    global production1
    global production2
    
    global empty_pi_que
    
    I3 = 0
    if len(tank_que) > 0:
        
        
        '''<<<<<<trigger point 1 start here for tank 3>>>>>>>>'''
        if f3 in tank_que['Flavor'].values:
            first_indx = tank_que[tank_que['Flavor'] == f3].index.values[0]
            tank3_mtl =  tank_que.loc[first_indx]            
               
            mean = flavoring_rate[(flavoring_rate['Size'] == tank3_mtl['Size']) & (flavoring_rate['Flavor'] == tank3_mtl['Flavor'])]['Mean'].values[0]
            std = flavoring_rate[(flavoring_rate['Size'] == tank3_mtl['Size']) & (flavoring_rate['Flavor'] == tank3_mtl['Flavor'])]['Std'].values[0]
            rate = random.normalvariate(mean, std)
            level = tank3_mtl['Level']
           
            tank_que_2_sized_que(first_indx)
            I3 =1           

            FEL_builder('Flavoring in tank3', level, rate)
        else:
                            
            for i in range(len(tank_que)):
                
                current_flavor = tank_que.iloc[i,5]
                
                if current_flavor not in [f1,f2,f3]:
                    
                    f3 = current_flavor
                    I3 = 1
                                   
                    FEL_builder('Flavor Changing tank3')
                    break
      

        '''<<<<<<<<<<<Trigger point 1 stop here for tank 3>>>>>>>>>'''
        
    if box1 == 0:

        if len(box_que) > 0:
            #if it is true then it calls that and take the amount that is required
            #to fulfill the demand of boxing
            if len(final_demand[(final_demand['Color'] == box_que.iloc[0,3]) & (final_demand['Size'] == box_que.iloc[0,4]) & (final_demand['Flavor'] == box_que.iloc[0,5]) & (final_demand['Pack'] == 'Box') & (final_demand['Demand'] > 0)]) > 0: 
                amount_needed = final_demand[(final_demand['Color'] == box_que.iloc[0,3]) & (final_demand['Size'] == box_que.iloc[0,4]) & (final_demand['Flavor'] == box_que.iloc[0,5]) & (final_demand['Pack'] == 'Box')]['Demand'].values[0] 
            
                #take the amount
                full_amount = box_que.iloc[0,6]
                
                if amount_needed > full_amount:
                    amount_needed = full_amount
                
                
                box_que.iloc[0,6] = amount_needed
                #update the production table
                production1 = production1.append(box_que.iloc[0,:]).reset_index(drop = True)
                #update the amount now
                box_que.iloc[0,6] = full_amount - amount_needed
    
                
                box1 = 1
                #finish_boxinf FEL builder
                level = amount_needed
                mean = pack_rate[(pack_rate['Size'] == box_que.iloc[0,4]) & (pack_rate['Packaging'] == 'Box')]['Mean'].values[0]
                std = pack_rate[(pack_rate['Size'] == box_que.iloc[0,4]) & (pack_rate['Packaging'] == 'Box')]['Std'].values[0]
                rate = random.normalvariate(mean, std)
                FEL_builder('Boxing', level, rate)
            else:
                #append it to the bag que
                bag_que = bag_que.append(box_que.iloc[:1]).reset_index(drop = True)
                #delete from box_que
                box_que = box_que.iloc[1:].reset_index(drop = True)
        
    
    if bag1 == 0:
        '''<<<<<<<<trigger point 4 start here for bagging machine 1>>>>>>>>>'''
        if len(bag_que) > 0:
            #if it is true then it calls that and take the amount that is required
            #to fulfill the demand of bagging
     
            level = bag_que.iloc[0,6]
            size = bag_que.iloc[0,4]
            bag1 = 1                   
            #update the production table
            production2 = production2.append(bag_que.iloc[:1]).reset_index(drop = True)
            #update the amount now
            bag_que.iloc[0,6] = 0
            
            
            
    
            #finish_boxinf FEL builder
            mean = pack_rate[(pack_rate['Size'] == size) & (pack_rate['Packaging'] == 'Bag')]['Mean'].values[0]
            std = pack_rate[(pack_rate['Size'] == size) & (pack_rate['Packaging'] == 'Bag')]['Std'].values[0]
            rate = random.normalvariate(mean, std)
            FEL_builder('Bagging in mc1', level, rate)
        '''<<<<<<<<trigger point 4 stop here for bagging machine 1>>>>>>>>>'''
    else:
        pass
    
    
    if num_of_bag > 1:
        if bag2 == 0:
            '''<<<<<<<<trigger point 4 start here but for bagging machine number 2>>>>>>>>>'''
            if len(bag_que) > 0:
                #if it is true then it calls that and take the amount that is required
                #to fulfill the demand of bagging
                 
                level = bag_que.iloc[0,6]
                size = bag_que.iloc[0,4]
                bag2 = 1                    
                #update the production table
                production2 = production2.append(bag_que.iloc[:1]).reset_index(drop = True)
                #update the amount now
                bag_que.iloc[0,6] = 0
                
                
                
                
                #finish_boxinf FEL builder
                mean = pack_rate[(pack_rate['Size'] == size) & (pack_rate['Packaging'] == 'Bag')]['Mean'].values[0]
                std = pack_rate[(pack_rate['Size'] == size) & (pack_rate['Packaging'] == 'Bag')]['Std'].values[0]
                rate = random.normalvariate(mean, std)
                FEL_builder('Bagging in mc2', level, rate)
                
                '''<<<<<<<<trigger point 4 stop here but for bagging machine number 2>>>>>>>>>''' 
    
    if I1 == 0:
        #trigger 1 start
        if len(tank_que) > 0:
            if f1 in tank_que['Flavor'].values:
                
                first_indx = tank_que[tank_que['Flavor'] == f1].index.values[0]
                tank1_mtl =  tank_que.loc[first_indx]
                mean = flavoring_rate[(flavoring_rate['Size'] == tank1_mtl['Size']) & (flavoring_rate['Flavor'] == tank1_mtl['Flavor'])]['Mean'].values[0]
                std = flavoring_rate[(flavoring_rate['Size'] == tank1_mtl['Size']) & (flavoring_rate['Flavor'] == tank1_mtl['Flavor'])]['Std'].values[0]
                rate = random.normalvariate(mean, std)
                level = tank1_mtl['Level']
               
                tank_que_2_sized_que(first_indx)
                I1 =1           
               
                FEL_builder('Flavoring in tank1', level, rate)
            else:
                for i in range(len(tank_que)):
                    
                    
                    current_flavor = tank_que.iloc[i,5]
                    if current_flavor not in [f1,f2,f3]:
                        
                        f1 = current_flavor
                        I1 = 1
                       
                        FEL_builder('Flavor Changing tank1')
                        
                        break    
            #trigger 1 stop
    if I2 == 0:
        if len(tank_que) > 0:
            #trigger 1 start
            if f2 in tank_que['Flavor'].values:
                
                first_indx = tank_que[tank_que['Flavor'] == f2].index.values[0]
                tank2_mtl =  tank_que.loc[first_indx]
                mean = flavoring_rate[(flavoring_rate['Size'] == tank2_mtl['Size']) & (flavoring_rate['Flavor'] == tank2_mtl['Flavor'])]['Mean'].values[0]
                std = flavoring_rate[(flavoring_rate['Size'] == tank2_mtl['Size']) & (flavoring_rate['Flavor'] == tank2_mtl['Flavor'])]['Std'].values[0]
                rate = random.normalvariate(mean, std)
                level = tank2_mtl['Level']
               
                tank_que_2_sized_que(first_indx)
                I2 =1           
    
                FEL_builder('Flavoring in tank2', level, rate)
           
            else:
                for i in range(len(tank_que)):
                    
                    
                    current_flavor = tank_que.iloc[i,5]
                    if current_flavor not in [f1,f2,f3]:
                        
                        f2 = current_flavor
                        I2 = 1
                       
                        FEL_builder('Flavor Changing tank2')
                        
                        break    
            #trigger 1 stop

        
def simulate():
    global color_of_rmi
    global level_of_rmi
    global Y
    global time
    global L #classifier busy or not 
    global FEL
    global tank_que
    global I1
    global I2
    global I3
    global tank1_mtl
    global tank2_mtl
    global tank3_mtl
    global color_wise_demand #when a drum opens it create a chart of color, size, flavor combination
    global empty_pi_que
    global box1
    global bag1
    global bag2
    global box_que
    global production1
    global production2
    global bag_que
    global num_of_bag
    global flavoring_rate
    global pack_rate
    
    global rmi
    global pfi
    global pi
    global f1
    global f2
    global f3
    global classifier_pr
    global site
    global sized_que1
    global sized_que2
    global sized_que3
    global sized_que4
    global sized_que5
    global final_demand
    global df1
    global df2
    global num_of_PFO
    global num_of_bag
    global R
    global last_color
    global data
    global SPLIT_PERCENT
    global pfi_cap
    global pi_cap
    
    
    production_output = []
    cost_output = []
    #tracelist = []
    #trace = pd.DataFrame(columns=['Time','Event', 'L', 'I1' ,'I2' , 'I3', 'f1', 'f2', 'f3', 'box1', 'bag1', 'bag2', 'S1', 'S2','S3', 'S4','S5', 'Tank_que', 'Box_que', 'Bag_que' ])
        
    for i in range(1):
     
        
        #initialize
        sitelist = ['Detroit, MI', 'Columbus, OH', 'Springfield, MO', 'Green Bay, WI', 'Omaha, NE']
        site = sitelist[0]
        rmi, pfi, pi = site_data(data, site = site)
        #rmi['Level'] = rmi['Level'] / 2
        pfi_cap , pi_cap = pd.unique(pfi['Capacity'])[0], pd.unique(pi['Capacity'])[0]
        sized_que1, sized_que2, sized_que3, sized_que4, sized_que5 = bin_segmentor()
        R = 0
        time = 0
        flavoring_rate = df1[df1['Site'] == site[0:-4]]
        pack_rate = df2[df2['Site'] == site[0:-4]]
        
        f1, f2, f3 = ['F14', 'F15', 'F16']
        num_of_bag = 1
        num_of_PFO = 2
        empty_pi_que = pi
        
        color_of_rmi = 1
        level_of_rmi = 0
        last_color = 0
        
        I1, I2, I3 = 0, 0, 1
        box1, bag1, bag2 = 0, 0, 1
        
        #initialize Y , the amount of Jelly beans of color i, size j in classifier
        Y = Y.iloc[:0]
        Y['Color'], Y['Size'], Y['Level'] = [0,0,0,0,0], ['S1','S2','S3','S4','S5'], [0,0,0,0,0]
        tank_que = tank_que.iloc[:0]
        tank1_mtl = tank1_mtl.iloc[:0]
        tank2_mtl = tank2_mtl.iloc[:0]
        tank3_mtl = tank3_mtl.iloc[:0]
        box_que = box_que.iloc[:0]
        bag_que = bag_que.iloc[:0]
        production1 = production1.iloc[:0]
        production2 = production2.iloc[:0]
        FEL = FEL.iloc[:0]
        FEL = FEL.append({'Event' : 'Releasing Drum', 'Time' : time}, ignore_index=True)
        
        cost = 0
        total = 0
        production = 0
        P = 'on'
        site_performance = []
        last_time  = 0
        
        keep_going = True
        #rnd = 0
        while keep_going == True:#rnd < 2:
            FEL = FEL.sort_values(by = ['Time']).reset_index(drop = True)
            event = FEL.iloc[0,0]
            time = FEL.iloc[0,1]
            
            if event == 'Releasing Drum':
                site_performance.append([color_of_rmi, time - last_time])
                print (str(color_of_rmi) + ' takes ' + str(time - last_time) + ' hours')
                last_time = time
                releasing_drum()
                #rnd += 1
            elif event == 'Classifying':
                classifier()
            elif event == 'Flavoring in tank1':
                finish_flavoring_tank1()
            elif event == 'Flavoring in tank2':
                finish_flavoring_tank2()
            elif event == 'Flavoring in tank3':
                finish_flavoring_tank3()
            elif event == 'Boxing':
                finish_boxing()
            elif event == 'Bagging in mc1':
                finish_bagging_m1()
            elif event == 'Bagging in mc2':
                finish_bagging_m2()
            elif event == 'Flavor Changing tank1':
                flavor_changed_tank1()
            elif event == 'Flavor Changing tank2':
                flavor_changed_tank2()
            elif event == 'Flavor Changing tank3':
                flavor_changed_tank3()
            else:
                print('Unknown Event')
                break
            
            #trace.loc[i] = time, event, L, I1, I2 , I3, f1, f2, f3, box1, bag1, bag2, len(sized_que1), len(sized_que2), len(sized_que3), len(sized_que4), len(sized_que5), len(tank_que), len(box_que), len(bag_que)
            #i +=1
            #print(FEL)
            #print("--------------------------------")
            #print(box_que)
            #print("--------------------------------")
            #print(bag_que)
            #print("--------------------------------")
            if len(FEL) > 1:
                FEL = FEL.iloc[1:].reset_index(drop = True)
            else:
                
                total += production1['Level'].sum()
                total += production2['Level'].sum()
                keep_going = False
                
                site_performance.append([color_of_rmi, time - last_time])
                print (str(color_of_rmi) + ' takes ' + str(time - last_time) + ' hours')
                print('--------------FEL is empty----------')
                if P == 'on':
                    production += production1['Level'].sum()
                    production += production2['Level'].sum()
             
            
            if time >= 4377 and P == 'on':
                P = 'off'
                production += production1['Level'].sum()
                production += production2['Level'].sum()
        
        #tracelist.append(trace)
        
        cost += (production1['Level'].sum() / 2.5) * 2.385
        cost += (production1['Level'].sum() / .25) * .250
        #print(cost)
        
        production1['Pack'] = 'Box'
        production2['Pack'] = 'Bag'
        
        output = production1
        output = output.append(production2).reset_index(drop = True)
        
        production_output.append(output)
        cost_output.append(cost)
        
        print('Round' + str(i))
        print('Total cost : $' + str(cost) )
        print('Total production : ' + str(production) + 'lb' )
        print('Total Loss sales : ' + str(total - production) + 'lb' )
        
        return (site_performance)
            
            
result1 = simulate()            
            
        
        
        
        
        


                                  