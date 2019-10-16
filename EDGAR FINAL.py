# -*- coding: utf-8 -*-
"""EDGAR v2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1z08EcegyKZBBMJXqrD46b1jBFpBSssqA
"""

from textblob import TextBlob
import nltk
nltk.download('punkt')

!pip install edgar
import edgar

import pandas as pd
import numpy as np
from google.colab import files  
files.upload() # Ensure the file is in the following format Date (yyyy-mm-dd) Company CIK DOC. The Edgar company name matches the one in the spreadsheet.

rawdata = pd.ExcelFile ("EDGAR (1).xlsx")
df = pd.read_excel(rawdata)
df

dates = df['DATE']
dates

companies = df['COMPANY']
companies

ciks = df['CIK']
ciks

docs = df['DOC']
docs

dfout = pd.DataFrame(columns=['DATE', 'CIK', 'DOC' , 'POLARITY' , 'SUBJECTIVITY'])
dfnull = pd.DataFrame(columns=['DATE', 'CIK', 'DOC'])
dfout
dfnull

itlen = len(df.index)
for x in range(itlen):
  company = edgar.Company(str(companies[x]), str(ciks[x]))
  tree = company.getAllFilings(filingType = str(docs[x]), priorTo = str(dates[x]))
  filings = edgar.getDocuments(tree, noOfDocuments=1)
  filingstr = str(filings)
  article = TextBlob(filingstr)
  articlepolarity = article.sentiment.polarity
  articlesubjectivity = article.sentiment.subjectivity
  if(articlepolarity != 0 and articlesubjectivity != 0):
    dfout = dfout.append({'DATE': dates[x], 'CIK': ciks[x], 'DOC': docs[x], 'POLARITY' : articlepolarity, 'SUBJECTIVITY' : articlesubjectivity}, ignore_index = True)
  if(articlepolarity == 0 and articlesubjectivity == 0):
    dfnull = dfnull.append({'DATE' : dates[x], 'CIK' : ciks[x], 'DOC' : docs[x]}, ignore_index = True)

dfout

dfnull

company = edgar.Company("Oracle Corp", "0001341439")
tree = company.getAllFilings(filingType = "10-K", priorTo = '2017-12-31')
filings = edgar.getDocuments(tree, noOfDocuments=1)

dfout = dfout.append({'DATE': , 'CIK': , 'DOC': , 'POLARITY' : , 'SUBJECTIVITY' : }, ignore_index=True)