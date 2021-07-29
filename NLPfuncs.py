import html
import nltk
import re
from unicodedata import normalize
from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize
from nltk.corpus import wordnet
from nltk.corpus import stopwords

from gensim.models import Phrases
from gensim.models.phrases import Phraser
from gensim.corpora.dictionary import Dictionary
from gensim.models.ldamulticore import LdaMulticore
from gensim.models.tfidfmodel import TfidfModel
from gensim.models import word2vec
import multiprocessing

def lemmatize_word(tagged_token):
    """
    Returns lemmatized word given  its tag
    """
    #create Lemmatizer object
    lemma = WordNetLemmatizer()
    
    root = []
    
    for token in tagged_token:
        tag = token[1][0]
        word = token[0]
        
        if tag.startswith('J'):
            root.append(lemma.lemmatize(word,wordnet.ADJ))
        
        elif tag.startswith('V'):
            root.append(lemma.lemmatize(word,wordnet.VERB))
        
        elif tag.startswith('N'):
            root.append(lemma.lemmatize(word,wordnet.NOUN))
        
        elif tag.startswith('R'):
            root.append(lemma.lemmatize(word,wordnet.ADV))
            
        else:
            root.append(word)
        
    return root
    
    
def lemmatize_doc(document):
    """
    Tags words and returns lemmatized words
    """
    lemmatized_list = []
    tokenized_sentence = sent_tokenize(document)
    
    for sentence in tokenized_sentence:
        no_punctuation = re.sub(r"[`' \",.!()?]", " ",sentence)
        tokenized_word = word_tokenize(no_punctuation)
        tagged_token = pos_tag(tokenized_word)
        lemmatized = lemmatize_word(tagged_token)
        lemmatized_list.extend(lemmatized)
    
    return " ".join(lemmatized_list)
    

def clean_text(data, col):
    pattern = r"[^\w\s]"
    remove_accent = lambda text: normalize("NFKD",
                                           text).encode("ascii",
                                                                'ignore').decode("utf-8","ignore")
    data[col] = data[col].apply(remove_accent)
    data[col] = data[col].str.replace(pat=pattern,repl=" ",regex=True)
    data[col] = data[col].str.lower()
    
    return data
    
    
def remove_stop_words(data,col):
    
    stop_words = stopwords.words("english")
    stop_words = [word.replace("\'", "") for word in stop_words]
    
    rm_stopwords = lambda row: " ".join([token for token in row.split(" ") \
                                        if token not in stop_words])
    
    data[col] = data[col].apply(rm_stopwords)
    
    return data, stop_words
    

def remove_extra_spaces(data, col):
    """
    use regular expressions to ensure we never get more
    than a single whitespace to separate words in our sentences.
    """
    pattern = r"[\s]+"
    data[col] = data[col].str.replace(pat=pattern,repl=" ",regex=True)

    return data

def get_tokens(data, col):
    
    """
    transform text into an ordered list of words.
    ** The process of tokenization –
    the document is broken down into individual words or tokens
    """
    
    corpora = data[col].values
    tokenized_text = [corpus.split(" ") for corpus in corpora]
    
    return tokenized_text
    
