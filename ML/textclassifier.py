import json #for data
import pandas as pd
import numpy as np
## for plotting
import matplotlib.pyplot as plt
import seaborn as sns
## for processing
import re
import nltk
## for bag-of-words
from sklearn import feature_extraction, model_selection, naive_bayes, pipeline, manifold, preprocessing
## for explainer
from lime import lime_text
## for word embedding
#import gensim
#import gensim.downloader as gensim_api
## for deep learning
#from tensorflow.keras import models, layers, preprocessing as kprocessing
#from tensorflow.keras import backend as K
## for bert language model
#import transformers
import pickle
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import Perceptron, PassiveAggressiveClassifier, SGDClassifier
#from sklearn.ensemble import RandomForestClassifier
import string
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
'''
fig, ax = plt.subplots()
fig.suptitle("y", fontsize=12)
dtf["label_maj"].reset_index().groupby("label_maj").count().sort_values(by= 
       "index").plot(kind="barh", legend=False, 
        ax=ax).grid(axis='x')
plt.show()
'''

'''
Preprocess a string.
:parameter
    :param text: string - name of column containing text
    :param lst_stopwords: list - list of stopwords to remove
    :param flg_stemm: bool - whether stemming is to be applied
    :param flg_lemm: bool - whether lemmitisation is to be applied
:return
    cleaned text
'''
def utils_preprocess_text(text, flg_stemm=False, flg_lemm=True, lst_stopwords=None):
    ## clean (convert to lowercase and remove punctuations and characters and then strip)
    text = re.sub(r'[^\w\s]', '', str(text).lower().strip())
            
    ## Tokenize (convert from string to list)
    lst_text = text.split()
    ## remove Stopwords
    if lst_stopwords is not None:
        lst_text = [word for word in lst_text if word not in 
                    lst_stopwords]
                
    ## Stemming (remove -ing, -ly, ...)
    if flg_stemm == True:
        ps = nltk.stem.porter.PorterStemmer()
        lst_text = [ps.stem(word) for word in lst_text]
                
    ## Lemmatisation (convert the word into root word)
    if flg_lemm == True:
        lem = nltk.stem.wordnet.WordNetLemmatizer()
        lst_text = [lem.lemmatize(word) for word in lst_text]
            
    ## back to string from list
    text = " ".join(lst_text)
    return text

def text_classify():
    dtf = pd.read_csv('Combined_Dataset.csv', usecols=["message", "label_maj"])

    #For shuffling the entire dataframe in-place 
    #dtf = dtf.sample(frac=1).reset_index(drop=True)

    #if not nltk.corpus.stopwords.words('english'):
    nltk.download('stopwords')
    #if not nltk.wordnet:
    nltk.download('wordnet')
    nltk.download('words')

    lst_stopwords = nltk.corpus.stopwords.words("english")
    dtf["message"] = dtf["message"].apply(lambda x: 
            utils_preprocess_text(x, flg_stemm=False, flg_lemm=True, 
            lst_stopwords=lst_stopwords))

    dtf_train, dtf_test = model_selection.train_test_split(dtf, test_size=0.25)
    ## get target
    y_train = dtf_train["label_maj"].values
    y_test = dtf_test["label_maj"].values

    ## Count (classic BoW)
    #vectorizer = CountVectorizer(ngram_range=(1,2))

    ## Tf-Idf (advanced variant of BoW)
    #vectorizer = online_vectorizer.OnlineTfidfVectorizer(max_features=5000, ngram_range=(1,2))

    vectorizer = TfidfVectorizer(max_features=50000, ngram_range=(1,2))


    corpus = dtf_train["message"]
    X_train = vectorizer.fit_transform(corpus)
    X_test = vectorizer.transform(dtf_test["message"])


    #lis=[]
    #lis.append(MultinomialNB())
    #Multinomial Naive Bayes is probably the weakest out of these with Tfidf
    #lis.append(Perceptron())
    #lis.append(PassiveAggressiveClassifier())
    #lis.append(SGDClassifier())
    #lis.append(RandomForestClassifier())
    #Random Forest Classifier is the strongest but is extremely slow, doesn't support online machine learning and may have overfitting

    classifier = SGDClassifier(alpha=0.000090)
    #classifier = PassiveAggressiveClassifier(max_iter=500)
    ## train classifier
    classifier.fit(X_train, y_train)
    pred=classifier.predict(X_test)
    print(classification_report(y_test, pred))
    print(confusion_matrix(y_test, pred))
    print(accuracy_score(y_test, pred))



    pickle.dump(classifier, open('model1.pkl','wb'))
    #pickle.dump(vectorizer, open('vec.pkl','wb'))

#text_classify()
