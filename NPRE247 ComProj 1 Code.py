import numpy as np 
import matplotlib.pyplot as plt
import csv
import glob

# find input csv file, or print an error about it
try:
    filepath1 = glob.glob('**\kepdecayinput.csv',root_dir='C:', dir_fd=None, recursive=True, include_hidden=True)
    print('filepath1:',filepath1[0])    
except:
    print('issue with glob decayinput function')
    
# put the csv file into mem as a dictionary
with open(filepath1[0], mode='r') as decaycsv:
    decaylist = list(csv.DictReader(decaycsv))

# read decaylist stats
tfinal = float(decaylist[0]['tfinal'])
etotal = len(decaylist)

# convert strings to floats
for element in decaylist:
    if element['t1/2'] != 'stable':
        element['t1/2'] = float(element['t1/2'])
    element['N%'] = float(element['N%'])

###################################################################

# config

iterlength = 30 # how many time units per iteration
i = 0 # iteration counter, defaults to 0, shifts decay axis but does not 'jump to' later timesteps
e = 0 # element counter, leave at 0, initial loops will behave weirdly otherwise
s = 0 # arbitrary step counter, needs to be 0

# create decayfraction iteration list
decayfraction = np.zeros(etotal)
# creat delta iteration list
delta = np.zeros(etotal)

# create plotting list(s)
totalsteps = int(tfinal/iterlength) # x axis plot granularity
plotx = np.linspace(0,tfinal,totalsteps) # sets up the x axis plot for the graphs

outputfilepath = 'kepdecayoutput.csv'

###################################################################

fieldnames = ['name','t1/2','N%','timestep']
decayoutput = open(outputfilepath,mode='r+')
csvwriter = csv.DictWriter(decayoutput,fieldnames=fieldnames,extrasaction='raise')
csvwriter.writeheader()

# the actual decay math and output loops
while i < tfinal:
    i += iterlength # decay iteration stepper, placement makes the timesteps start above 0
    
    while e < etotal:
        # makes a new dictionary to satisfy output requirements
        decaywrite = {'name':decaylist[e]['name'],'t1/2':decaylist[e]['t1/2'],'N%':decaylist[e]['N%'],'timestep':i}
        csvwriter.writerow(decaywrite)
        e += 1
    e=0 # reset e counter
    
    #print('=========initial values=========')
    while e < etotal:
        if decaylist[e]['t1/2'] != 'stable':
            decayfraction[e] = decaylist[e]['N%']*(1/2)**(iterlength/decaylist[e]['t1/2'])
        #print(decaylist[e],i)
        e += 1 # isotope decay stepper
    e = 0 # reset e counter
    #print('=========decayed values=========')
    while e < etotal:
        delta[e] = decaylist[e]['N%'] - decayfraction[e]
        if decaylist[e]['t1/2'] != 'stable':
            decaylist[e]['N%'] = decayfraction[e]
        if e > 0:
            decaylist[e]['N%'] += delta[e-1]
        #print(decaylist[e],i)
        #print('delta:',delta[e]) # debug
        e += 1 # isotope post-decay addition stepper
    e = 0 # reset e counter
    #print('========================timestep========================')
# find output csv file, or print an error about it
try:
    filepath2 = glob.glob('**\kepdecayoutput.csv',root_dir='C:', dir_fd=None, recursive=True, include_hidden=True)
    print('filepath2:',filepath2[0])
except:
    print('issue with glob decayoutput function')

# put the csv file into mem as a dictionary
with open(filepath2[0], mode='r') as decaycsv:
    decayoutlist = list(csv.DictReader(decaycsv))
#print(decayoutlist) # debug

if len(decayoutlist) == totalsteps:
    print('decay output read error')

# create iteration list
#decayread = np.zeros(etotal) future use
N_Alist = np.zeros(int(totalsteps))
N_Blist = np.zeros(int(totalsteps))
N_Clist = np.zeros(int(totalsteps))

# fill the element lists
while s < totalsteps*3-2: # -2 because we add it back when grabbing specific elements

    if s >= 100000:
        print('decay output length exceeds 100k values')
        break
    
    #decaywrite = {'name':decaylist[e]['name'],'t1/2':decaylist[e]['t1/2'],'N%':decaylist[e]['N%'],'timestep':i} dict format
    N_Alist[e] = decayoutlist[s]['N%']
    N_Blist[e] = decayoutlist[1+s]['N%']
    N_Clist[e] = decayoutlist[2+s]['N%']
    s += etotal
    e += 1
s = 0
e = 0

# Isotope Plot Label Config
#plt.plot(plotx, 0, label = "Predicted1")
plt.plot(plotx, N_Alist, label = "N_A")
plt.plot(plotx, N_Blist, label = "N_B")
plt.plot(plotx, N_Clist, label = "N_C")

plt.xlabel('Timesteps')
plt.ylabel('Isotope Percentages')
plt.title('Isotope Decay Chain Percentages')
plt.legend()
plt.show()