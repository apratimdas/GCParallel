
from scipy.stats import random_correlation

x = random_correlation.rvs((.5, .8, 1.2, 1.5,.5,1.5,.5, .8, 1.2, 1.5,.5,1.5,.5, .8, 1.2, 1.5,.5,1.5,.5, .8, 1.2, 1.5,.5,1.5,.5, .8, 1.2, 1.5,.5,1.5,.5, .8, 1.2, 1.5,.5,1.5,.5, .8, 1.2, 1.5,.5,1.5,.5, .8, 1.2, 1.5,.5,1.5,.5, .8, 1.2, 1.5,.5,1.5,.5, .8, 1.2, 1.5,.5,1.5,.5, .8, 1.2, 1.5,.5,1.5,.5, .8, 1.2, 1.5,.5,1.5,.5, .8, 1.2, 1.5,.5,1.5,.5, .8, 1.2, 1.5,.5,1.5,.5, .8, 1.2, 1.5,.5,1.5,.5, .8, 1.2, 1.5,.5,1.5,.5, .8, 1.2, 1.5,.5,1.5,.5, .8, 1.2, 1.5,.5,1.5,.5, .8, 1.2, 1.5,.5,1.5,.5, .8, 1.2, 1.5,.5,1.5))

posctr,negctr=0,0
# 50%
# posthreshold = 0.08
# negthreshold = -0.075
# 10%
posthreshold = 0.053
negthreshold = -0.09
for arr in x:
    for i in arr:
        if i > posthreshold or i <negthreshold:
            print(i,end=",")
            if i > posthreshold:
                posctr+=1
            elif i < negthreshold:
                negctr+=1
        else:
            print(0,end=",")
    print()

print(posctr,negctr)

#1300,130