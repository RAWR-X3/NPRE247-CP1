import numpy as np 
import matplotlib.pyplot as plt
import csv
#import glob # rendered obselete by asking user to put all the files in the same folder that they then run from

###################################################################

# config

i = 0 # iteration counter, defaults to 0, shifts decay axis but does not 'jump to' later timesteps
#e = 0 # element counter, leave at 0, initial loops will behave weirdly otherwise, depreciated
s = 0 # arbitrary step counter, needs to be 0

inputfilepath = 'kepdecayinput.csv'
outputfilepath = 'kepdecayoutput.csv'

# csvwriter setup
fieldnames = ['N_Ahalf','N_Bhalf','N_Chalf','N_A%','N_B%','N_C%','AnN_A%','AnN_B%','AnN_C%','tfinal','iterlength','elementtotal','timestep']
decayoutput = open(outputfilepath,mode='r+')
csvwriter = csv.DictWriter(decayoutput,fieldnames=fieldnames,extrasaction='raise')
csvwriter.writeheader()

###################################################################

# find input csv file, or print an error about it
#try:
#    filepath1 = glob.glob('**\kepdecayinput.csv',root_dir='C:', dir_fd=None, recursive=True, include_hidden=True)
#    print('filepath1:',filepath1[0])    
#except:
#    print('issue with glob decayinput function')
# rendered obselete by asking user to put all the files in the same folder that they then run from

# put the csv file into mem as a dictionary
with open(inputfilepath, mode='r') as decaycsv:
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
N_A0 = decaylist[0]['N_A%'] # N_A0 shortcut for the sake of my eyes and fingers. also stores initial percentages
N_B0 = decaylist[0]['N_B%']
N_C0 = decaylist[0]['N_C%']

lamA = np.log(2)/decaylist[0]['N_Ahalf'] # decay constant calculations
lamB = np.log(2)/decaylist[0]['N_Bhalf']

AnN_A = np.zeros(totalsteps) # iterable lists for graphing
AnN_B = np.zeros(totalsteps)
AnN_C = np.zeros(totalsteps)

AnN_A[0] = N_A0 # setting initial values for analytical lists
AnN_B[0] = N_B0
AnN_C[0] = N_C0

# the actual decay math and output loops
while i < tfinal:

    i += iterlength # decay iteration stepper, used exclusively for the timestep, located here because the machine gods like it.
    s += 1 # analytical decay list stepper
    # Analytical Solution code:
    if s < totalsteps:
        AnN_A[s] = N_A0*np.e**(-lamA*i)
        AnN_B[s] = N_B0*np.e**(-lamB*i) + lamA*N_A0/(lamB-lamA) * (np.e**(-lamA*i) - np.e**(-lamB*i))
        AnN_C[s] = N_C0 + N_B0*(1-np.e**(-lamB*i)) + N_A0/(lamB-lamA) * (lamB*(1-np.e**(-lamA*i)) - lamA*(1-np.e**(-lamB*i)))

    s += -1
    # makes a new dictionary to satisfy output requirements, to be clear: i think it's awful
    decaywrite = {'N_Ahalf':decaylist[0]['N_Ahalf'],'N_Bhalf':decaylist[0]['N_Bhalf'],'N_Chalf':decaylist[0]['N_Chalf'],
                  'N_A%':decaylist[0]['N_A%'],'N_B%':decaylist[0]['N_B%'],'N_C%':decaylist[0]['N_C%'],
                  'AnN_A%':AnN_A[s],'AnN_B%':AnN_B[s],'AnN_C%':AnN_C[s],
                  'tfinal':tfinal,'iterlength':iterlength,'elementtotal':etotal,'timestep':i}
    csvwriter.writerow(decaywrite)
    s += 1 # this may seem like a crude way of adding and subtracting: it is to be clear however if it isn't written like this then it makes an extra line in the output file that does nothing and bothers me

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
#try:
#    filepath2 = glob.glob('**\kepdecayoutput.csv',root_dir='C:', dir_fd=None, recursive=True, include_hidden=True)
#    print('filepath2:',filepath2[0])
#except:
#    print('issue with glob decayoutput function')
# rendered obselete by asking user to put all the files in the same folder that they then run from
decayoutput.close() # "you should use try and finally!" if i had more forethought, yeah sure. but i didn't lol.
# put the csv file into mem as a dictionary
with open(outputfilepath, mode='r') as decaycsv:
    decayoutlist = list(csv.DictReader(decaycsv))
