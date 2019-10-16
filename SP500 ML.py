# -*- coding: utf-8 -*-
"""Assignment Instructions v1.1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1atTV-pyTJMR-s7N00pxEvJzPB9Zr9IbA

**Allen Baiju**

**You have succesfully created a machine-readable spreadsheet in Microsoft Excel. Now you will be building a model using the input variables for the Altman Z-Score in conjuction with the standard deviation of daily returns to predict the credit rating of stocks in the S&P 500 Index.**

*Each text and code block in this Jupyter Notebook environment is interactive and can be edited by double clicking on the desired cell. Once a code block is selected, click on the play button in the left margin of the block to run the code. Alternatively, you can press (Ctrl+Enter)/(Cmd+Enter).*

*This notebook is structed so that informational text blocks are placed ABOVE the code block which accompanies it. Read the text blocks to understand each subsequent code block, then run the code.*

*You will conduct exploratory data analysis and data visualization(s) to better understand the data prior to building a predictive model.*

The first line of code below allows you to import the pandas package with the identifier "pd" to reference functions found in the package. Pandas is a data analysis and visualization package which will best serve our purposes in this preliminary stage. *numpy* (NumPy) is a mathematical library allowing for the usage of multi-dimensional arrays and matrices. The next two lines of code are commonly used within Google Colaboratory to import files. After you run the first code block, you will be able to choose and upload a file here. Upload the final version of the spreadsheet which you created in Part 1 of the assignment.
"""

import pandas as pd
import numpy as np
from google.colab import files
files.upload()

"""The first line of code below creates a reference to the file you just uploaded. As you can see, my spreadsheet was titled "SP500 FINAL.xlsx" and I created the reference "rawdata". Google Colaboratory automatically highlights strings in your code, as shown by the red font applied to the text captured within the double quotes. The next line of code creates a reference for the dataframe created by the *pd.read_excel* function to which I entered my "rawdata" reference for the Excel file. The last line of code calls the reference which was just created. This is not a required step in completing the assignment but will display the dataframe in the Jupyter Notebook environment."""

rawdata = pd.ExcelFile ("SP500 FINALC.xlsx")
df = pd.read_excel(rawdata)
df

"""The first line of code below uses the *rename* function to change the name of the columns containing the standard deviation of daily returns and the credit ratings for readability purposes. Note the second argument inputted to the *rename* function: inplace. The inplace argument replaces the existing column header for a new header, in this case, *SDDR* and *CR*. The next line creates a duplicate dataframe with the reference "dfndnt" (for dataframe, no date, no ticker). The next two lines of code remove two columns which are not required to build a predictive model: *Date* and *Ticker*. The last line of code displays the new dataframe. Note that this format of creating duplicate dataframes per change allows you to recall any stage of your dataframe transformation. Calling "df" will display the original dataframe with all columns intact."""

df.rename(columns={'σ Daily Returns (Annualized)':'SDDR','S&P':'CR'},inplace = True)
df = df.drop(columns = "Date")
df = df.drop(columns = "Ticker")
df

"""To continue EDA, you will need to make sure all data is numeric. As the credit rating column still has string data, you will have to convert all the credit ratings into whole numbers. The rating dictionary defined below will assign the number *1* to the CC rating and implement an ascending increment by 1 for each asccending credit rating, blind to (+/-). This rating dictionary is referenced using *crnum* for 'credit rating number'."""

crnum = {'CC' : 1, 'CCC+' : 2, 'B-' : 3, 'B' : 3, 'B+' : 3, 'BB-' : 4,
        'BB' : 4, 'BB+' : 4, 'BBB-' : 5, 'BBB' : 5, 'BBB+' : 5,
        'A-' : 6, 'A': 6, 'A+' : 6, 'AA-' : 7, 'AA': 7, 'AA+': 7,
        'AAA' : 8}

"""The set of code below applies the newly created dictionary to the "CR" column of the total dataset. Here, *dfa* contains the whole, numeric dataset."""

dfa = df
dfa.CR = [crnum[entry] for entry in dfa.CR]
dfa

"""The set of code below creates a new dataset with reference "dff" containing solely the input variables (features) for the model."""

dff = dfa.drop(columns = "CR")     # dff is the features dataset (inputs for prediction)
dff

"""The set of code below creates a new dataset with reference "dfl" containing solely the outcome variable (labels) for the model."""

dfl = dfa.drop(columns = {"A", "B", "C", "D", "E", "SDDR"})     # dfl is the labels dataset (what is to be predicted -> credit score)
dfl

"""To construct a predictive model in Python, you will need the features and labels as arrays. They are currently dataframes. Prior to converting "dff" and "dfl" to arrays, you must perform a final data cleaning step. For both dataframes, drop any invalid values. As data cleaning was completed in Excel, this can be taken as a final check prior to model-building."""

dff.dropna()
dfl.dropna()

"""Now, convert the features dataframe and the labels dataframe to arrays."""

dffa = dff.values
dfla = dfl.values

"""The line of code below uses the *train_test_split*  to randomly split the data arrays into training and testing subsets. The inclusion of the random state parameter ensures that each time the code block is run, the kernel does not change and the randomization can be repeated. To call a new randomization, simply change the number to which the  random state is set. This number is functionally arbitrary; changing the number changes the randomization state so that different rows are placed in the training and testing sets for the model."""

from sklearn.model_selection import train_test_split
ftrain, ftest, ltrain, ltest = train_test_split(dffa, dfla, random_state = 13)

"""The first line of code below uses the *ravel* function to transform the column vector created by dropping columns from the original dataframe into a one-dimensional array for usage in the *sklearn* functions further on. The second line of code checks that there are no null vales in the original dataframe used to create the arrays; through all the null values have been dropped in data cleaning, this is a final check prior to inputting the arrays into the modeling functions."""

ltrain = ltrain.ravel()     # re-creates to 1d arrray from column vector
np.any(np.isnan(df))

"""The following code block implements a support vector machine for a multiple classification problem. The *SVC* function has many more parameters than those shown below; fine-tuning these parameters will ultimately yield the highest predictive accuracy. Below is a simple example of one of the many modelling options within the *sklearn* package."""

from sklearn.svm import SVC
svmlm = SVC(C = 1000000, kernel = 'rbf', gamma = 'scale', decision_function_shape = 'ovo').fit(ftrain, ltrain)
svmpred = svmlm.predict(ftest)
svmacc = svmlm.score(ftest, ltest)
print (svmacc)

"""The following code block implements a k-nearest neighbors model for a multiple classification problem. The *KNeighborsClassifier* function has many more parameters than those shown below; fine-tuning these parameters will ultimately yield the highest predictive accuracy. The *class weight* parameter is of particular interest as you can set the prediction function coefficients through the use of an array or dictionary."""

from sklearn.neighbors import KNeighborsClassifier 
knn = KNeighborsClassifier(n_neighbors = 3, weights = 'distance', p = 1).fit(ftrain, ltrain)
knnpred = knn.predict(ftest)
knnacc = knn.score(ftest, ltest)
print (knnacc)

"""This notebook has provided a methodology for data analysis and predictive model building. There are many more model types within the *sklearn* package which can be implemented for the dataset. Using the Python documentation for each model, try to maximize the prediction accuracy. Remember to use the *train_test_split* to randomly group your dataset."""
