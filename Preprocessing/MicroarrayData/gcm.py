
import numpy
import sys


gdv=[]

with open(sys.argv[1], "r",encoding='utf-8') as ins:
    for idx,line in enumerate(ins):

        if(idx < 7):
            continue

        # print(idx, line)
        temp = line[:-1].split(" ")
        # temp.pop(-1)
        # print(temp)
        # temp.pop(10)
        # temp.pop(10)
        # temp.pop(12)
        if temp[-1] == '':
            temp.pop()
        # print(temp)
        numbers = [int(x) for x in temp]
        gdv.append(numbers)

# print(gdv)
gdvt = [*zip(*gdv)]
# print(gdvt)
gdvtarray = []
for i in gdvt:
    gdvtarray.append((list(i)))
    # print((list(i)))

gcm = numpy.corrcoef(gdvtarray)

# print(gcm)

# gcmshuffle = []
# gcmshuffle.append(gcm[9])
# gcmshuffle.append(gcm[4])
# gcmshuffle.append(gcm[6])
# gcmshuffle.append(gcm[1])
# gcmshuffle.append(gcm[12])
# gcmshuffle.append(gcm[13])
# gcmshuffle.append(gcm[2])
# gcmshuffle.append(gcm[5])
# gcmshuffle.append(gcm[11])
# gcmshuffle.append(gcm[7])
# gcmshuffle.append(gcm[8])
# gcmshuffle.append(gcm[0])
# gcmshuffle.append(gcm[3])
# gcmshuffle.append(gcm[10])
# gcmshuffle.append(gcm[14])

# gcmshuffle2 = []
# for i in range(0,15):
#     gcmshuffle2.append([])

# for i in range(0,15):
#     gcmshuffle2[i].append(gcmshuffle[i][9])
#     gcmshuffle2[i].append(gcmshuffle[i][4])
#     gcmshuffle2[i].append(gcmshuffle[i][6])
#     gcmshuffle2[i].append(gcmshuffle[i][1])
#     gcmshuffle2[i].append(gcmshuffle[i][12])
#     gcmshuffle2[i].append(gcmshuffle[i][13])
#     gcmshuffle2[i].append(gcmshuffle[i][2])
#     gcmshuffle2[i].append(gcmshuffle[i][5])
#     gcmshuffle2[i].append(gcmshuffle[i][11])
#     gcmshuffle2[i].append(gcmshuffle[i][7])
#     gcmshuffle2[i].append(gcmshuffle[i][8])
#     gcmshuffle2[i].append(gcmshuffle[i][0])
#     gcmshuffle2[i].append(gcmshuffle[i][3])
#     gcmshuffle2[i].append(gcmshuffle[i][10])
#     gcmshuffle2[i].append(gcmshuffle[i][14])

orbits = [0,2,3,4,9,1,5,6,7,8,12,13] # change based on serriation

for i in orbits:
    for j in orbits:
        if numpy.isnan(gcm[i][j]):
            print("0",end=',')
        else:
            print("{0:.2f}".format(gcm[i][j]),end=',')
    print()

# # print(gcm[0][1])



