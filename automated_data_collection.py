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
    columns_to_track = ['Trial', 'Gamma', 'Epsilon', 'Epsilon Decay',
                        'Start Location', 'Desination', 'Deadline','Successful?']
    dframe = pd.DataFrame(columns=columns_to_track) #create empty dataframe

    #build one row of a time looking for columns to track data
    row = []
    main_trial = 0
    for line in content:
        if 'Gamma:' in line:
            line_list = line.split(' ') #split on space
            gamma = line_list[1][:-1] # get the gamma value
            epsilon = line_list[3][:-1] # get the epsilon value
            epsilon_decay = line_list[-1].strip() # get the epsilon decay value
            main_trial += 1 # increment main trail (1.1, 1.2....2.1, 2.2.....etc.)
        if 'Simulator.run()' in line:
            trial = line[16:].strip() # get trial number
            row.append(trial[:6] + str(main_trial) + '.' + trial[6:]) # splice in main trial
            row.append(gamma)
            row.append(epsilon)
            row.append(epsilon_decay)
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


def iterative_data_collection(gamma_values, epsilon_values, epsilon_decay_values,
        appended_file_string=''):
    ''' Automate iterative data collection for a multiple gamma, epsilon and
        epsilon decay values. '''

    # create dynamic file name
    file_name = './data/txt_files/iteration_data' + appended_file_string + '.txt'

    # create file
    f = open(file_name, "w")

    # for every combination of gamma, epsilon, and epsilon decay run smartcab program
    for value in product(gamma_values, epsilon_values, epsilon_decay_values):
        print value

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

    return True


def single_scenario_repeat_data_collection(gamma, epsilon, epsilon_decay, number_of_times):
    ''' Automate repeated data collection for a single gamma, epsilon and
        epsilon decay value. '''

    #create a single file
    file_name = './data/txt_files/' + \
        'gamma_' + str(gamma) + \
        '_epsilon_' + str(epsilon) + \
        '_ep_decay_' + str(epsilon_decay) + \
        '_number_of_times_' + str(number_of_times) + \
        '.txt'

    # create file
    f = open(file_name, "w")

    # creat the command string
    command_string = 'python smartcab/agent.py ' + \
                     'gamma=' + str(gamma) + ' ' + \
                     'epsilon=' + str(epsilon) + ' ' + \
                     'ep_decay=' + str(epsilon_decay)

    # for each number of times run the smartcab program
    for i in range(0, number_of_times):
        print 'Iteration {}'.format(i) # print to command line
        args = shlex.split(command_string) # create subprocess args (a list of strings)
        p = subprocess.Popen(args, stdout=f) # create subprocess
        p.wait() # wait for subprocess to end

    # clost the file
    f.close()

    # parse the text to .csv file
    with open(file_name) as f1:
        complete = text_to_csv_parsing(f1)

    return True


# Setup iteration values
gamma_values = [(x / 100.0) for x in  range(80, 86, 5)] # possible gamma values (future reward multiplier)
epsilon_values = [(x / 100.0) for x in range(50, 56, 5)] # possilbe epsilon values (Exploration vs Exploitation)
epsilon_decay_values = [(x / 100.0) for x in range(95, 100, 1)] # epsilon decay values (GLIE Greedy Exploraiton vs Exploitation)

# call iterative data collection (comment out to do single values multiple times)
number_of_times = 5
for i in range(0, number_of_times):
    iterative_data_collection(gamma_values, epsilon_values, epsilon_decay_values, str(i))

# call single data collection (comment out to do iterative values multiple times)
#single_scenario_repeat_data_collection(0.80, 0.5, 0.99, 2)

print 'Finished!'
