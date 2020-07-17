#!/usr/bin/env python
# coding: utf-8

# # Importing Libraries

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')

get_ipython().system('{sys.executable} -m pip install pandas')
get_ipython().system('{sys.executable} -m pip install numpy')
get_ipython().system('{sys.executable} -m pip install datetime')
get_ipython().system('{sys.executable} -m pip install seaborn')

# general
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
import pandasql as ps

#Hide warnings
import warnings
warnings.filterwarnings('ignore')

# Set plot preference
plt.style.use(style='ggplot')
plt.rcParams['figure.figsize'] = (10, 6)

print('Libraries imported.')


# # Libraries for pandas data profiling which does the exploratory analysis.

# In[2]:


get_ipython().system('{sys.executable} -m pip install pandas-profiling')

from pathlib import Path

# Installed packages
from ipywidgets import widgets

# Our package
from pandas_profiling import ProfileReport
from pandas_profiling.utils.cache import cache_file


# # Load the first dataset - List of customers with their personal data

# In[3]:


df1 = pd.read_csv('BI_assignment_person.csv')
print(f"The dataset contains {len(df1)} Condo Rent listings")
pd.set_option('display.max_columns', len(df1.columns)) # To view all columns
pd.set_option('display.max_rows', 100)
df1.head(10)


# In[4]:


df1.tail()


# In[5]:


# Checking the null values in a dataset
df1.isnull().any()


# In[6]:


# Sum of null values
df1.isnull().sum()


# There is one name missing and 280 surnames. The phone number is empty, so will remove that from the data set.

# In[7]:


# Drop the unnamed column
df1.drop(['phone_number'], axis=1, inplace=True)


# In[8]:


# Drop the missing data
#df1 = df1.dropna()


# In[9]:


# Check again for the missing data
df1.isna().sum()


# We will keep the names and surnames in the dataset. 

# # Load the second dataset - List of accounts that belong to the customers

# In[10]:


df2 = pd.read_csv('BI_assignment_account.csv')
print(f"The dataset contains {len(df2)} Condo Rent listings")
pd.set_option('display.max_columns', len(df2.columns)) # To view all columns
pd.set_option('display.max_rows', 100)
df2.head(10)


# In[11]:


# Checking the null values in a dataset
df2.isnull().any()


# In[12]:


# Load the third dataset - List of transactions from/to these accounts
df3 = pd.read_csv('BI_assignment_transaction.csv')
print(f"The dataset contains {len(df3)} Condo Rent listings")
pd.set_option('display.max_columns', len(df3.columns)) # To view all columns
pd.set_option('display.max_rows', 100)
df3.head(10)


# In[13]:


df3.tail(10)


# In[14]:


# Checking the null values in a dataset
df3.isnull().any()


# There is no missing data, dataset is clean

# # Concatenating the datasets
# First we will concatenate the second and the third dataset - List of accounts that belong to the customers and 
# List of transactions from/to these accounts with their common variable name "id_account" using the inner join operation. 

# In[15]:


df10 = pd.merge(df2, df3, how='inner', on=['id_account'])


# In[16]:


df10.head()


# We have successfully concatenated the datasets and now will check if everything is right.  

# In[17]:


# Check for the null values
df10.isna().sum()


# Now we will concatenate the df10 (the one we just merged) and the first dataset "List of customers with their personal data" using the same method by their common variable name id_person. 

# In[18]:


df = pd.merge(df1, df10, how='inner', on=['id_person'])


# In[19]:


df.head()


# In[20]:


df.tail()


# The transaction_date column doesn't look like in a proper format. Instead of four digit year (2020) it shows two digit (20). We need to fix this. First check for the null values and then we can fix the date time format. 

# In[21]:


# check for the missing values
df.isna().sum()


# There are 807 names missing and 28 surnames missing. Lets check what names and surnames missing. 

# In[22]:


