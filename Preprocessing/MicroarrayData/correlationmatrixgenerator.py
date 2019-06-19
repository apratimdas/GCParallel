
import numpy

# tumor-cardia

data = []

with open("C:\Dev\GCParallel\Preprocessing\MicroarrayData\output-tumor-cardia.csv", "r") as ins:
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

# for i in range(0, len(correlationmatrix)):
#     for j in range(i, len(correlationmatrix)):
#         correlationmatrix[i][j] = numpy.corrcoef(data[i], data[j])[0][1]
#         correlationmatrix[j][i] = numpy.corrcoef(data[i], data[j])[0][1]
#     print(i)

# br = numpy.corrcoef(data[:13000])

n = len(data)
print(n)
posedgectr = 0
negedgectr = 0

for i in range(0,len(correlationmatrix)):
    for j in range(i+1, len(correlationmatrix)):
        if(correlationmatrix[i][j] > 0.65):
            # print(i,j,1)
            posedgectr+=1
        elif(correlationmatrix[i][j] < -0.55):
            # print(i,j,-1)
            negedgectr+=1
    if i%100 == 0:
        print(i)

print(posedgectr)
print(negedgectr)
print((posedgectr+negedgectr)/(n*(n-1)/2))


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