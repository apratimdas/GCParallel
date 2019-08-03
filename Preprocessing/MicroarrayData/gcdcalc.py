
import sys
import math

mat1 = []
mat2 = []

file1list = []
file1list.append("SignedGraphs/TumorNonCardia/gcm_611_tnc_60_r_a.csv")
file1list.append("SignedGraphs/TumorNonCardia/gcm_611_tnc_60_r_b.csv")
file1list.append("SignedGraphs/TumorNonCardia/gcm_611_tnc_60_r_c.csv")
file1list.append("SignedGraphs/TumorNonCardia/gcm_611_tnc_60_r_d.csv")
file1list.append("SignedGraphs/TumorNonCardia/gcm_611_tnc_60_r_e.csv")
file1list.append("SignedGraphs/TumorNonCardia/gcm_611_tnc_60_r_f.csv")

file2 = "GCMOutput/gcm_611_tnc_60.csv"
gcdsum = 0

for file1 in file1list:

    with open(file1, "r") as ins:
        for line in ins:

            temp = line.split(",")[:-1]
            # print(temp)
            mat1.append([float(i) for i in temp])

    with open(file2, "r") as ins:
        for line in ins:

            temp = line.split(",")[:-1]
            mat2.append([float(i) for i in temp])

    gcd=0
        
    for i in range(0,12):
        for j in range(i,12):
            gcd += (mat1[i][j] - mat2[i][j])**2

    # print(math.sqrt(gcd))
    gcdsum += math.sqrt(gcd)

    mat1 = []
    mat2 = []

print(gcdsum/6)
