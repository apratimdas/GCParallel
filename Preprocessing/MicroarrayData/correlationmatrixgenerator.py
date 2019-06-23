
import numpy

# tumor-cardia

data = []

with open("C:\Dev\GCParallel\Preprocessing\MicroarrayData\output-healthy.csv", "r") as ins:
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
posedgectr90 = 0
negedgectr90 = 0
posedgectr95 = 0
negedgectr95 = 0


for i in range(0,len(correlationmatrix)):
    for j in range(i+1, len(correlationmatrix)):
        # if(correlationmatrix[i][j] > 0.60):
        #     # print(i,j,1)
        #     posedgectr60+=1
        # elif(correlationmatrix[i][j] < -0.60):
        #     # print(i,j,-1)
        #     negedgectr60+=1
        # if(correlationmatrix[i][j] > 0.70):
        #     # print(i,j,1)
        #     posedgectr70+=1
        # elif(correlationmatrix[i][j] < -0.70):
        #     # print(i,j,-1)
        #     negedgectr70+=1
        # if(correlationmatrix[i][j] > 0.65):
        #     # print(i,j,1)
        #     posedgectr65+=1
        # elif(correlationmatrix[i][j] < -0.65):
        #     # print(i,j,-1)
        #     negedgectr65+=1
        # if(correlationmatrix[i][j] > 0.75):
        #     # print(i,j,1)
        #     posedgectr75+=1
        # elif(correlationmatrix[i][j] < -0.75):
        #     # print(i,j,-1)
        #     negedgectr75+=1
        # if(correlationmatrix[i][j] > 0.80):
        #     # print(i,j,1)
        #     posedgectr80+=1
        # elif(correlationmatrix[i][j] < -0.80):
        #     # print(i,j,-1)
        #     negedgectr80+=1
        # if(correlationmatrix[i][j] > 0.90):
        #     # print(i,j,1)
        #     posedgectr90+=1
        # elif(correlationmatrix[i][j] < -0.90):
        #     # print(i,j,-1)
        #     negedgectr90+=1
        if(correlationmatrix[i][j] > 0.95):
            print(i,j,1)
            posedgectr95+=1
        elif(correlationmatrix[i][j] < -0.95):
            print(i,j,-1)
            negedgectr95+=1
        
    # if i%100 == 0:
    #     print(i)

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

print(90,posedgectr90)
print(90,negedgectr90)
print(90,(posedgectr90+negedgectr90)/(n*(n-1)/2))

print(95,posedgectr95)
print(95,negedgectr95)
print(95,(posedgectr95+negedgectr95)/(n*(n-1)/2))


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


# ----------------------------

