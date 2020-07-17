#!/usr/bin/env python
# coding: utf-8

# # Migrating CSV Data into a Relational Database
# # Step 1: Import CSV Data into Pandas Dataframes

# In[1]:


import pandas as pd


# # Reading the csv file

# In[2]:


df = pd.read_csv('cleaned_data.csv')
print(f"The dataset contains {len(df)} Condo Rent listings")
pd.set_option('display.max_columns', len(df.columns)) # To view all columns
pd.set_option('display.max_rows', 100)
df.head(10)


# In[3]:


df.count()


# In[4]:


df.dtypes


# # Step 2: Mapping Data and Connecting the Schema

# We are using SQLAlchemy, SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.
# 
# SQLAlchemy is most famous for its object-relational mapper (ORM), an optional component that provides the data mapper pattern, where classes can be mapped to the database in open ended, multiple ways - allowing the object model and database schema to develop in a cleanly decoupled way from the beginning.

# In[5]:


get_ipython().system('{sys.executable} -m pip install pip install SQLAlchemy')

import sqlalchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Float, Text


# Creating a relationdal datbase name enote2.sqlite. 

# In[6]:


engine = create_engine('sqlite:///enote2.sqlite')


# # Construct a base class for declarative class definitions.
# 
# The new base class will be given a metaclass that produces appropriate Table objects and makes the appropriate mapper() calls based on the information provided declaratively in the class and any subclasses of the class.
# 
# bind – An optional Connectable, will be assigned the bind attribute on the MetaData instance.

# In[7]:


Base = declarative_base(bind=engine)


# In[8]:


class enote(Base):
    __tablename__ = 'enote_data'
    id = Column(Integer, primary_key=True)
    id_person = Column(Integer)
    name = Column(String(15))
    surname = Column(String(15))
    zip = Column(Integer)
    city = Column(String(15))
    country = Column(String(15))
    email = Column(String(15))
    birth_date = Column(String(15))
    id_account = Column(Integer)
    account_type = Column(String(15))
    id_transaction = Column(Integer)
    transaction_type = Column(String(15))
    transaction_date = Column(String(15))
    transaction_amount = Column(Float(6,4))


# In[9]:


Base.metadata.create_all()


# # Step 3: Migrating Dataframe into Schema

# In[10]:


enote_measurements = df.to_dict(orient='records')


# In[11]:


metadata = MetaData(bind=engine)
metadata.reflect()


# In[12]:


table1_measurement = sqlalchemy.Table('enote_data', metadata, autoload=True)


# In[13]:


engine.execute(table1_measurement.delete())


# In[14]:


engine.execute(table1_measurement.insert(), enote_measurements)


# # Testing the tables that store the migrated data

# In[15]:


engine.execute("SELECT * FROM enote_data LIMIT 5").fetchall()


# In[16]:


engine.execute("SELECT id_person, strftime('%m.%Y', transaction_date) as month, SUM(transaction_amount) as sum_of_transactions FROM enote_data WHERE id_person IN ('1234' , '345') AND transaction_date BETWEEN '2020-02-15' and '2020-07-06' GROUP BY id_person, strftime('%m.%Y', transaction_date) ORDER BY id_person DESC").fetchall()


# We also got the results like this but we are missing the headers. We can also use sqlite3 and pandas to do
# the queries. We will read the enote2.sqlite database and d the query.

# In[17]:


import pandas as pd
import sqlite3

# Create a SQL connection to our SQLite database
con = sqlite3.connect("enote2.sqlite")

cur = con.cursor()


# In[18]:


# Read sqlite query results into a pandas DataFrame
con = sqlite3.connect("enote2.sqlite")
df = pd.read_sql_query("SELECT id_person, strftime('%m.%Y', transaction_date) as month, SUM(transaction_amount) as sum_of_transactions FROM enote_data WHERE id_person IN ('1234' , '345') AND transaction_date BETWEEN '2020-02-15' and '2020-06-06' GROUP BY id_person, strftime('%m.%Y', transaction_date) ORDER BY id_person DESC", con)

# Verify that result of SQL query is stored in the dataframe
print(df.head())

con.close()


# In[19]:


df


# We migrated the csv files into the relational database and did the query to get the desired results. Now we have a relational datbase in out folder. We can read the relational database from python and execute the queries. We can also modify the relational datbase we created. Let's check the tables in the relational
# database enote2.sqlite

# In[20]:


from sqlalchemy import create_engine, inspect, func


# In[21]:


engine = create_engine('sqlite:///enote2.sqlite')


# In[22]:


inspector_gadget = inspect(engine)


# Now we can check the tables in our relational datbase called enote2.sqlite

# In[23]:


inspector_gadget.get_table_names()


# We can see we have only one table called enote_data. 

# In[24]:


print("tablename: enote_data \n")
for piece in inspector_gadget.get_columns(table_name='enote_data'):
    print(piece['name'], piece['type'])


# In[ ]:




