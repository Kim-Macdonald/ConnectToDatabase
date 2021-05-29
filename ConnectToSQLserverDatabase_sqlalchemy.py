# -*- coding: utf-8 -*-
"""
Created on Wed May 12 14:12:25 2021

# References:
# https://stackoverflow.com/questions/41344054/python-sqlalchemy-data-source-name-not-found-and-no-default-driver-specified 
# https://www.sqlalchemy.org/library.html#tutorials
# https://docs.sqlalchemy.org/en/14/dialects/mssql.html
# https://docs.sqlalchemy.org/en/14/core/engines.html

@author: kmacdonald
"""
#created & tested on PC using:
# pandas v1.1.3
# python v3.8.5
#and on laptop with:
# pandas v1.0.5
# python v3.8.3


#import packages I need:
import pandas as pd
import sqlalchemy as sq
 
# Create the engine to connect: (replace YourUsername, yourdatabasePassword, ##.#.##.### (with the actual numbers for your server location), and DatabaseName)
engine = sq.create_engine("mssql+pyodbc://YourUsername:yourdatabasePassword@##.#.##.###/DatabaseName" + "?driver=SQL+Server")
# I had to add that last ?driver stuff, b/c it had problems connecting and a discussion forum mentioned that adding that allowed it to connect. 
 
# apparently it may be better to use the pymssql option instead of the pyodbc, according to discussion forums. 
#e.g. engine = sq.create_engine("mssql+pymssql://username:password@servername/dbname")
 
 
# Read data from SQL table: (replace DatabaseTableName)
sql_data = pd.read_sql_table('DatabaseTableName', engine)

# # Print all the columns of the dataframe
#print(sql_data.info())

#This pulls entire db contents. So will take a long time if db is big. THEN you can filter further with python. 
 
# Store db contents in variable:
df_ploverMetadata0=pd.DataFrame(sql_data)
 
 
# Store desired columns + COVID PCR result (pos/neg etc for filtering results) in df:
df_ploverMetadata1 = df_ploverMetadata0[['containerid', 'collection_date', 'ncov_qpcr_e_sarbeco_result', 'ncov_qpcr_rdrp_lee_result', 'ncov_qpcr_n_sarbeco_result', 'ncov_qpcr_n2_result', 'ncov_qpcr_orf1_result', 'ncov_qpcr_result_sq']]
 
# Filter data so only have Positive and Indeterminate Results: (replace these with whatever your desired result options are)
Pos_Indet_values = ['Positive', 'PRESUMPTIVE POS', 'Presumptive Posiitive', 'Presumptive Positive', 'Indeterminate', 'Indeterminate for E and N', 'Indeterminate for interna', 'Indeterminate for N gene']
df_ploverMetadata2 = df_ploverMetadata1.loc[df_ploverMetadata1['ncov_qpcr_result_sq'].isin(Pos_Indet_values)]
 
# Store desired columns only (no ncov_qpcr_result_sq - was only used to filter above) in new df:
df_ploverMetadata = df_ploverMetadata2[['containerid', 'collection_date', 'ncov_qpcr_e_sarbeco_result', 'ncov_qpcr_rdrp_lee_result', 'ncov_qpcr_n_sarbeco_result', 'ncov_qpcr_n2_result', 'ncov_qpcr_orf1_result']]
 
 
# Save df contents to file:
df_ploverMetadata.to_csv('Path/To/OutputFile/All_Metadata2.csv')
 
 
# ****Disconnect to avoid deadlocking database:***** (From Jaideep Singh - https://github.com/jaideep2)
engine.close()
sq.dispose()
