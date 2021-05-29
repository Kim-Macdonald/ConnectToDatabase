# -*- coding: utf-8 -*-
"""
Created on Wed May 12 14:10:11 2021

#References: 
# https://docs.microsoft.com/en-us/sql/connect/python/pyodbc/step-3-proof-of-concept-connecting-to-sql-using-pyodbc?view=sql-server-ver15 
# https://stackoverflow.com/questions/11451101/retrieving-data-from-sql-using-pyodbc 

@author: kmacdonald
"""
#created & tested on PC using:
# pandas v1.1.3
# python v3.8.5
#and on laptop with:
# pandas v1.0.5
# python v3.8.3


#import packages I need
import glob
import os
import subprocess
import fnmatch
import pandas as pd
import numpy as np
from datetime import datetime
from openpyxl import Workbook

import pyodbc 


#------------CREDENTIALS:-------------------------  
#Connect to SQL server db:
server = '##.#.##.###' #(format is like 00.0.00.000)
database = 'databasename' 
username = 'YourUsername' 
password = 'YourPasswordToDatabase' 

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

#----------------------------------
# # Alt method: 
# cursor = cnxn.cursor()

# # Select query
# cursor.execute("SELECT containerid, collection_date, ncov_qpcr_e_sarbeco_result, ncov_qpcr_rdrp_lee_result, ncov_qpcr_n_sarbeco_result, ncov_qpcr_n2_result, ncov_qpcr_orf1_result FROM databaseTableName WHERE ncov_qpcr_result_sq IS NOT NULL AND ncov_qpcr_result_sq in ('Positive', 'PRESUMPTIVE POS', 'Presumptive Posiitive', 'Presumptive Positive', 'Indeterminate', 'Indeterminate for E and N', 'Indeterminate for interna', 'Indeterminate for N gene');") 
# row = cursor.fetchone() 
# while row: 
#     print(row[0])
#     row = cursor.fetchone()

# # This will print to screen. Use below instead if want saved to file:
#-----------------------------------

# #OR create excel/csv file with results: (Worked. Used this instead of the above (commented out) b/c wanted an output file)
# Create Table of results:
# replace databaseTableName in query with your desired table name from the database you connected to above. And replace SQL query with fields etc as needed. 
tableResult = pd.read_sql("SELECT containerid, second_containerid, seq_containerid, collection_date, ncov_qpcr_e_sarbeco_result, ncov_qpcr_rdrp_lee_result, ncov_qpcr_n_sarbeco_result, ncov_qpcr_n2_result, ncov_qpcr_orf1_result FROM databaseTableName WHERE ncov_qpcr_result_sq IS NOT NULL AND ncov_qpcr_result_sq in ('Positive', 'PRESUMPTIVE POS', 'Presumptive Posiitive', 'Presumptive Positive', 'Indeterminate', 'Indeterminate for E and N', 'Indeterminate for interna', 'Indeterminate for N gene');", cnxn)

# Create Excel file with the results
df_ploverMetadata=pd.DataFrame(tableResult)
#df_ploverMetadata.to_excel("FileExample.xlsx",sheet_name='Results')
df_ploverMetadata.to_csv('H:/2019-nCoV/Line Lists/COG-UK/RunsSummary/UpdatedLineages/All_Metadata.csv')



# ****Disconnect to avoid deadlocking the database:***** (Thanks to Jaideep Singh for this!!)
#cursor.close()
cnxn.close()   
 
#takes about 5-10s to run (as of May25/2021)  (for >100,000 rows of data)