#print(decayoutlist) # debug

# create iteration list
#decayread = np.zeros(etotal) future use
N_Alist = np.zeros(int(totalsteps))
N_Blist = np.zeros(int(totalsteps))
N_Clist = np.zeros(int(totalsteps))

# fill the numerical element lists
while s < totalsteps:
    N_Alist[s] = decayoutlist[s]['N_A%']
    N_Blist[s] = decayoutlist[s]['N_B%']
    N_Clist[s] = decayoutlist[s]['N_C%']
    s += 1
s = 0

# uses extra saved output files to graph N_B over different runs
y = True
n = False
prompt=eval(input('graph N_B trials? (y/n)'))

if prompt == False:
    # numerical graphing
    plt.plot(plotx, N_Alist, label = "N_A Simulated")
    plt.plot(plotx, N_Blist, label = "N_B Simulated")
    plt.plot(plotx, N_Clist, label = "N_C Simulated")
    plt.plot(plotx, N_Alist + N_Blist + N_Clist, label = "Total Simulated")
    plt.xlabel('Timestep (Hours)')
    plt.ylabel('Isotope Percentages (%)')
    plt.title('Numerical Isotope Decay Chain Percentages')

if prompt == True:
    try: # input extra decay files
        with open('kepdecayoutput_t0.5.csv', mode='r') as decaycsv:
            decayoutlist2 = list(csv.DictReader(decaycsv))
        with open('kepdecayoutput_t0.1.csv', mode='r') as decaycsv:
            decayoutlist3 = list(csv.DictReader(decaycsv))
    except: # print error
        print('ERROR: N_B TRIALS NOT FOUND')

    #total step calculation
    totalsteps2 = int(float(decayoutlist2[0]['tfinal'])/float(decayoutlist2[0]['iterlength']))
    totalsteps3 = int(float(decayoutlist3[0]['tfinal'])/float(decayoutlist3[0]['iterlength']))
    # iteration lists
    N_Blist2 = np.zeros(totalsteps2)
    N_Blist3 = np.zeros(totalsteps3)
    # iteration list filling
    while s < totalsteps2:
        N_Blist2[s] = decayoutlist2[s]['N_B%']
        s += 1
    s = 0
    while s < totalsteps3:
        N_Blist3[s] = decayoutlist3[s]['N_B%']
        s += 1
    s = 0
    
    prompt=eval(input('N_Bmax trials? (y/n)'))
    
    if prompt == True:
        # find max time values!
        N_Bmaxt = N_Blist.argmax()*iterlength
        N_Bmaxt2 = N_Blist2.argmax()*float(decayoutlist2[0]['iterlength'])
        N_Bmaxt3 = N_Blist3.argmax()*float(decayoutlist3[0]['iterlength'])
        AnMaxt = (lamA-lamB)**(-1)*np.log(lamA/lamB)
        # getting unexpected values from the numerical calculations
        N_Bmaxlist = np.array([N_Bmaxt,N_Bmaxt2,N_Bmaxt3])
        inverseiterlist = np.array([1/iterlength,1/float(decayoutlist2[0]['iterlength']),1/float(decayoutlist3[0]['iterlength'])])
        # plot max values!
        plt.scatter(inverseiterlist, N_Bmaxlist, label = "Numerical Maximums")
        plt.hlines(AnMaxt,0,1/float(decayoutlist3[0]['iterlength']),linestyle='--',label = "Analytical Max")
        plt.xlabel('1/(iteration length) (1/hours)')
        plt.ylabel('N_Bmax time (hours)')
        plt.title('Maximum N_B time vs 1/(iteration length)')
        
    
    if prompt == False:
        # x element plots for N_B
        plotx2 = np.linspace(0,tfinal,totalsteps2)
        plotx3 = np.linspace(0,tfinal,totalsteps3)
        # N_B plotting
        plt.plot(plotx, N_Blist, label = "Course (iteration length = 1)")
        plt.plot(plotx2, N_Blist2, label = "Medium (iteration length = 0.5)")
        plt.plot(plotx3, N_Blist3, label = "Fine (iteration length = 0.1)")
        plt.plot(plotx, AnN_B, label = "Analytical")
        plt.xlabel('Timestep (Hours)')
        plt.ylabel('Isotope Percentages (%)')
        plt.title('Isotope B Iteration Length trials')

# Isotope Plot Final Config
plt.legend()
plt.show()