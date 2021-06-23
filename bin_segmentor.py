#import section
import numpy as np
from Data_structure import *
import random

#variable declaration if its global
global sized_que1
global sized_que2
global sized_que3
global sized_que4
global sized_que5


def bin_segmentor():              #this function will return the percentage of each size
    global sized_que1
    global sized_que2
    global sized_que3
    global sized_que4
    global sized_que5
    global rmi
    global pfi
    global SPLIT_PERCENT
    
    classifier_split = SPLIT_PERCENT
    #filter first with classifier_split_size
    sizelist = ['S1', 'S2', 'S3', 'S4', 'S5']
    segment_percent = []
    for size in sizelist:
        total = 0
        cap_total = 0
        for i in range(len(rmi)):
        #input
            RMI = rmi.loc[i]
            cav = RMI['Color']                         #coloring agent value
            cap = RMI['Level']              #capacity
            swcs = classifier_split[classifier_split['Size'] == size ]  #size wise classifier split
            swcs = swcs[swcs['Color'] == cav]
            percent = float(swcs['Percentage'].astype(int)/100)
            total += percent * cap
            cap_total += cap
        bss = total / cap_total                                    #bin size wise segmentor

        segment_percent.append(bss)
    bin_segment = np.array(segment_percent)
    bin_segment = np.round(bin_segment * len(pfi))
    slb = pfi 
       
    final_list = []                #slb = size labeled Bin
    sn = 0
    for size in sizelist:
      temp = [size]
      temp = temp * int(bin_segment[sn])
      sn += 1
     
      final_list = final_list + temp
    temparr = final_list
    
    if len(temparr) > len(pfi):
        n = random.randint(0,len(pfi))
        del temparr[n]
    if len(temparr) < len(pfi):
        n = random.randint(0,4)
        temparr.append(sizelist[n])
    temparr = np.array(final_list)
    
    slb['Size'] = temparr
    
    
    '''sized_que1['Flavor'] = np.NaN
    sized_que2['Flavor'] = np.NaN
    sized_que3['Flavor'] = np.NaN
    sized_que4['Flavor'] = np.NaN
    sized_que5['Flavor'] = np.NaN'''
    
    sized_que1 = slb[slb['Size'] == 'S1'].sort_values(by=['Drum']).reset_index(drop = True)
    sized_que2 = slb[slb['Size'] == 'S2'].sort_values(by=['Drum']).reset_index(drop = True)
    sized_que3 = slb[slb['Size'] == 'S3'].sort_values(by=['Drum']).reset_index(drop = True)
    sized_que4 = slb[slb['Size'] == 'S4'].sort_values(by=['Drum']).reset_index(drop = True)
    sized_que5 = slb[slb['Size'] == 'S5'].sort_values(by=['Drum']).reset_index(drop = True)
    
    
    
    return sized_que1, sized_que2, sized_que3, sized_que4, sized_que5
sized_que1, sized_que2, sized_que3, sized_que4, sized_que5 = bin_segmentor()

    

