
import pandas as pd
import numpy as np
import random
from gurobipy import *





#********From Final Optimization Import All ************
#renaming Drum and S matrix define here

S = np.zeros((170, 5)) # Drum at which site
S[0:40, 0] = 1
S[40:70, 1] = 1
S[70:120, 2] = 1
S[120:140, 3] = 1
S[140:170, 4] = 1

#cap of each drum
Cap = np.zeros((170,1))
Cap[0:40, 0] = 300000
Cap[40:70, 0] = 320000
Cap[70:120, 0] = 88000
Cap[120:140, 0] = 330000
Cap[140:170, 0] = 440000

#perc calculation
orders = pd.read_csv('Order Bank.csv')
orders = orders.rename(columns={"Qty (pack unit)": "Level", "Package Type": "Pack"})
orders = orders.iloc[:, 1:]
temp1= orders[orders['Pack']=='Bag']
temp1.iloc[:,4] = temp1.iloc[:,4] * 0.25
temp2= orders[orders['Pack']=='Box']
temp2.iloc[:,4] = temp2.iloc[:,4] * 2.5
orders = temp1.append(temp2)
orders = orders.sort_values(by = ['Color', 'Size', 'Flavor', 'Pack'])

perc = []
a = np.zeros((40,2))
colors = pd.unique(orders['Color'])
i = 0
total = 0
for color in colors:
    sub_total = orders[orders['Color'] == color]['Level'].sum()
    perc.append(sub_total)
    total += sub_total
    
    box_total = orders[(orders['Color'] == color) & (orders['Pack'] == 'Box')]['Level'].sum()
    bag_total = orders[(orders['Color'] == color) & (orders['Pack'] == 'Bag')]['Level'].sum()
    a[i, 0], a[i,1] = box_total/sub_total, bag_total/sub_total
    
    i += 1
    
perc = perc / total

#distance matrix is here
dist = np.array([[0,210,750,510,730,280],
                       [210,0,630,530,750,320],
                       [750,630,0,720,630,510],
                       [510,530,720,0,570,210],
                       [730,780,630,570,0,470],
                       [280,320,510,210,470,0]])
    
cost_matrix = np.array([[2.494,.2630 ],
                        [2.613, .2750],
                        [2.731, .2880],
                        [2.3850, .25],
                        [2.4230, .2550]])


    #--------------ColorID, SiteID-------------#

colors = np.arange(0,40,1)
sites = np.arange(0,6,1)
drums = np.arange(0,170,1)
D= drums #Drum Number All change 
C= colors 
M = np.arange(0,5,1)
B= np.arange(0,2,1) 
Per = perc # Percentage of Drum filled
Bias = 65569 # Bias Value
Alpha = 145545 # Lost sales allowance
TT = 500000 # Transportation Threshold 'The value is correct'
CP = cost_matrix #cost matrix
Dist = dist #Distance matrix
CT= 3.5 #Cost of Truck per trip 'The value is correct'
LT = 50000 # Truck Load 'The value is correct'
W = [2.5,0.25] # weight of Box and bag
A= a
P = [6358979.83617001, 3219195.3722, 2336203.9336440004, 2940000.0, 5244041.949424751]

m = Model('Optimize')

J = m.addVars(D,C, vtype=GRB.BINARY, name='Color Assignment in Drum')
T = m.addVars(D,M, vtype=GRB.BINARY, name='Drum Destination') #
X = m.addVars(D, vtype=GRB.CONTINUOUS , name='Drum Level')
Y = m.addVars(C,M, vtype=GRB.CONTINUOUS, name='Amount of Color at particular Site after transportation')
Z= m.addVars(D,M,C, vtype=GRB.BINARY, name="Z")
L= m.addVars(D,M,C, vtype=GRB.BINARY, name="L")

m.addConstrs( (quicksum(T[d,n] for n in M ) <= 1 for d in D)) #2nd constraint
m.addConstrs( T[d,m] <= (1 - S[d][m]) for d in D for m in M)  # 1st constraint

m.addConstrs((T[d,n]+J[d,c] <= Z[d,n,c] + 1) for d in D for n in M for c in C)
m.addConstrs(Z[d,n,c] <= T[d,n] for d in D for n in M for c in C)
m.addConstrs(Z[d,n,c] <= J[d,c] for d in D for n in M for c in C)

m.addConstrs((quicksum(S[d][n]*T[d,m] for m in M) + J[d,c] <= L[d,n,c] + 1) for d in D for n in M for c in C)
m.addConstrs((L[d,n,c] <= quicksum(S[d][n]*T[d,m] for m in M) for d in D for n in M for c in C))
m.addConstrs((L[d,n,c] <= J[d,c]) for d in D for n in M for c in C)
m.addConstrs((quicksum(J[d,c] for c in C)==1)for d in D)



