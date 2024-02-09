import numpy as np 
import matplotlib.pyplot as plt
import csv
import glob

# config
iterlength = 1 # how many time units per iteration
i = 0 # iteration counter
e = 0 # element counter
# commented print statements are for debugging

# find the goddamn csv file
try:
    filepath = glob.glob('**\decayinput.csv',root_dir='C:', dir_fd=None, recursive=True, include_hidden=True)
    #print('filepath:',filepath[0])    
except:
    print('issue with glob function')
    
# put the csv file into mem as a dictionary
with open(filepath[0], mode='r') as decaycsv:
    decaylist = list(csv.DictReader(decaycsv))

# read decaylist stats
tfinal = float(decaylist[0]['tfinal'])
etotal = len(decaylist)
#print(decaylist)

# create decayfraction iteration list
decayfraction = np.zeros(etotal)
# creat delta iteration list
delta = np.zeros(etotal)

# convert strings to floats
for element in decaylist:
    if element['t1/2'] != 'stable':
        element['t1/2'] = float(element['t1/2'])
    element['N%'] = float(element['N%'])

# the actual decay math loop(s)
while i < tfinal:
    #print(decaylist)
    i += iterlength # decay iteration stepper
    while e < etotal:
        if decaylist[e]['t1/2'] != 'stable':
            decayfraction[e] = (decaylist[e]['N%'])/(2**(decaylist[e]['t1/2']**(-1)))
        #print(decayfraction[e])
        e += 1 # isotope decay stepper
    e = 0 # reset e counter
    
    while e < etotal:
        delta[e] = decaylist[e]['N%'] - decayfraction[e]
        if decaylist[e]['t1/2'] != 'stable': # decayfraction for stable isotope is always 0. bad.
            decaylist[e]['N%'] = decayfraction[e]
        if e > 0:
            decaylist[e]['N%'] += delta[e-1]
        #print(decaylist[e],i)
        #print(delta)
        e += 1 # isotope post-decay addition stepper

    #print('=====timestep=====')
    e = 0 # reset e counter