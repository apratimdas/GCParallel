
import sys
import math

mat1 = []
mat2 = []

with open(sys.argv[1], "r") as ins:
    for line in ins:

        temp = line[:-1].split(",")
        mat1.append([float(i) for i in temp])

with open(sys.argv[2], "r") as ins:
    for line in ins:

        temp = line[:-1].split(",")
        mat2.append([float(i) for i in temp])

gcd=0
       
for i in range(0,12):
    for j in range(i,12):
        gcd += (mat1[i][j] - mat2[i][j])**2

print(math.sqrt(gcd))