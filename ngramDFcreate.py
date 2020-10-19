from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pandas as pd
import csv
import re
from collections import Counter
from nltk import ngrams

stream_stopwords = ['list','of','custom','stopwords']
lemmatizer = WordNetLemmatizer()
tokenizer = RegexpTokenizer(r'\w+')
stop_words = stopwords.words('english')
stop_words_list = list(set(stop_words + stream_stopwords))

filepath = 'PATH/TO/PROJECT/FOLDER/'
df = pd.read_csv(filepath + 'CSV_INFILE.csv',sep='\t',dtype=str)

def remove_url(txt):
    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", str(txt)).split())

def clean_text(text, stop_words_list):
    if text:
        no_urls = remove_url(text)
        no_xrtalines = no_urls.replace('\n','')
        only_alphanum = re.sub(r'[A-Z]+(?![a-z])', '', no_xrtalines)
        no_nums = re.sub(r'\d+', '', only_alphanum)
        clean_list = [i.lower() for i in tokenizer.tokenize(no_nums)]
        lemmatized_list = [lemmatizer.lemmatize(x) for x in clean_list]
        no_stops = [word for word in lemmatized_list if not word in stop_words_list]
    else:
        no_stops = ['']
    return ' '.join(no_stops)

def format_ngram_counter(n_grams):
    plist = []
    for x in n_grams:
        value = n_grams[x]    
        num_ngrams =range(len(x))
        terms = ', '.join([x[i] for i in num_ngrams])
        ntype = str(len(x))
        xlist = [terms,value,ntype]
        plist.append(xlist)
    pdf = pd.DataFrame(plist,columns = ['ngrams','count','type'])  
    return pdf

def text_ngram_process(texts):
    token = nltk.word_tokenize(texts)
    bigrams = format_ngram_counter(Counter(ngrams(token,2)))
    trigrams = format_ngram_counter(Counter(ngrams(token,3)))
    fourgrams = format_ngram_counter(Counter(ngrams(token,4)))
    fivegrams = format_ngram_counter(Counter(ngrams(token,5)))
    frames = [bigrams,trigrams,fourgrams,fivegrams]
    ngram_df = pd.concat(frames)
    return ngram_df

df['clean_text'] = df['text'].apply(lambda x: clean_tweet(x, stop_words2))
texts = df['clean_text'].tolist()
ngram_df = text_ngram_process(' '.join(texts))
ngram_df.sort_values(by='count', ascending=False,inplace=True)
ngram_df.to_csv(filepath +'NGRAM_DF_OUTFILE.csv', sep='\t',index=False, quoting=csv.QUOTE_ALL)