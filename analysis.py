# this program should do some analysis of some csv data files

# this version is written as a script.
# It does not use a 'pythonic' object oriented approach

import csv
import os
import numpy
import pylab

data=dict() # create empty dictionary for all data (key = filename)
data_folder = "data"


filenames = os.listdir(data_folder)
for filename in filenames:
    # create new dictionary for data
    this_file_data = dict()
    
    # read data file
    print "Reading ",filename
    filepath = os.path.join(data_folder, filename)
    csvfile = file(filepath)
    reader = csv.DictReader(csvfile)
    # initialise empty lists
    t=list()
    DotX=list()
    DotY=list()
    # read in all rows
    for row in reader:
        t.append(row['t'])
        DotX.append(row['DotX'])
        DotY.append(row['DotY'])
    #turn lists into arrays and store in dictionary
    this_file_data['t'] = numpy.array(t)
    this_file_data['DotX'] = numpy.array(DotX)
    this_file_data['DotY'] = numpy.array(DotY)
    
    #store in the master dictionary
    data[filename] = this_file_data

# do some plots
for filename in filenames:
    t = data[filename]['t']
    DotX = data[filename]['DotX']
    DotY = data[filename]['DotY']    
    
    pylab.figure(1)
    pylab.title('Y vs X')
    pylab.plot(DotX,DotY, label=filename)
    pylab.legend()
    pylab.show()
    
    pylab.figure(2)
    pylab.title('Y vs t')
    pylab.plot(t,DotY, label=filename)
    pylab.legend()
    pylab.show()
        