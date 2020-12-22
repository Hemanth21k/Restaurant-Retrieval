import csv
import json
import sys

maxInt = sys.maxsize

while True:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.

    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)


def getstuff(filename):
    with open(filename, "r") as csvfile:
        datareader = csv.reader(csvfile)
        try:
            yield next(datareader)  # yield the header row
        except StopIteration:
            print("\n..........Done saving to all files.........\n")
        for row in datareader:
            yield row
    
def getdata(filename):
    count = 0
    for row in getstuff(filename):
        if count == 0:
            header = row
        if count>0:
            temp = {}
            for i in range(len(header)):
                temp[header[i]] = row[i]
            filename = "dataset/"+str(count)+".json"
            with open(filename,"w") as outfile:
                json.dump(temp,outfile)
            temp.clear()
        if count%100 == 0:
            print("\nNow File:",count)
        count+=1



getdata("zomato.csv")


        
    

