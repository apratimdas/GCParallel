
import re

store = []

with open("watershed-s-gov.txt", "r",encoding='utf-16') as ins:
    for line in ins:
        # print(line)
        temp = line[:-1].split(",")
        temp.pop(-1)
        if temp[-1] == '':
            temp.pop()
        # print(temp)
        store.append([int(i) for i in temp])

orderlist = []
indexmap = {}

with open("order_s.txt", "r",encoding='utf-8') as ins:
    for line in ins:
        # print(line[:-1])
        orderlist.append(line[:-1])

with open("watershed-s-mapping.txt", "r", encoding = 'utf-8') as ins:
    for line in ins:
        temp = line[:-1]
        # print(int(line[:2]))
        name = line[2:-1]
        index = int(line[:2])
        if name[0] == ' ':
            name = name[1:]
        # print(name)
        indexmap[name] = index

for name in orderlist:
    if name in indexmap:
        # print(name,":",store[indexmap[name]])
        for i in store[indexmap[name]]:
            print(i, end = ',')
            pass
    else:
        # print(name,":",[0]*13)
        for i in ([0]*13):
            print(i, end=',')
            pass
    
    print()
