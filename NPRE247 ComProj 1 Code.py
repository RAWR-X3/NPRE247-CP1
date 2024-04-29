import numpy as np 
import matplotlib.pyplot as plt
import csv
import glob

###################################################################

# config

i = 0 # iteration counter, defaults to 0, shifts decay axis but does not 'jump to' later timesteps
#e = 0 # element counter, leave at 0, initial loops will behave weirdly otherwise, depreciated
s = 0 # arbitrary step counter, needs to be 0

outputfilepath = 'kepdecayoutput.csv'

# csvwriter setup
fieldnames = ['N_Ahalf','N_Bhalf','N_Chalf','N_A%','N_B%','N_C%','tfinal','iterlength','elementtotal','timestep']
decayoutput = open(outputfilepath,mode='r+')
csvwriter = csv.DictWriter(decayoutput,fieldnames=fieldnames,extrasaction='raise')
csvwriter.writeheader()

###################################################################

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
etotal = int(decaylist[0]['elementtotal'])
iterlength = float(decaylist[0]['iterlength']) # how many time units per iteration

# convert strings to floats
decaylist[0]['N_Ahalf'] = float(decaylist[0]['N_Ahalf'])
decaylist[0]['N_Bhalf'] = float(decaylist[0]['N_Bhalf'])
decaylist[0]['N_A%'] = float(decaylist[0]['N_A%'])
decaylist[0]['N_B%'] = float(decaylist[0]['N_B%'])
decaylist[0]['N_C%'] = float(decaylist[0]['N_C%'])

# create decayfraction iteration list
decayfraction = np.zeros(etotal)
# creat delta iteration list
delta = np.zeros(etotal)

# create plotting list(s)
totalsteps = int(tfinal/iterlength) # x axis plot granularity
plotx = np.linspace(0,tfinal,totalsteps) # sets up the x axis plot for the graphs

# Analytical Solution pre-code:
lamA = np.log(2)/decaylist[0]['N_Ahalf'] # decay constant calculations
lamB = np.log(2)/decaylist[0]['N_Bhalf']

N_A0 = decaylist[0]['N_A%'] # N_A0 shortcut for the sake of my eyes and fingers. also stores initial percentages
N_B0 = decaylist[0]['N_B%']
N_C0 = decaylist[0]['N_C%']

AnN_A = np.zeros(totalsteps) # iterable lists for graphing
AnN_B = np.zeros(totalsteps)
AnN_C = np.zeros(totalsteps)

AnN_A[0] = N_A0 # setting initial values for analytical lists
AnN_B[0] = N_B0
AnN_C[0] = N_C0

# the actual decay math and output loops
while i < tfinal:
    i += iterlength # decay iteration stepper, used exclusively for the timestep, located here because the machine gods like it.
    s += 1 # analytical decay stepper
    # Analytical Solution code:
    if s < totalsteps:
        AnN_A[s] = N_A0*np.e**(-lamA*i)
        AnN_B[s] = N_B0*np.e**(-lamB*i) + lamA*N_A0/(lamB-lamA) * (np.e**(-lamA*i) - np.e**(-lamB*i))
        AnN_C[s] = N_C0 + N_B0*(1-np.e**(-lamB*i)) + N_A0/(lamB-lamA) * (lamB*(1-np.e**(-lamA*i)) - lamA*(1-np.e**(-lamB*i)))
    
    # makes a new dictionary to satisfy output requirements, to be clear: i think it's awful
    decaywrite = {'N_Ahalf':decaylist[0]['N_Ahalf'],'N_Bhalf':decaylist[0]['N_Bhalf'],'N_Chalf':decaylist[0]['N_Chalf'],
                  'N_A%':decaylist[0]['N_A%'],'N_B%':decaylist[0]['N_B%'],'N_C%':decaylist[0]['N_C%'],
                  'tfinal':tfinal,'iterlength':iterlength,'elementtotal':etotal,'timestep':i}
    csvwriter.writerow(decaywrite)
    
    # numerical solution, commented print statements used for debugging through the terminal
    #print('=========initial values=========')
    #print(decaylist[0],i) # debug
    #print('=========decayed values=========')
    decayfraction[0] = decaylist[0]['N_A%']*(1/2)**(iterlength/decaylist[0]['N_Ahalf']) # half life equations used to calculate the remaining material fractions
    decayfraction[1] = decaylist[0]['N_B%']*(1/2)**(iterlength/decaylist[0]['N_Bhalf'])
    
    delta[0] = decaylist[0]['N_A%'] - decayfraction[0] # calculate deltas for decaying elements
    delta[1] = decaylist[0]['N_B%'] - decayfraction[1]

    decaylist[0]['N_A%'] = decayfraction[0] # send the decay fraction to the main list
    decaylist[0]['N_B%'] = decayfraction[1]
    
    decaylist[0]['N_B%'] += delta[0] # add deltas to the next element down the chain
    decaylist[0]['N_C%'] += delta[1]
    #print(decaylist[0],i) # debug
    #print('========================timestep========================')
i = 0 # reset i counter
s = 0 # reset s counter

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

# create iteration list
#decayread = np.zeros(etotal) future use
N_Alist = np.zeros(int(totalsteps))
N_Blist = np.zeros(int(totalsteps))
N_Clist = np.zeros(int(totalsteps))

# fill the element lists
while s < totalsteps:
    
    #decaywrite = {'name':decaylist[e]['name'],'t1/2':decaylist[e]['t1/2'],'N%':decaylist[e]['N%'],'timestep':i} dict format
    N_Alist[s] = decayoutlist[s]['N_A%']
    N_Blist[s] = decayoutlist[s]['N_B%']
    N_Clist[s] = decayoutlist[s]['N_C%']
    s += 1
s = 0

# Isotope Plot Label Config
# analytical
plt.plot(plotx, AnN_A, label = "N_A Predicted")
plt.plot(plotx, AnN_B, label = "N_B Predicted")
plt.plot(plotx, AnN_C, label = "N_C Predicted")
# numerical
plt.plot(plotx, N_Alist, label = "N_A Simulated")
plt.plot(plotx, N_Blist, label = "N_B Simulated")
plt.plot(plotx, N_Clist, label = "N_C Simulated")
# labels n stuff
plt.xlabel('Timestep (Hour)')
plt.ylabel('Isotope Percentages')
plt.title('Isotope Decay Chain Percentages Simulated and Predicted')
plt.legend()
plt.show()