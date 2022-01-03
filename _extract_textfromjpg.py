import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import requests, re, json, time, random, csv, os, datetime, lxml, glob, cv2, imutils, subprocess, pytesseract, operator, multiprocessing
from bs4 import BeautifulSoup as bs
from PIL import Image
from pytesseract import image_to_string
from pdf2image import convert_from_path
from itertools import combinations, tee
from joblib import Parallel, delayed
from tqdm import tqdm
import multiprocessing as mp
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.util import ngrams
from datetime import datetime
from ast import literal_eval   
from timeit import timeit

def write_json_tofile(response,outfilename):
    with open(outfilename,"a") as f:
        f.write(json.dumps(response)+'\n')
        
def read_jsoncsv(fname):
    with open(fname,'r') as f:
        jobs = [json.loads(x) for x in f.readlines()]
    return jobs

def extract_pdftexts_fromjpgs(pimages,pdftexts_outfile):
    for pimage in pimages:
        try:
            text = image_to_string(cv2.imread(pimage), lang='eng')
            write_json_tofile({pimage:text.strip()},pdftexts_outfile)
        except Exception as err:
            write_json_tofile({pimage:str(err)},pdftexts_outfile)
            continue

def update(*a):
    pbar.update()
            
mainpath = str(os.getcwd())+'/'
imagefiles = glob.glob(mainpath + 'data/images/*/*.jpg')
pdftexts_outfile = mainpath + 'output/pdftexts.csv'

# extract_pdftexts_fromjpgs(imagefiles,pdftexts_outfile)

n = 100
outfilechunks = [imagefiles[i * n:(i + 1) * n] for i in range((len(imagefiles) + n - 1) // n )] 
print(len(outfilechunks))

pool = mp.Pool(processes=8)
pbar = tqdm(outfilechunks)
    
for i in range(pbar.total):
    pool.apply_async(extract_pdftexts_fromjpgs, args=(outfilechunks[i],pdftexts_outfile), callback=update)
    
pool.close()
pool.join()