def percent_value_counts(df, feature):
    """This function takes in a dataframe and a column and finds the percentage of the value_counts"""
    percent = pd.DataFrame(round(df.loc[:,feature].value_counts(dropna=False, normalize=True)*100,2))
    ## creating a df with the
    total = pd.DataFrame(df.loc[:,feature].value_counts(dropna=False))
    
    ## concating percent and total dataframe
    total.columns = ["Total"]
    percent.columns = ['Percent']
    return pd.concat([total, percent], axis = 1)


# In[23]:


percent_value_counts(df, 'name')


# In[24]:


percent_value_counts(df, 'surname') 


# We need to fix the date format first. Date format should be in a proper format. In our dataset the the date is 
# like this "2/18/20" and we need full year and will change it to this fomrat YYYY-MM-DD. 

# In[25]:


# Fixing date format 
df['transaction_date'] = pd.to_datetime(df['transaction_date'],  utc=False)


# In[26]:


df.head()


# In[27]:


#df['transaction_date'] = df['transaction_date'].dt.strftime("%d-%m-%y20")
df['transaction_date'] = df['transaction_date'].dt.strftime("%y20-%m-%d")


# In[28]:


df.head()


# Now the date looks good and in the format we needed. 

# In[29]:


# Save cleaned dataset
cleaned_data = df.to_csv(r'cleaned_data.csv', header=True)


# Read the clean data and we still need to do some changes. 

# In[30]:


df = pd.read_csv('cleaned_data.csv')
print(f"The dataset contains {len(df)} Condo Rent listings")
pd.set_option('display.max_columns', len(df.columns)) # To view all columns
pd.set_option('display.max_rows', 100)
df.head(10)


# We will change the unnamed 0 column to id, we need that id in the relational database. 

# In[31]:


df.rename( columns={'Unnamed: 0':'id'}, inplace=True )


# In[32]:


df.head()


# In[33]:


# Save cleaned dataset
cleaned_data = df.to_csv(r'cleaned_data.csv', header=True, index=False)


# The dataset is perfectly merged and saved. Now there is only one dataset with all the information needed. 
# Let's do some data profiling using pandas and some analysis on this dataset.
# 

# # Data Profiling
# Data profiling is done using the pandas data profiling, by using this we can automatically generate the profile reports from a pandas DataFrame. The pandas df.describe() function is great but a little basic for serious exploratory data analysis. pandas_profiling extends the pandas DataFrame with df.profile_report() and does the exploratory analysis for us. It is fast and efficient. This helps to understand the data very well. The report is also present in the folder by the name of data_profile.

# In[34]:


profile = ProfileReport(df, title="Condo Rent Prices", html={'style': {'full_width': True}}, sort="None")


# In[35]:


# Or use the HTML report in an iframe
profile.to_notebook_iframe()


# In[36]:


# save the data profiling report
profile.to_file(output_file="data_profile.html")


# In[37]:


# Plotting the distribution of numerical and boolean categories
df.hist(figsize=(20,20));


# In[38]:


df.head()


# # We can also do the sql query using pandas sql function. We can check if the sql queries is working and giving results. 

# In[39]:


import pandas as pd
import pandasql as ps
output = ps.sqldf("select * from df")


# In[40]:


output2 = ps.sqldf("select * FROM df WHERE id_person = 1234 and 345")


# In[41]:


output2.head()


# In[42]:


# 15.02.2020 till 06.06.2020:
output4 = ps.sqldf("SELECT * FROM df WHERE id_person IN ('1234' , '345') AND transaction_date BETWEEN '2020-02-04' and '2020-04-20'")


# In[43]:


output4.head()


# In[44]:


output3 = ps.sqldf("SELECT id_person, SUM(transaction_amount) as sum_of_transactions, strftime('%m.%Y', transaction_date) as month FROM df WHERE id_person IN ('1234' , '345') AND transaction_date BETWEEN '2020-02-04' and '2020-04-20' GROUP BY id_person, strftime('%m.%Y', transaction_date) ORDER BY id_person DESC  ")


# In[45]:


output3.head()


# We got the results using pandas sql function but we need to ingest this data into relational database and fetch from there and do the queries. There are few null values in the dataset and we cannoit remove them because the person_id 345 will be vanished because the name is not available for person_id 345. So we have kept the data like that only with the missing values. 

# In[ ]:




