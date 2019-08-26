
import re

flag = False

name = "output_gastro_all_tnc_signed_60.txt"
threshold = [30]

outputfiles = []
outputfiles.append(name + ".dot") #[ name + str(i) + ".dot" for i in threshold]
inputfiles = []
inputfiles.append(name) #[ name + str(i) + ".txt" for i in threshold]
filestowrite=[]

for output in outputfiles:
    filestowrite.append(open(output, 'w'))

for files in filestowrite:
    files.write("graph anyrelation {\n" + "overlap = false;\n" + "\n")

# print("""
# graph anyrelation {
#     overlap = false;

# """)
ctr = 0
for idx, inputfile in enumerate(inputfiles):

    with open (inputfile, "r", encoding = "utf-8") as ins:
        for line in ins:
            # print(line)
            if ctr < 7:
                ctr += 1
                # print(ctr)
                continue

            temp = line.split(" ")
            # print(temp)
            temp[-1] = temp[-1][:-1]
            color = "blue"
            # print(temp)
            if temp[2] == "1":
                color = "blue"
            elif temp[2] == "-1":
                color = "red"
            filestowrite[idx].write("\"" + temp[0] + "\"" + " -- " + "\"" + temp[1] + "\"" + " [color=" + color + ", penwidth=1]\n")
            # print("\"" + temp[0] + "\"" + " -- " + "\"" + temp[1] + "\"" + " [color=" + color + ", penwidth=1]")
    flag = False
    print(idx)

for files in filestowrite:
    files.writelines(["\n", "}\n"])
    files.close()
