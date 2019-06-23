
import re

flag = False

print("""
graph anyrelation {
    overlap = false;

""")

with open ("healthy-signed-00217.txt", "r") as ins:
    for line in ins:
        if not flag:
            flag = True
            continue
        temp = line.split(" ")
        temp[-1] = temp[-1][:-1]
        color = "blue"
        if temp[2] == "1":
            color = "blue"
        elif temp[2] == "-1":
            color = "red"
        print("\"" + temp[0] + "\"" + " -- " + "\"" + temp[1] + "\"" + " [color=" + color + ", penwidth=1]")


print()
print("}")