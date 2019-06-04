

genedata = []
genecategorydata = {}
genecategorydata['healthy'] = {} #{'gene' : count[]}
genecategorydata['tumor-cardia'] = {}
genecategorydata['tumor-non-cardia'] = {}


flag = True

output = open('testoutput.csv', 'w')

with open("gastro_3class.arff", "r") as ins:
    for line in ins:
        # print(line)
        if(flag):
            temp = line.split("\t")
            # temp.pop(-1)
            if(len(temp) == 3):
                # print(temp[1])
                genedata.append(temp[1])


        if(not flag):

            temp = line.split(",")
            category = temp[-1][:-1]
            temp.pop()
            for idx,val in enumerate(temp):
                genecategorydata[category][genedata[idx]].append(val)

        if(line[:5] == "@DATA"):
            genedata.pop()
            for gene in genedata:
                genecategorydata['healthy'][gene] = []
                genecategorydata['tumor-cardia'][gene] = []
                genecategorydata['tumor-non-cardia'][gene] = []
                
            flag = False


for gene in genedata:
    for val in genecategorydata['tumor-cardia'][gene]:
        output.write(val+',')
    output.write('\n')

output.close()