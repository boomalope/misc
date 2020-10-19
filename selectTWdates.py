import pandas as pd
import csv

def read_bigfile(file, dates_to_keep):
    # function: selecting tweets from a very large .csv file using list of date strings. Only loads 10,000 lines into memory at a time, so it can quickly select the rows where the date strings match 'dates_keep' list
    dateCols = ['timestamp']
    frames = []
    for chunk in pd.read_csv(file,sep='\t', chunksize=chunksize):
        chunk2 = chunk[chunk['timestamp'].str.contains('|'.join(dates_to_keep))]
        frames.append(chunk2)
    df = pd.concat(frames)
    return df

folderpath = 'PATH/TO/BIGCSV/'
file = folderpath + 'BIG_CSV.csv'
chunksize = 10000
# example list of date strings:
dates_keep = ['Mon Sep 16', 'Tue Sep 17', 'Wed Sep 18', 'Thu Sep 19', 'Fri Sep 20', 'Sat Sep 21', 'Sun Sep 22']

tdf = read_bigfile(file,dates_keep)
tdf.to_csv(filepath +'SPECIFIC_DATES.csv', sep='\t',index=False, quoting=csv.QUOTE_ALL)