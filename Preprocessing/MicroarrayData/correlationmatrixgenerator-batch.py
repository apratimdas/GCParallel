
import numpy

# tumor-cardia

data = []

filename = "output_gastro_611_h"

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
posedgectr60 = 0
negedgectr60 = 0
posedgectr65 = 0
negedgectr65 = 0
posedgectr70 = 0
negedgectr70 = 0
posedgectr75 = 0
negedgectr75 = 0
posedgectr80 = 0
negedgectr80 = 0
posedgectr85 = 0
negedgectr85 = 0
posedgectr90 = 0
negedgectr90 = 0
posedgectr95 = 0
negedgectr95 = 0

output60 = filename + "_signed_60.txt"
output65 = filename + "_signed_65.txt"
output70 = filename + "_signed_70.txt"
output75 = filename + "_signed_75.txt"
output80 = filename + "_signed_80.txt"
output85 = filename + "_signed_85.txt"
output90 = filename + "_signed_90.txt"
output95 = filename + "_signed_95.txt"

filewrite60 = open(output60, 'w')
filewrite65 = open(output65, 'w')
filewrite70 = open(output70, 'w')
filewrite75 = open(output75, 'w')
filewrite80 = open(output80, 'w')
filewrite85 = open(output85, 'w')
filewrite90 = open(output90, 'w')
filewrite95 = open(output95, 'w')

filewrite60.write(str(n))
filewrite60.write('\n')
filewrite65.write(str(n))
filewrite65.write('\n')
filewrite70.write(str(n))
filewrite70.write('\n')
filewrite75.write(str(n))
filewrite75.write('\n')
filewrite80.write(str(n))
filewrite80.write('\n')
filewrite85.write(str(n))
filewrite85.write('\n')
filewrite90.write(str(n))
filewrite90.write('\n')
filewrite95.write(str(n))
filewrite95.write('\n')


for i in range(0,len(correlationmatrix)):
    for j in range(i+1, len(correlationmatrix)):
        if(correlationmatrix[i][j] > 0.60):
            # print(i,j,1)
            filewrite60.write(str(i) + " " + str(j) + " " + str(1) + "\n")
            posedgectr60+=1
        elif(correlationmatrix[i][j] < -0.60):
            # print(i,j,-1)
            filewrite60.write(str(i) + " " + str(j) + " " + str(-1) + "\n")
            negedgectr60+=1
        if(correlationmatrix[i][j] > 0.65):
            # print(i,j,1)
            filewrite65.write(str(i) + " " + str(j) + " " + str(1) + "\n")
            posedgectr65+=1
        elif(correlationmatrix[i][j] < -0.65):
            # print(i,j,-1)
            filewrite65.write(str(i) + " " + str(j) + " " + str(-1) + "\n")
            negedgectr65+=1
        if(correlationmatrix[i][j] > 0.70):
            # print(i,j,1)
            filewrite70.write(str(i) + " " + str(j) + " " + str(1) + "\n")
            posedgectr70+=1
        elif(correlationmatrix[i][j] < -0.70):
            # print(i,j,-1)
            filewrite70.write(str(i) + " " + str(j) + " " + str(-1) + "\n")
            negedgectr70+=1
        if(correlationmatrix[i][j] > 0.75):
            # print(i,j,1)
            filewrite75.write(str(i) + " " + str(j) + " " + str(1) + "\n")
            posedgectr75+=1
        elif(correlationmatrix[i][j] < -0.75):
            # print(i,j,-1)
            filewrite75.write(str(i) + " " + str(j) + " " + str(-1) + "\n")
            negedgectr75+=1
        if(correlationmatrix[i][j] > 0.80):
            # print(i,j,1)
            filewrite80.write(str(i) + " " + str(j) + " " + str(1) + "\n")
            posedgectr80+=1
        elif(correlationmatrix[i][j] < -0.80):
            # print(i,j,-1)
            filewrite80.write(str(i) + " " + str(j) + " " + str(-1) + "\n")
            negedgectr80+=1
        if(correlationmatrix[i][j] > 0.85):
            # print(i,j,1)
            filewrite85.write(str(i) + " " + str(j) + " " + str(1) + "\n")
            posedgectr85+=1
        elif(correlationmatrix[i][j] < -0.85):
            # print(i,j,-1)
            filewrite85.write(str(i) + " " + str(j) + " " + str(-1) + "\n")
            negedgectr85+=1    
        if(correlationmatrix[i][j] > 0.90):
            # print(i,j,1)
            filewrite90.write(str(i) + " " + str(j) + " " + str(1) + "\n")
            posedgectr90+=1
        elif(correlationmatrix[i][j] < -0.90):
            # print(i,j,-1)
            filewrite90.write(str(i) + " " + str(j) + " " + str(-1) + "\n")
            negedgectr90+=1
        if(correlationmatrix[i][j] > 0.95):
            # print(i,j,1)
            filewrite95.write(str(i) + " " + str(j) + " " + str(1) + "\n")
            posedgectr95+=1
        elif(correlationmatrix[i][j] < -0.95):
            # print(i,j,-1)
            filewrite95.write(str(i) + " " + str(j) + " " + str(-1) + "\n")
            negedgectr95+=1
    
    if i%100 == 0:
        print(i)

print(60,posedgectr60)
print(60,negedgectr60)
print(60,(posedgectr60+negedgectr60)/(n*(n-1)/2))

print(65,posedgectr65)
print(65,negedgectr65)
print(65,(posedgectr65+negedgectr65)/(n*(n-1)/2))

print(70,posedgectr70)
print(70,negedgectr70)
print(70,(posedgectr70+negedgectr70)/(n*(n-1)/2))

print(75,posedgectr75)
print(75,negedgectr75)
print(75,(posedgectr75+negedgectr75)/(n*(n-1)/2))

print(80,posedgectr80)
print(80,negedgectr80)
print(80,(posedgectr80+negedgectr80)/(n*(n-1)/2))

print(85,posedgectr85)
print(85,negedgectr85)
print(85,(posedgectr85+negedgectr85)/(n*(n-1)/2))

print(90,posedgectr90)
print(90,negedgectr90)
print(90,(posedgectr90+negedgectr90)/(n*(n-1)/2))

print(95,posedgectr95)
print(95,negedgectr95)
print(95,(posedgectr95+negedgectr95)/(n*(n-1)/2))


filewrite60.close()
filewrite65.close()
filewrite70.close()
filewrite75.close()
filewrite80.close()
filewrite85.close()
filewrite90.close()
filewrite95.close()




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

# 0.65,-0.55 thresholds
# 267k posedges
# 165k negedges
# 0.017% edge density

# sfdp -x -Goverlap=prism -Tpng -v tumor-cardia.dot -O
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

