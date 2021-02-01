import pandas as pd
import numpy as np

class StarforceCalculator:
    def __init__(self, start = 0, end = 30, 
                 scroll = None, ward = None, lucky = None, click = None):
        # 30 >= end > start >= 0
        # scroll, ward, lucky have to be lists if provided
        self.start = start
        self.end = end
        
        self.scroll = [bool(s) for s in scroll] if scroll!= None else scroll
        self.ward = [bool(s) for s in ward] if ward!= None else ward
        self.lucky = [bool(s) for s in lucky] if lucky!= None else lucky
        self.click = [bool(s) for s in click] if click!= None else click
        
        self.table = None
        
        
    def create_table(self):
        starforce_state = list(range(31)) 
        #must add 20 more states (destroyed states)
        
        increase = np.array([100 - i*5 for i in range(20)] + [1]*10)/100 
        decrease = np.array([0]*10 + [10,10,15,15,20,20,25,25,30,30]+ [40]*5 + [45]*5)/100
        destroy = np.array([0]*10 + [5]*10 + [10]*5 + [15]*5)/100
        if self.click != None:
            increase = np.minimum(np.array(self.click)*0.05 + increase,1)
        if self.lucky != None:
        	increase = np.minimum(np.array(self.lucky)*0.1 + increase,1)
        
        
        same = 1 - increase - decrease - destroy
        cost = np.array([0.01,0.015,0.03,0.055,0.1,0.18,0.27,0.36,0.45,0.54,
                         0.56,0.64,0.72,0.8,1.2,1.6,2,2.4,2.8,3.2,3.6,
                         4,4.8,5.6,6.4,8.1,9,13.5,18,20.7])
        table = pd.DataFrame(list(zip(starforce_state,increase,
                                      same,decrease,destroy,cost)))
        table.columns = ['state','increase','same','decrease','destroy','cost']

        if self.scroll != None:
            table.loc[self.scroll,'same'] = table.iloc[self.scroll]['decrease'] + table.iloc[self.scroll]['same']
            table.loc[self.scroll,'decrease'] = 0
        if self.ward != None:
            table.loc[self.ward,'same'] = table.iloc[self.ward]['destroy'] + table.iloc[self.ward]['same']
            table.loc[self.ward,'destroy'] = 0
        #now we have to restrict based on start and endif 
        table = table[(table['state'] < self.end) & (table["state"] >= min(self.start, 9))]
        
        self.table = table
        
    def transient(self):
        part1 = np.diag(self.table['increase'].values[:-1],1)
        part1 += np.diag(self.table['same'].values + self.table['destroy'].values)
        part1 += np.diag(self.table['decrease'].values[1:],-1)
        self.TMatrix = part1

    def get_counts(self):
        Cinv = np.eye(self.TMatrix.shape[0])-self.TMatrix
        
        b = np.zeros(self.TMatrix.shape[0])
        b[max(self.start-9, 0)] = 1
        self.CMatrix = np.linalg.solve(Cinv.T, b) 
        
    
    def get_state_counts(self):
        tol = 1e-5
        self.CMatrix = self.CMatrix * (np.abs(self.CMatrix) > tol)
        if self.start < 10:
            self.NScount = self.CMatrix[:(self.end-self.start)]
            self.DScount = self.CMatrix[(self.end-self.start):]
        else:
            self.NScount = self.CMatrix[:(self.end-min(9,self.start))]
            self.DScount = self.CMatrix[(self.end-min(9,self.start)):]

        self.table['Num Visits'] = list(np.round(self.NScount,2))
        self.table['Num Destroyed'] = np.round(self.table['destroy'] * self.table['Num Visits'],2)
        self.table['Total Cost(M)'] = np.round(self.table['cost'] * self.table['Num Visits'],2)
        
    def print_results(self):
        print(self.table)
