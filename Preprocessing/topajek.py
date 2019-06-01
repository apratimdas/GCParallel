
import re

flag = False

print("*Vertices 55")
for i in range(0,55):
    print(i,"\"" + str(i) + "\"")

print()
print("*arcs")

with open("watershed-s-directedgraph.txt", "r") as ins:
    for line in ins:
        if not flag:
            flag = True
            continue

        temp = line[:-1].split(" ")
        # temp.pop(-1)
        print(temp[0],temp[1])
