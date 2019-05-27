
import re

dictmap = {}
ctr = 0

with open("watershed-k.csv", "r") as ins:
    for line in ins:
        # print(line)
        temp = line[:-1].split(",")
        temp.pop()
        for strval in temp:
            if strval not in dictmap:
                dictmap[strval] = ctr
                ctr += 1
            print(dictmap[strval], end = " ")
        print()
        

# mapping the vertex name to index
# for i in dictmap:
#     print(dictmap[i],i)


