
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
correlationmatrix = [[0 for _ in range(0,len(data))]] * len(data)

tl = numpy.corrcoef(data[:13000])
br = numpy.corrcoef(data[:10000])

# for i in range(0, len(correlationmatrix)):
#     for j in range(i, len(correlationmatrix)):
#         correlationmatrix[i][j] = numpy.corrcoef(data[i], data[j])[0][1]
#         correlationmatrix[j][i] = numpy.corrcoef(data[i], data[j])[0][1]
#     print(i)

# br = numpy.corrcoef(data[:13000])

print(len(data))

# print(numpy.corrcoef(data[0], data[2])[0][1])

# f = open("cmatrix.csv", "w+")

# for i in range(0, len(correlationmatrix)):
#     for j in range(0,len(correlationmatrix)):
#         f.write(str(correlationmatrix[i][j])+',')
#     f.write('\n')

# f.close()
 
# https://stackoverflow.com/questions/24717513/python-numpy-corrcoef-memory-error

