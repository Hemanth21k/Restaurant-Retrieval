import re


outFile = "postlist/output"
outCount = 13000
outI = 1
Indexer = {}
print("\nStarting to merge...")
while outI < 5:
    outF = outFile+str(outI*outCount)+".txt"
    print("Opening ",outF,"\n")
    file = open(outF,"r+")
    text = file.read()
    lines = text.split("\n")
    for line in lines:
        t = line.split("==>")
        if t[0] == '':
            continue
        word = t[0].split("[")
        term = word[0]
        df =  int(word[1].strip("] "))
        post_list = eval(t[1])
        if term in Indexer:
            Indexer[term][1] = {**Indexer[term][1],**post_list}
            Indexer[term][0] += df
        else:
            Indexer[term] = [df,post_list]
    outI+=1
    print("Done reading ",outF,"\n")
    

merged_file = "postlist/merged.txt"
with open(merged_file,"w") as merge:
    for index,key in enumerate(Indexer):
        matter = key+"["+str(Indexer[key][0])+"] ==>"+str(Indexer[key][1])+"\n"
        merge.write(matter)
    merge.close()

print("\n --- Merge done Successfully!!! --- \n")
        
    

