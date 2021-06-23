from bin_segmentor import *


def fill(giver_level, taker_cap):
    taker_level = 0
    if giver_level >= taker_cap:
        giver_level -= taker_cap * .95
        taker_level += taker_cap * .95
    if giver_level < taker_cap*.95:
        taker_level += giver_level
        giver_level = 0
        
    return giver_level, taker_level


def pfi_fill():
    global sized_que1, sized_que2, sized_que3, sized_que4, sized_que5
    global Y
   
    sized_que = [sized_que1, sized_que2, sized_que3, sized_que4, sized_que5]
    j = -1
    for que in sized_que:
        j += 1    
        for i in range(len(que)):    
            bin_cap = que.loc[i,'Capacity']
            giver_level = Y.loc[j, 'Level']
            Y.loc[j, 'Level'], que.loc[i,'Level'] = fill(giver_level = giver_level, taker_cap= bin_cap)
            #tank_que = tank_que.append(sized_que1.loc[0]).reset_index(drop = True)
            #sized_que1 = sized_que1.drop(0).reset_index(drop = True)
    
        print(que)

def sized_que_2_tank_que():
    global sized_que1, sized_que2, sized_que3, sized_que4, sized_que5
    global tank_que
    sized_que = [sized_que1, sized_que2, sized_que3, sized_que4, sized_que5]
    

