import csv
import os

import pylab
import numpy

#added by psyche 2009-08-28 
from scipy import *
#-------------

data_folder = "data"

import joystick
from joystick import Dataset, Datafile


ds = Dataset('data')

colours={'i': 'b', 'l': 'r'} # instrumental = blue, lyrics = red
print "Reminder: Lyrics = Red, Instrumental = Blue "

sample_file = ds.filter(songno=105).next()
for i in range(0, sample_file.get_frame_count(), 1 ):
	
		y_arrays=dict() # new dictionary for this time step
        
		for condition in ['i','l']:
        		col = colours[condition]
        		y_list=list()
                        x_list=list()
        		differencelist=list()

        	for df in ds.filter(songno=105,condition=condition):
            			t = df.data['t'][i]
            			DotY = df.data['DotY'][i]
            			DotX = df.data['DotX'][i]
            			t = df.data['t'][i]
            			y_list.append(DotY)
            			x_list.append(DotX)
            			differencelist.append(DotY-DotX)
            			
        	y_array = numpy.array(y_list,dtype=float)
        	x_array = numpy.array(x_list,dtype=float)
        		
   		y_arrays[condition] = y_array
		instrumental = y_array['i']
		lyric = y_array['l']
		# added by Psyche 2009-08-28
		mean_diff = mean(lyric) - mean(instrumental)
		var_sum = var(lyric)/len(lyric) + var(instrumental)/len(instrumental)
		tstat = mean_diff / (var_sum**0.5) 
		pval_list = list()
		pval = stats.t.sf(abs(tstat), len(lyric)-1)
		# ---------------------  
        
    
		pval_list.append(pval)
		
		print "At time = %.1fs the lyric is %f more arousing than the instrumental"%(
    			t, lyric.mean()-instrumental.mean() )

  
#differencelist = list()
#timelist = list()
#for i in range (0, sample_file.get_frame_count(),1):
#	for condition in ['i','l']:
#		differencelist.append(lyric.mean()-instrumental.mean() )
#for i in range(0, sample_file.get_frame_count(), 1):

    


# do a Y verses time plot
#pylab.figure(1)
#for df in ds.filter(songno=105):
#    t = df.data['t']
#    DotX = df.data['DotX']
#    DotY = df.data['DotY']    
#    col = colours[df.metadata['condition']]
#    pylab.title('Y vs t')
#    pylab.plot(t,DotY, col+'-', label=df.metadata['subject'])
#pylab.legend()
#pylab.show()