#expr1 = QuadExpr(quicksum(J[d,c]*X[d] for d in D))
#expr2 = QuadExpr(quicksum(X[d] for d in D))
for c in C:
    m.addQConstr( (QuadExpr(quicksum(J[d,c]*X[d] for d in D)) <= (quicksum(X[d] for d in D) * Per[c] + Bias)))# 3rd Contraints
    m.addQConstr( (QuadExpr(quicksum(J[d,c]*X[d] for d in D))) >= Per[c]*quicksum(X[d] for d in D) - Bias) # 4th Contraints
    for n in M:
        m.addQConstr( QuadExpr(quicksum(S[d][n]*J[d,c]*X[d] for d in D))+ QuadExpr(quicksum(Z[d,n,c]*X[d] for d in D))-QuadExpr(quicksum(L[d,n,c]*X[d] for d in D)) == Y[c,n]) # 6th constraint
#m.addQConstrs( (quicksum(J[d,c]*X[d] for d in D) <= Per[c]*quicksum(X[d] for d in D) + Bias) for c in C) # 3rd Contraints
#expr1 = QuadExpr((quicksum(X[d]*J[d,0] for d in D)))
#expr2 = Per[0]* quicksum(X[d] for d in D)
#m.addQConstr(X[d1]*X[d2] + X[d]*X[5] <= 500000.0, "c1")
#m.addQConstr( expr1 - expr2 <= Bias)
#m.addConstrs( (quicksum(J[d,c]*X[d] for d in D) >= Per[c]*quicksum(X[d] for d in D) - Bias) for c in C) # 4th Contraints
    
#m.addConstrs( (quicksum(Y[c,n]-P[c,n] for c in C) <= Alpha) for n in M) # 5th constraint
m.addConstrs(((quicksum(Y[c,n] for c in C))-P[n]  <= 0.1*P[n]) for n in M) # 5th constraint        
#for c in C:
#    for n in M:
#        m.addQConstr( QuadExpr(quicksum(S[d][n]*J[d,c]*X[d] for d in D))+ QuadExpr(quicksum(T[d,n]*J[d,c]*X[d] for d in D))-quicksum(S[d][n]*T[d,m]*X[d]*J[d,c] for d in D for m in M) == Y[c,n]) # 6th constraint
m.addConstrs( X[d] <= Cap[d]  for d in D)  # 7th Constraint
for l in M:
    for n in M:
        m.addQConstr( (quicksum(S[d][l]*(QuadExpr(T[d,n]*X[d])) for d in D)) <= TT) # 8th constraint


obj1 = quicksum(X[d] for d in D)
obj2 = quicksum((CP[n][b]*quicksum(A[c][b]*Y[c,n] for c in C) / W[b]) for n in M for b in B) +quicksum(T[d,n]*quicksum(S[d][m]*Dist[m][n] for m in M)* X[d] for d in D for n in M)*(CT/LT)

obj = (obj1/4.5) - (obj2/5.3)
#obj4 = quicksum(quicksum(y[c,n] for c in C)*Dist[n][5] for n in M)*(CT/LT) #Chicago
m.params.timelimit= 60*60*2.1
m.setObjective(obj,GRB.MAXIMIZE)
#m.setObjective(obj2,GRB.MINIMIZE)

m.update()
m.optimize()

Drums = np.zeros((170,1))
for i in range(170):
    Drums[i,0] = X[i].x
Drums = pd.DataFrame(Drums)
Drums.to_csv('Final_X.csv', header = False, index=False)

Color_assign = np.zeros((170,40))
for i in range(170):
    for j in range(40):
        Color_assign[i,j] = J[i,j].x
Color_assign = pd.DataFrame(Color_assign)
Color_assign.to_csv('Final_J.csv', header = False, index=False)

Drum_dest = np.zeros((170,5))
for i in range(170):
    for j in range(5):
        Drum_dest[i,j] = T[i,j].x
Drum_dest = pd.DataFrame(Drum_dest)
Drum_dest.to_csv('Final_T.csv', header = False, index=False)


amnt_after_trans = np.zeros((40,5))
for i in range(40):
    for j in range(5):
        amnt_after_trans[i,j] = Y[i,j].x
amnt_after_trans = pd.DataFrame(amnt_after_trans)
amnt_after_trans.to_csv('Final_Y.csv', header = False, index=False)

