import re
import numpy as np
import json
from stemmer import PorterStemmer2
import time

p_start = time.time()
invertedIndex = {}
stopwords = []
N = 51717

query = input("Give your query: ")

def get_stopwords(fname):
    stopwrd_file = open(fname,"r+")
    stopwrd_text = stopwrd_file.read()
    stopwords = stopwrd_text.split("\n")
    return stopwords


def get_indices(fname):
    file = open(fname,"r+")
    text = file.read()
    lines = text.split("\n")
    for line in lines:
        t = line.split("==>")
        if t[0] == '':
            continue
        word = t[0].split("[")
        if word[0] not in stopwords:
            word[1] = word[1].strip("] ")
            idf = np.log10(N/(1+int(word[1])))
            pl = eval(t[1])
            for k,v in enumerate(pl):
                pl[v] = (1+np.log10(pl[v]))*(idf)
            
            invertedIndex[word[0]] = pl


def filter_query(query_tokens):
    l = len(query_tokens)
    i = 0
    PS2 = PorterStemmer2()
    while i < l:
        query_tokens[i] = PS2.stem(query_tokens[i])
        if query_tokens[i] in stopwords:
            query_tokens.pop(i)
            l -=1
        i+=1
    


def search_query(query):
    result = {}
    token_q =  query.split(" ")
    doc = {}
    filter_query(token_q)
    
    for i in range(len(token_q)):
        if token_q[i] in invertedIndex.keys():
            pl = invertedIndex[token_q[i]]
            for k,v in enumerate(pl):
                if v in doc.keys():
                    result[v].append(pl[v])
                else:
                    result[v] = [pl[v]]
    return dict(sorted(result.items(), key=lambda item: item[1],reverse = True))



stopword_start = time.time()
stopwords = get_stopwords("stopwords.txt")
print("\nTook ",time.time()-stopword_start," to read stopwrds..\n")
ind_start = time.time()
get_indices("postlist/merged.txt")
print("Indexing took: ",time.time()-ind_start,"time\n")
print("Number of tokens present in the dictionary: ",len(invertedIndex))
print("------- Given Query ------\n",query,"\nResults:\n")
search_time = time.time()
print("Loaded the indexing file.....\n")
sorted_result = search_query(query)
print("Searching and sorting result took: ",time.time()-search_time,"\n")
names_presented = []
outDoc = 0
dataPath = "dataset/"
for i,key in enumerate(sorted_result):
    if outDoc >= 10:
        break
    fname = dataPath + key + ".json"
    f = open(fname,)
    data = json.load(f)
    if data['name'] in names_presented:
        continue
    print(key)
    print("Name: "+data['name'] + "\n" + "URL: "+
          data["url"]+"\n"+"Rating: "+data["rate"])
    names_presented.append(data['name'])
    outDoc +=1
    print("\n\n---------------------------------------------------------\n\n")
    
    
print("Took ",time.time()-search_time," to search query and retrieve docs...")
print("Total time elapsed: ",time.time()-p_start)
        
    
    










        
