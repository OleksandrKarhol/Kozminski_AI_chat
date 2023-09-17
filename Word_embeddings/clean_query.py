import pandas as pd 
import numpy as np 
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
nltk.download('stopwords')
from nltk.stem import WordNetLemmatizer
nltk.download("wordnet")
nltk.download("omw-1.4")


# remove punctuation
def remove_punct(line):
    line_no_punct = line.translate(str.maketrans("", "", string.punctuation))
    return line_no_punct

# tokenization 
def tokenize_text(line):
    word_tokens = word_tokenize(line)
    return word_tokens

# lowercase data 
def lowercase_text(line):
    new_line = [word.lower() for word in line]
    return new_line

# remove strop words
def remove_stop_words(line):
 
    stop_words = set(stopwords.words('english'))
    new_sentence = [w for w in line if not w.lower() in stop_words]
    return new_sentence
   
# Lemmitization
wnl = WordNetLemmatizer()
def lemitization(sentence):

    new_sentence = []
    for word in sentence:
        word = wnl.lemmatize(word, pos="v")
        new_sentence.append(word)
    return new_sentence

# Join the tokens back into a string
def join_tokens(line):
    processed_text = ' '.join(line)
    return processed_text

# bring all together 
def preprocess_text(text):
    text = remove_punct(text)
    text = tokenize_text(text)
    text = lowercase_text(text)
    text = remove_stop_words(text)
    text = remove_stop_words(text)
    text = lemitization (text)
    text = join_tokens(text)
    return text 
