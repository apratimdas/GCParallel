

genedata = []
genecategorydata = {}
genecategorydata['healthy'] = {} #{'gene' : count[]}
genecategorydata['tumor-cardia'] = {}
genecategorydata['tumor-non-cardia'] = {}


flag = True


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

        if(line[:5] == "@DATA" or line[:5] == "@data"):
            genedata.pop()
            for gene in genedata:
                genecategorydata['healthy'][gene] = []
                genecategorydata['tumor-cardia'][gene] = []
                genecategorydata['tumor-non-cardia'][gene] = []
                
            flag = False


output1 = open('output_gastro_all_tnc', 'w')

for gene in genedata:
    for val in genecategorydata['tumor-non-cardia'][gene]:
        output1.write(val+',')
    output1.write('\n')

output1.close()


output2 = open('output_gastro_all_tcc', 'w')

for gene in genedata:
    for val in genecategorydata['tumor-cardia'][gene]:
        output2.write(val+',')
    output2.write('\n')

output2.close()


output3 = open('output_gastro_all_h', 'w')

for gene in genedata:
    for val in genecategorydata['healthy'][gene]:
        output3.write(val+',')
    output3.write('\n')

output3.close()

