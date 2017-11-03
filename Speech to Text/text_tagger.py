import treetaggerwrapper
from nltk import word_tokenize
from nltk.corpus import stopwords


def process_text(text):
    """Return the text as list of tagged words removing italian stopwords"""
    text = text.lower()
    tokens = word_tokenize(text)
    temp = []
    for x in tokens:
        if not x.isdigit() and not x in stopwords.words('italian'):
            temp.append(x)

    #se vuoi usare il LEMMA
    appoggio = ""
    tok = []
    for x in temp:
        appoggio = appoggio + " " + x
    #print appoggio
    tagger = treetaggerwrapper.TreeTagger(TAGLANG='it')
    tags = tagger.tag_text(unicode(appoggio))
    #print tags
    tags2 = treetaggerwrapper.make_tags(tags)
    #print tags2
    for ind in tags2:
        L = ind[2]
        tok.append(L)
    return tok
