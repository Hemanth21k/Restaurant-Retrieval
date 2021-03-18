# Restaurant Retrieval
by Hemanth Pasupuleti 

A search engine that retrieves popular restaurants based on the dishes. It retrieves best restaurants for a given dish (user query) based on user reviews and menu.

### Reading the dataset
I have used [Zomato Bangalore Restaurants](https://www.kaggle.com/himanshupoddar/zomato-bangalore-restaurants) dataset for this project.
Since the dataset which is in **.csv** is very huge we cannot load it on memory at once. 
<code>reading.py</code>loads the **.csv** file row by row where each row refers to a single restaurant and saves the rows as **.json** file in **dataset/** folder.

### Indexing
The indexing of the documents is done by creating a inverted index on the documents and its terms. <code>stemmer.py</code> implements the [PorterStemmer2](http://snowball.tartarus.org/algorithms/english/stemmer.html) algorithm to reduce the index size. The <code>indexer.py</code> uses the <code>stemmer.py</code> and <code>stopwords.txt</code> to stem the words, remove the stopwords and create a posting list in **postlist** directory.
There are a total of **51717** rows i.e. 51717 documents in the dataset folder. 
<code>indexer.py</code> creates one posting list for every **13000** documents.
After indexing we can use <code>merger.py</code> to merge small posting lists into one large posting list.

### Tf-Idf 
<code>tfidf.py</code> retrieves the documents based up on their tf-idf score.
The term frequency score can be defined as <code> *tf(t,d) = log(1+freq(t,d))* </code> where freq(t,d) is the frequency of term t occuring in document d.
The inverse document frequency can be defined as <code>*idf(t,D) = log(N/(1+freq(t,D)))*</code> where N is the total number of documents and freq(t,D) is the number of documents containing the term t.

So finally the tf-idf score can be defined as <code>**tfidf(t,d) = tf(t,d) * idf(t,D)**</code> and the top 10 results will be displayed.

### BM25 model
<code>BM25.py</code> implements **Okapi BM25** ranking function. 
For a given query Q containing terms q1,q2,q3 and so on.. the BM25 score for the document D can be defined as:

![BM25 score](https://wikimedia.org/api/rest_v1/media/math/render/svg/8624885ce5cd14936807927801f6d29c315d3828)

*Image source: https://en.wikipedia.org/wiki/Okapi_BM25*

where f(qi,D) is term frequency, |D| is length of document in words, avgdl is the average length of documents in the collection. k and b are free parameters that can be passed but usually k will be drawn in between 1.2 and 2, while b is set as 0.75.

### Pseudo Relevance Feedback
<code>BM25\_PRF\_Rocchio.py</code> implements the [Pseudo Relevance feedback](https://nlp.stanford.edu/IR-book/html/htmledition/pseudo-relevance-feedback-1.html) by considering the top 10 retrieved documents as relevant. 
[Rocchio Algorithm](https://nlp.stanford.edu/IR-book/html/htmledition/the-underlying-theory-1.html) has been used to conduct the pseudo relevance feedback.
