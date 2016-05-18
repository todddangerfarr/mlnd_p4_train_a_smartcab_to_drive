########################################
# Text Parsing for Udacity Nano Degree #
#                                      #
#            By: Todd Farr             #
########################################

import pandas as pd
import os

#get a list of all .txt files in txt_files
file_list = [file for file in os.listdir('txt_files') if file.endswith(".txt")]

# Store Gamma Performance
gamma_performance = []

#open file
for file in file_list:
    #open file and read lines
    with open('txt_files/' + file) as f:
        content = f.readlines()

    #data to track
    columns_to_track = ['Trial', 'Start Location', 'Desination', 'Deadline', 'Successful?']
    dframe = pd.DataFrame(columns=columns_to_track) #create empty dataframe

    #build one row of a time looking for columns to track data
    row = []
    for line in content:
        if 'Simulator.run()' in line:
            row.append(line[16:].strip())
        if 'Environment.reset(): Trial set' in line:
            row.append(line[47:53].strip()) # get Start location
            row.append(line[69:75].strip()) # get distination
            row.append(line[88:91].strip()) # get Deadline
        if 'Environment.act()' in line or 'Environment.reset(): Primary' in line:
            if 'could not' in line:
                row.append('No') #Not successful
            else:
                row.append('Yes') #Successful

            #put in dataframe
            dframe = dframe.append(pd.Series(row, index=columns_to_track), ignore_index=True)
            row = [] #delete row data and start again

    gamma_performance.append([f.name[16:-4], len(dframe[dframe['Successful?'] == 'Yes'])])

    #Save Gamma DataFrame as backup as .csv, splice off path and .txt and add .csv
    csv_path = './csv_files/' + f.name[10:-4] + '.csv'
    dframe.to_csv(csv_path, index=False)

print gamma_performance
