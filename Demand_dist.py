from Data_structure import *
import pandas as pd
import numpy as np
import random

global final_demand

demand = pd.read_csv('Order Bank.csv')
for i in range(len(demand)):
    if len(demand.iloc[i,1]) == 12:
        demand.iloc[i,1] = demand.iloc[i,1].replace(demand.iloc[i,1][11:],'0'+ demand.iloc[i,1][11:])

demand = demand.iloc[:,1:]
demand = demand.rename(columns={"Package Type": "Pack", "Qty (pack unit)": "Level"})

colors = list(pd.unique(demand['Color']))
sizes = list(pd.unique(demand['Size']))
flavors = list(pd.unique(demand['Flavor']))
packs = list(pd.unique(demand['Pack']))

temp1= demand[demand['Pack']=='Bag']
temp1.iloc[:,4] = temp1.iloc[:,4] * 0.25

temp2= demand[demand['Pack']=='Box']
temp2.iloc[:,4] = temp2.iloc[:,4] * 2.5

demand = temp1.append(temp2)
demand = demand.sort_values(by = ['Color', 'Size', 'Flavor', 'Pack'])

site_demand = pd.DataFrame(columns=['Color', 'Size', 'Flavor','Pack','Mean','Std','Random','W'])
site_demand['Mean'],site_demand['Std'],site_demand['Random'],site_demand['W'] = 0,0,0,0

keep_going = True
m = 0
for i in colors:
    for j in sizes:
        for k in flavors:
            for l in packs:
                temp = demand[(demand['Color']==i) & (demand['Size']==j) & (demand['Flavor']==k) & (demand['Pack']==l)]
                if len(temp['Level']) > 0:
                    mu = np.array(temp['Level']).mean()
                    std = np.array(temp['Level']).std()
                    rand = np.random.normal(mu,std)
                    if rand < 0:                      
                        rand = 0 
                else:
                    mu = 0
                    std = 0
                    rand = 0
                site_demand.loc[m,'Std'] = std
                site_demand.loc[m,'Color'] = i[:5] + 'ing' + i[5:]
                site_demand.loc[m,'Size'] = j
                site_demand.loc[m,'Flavor'] = k
                site_demand.loc[m,'Pack'] = l
                site_demand.loc[m,'Mean'] = mu                
                site_demand.loc[m,'Random'] = rand
                m += 1

#site_demand = site_demand.sort_values(by = ['Color', 'Size', 'Flavor', 'Pack'])
site_demand = site_demand.reset_index(drop = True)
df3 = pd.DataFrame(columns = ['Color', 'Size', 'Flavor','Pack','Mean','Std','Random','W', 'Demand'])

def site_wise_demand(site_demand =site_demand, df3= df3 ):
    global rmi
        
    colors = list(pd.unique(rmi['Color']))
    for color in colors:
        site_level = float(rmi[rmi.iloc[:,2] == color].iloc[:,3].sum())
        dist_level = float(site_demand[site_demand.iloc[:,0] == color].iloc[:,6].sum())
        if dist_level == 0:
            w = 0
        else:
            w = float(site_level / dist_level)      
            
        temp = site_demand[site_demand.iloc[:,0] == color]
        temp.iloc[:,7] = w
        temp = temp.assign(Demand = temp.iloc[:,7] * temp.iloc[:,6])
        df3 = df3.append(temp)
    #print(df3)    
    data = pd.DataFrame()
    data['Color'], data['Size'], data['Flavor'], data['Pack'], data['Demand'] = df3['Color'], df3['Size'], df3['Flavor'], df3['Pack'] , df3['Demand']
    data = data.reset_index(drop = True)
    
    return data

DEMAND = site_wise_demand()
final_demand = DEMAND
final_demand['Demand'] = round(final_demand['Demand'])

Inv_balance = pd.DataFrame(columns = ['Location', 'Color','Qty in Pounds at Classifier','Size', 'Flavor','Qty in Pounds At Pre-finish Operations','Packaging','Qty in Pounds At Pack Operations'])

for p in range(len(final_demand.index)):
    Inv_balance.loc[p,'Location'] = rmi.loc[0,'Site']
    Inv_balance.loc[p,'Color'] = final_demand.loc[p,'Color']
    Inv_balance.loc[p,'Size'] = final_demand.loc[p,'Size']
    Inv_balance.loc[p,'Flavor'] = final_demand.loc[p,'Flavor']
    Inv_balance.loc[p,'Packaging'] = final_demand.loc[p,'Pack']
    Inv_balance.loc[p,'Qty in Pounds At Pack Operations'] = final_demand.loc[p,'Demand']
    Inv_balance.loc[p,'Qty in Pounds At Pre-finish Operations'] = final_demand[(final_demand['Color']==final_demand.loc[p,'Color']) & (final_demand['Size']==final_demand.loc[p,'Size']) & (final_demand['Flavor']==final_demand.loc[p,'Flavor'])]['Demand'].sum()
    Inv_balance.loc[p,'Qty in Pounds at Classifier'] = final_demand[(final_demand['Color']==final_demand.loc[p,'Color'])]['Demand'].sum() 

U = pd.Series(Inv_balance['Location']).duplicated()
V = pd.Series(Inv_balance['Color']).duplicated()
X = pd.Series(Inv_balance['Qty in Pounds at Classifier']).duplicated()
Y = pd.Series(Inv_balance['Qty in Pounds At Pre-finish Operations']).duplicated()
for i in range(len(Inv_balance)):
    if U[i] == True:
        Inv_balance.loc[i,'Location'] = U[i] and ""
    if V[i] == True:
        Inv_balance.loc[i,'Color'] = V[i] and ""
    if X[i] == True:
        Inv_balance.loc[i,'Qty in Pounds at Classifier'] = X[i] and ""
    if Y[i] == True:
        Inv_balance.loc[i,'Qty in Pounds At Pre-finish Operations'] = Y[i] and ""
          
Inv_balance.to_csv('Inv_balance.csv', header = True, index = False)

def prepare_color_wise_demand(color, d =DEMAND):
    
    colors = list(pd.unique(d['Color']))
    sizes = list(pd.unique(d['Size']))
    flavors = list(pd.unique(d['Flavor']))
    
    temp = pd.DataFrame(columns = ['Color', 'Size', 'Flavor', 'Demand'])
    
    count = 0
    for i in colors:
        for j in sizes:
            for k in flavors:
                
                temp.loc[count,'Color'] = i
                temp.loc[count,'Size'] = j
                temp.loc[count,'Flavor'] = k
                
                amt = round(d[(d['Color']==i) & (d['Size']==j) & (d['Flavor']==k)]['Demand'].sum())
                temp.loc[count,'Demand'] = amt
                #print(d)
                count +=1
    
    temp = temp[temp['Color'] == color].sort_values(by = ['Size', 'Flavor']).reset_index(drop = True)
    return temp

#color_wise_demand = prepare_color_wise_demand('Coloring Agent21')
                
        
    