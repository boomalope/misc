import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import requests, re, json, time, random, csv, os, datetime, lxml, glob, cv2, imutils, subprocess, pytesseract
from bs4 import BeautifulSoup as bs
from PIL import Image
from pytesseract import image_to_string
from pdf2image import convert_from_path

def write_json_tofile(response,outfilename):
    with open(outfilename,"a") as f:
        f.write(json.dumps(response)+'\n')
        
def read_jsoncsv(fname):
    with open(fname,'r') as f:
        jobs = [json.loads(x) for x in f.readlines()]
    return jobs

def convert_tojpeg(pdffiles,imageoutfilepath):
    for i, pdffile in enumerate(pdffiles):
        pdfoutfilename = "pdfimage_"+str(pdffile.split('/')[-1].split('.pdf',1)[0])
        imageoutfolder = imageoutfilepath + pdfoutfilename + '/'
        os.mkdir(imageoutfolder)
        pages = convert_from_path(pdffile, 600)
        print(len(pages))
        for n, page in enumerate(pages):
            pimageoutfile = imageoutfolder+'page_'+str(n)+'_of_'+str(len(pages))+'__'+pdfoutfilename+'.jpg'
            page.save(pimageoutfile, 'JPEG')
        print(i)

mainpath = str(os.getcwd())+'/'
imageoutfilepath = mainpath + 'data/images/'

pdffiles = glob.glob(mainpath +'data/pdfs/*.pdf')
print(len(pdffiles))

# convert_tojpeg(pdffiles,imageoutfilepath)

n = 100
outfilechunks = [pdffiles[i * n:(i + 1) * n] for i in range((len(pdffiles) + n - 1) // n )] 
print(len(outfilechunks))

pool = mp.Pool(processes=8)
pbar = tqdm(outfilechunks)
    
for i in range(pbar.total):
    pool.apply_async(convert_tojpeg, args=(outfilechunks[i],imageoutfilepath), callback=update)
    
pool.close()
pool.join()