
import re

flag = False

print("*Vertices 120")
for i in range(0,120):
    print(i,"\"" + str(i) + "\"")

print()
print("*arcs")

with open("signedgenerated10_2.txt", "r") as ins:
    for line in ins:
        if not flag:
            flag = True
            continue

        temp = line[:-1].split(" ")
        temp.pop(-1)
        print(temp[0],temp[1])
