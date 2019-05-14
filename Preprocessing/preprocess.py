
import re

flag = False

correlationmatrix = []

with open ("correlationmatrix.csv", "r") as ins:
    for line in ins:
        if not flag:
            flag = True
            continue
        data = line.split(",")
        if data[0] == '':
            continue
        data.pop(0)
        data[-1] = data[-1][0:-1]
        result = [float(i) for i in data]
        correlationmatrix.append(result)

edgectr = 0
negativeedgectr = 0
for i in range(0,56):
    for j in range(i+1,56):
        if correlationmatrix[i][j] != 0:
            correlationmatrix[i][j] += correlationmatrix[j][i]
            print(i,j, 1 if correlationmatrix[i][j] > 0 else -1)
            if(correlationmatrix[i][j] < 0):
                negativeedgectr += 1
            edgectr += 1

# print(edgectr)
# print(negativeedgectr)
# 8.9% negative edges

# print(correlationmatrix[55][55])