
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

print(numpy.corrcoef(data[10000:20000]))

# https://stackoverflow.com/questions/24717513/python-numpy-corrcoef-memory-error

