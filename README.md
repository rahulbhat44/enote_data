# enote_data Task

The task is given by enote company for the position of Data Engineering. The task is to model the data, so that all the information can be stored in a relational 
database.  

There are three csv files given. one file contains the the list of customers with their personal data, second file contains the list of accounts that belong to 
the customers and the third file contains the list of transactions from/to these accounts. 

I have concatenated the three files by their common id variable and cleaned the data using python in Jupyter Notebook. I have also done some data engineering, 
including data profiling using pandas data profiling. The cleaned data is generated as a single csv file which contains all the information of the customers. 

After that the cleaned csv file is migrated into the relational database using SQLAlchemy to get the desired query. 

Folders :

Dataset - This folder contains all the csv files with the new concatenated and cleaned csv file as well.

Jupyter_Notebook - This folder contains the jupyter notebook files. 

Markdown_Report - This folder contains the mardown reports in html format. 

Python_Script - This folder contains the python script generated from python notebook. This folder contains two script files one is the data engineering (cleaning 
and preparing the data). The another one is migrate database (migrated the csv file into the relational datbase and did the query). 


