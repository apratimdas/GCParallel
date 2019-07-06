
import numpy

# tumor-cardia

data = []

filename = "output_gastro_all_h"

with open(filename, "r") as ins:
    for line in ins:

        temp = line.split(",")
        temp.pop()

        floattemp = [ float(i) for i in temp ]
        data.append(floattemp)
        # print(floattemp)

# # 1000 random integers between 0 and 50
# x = np.random.randint(0, 50, 1000)

# # Positive Correlation with some noise
# y = x + np.random.normal(0, 10, 1000)


# data = []
# print(x)
# data.append(x)
# data.append(y)
# data.append(y)

# print(data[-1])
# correlationmatrix = [[0 for _ in range(0,len(data))]] * len(data)

correlationmatrix = numpy.corrcoef(data)
# br = numpy.corrcoef(data[:10000])


n = len(data)
print(n)
posedgectr01 = 0
negedgectr01 = 0
posedgectr05 = 0
negedgectr05 = 0
posedgectr10 = 0
negedgectr10 = 0
posedgectr15 = 0
negedgectr15 = 0
posedgectr20 = 0
negedgectr20 = 0
posedgectr25 = 0
negedgectr25 = 0
posedgectr30 = 0
negedgectr30 = 0
posedgectr35 = 0
negedgectr35 = 0

output01 = filename + "_signed_01.txt"
output05 = filename + "_signed_05.txt"
output10 = filename + "_signed_10.txt"
output15 = filename + "_signed_15.txt"
output20 = filename + "_signed_20.txt"
output25 = filename + "_signed_25.txt"
output30 = filename + "_signed_30.txt"
output35 = filename + "_signed_35.txt"

filewrite01 = open(output01, 'w')
filewrite05 = open(output05, 'w')
filewrite10 = open(output10, 'w')
filewrite15 = open(output15, 'w')
filewrite20 = open(output20, 'w')
filewrite25 = open(output25, 'w')
filewrite30 = open(output30, 'w')
filewrite35 = open(output35, 'w')

filewrite01.write(str(n))
filewrite01.write('\n')
filewrite05.write(str(n))
filewrite05.write('\n')
filewrite10.write(str(n))
filewrite10.write('\n')
filewrite15.write(str(n))
filewrite15.write('\n')
filewrite20.write(str(n))
filewrite20.write('\n')
filewrite25.write(str(n))
filewrite25.write('\n')
filewrite30.write(str(n))
filewrite30.write('\n')
filewrite35.write(str(n))
filewrite35.write('\n')


for i in range(0,len(correlationmatrix)):
    for j in range(i+1, len(correlationmatrix)):
        if(correlationmatrix[i][j] > 0.01):
            # print(i,j,1)
            filewrite01.write(str(i) + " " + str(j) + " " + str(1) + "\n")
            posedgectr01+=1
        elif(correlationmatrix[i][j] < -0.01):
            # print(i,j,-1)
            filewrite01.write(str(i) + " " + str(j) + " " + str(-1) + "\n")
            negedgectr01+=1
        if(correlationmatrix[i][j] > 0.05):
            # print(i,j,1)
            filewrite05.write(str(i) + " " + str(j) + " " + str(1) + "\n")
            posedgectr05+=1
        elif(correlationmatrix[i][j] < -0.05):
            # print(i,j,-1)
            filewrite05.write(str(i) + " " + str(j) + " " + str(-1) + "\n")
            negedgectr05+=1
        if(correlationmatrix[i][j] > 0.10):
            # print(i,j,1)
            filewrite10.write(str(i) + " " + str(j) + " " + str(1) + "\n")
            posedgectr10+=1
        elif(correlationmatrix[i][j] < -0.10):
            # print(i,j,-1)
            filewrite10.write(str(i) + " " + str(j) + " " + str(-1) + "\n")
            negedgectr10+=1
        if(correlationmatrix[i][j] > 0.15):
            # print(i,j,1)
            filewrite15.write(str(i) + " " + str(j) + " " + str(1) + "\n")
            posedgectr15+=1
        elif(correlationmatrix[i][j] < -0.15):
            # print(i,j,-1)
            filewrite15.write(str(i) + " " + str(j) + " " + str(-1) + "\n")
            negedgectr15+=1
        if(correlationmatrix[i][j] > 0.20):
            # print(i,j,1)
            filewrite20.write(str(i) + " " + str(j) + " " + str(1) + "\n")
            posedgectr20+=1
        elif(correlationmatrix[i][j] < -0.20):
            # print(i,j,-1)
            filewrite20.write(str(i) + " " + str(j) + " " + str(-1) + "\n")
            negedgectr20+=1
        if(correlationmatrix[i][j] > 0.25):
            # print(i,j,1)
            filewrite25.write(str(i) + " " + str(j) + " " + str(1) + "\n")
            posedgectr25+=1
        elif(correlationmatrix[i][j] < -0.25):
            # print(i,j,-1)
            filewrite25.write(str(i) + " " + str(j) + " " + str(-1) + "\n")
            negedgectr25+=1    
        if(correlationmatrix[i][j] > 0.30):
            # print(i,j,1)
            filewrite30.write(str(i) + " " + str(j) + " " + str(1) + "\n")
            posedgectr30+=1
        elif(correlationmatrix[i][j] < -0.30):
            # print(i,j,-1)
            filewrite30.write(str(i) + " " + str(j) + " " + str(-1) + "\n")
            negedgectr30+=1
        if(correlationmatrix[i][j] > 0.35):
            # print(i,j,1)
            filewrite35.write(str(i) + " " + str(j) + " " + str(1) + "\n")
            posedgectr35+=1
        elif(correlationmatrix[i][j] < -0.35):
            # print(i,j,-1)
            filewrite35.write(str(i) + " " + str(j) + " " + str(-1) + "\n")
            negedgectr35+=1
    
    if i%100 == 0:
        print(i)

print(1,posedgectr01)
print(1,negedgectr01)
print(1,(posedgectr01+negedgectr01)/(n*(n-1)/2))

print(5,posedgectr05)
print(5,negedgectr05)
print(5,(posedgectr05+negedgectr05)/(n*(n-1)/2))

print(10,posedgectr10)
print(10,negedgectr10)
print(10,(posedgectr10+negedgectr10)/(n*(n-1)/2))

print(15,posedgectr15)
print(15,negedgectr15)
print(15,(posedgectr15+negedgectr15)/(n*(n-1)/2))

print(20,posedgectr20)
print(20,negedgectr20)
print(20,(posedgectr20+negedgectr20)/(n*(n-1)/2))

print(25,posedgectr25)
print(25,negedgectr25)
print(25,(posedgectr25+negedgectr25)/(n*(n-1)/2))

print(30,posedgectr30)
print(30,negedgectr30)
print(30,(posedgectr30+negedgectr30)/(n*(n-1)/2))

print(35,posedgectr35)
print(35,negedgectr35)
print(35,(posedgectr35+negedgectr35)/(n*(n-1)/2))


filewrite01.close()
filewrite05.close()
filewrite10.close()
filewrite15.close()
filewrite20.close()
filewrite25.close()
filewrite30.close()
filewrite35.close()




# print(numpy.corrcoef(data[0], data[2])[0][1])

# f = open("cmatrix2.csv", "w+")

# for i in range(0, len(correlationmatrix)):
#     for j in range(0,len(correlationmatrix)):
#         f.write(str(round(correlationmatrix[i][j], 2))+',')
#     f.write('\n')
#     print(i)

# f.close()
 
# https://stackoverflow.com/questions/24717513/python-numpy-corrcoef-memory-error

# ------------------
# TUMOR CARDIA
# N = 22500
# Max edges = ~250m

# 0.3 threshold
# 20.6m posedge
# 12.4m negedge
# 13.3% edge density

# 0.4 threshold
# 8.3m posedge
# 3.1m negedge
# 4.5% edge density

# 0.7 threshold
# 111k posedge
# 1.2k negedge
# 0.045% edge density

# 0.6 threshold
# 267k posedge
# 9k negedge
# 0.11% edge density

# 0.05,-0.55 thresholds
# 267k posedges
# 165k negedges
# 0.017% edge density

# sfdp -x -Goverlap=prism -Tpng -v tumor-cardia.dot > tumor-cardia.png
# sfdp -x -Goverlap=prism -Tpng -Gsize="40!" -v tumor-cardia-signed-00174.dot -O

# ------------------

# Tumor non-cardia

# 60 1237304
# 60 169087
# 60 0.00566510865648442

# 65 575698
# 65 57756
# 65 0.002551627348926921

# 70 243638
# 70 16389
# 70 0.00104741939376722

# 75 95546
# 75 3102
# 75 0.00039736576723320546

# 80 34776
# 80 282
# 80 0.00014121775472043747

# ------------------

# healthy

# 60 130937236
# 60 150790
# 60 0.5280380142179911

# 65 111385526
# 65 79354
# 65 0.44899367002632773

# 70 89931266
# 70 36506
# 70 0.3624007860984723

# 75 67047519
# 75 14799
# 75 0.270134918543784

# 80 44052654
# 80 5856
# 80 0.1774728694885031


# 90 7520365
# 90 169
# 90 0.030293597061404262

# 95 537787
# 95 1
# 95 0.0021662734290488514
# ----------------------------

