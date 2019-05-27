
from numpy import corrcoef

gdv=[]

with open("gov10_2.txt", "r",encoding='utf-16') as ins:
    for line in ins:
        # print(line)
        temp = line[:-1].split(",")
        temp.pop(-1)
        # print(temp)
        # temp.pop(10)
        # temp.pop(10)
        # temp.pop(12)
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

gcm = corrcoef(gdvtarray)

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


for i in gcm:
    for j in i:
        print("{0:.2f}".format(j),end=',')
    print()

# # print(gcm[0][1])



