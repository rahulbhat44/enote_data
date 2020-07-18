# enote_data Task

The task is given by enote company for the position of Data Engineering. The task is to model the data so that all the information can be stored in a relational database.

There are three CSV files given. one file contains the list of customers with their personal information data, the second file contains the list of accounts that belong to the customers and the third file contains the list of transactions from/to these accounts.

I have concatenated the three files by their common id variable and cleaned the data using python in Jupyter Notebook. I have also done some data engineering, including data profiling using pandas data profiling. The cleaned data is generated as a single CSV file which contains all the information of the customers.
After that, the cleaned CSV file is migrated into the relational database using SQLAlchemy to get the desired query.

Folders :

- Dataset - This folder contains all the CSV files with the new concatenated and cleaned CSV file as well.

- Jupyter_Notebook - This folder contains the Jupyter Notebook files.

- Markdown_Report - This folder contains the markdown reports in HTML format.

- Python_Script - This folder contains the python script generated from python notebook. This folder contains two script files one is the data engineering (cleaning and preparing the data). The other one has migrated the database (migrated the CSV file into the relational database and did the query).


