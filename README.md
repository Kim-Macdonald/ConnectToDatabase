# ConnectToDatabase
Various database connection scripts


# Example: Pull metadata.tsv fields, from SQL server database, for ncov-tools metadata


## Determine all result classes in database using SSMS (or alternative) (e.g. positive, POSITIVE, presumptive positive, indeterminate, negative, labelling error, invalid, etc)

1. First I use the query below in SSMS (SQL Server Management Studio 17) to show all qPCR result values that currently exist:

~~~SQL
    
    SELECT
           ncov_qpcr_result_sq,
         count(ncov_qpcr_result_sq) AS Result_count
    FROM databaseTableName
    WHERE 
           ncov_qpcr_result_sq IS NOT NULL 
    GROUP BY ncov_qpcr_result_sq
    ORDER BY ncov_qpcr_result_sq ASC;
    
~~~

2. Then I use these results to decide which results (e.g. positive, indeterminate only) to use in the SQL query in ConnectToSQLserverDatabase_pyodbc.py

3. I then update my SQL query in the script with the desired results. 


## Run ConnectToSQLserverDatabase_pyodbc.py

1. First update variable names for credentials (lines 26-29), the SQL query of interest (line 50) and paths to files in the script (line 55 - where you want your output file saved), as per your set-up.

2. Launch Spyder, or other IDE on your PC.

3. Open and run script in Spyder on your PC.

4. The file should appear in the folder you specified for saving (in line 55).

5. You'll use this file as input for another script to clean the data (e.g. remove text from Ct fields, merge Cts from 5 fields/targets into 1 combined Ct column, and match to multiple sample identifiers), and then match to samples on a run to integrate with ncov-tools output. 


## Run another script to clean All_metadata.csv before integrating with ncov-tools etc Result Summary File 

(Result Summary file is the final output from running mergeQCresults_plusMissing (https://github.com/Kim-Macdonald/mergeQCresults_plusMissing), VoCcaller (https://github.com/Kim-Macdonald/VoCcaller), LineageUpdater (https://github.com/Kim-Macdonald/LineageUpdater))

Script not on github yet



