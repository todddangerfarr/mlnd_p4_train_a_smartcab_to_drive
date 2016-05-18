########################################
# Iterative Automated Data Collection  #
#                                      #
#            By: Todd Farr             #
########################################

import os, subprocess, shlex
from itertools import product
import pandas as pd

# moved text parsing to automated data collection file
def text_to_csv_parsing(txt_file):
    ''' A function used to parse .txt files output by the agent into .csv files
        for data exploration. '''

    # read lines into content variable
    content = txt_file.readlines()

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

    # gamma_performance.append([f.name[16:-4], len(dframe[dframe['Successful?'] == 'Yes'])])

    #Save Gamma DataFrame as backup as .csv, splice off path and .txt and add .csv
    csv_path = 'data/csv_files/' + txt_file.name[17:-4] + '.csv'
    dframe.to_csv(csv_path, index=False)
    return True


# Setup iteration values
gamma_values = [(x / 100.0) for x in  range(70, 96, 5)] # possible gamma values (future reward multiplier)
epsilon_values = [(x / 100.0) for x in range(40, 61, 10)] # possilbe epsilon values (Exploration vs Exploitation)
epsilon_decay_values = [(x / 100.0) for x in range(93, 100, 2)] # epsilon decay values (GLIE Greedy Exploraiton vs Exploitation)

# for every combination of gamma, epsilon, and epsilon decay run smartcab program
#for value in product(gamma_values, epsilon_values, epsilon_decay_values):
for value in product(gamma_values, epsilon_values, epsilon_decay_values):
    print value

    # create dynamic file name
    file_name = './data/txt_files/' + \
        'gamma_' + str(value[0]) + \
        '_epsilon_' + str(value[1]) + \
        '_ep_decay_' + str(value[2]) + \
        '.txt'

    # create file
    f = open(file_name, "w+")
    #create command string
    command_string = 'python smartcab/agent.py ' + \
                     'gamma=' + str(value[0]) + ' ' + \
                     'epsilon=' + str(value[1]) + ' ' + \
                     'ep_decay=' + str(value[2])

    # subprocess to run smartcab program
    args = shlex.split(command_string) # create subprocess args (a list of strings)
    p = subprocess.Popen(args, stdout=f) # create subprocess
    p.wait() # wait for subprocess to end

    # close file
    f.close()

    # parse the text to .csv file
    with open(file_name) as f1:
        complete = text_to_csv_parsing(f1)

print 'Finished!'
