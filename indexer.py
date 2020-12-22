
import re
import json
from stemmer import PorterStemmer2
import time

start = time.time()


class Trie:
    def __init__(self):
        self.child = dict()
    
    def insert(self,word):
        end = '_end_'
        curr_dict = self.child
        for letter in word:
            curr_dict = curr_dict.setdefault(letter,{})
        curr_dict[end] = {'post_list':PostingList()}
    
    def search(self,word):
        end = '_end_'
        curr_dict = self.child
        for letter in word:
            if letter not in curr_dict:
                return 0
            curr_dict = curr_dict[letter]
        if end in curr_dict:
            return curr_dict[end]
        else:
            return 0
    
    

class PostingList:
    def __init__(self):
        self.docfreq = 0
        self.postlist = dict()
    def update(self,docid):
        if docid in self.postlist.keys():
            self.postlist[docid]+=1    
        else:
            self.postlist.setdefault(docid,1)
            self.docfreq += 1

        
        
        
def list_words(trie):
    my_list = []
    for k,v in trie.items():
        if k != '_end_':
            for el in list_words(v):                
                my_list.append(k+el)
        else:
            my_list.append('')
    return my_list
       
       
def printall(words):
    
    for word in words:
        ps = dic.search(word)
        matter =word+"["+str(ps["post_list"].docfreq)+"] ==>"+str(ps["post_list"].postlist)+"\n"
        print(matter)
       # output.write(matter)    
                


def getdata(filename):
    with open(filename,'r') as f:
        data = json.load(f)
        f.close()
        global reviews
        reviews = data["reviews_list"]
        yield data['dish_liked'],data['menu_item'],data["rest_type"],data["cuisines"]

def get_stopwords(fname):
    stopwrd_file = open(fname,"r+")
    stopwrd_text = stopwrd_file.read()
    stopwords = stopwrd_text.split("\n")
    return stopwords


dic = Trie()    #defining a trie
reviews = ""
stopwords = []

PS2 = PorterStemmer2()

curr_file = 1

curr_dir = "dataset/"
outFile = "postlist/output"
outCount = 13000
outI = 1


stopwords = get_stopwords("stopwords.txt")

while(curr_file<=51717):
    file = curr_dir+str(curr_file)+".json"
    for obj in getdata(file):
        x=[]
        for data in obj:
            x.extend(re.findall("[a-zA-Z0-9]+", data))
##    print(x)
    for w in x:
        word = w.lower()
        word_stem = PS2.stem(word)
        if word_stem in stopwords:
            continue
        word = word_stem
        if word == "person":
            print(curr_file)
            break
        temp = dic.search(word)
        if temp: 
            temp['post_list'].update(str(curr_file))
        else:
            dic.insert(word)
            temp =dic.search(word)
            temp['post_list'].update(str(curr_file))
    review_tokens = re.findall("\w[a-zA-Z]+", reviews)
##    print(review_tokens)
    for tok in review_tokens:
        rev_token = tok.lower()
        cRevTok = PS2.stem(rev_token)
        if cRevTok in stopwords:
            continue
        tempTokPath = dic.search(cRevTok)
        if tempTokPath:
##            print(cRevTok)
            tempTokPath['post_list'].update(str(curr_file))
    curr_file+=1

   if curr_file%outCount == 0 or curr_file == 51717:
       outF = outFile+str(outI*outCount)+".txt"
       with open(outF,"w") as f:
           for word in list_words(dic.child):
               ps = dic.search(word)
               matter =word+"["+str(ps["post_list"].docfreq)+"] ==>"+str(ps["post_list"].postlist)+"\n"
               f.write(matter)
       f.close()
       outI+=1
       try:
           del dic
       finally:
           dic = Trie()
            
    
print("Took ",time.time()-start,"secs to index all docs")


    


