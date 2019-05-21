
import re

flag = False

correlationmatrix = []

with open ("rcm50.csv", "r") as ins:
    for line in ins:
        # if not flag:
        #     flag = True
        #     continue
        data = line.split(",")
        if data[0] == '':
            continue
        # data.pop(0)
        data.pop(-1)
        # data[-1] = data[-1][0:-1]
        # print(data)
        result = [float(i) for i in data]
        correlationmatrix.append(result)

# print (correlationmatrix)

edgectr = 0
negativeedgectr = 0
for i in range(0,60):
    for j in range(i+1,60):
        if correlationmatrix[i][j] != 0:
            # correlationmatrix[i][j] += correlationmatrix[j][i]
            print(i,j, 1 if correlationmatrix[i][j] > 0 else -1)
            if(correlationmatrix[i][j] < 0):
                negativeedgectr += 1
            edgectr += 1

print(edgectr)
print(negativeedgectr)
# 8.9% negative edges

# print(correlationmatrix[55][55])