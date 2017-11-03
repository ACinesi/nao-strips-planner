import numpy as np
import string
import collections
from nltk import word_tokenize
from nltk.stem.snowball import ItalianStemmer
from nltk.corpus import stopwords
from sklearn.cluster import KMeans
from pprint import pprint
from matplotlib import pyplot
from rake_nltk import Rake
from gensim import utils
from gensim.models.doc2vec import LabeledSentence
from gensim.models import Doc2Vec
from nltk.corpus import wordnet 
import pprint
from nltk.corpus import wordnet_ic
import treetaggerwrapper
import numpy
import re
import string
import glob
from numpy import linalg as LA
from nltk.corpus import genesis

def process_text(text, stem=True):
    """ Tokenize text and stem words removing punctuation """
    intab = string.punctuation+"’“°»«”" #!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~   DA CONTROLLARE SE TOGLIERE LE LETTERE ACCENTATE
    outtab = "                                      "
    trantab = str.maketrans(intab, outtab)
    text = text.translate(trantab)
    text =" ".join(text.split())
    text= text.lower()
    tokens = word_tokenize(text)
    z=[]
    for x in tokens:
        if not x.isnumeric() and not x in stopwords.words('italian'):
            z.append(x)
 
    # if stem:
    #     stemmer = ItalianStemmer()
    #     tok = [stemmer.stem(t) for t in z]
    
    #se vuoi usare il LEMMA
    appoggio=""
    tok=[]
    for x in z:
        appoggio=appoggio+" "+x
    if stem:
        tagger = treetaggerwrapper.TreeTagger(TAGLANG='it')
        tags = tagger.tag_text(unicode(appoggio)
        tags2 = treetaggerwrapper.make_tags(tags)
        for ind in tags2:
            L=ind[2]
            tok.append(L)
    
 
    return tok


x=process_text("ciao mi piace molto mangiare la frutta")
print(x)