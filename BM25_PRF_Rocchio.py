import re
import numpy as np
import json
from stemmer import PorterStemmer2
import time

p_start = time.time()
invertedIndex = {}
stopwords = []
N = 51717
docLen = {}
PS2 = PorterStemmer2()
queryVec = {}
dataPath = "dataset/"

def get_stopwords(fname):
    stopwrd_file = open(fname,"r+")
    stopwrd_text = stopwrd_file.read()
    stopwords = stopwrd_text.split("\n")
    return stopwords


def get_indices(fname):
    total_count = 0
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
            idf = np.log10(1+((N-int(word[1])+0.5)/(0.5+int(word[1]))))
            pl = eval(t[1])
            for k,v in enumerate(pl):
                if v in docLen.keys():
                    docLen[v] += pl[v]
                else:
                    docLen[v] = pl[v]
                total_count += pl[v]
                pl[v] = 1+np.log10(pl[v])
            
            invertedIndex[word[0]] = [idf,pl]
    global avgDl
    avgDl = total_count


def filter_query(query_tokens):
    global queryVec
    queryVec = {}
    PS2 = PorterStemmer2()
    for term in query_tokens:
        word = PS2.stem(term)
        if word in stopwords:
            continue
        else:
            if word in queryVec:
                queryVec[word]+=1
            else:
                queryVec[word] = 1
            
    
def getdata(filename):
    with open(filename,'r') as f:
        data = json.load(f)
        f.close()
        yield data['dish_liked'],data['menu_item'],data["rest_type"],data["cuisines"],data["reviews_list"]

def search_query(query,case):
    result = {}
    doc = {}
    if case == 0:
        token_q =  query.split(" ")
        filter_query(token_q)
        localQvec = queryVec
    else:
        localQvec = query
    k = 1.2
    b = 0.75
    for i,token in enumerate(localQvec):
        if token in invertedIndex:
            pl = invertedIndex[token]
            for k,v in enumerate(pl[1]):
                tf = pl[1][v]
                numer = pl[0] * ((k+1)*tf)
                fac = k*(1-b+(b*(docLen[v]/avgDl))) + tf
                sQ_D = numer/fac
                if v in doc.keys():
                    result[v] += sQ_D 
                else:
                    result[v] = sQ_D 

    return dict(sorted(result.items(), key=lambda item: item[1],reverse = True))


def print_docs(docs):
    names_presented = set()
    outDoc = 0
    for i,key in enumerate(docs):
        if outDoc >= 10:
            break
        fname = dataPath + key + ".json"
        f = open(fname,'r')
        data = json.load(f)
        if data['name'] in names_presented:
            continue
        print("DocID: ",key," Score: ",docs[key])
        print("Name: "+data['name'] + "\n" + "URL: "+
              data["url"]+"\n"+"Rating: "+data["rate"])
        names_presented.add(data['name'])
        outDoc +=1
        print("\n\n---------------------------------------------------------\n\n")


    
def get_vectors(docs,query):
    total = {}
    n = 0
    for i,k in enumerate(docs):
        for obj in getdata(dataPath + k + ".json"):
            x=[]
            for data in obj:
                x.extend(re.findall("[a-zA-Z]+", data))
    
        for w in x:
            word = PS2.stem(w.lower())
            if word in invertedIndex:
                if word in total:
                    if i < len(total[word]):
                        total[word][i] += 1
                    else:
                        for k in range(i+1-len(total[word])):
                            total[word].append(0)
                        total[word][i]+=1
                else:
                    total[word] = [0 for t in range(i+1)]
                    total[word][i] += 1
        n+=1
        if n == 10:
            break
    classes = []
    vectors = np.zeros((len(docs),len(total)))
    for i,key in enumerate(total):
        classes.append(key)
        curr = total[key]
        vectors[:len(curr),i] = curr
    queryVec = np.zeros((1,len(total)))
    for term in query:
        for i,k in enumerate(total):
            if term == k:
                queryVec[0,i]+=1
    return classes,vectors,queryVec
    


def do_PRF(docs):
    alpha = 1
    beta = 0.75
    total = {}
    outQueryVec = {}
    n = 0
    for i,k in enumerate(docs):
        for obj in getdata(dataPath + k + ".json"):
            x=[]
            for data in obj:
                x.extend(re.findall("[a-zA-Z]+", data))
    
        for w in x:
            word = PS2.stem(w.lower())
            if word in invertedIndex:
                if word in total:
                    total[word] +=1
                else:
                    total[word] = 1
        n+=1
        if n == 10:
            break
    for i,key in enumerate(total):
        if key in queryVec:
            outQueryVec[key] = alpha*queryVec[key] + beta*(total[key]/n)
        else:
            outQueryVec[key] = beta*(total[key]/n)

    afterPRFdocs = search_query(outQueryVec,1)
    print_docs(afterPRFdocs)
            
    
    
    


    
print("\n...Please wait while we set things up for you...\n")
stopword_start = time.time()
stopwords = get_stopwords("stopwords.txt")
print("\nTook ",time.time()-stopword_start," to read stopwrds..\n")
ind_start = time.time()
##get_indices("postlist/merged.txt")
get_indices("postlist with reviews/merged_2_excluded.txt")
print("Indexing took: ",time.time()-ind_start,"time\n")
print("Number of tokens present in the dictionary: ",len(invertedIndex))
print("\n...Loaded... You can give your query now...\n")
query = input("Give your query input: ")
print("------- Given Query ------\n",query,"\nResults:\n")
search_time = time.time()
sorted_result = search_query(query,0)
print_docs(sorted_result)
print("Searching and sorting result took: ",time.time()-search_time,"\n")
print("Took ",time.time()-search_time," to search query and retrieve docs...")
prf_start = time.time()
print("\n...Starting Pseudo Relevance Feedback...\n")
do_PRF(sorted_result)
print("\nPseudo Relevance Feedback took ",time.time()-prf_start,"secs...\n")
print("Total time elapsed: ",time.time()-p_start)
        
    
    










        
