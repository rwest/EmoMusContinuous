import csv
import os

import pylab
import numpy

#added by psyche 2009-08-28 
from scipy import stats
#-------------

data_folder = "data"

import joystick
from joystick import Dataset, Datafile


ds = Dataset('data')
songno = 105 # Alanis Morrisette 


colours={'i': 'b', 'l': 'r'} # instrumental = blue, lyrics = red
print "Reminder: Lyrics = Red, Instrumental = Blue "

sample_file = ds.filter(songno=songno).next()

pval_list = list() # list of P values (one for each time step)


csv_file = open(sample_file.metadata['artist']+'.csv', 'w') # open a file for writing
csv_out =  csv.DictWriter(csv_file, ['t','imy','ivy','iny','lmy','lvy','lny','tstat','pval'],
 			dialect='excel')
labels = {  't': 'Time (s)',
			'imy': 'Mean(Yi)', 
			'ivy': 'Var(Yi)', 
			'iny': 'N(Yi)',
			'lmy': 'Mean(Yl)',
			'lny': 'N(Yl)',
			'lvy': 'Var(Yl)',
			'tstat': 'T-test statistic',
			'pval': 'P value' }
csv_out.writerow(labels)

# loop over timesteps
for i in range(0, sample_file.get_frame_count(), 1 ): 

	y_arrays=dict() # new dictionary for this time step
	
	#loop over condition (instrumental/lyric)
	for condition in ['i','l']:
		col = colours[condition]
		y_list=list()
		x_list=list()
		differencelist=list()
			
		for df in ds.filter(songno=songno,condition=condition):
			t = df.data['t'][i]
			DotY = df.data['DotY'][i]
			DotX = df.data['DotX'][i]
			t = df.data['t'][i]
			y_list.append(DotY)
			x_list.append(DotX)
			differencelist.append(DotY-DotX)
		
		# convert the lists to arrays
		y_array = numpy.array(y_list,dtype=float)
		x_array = numpy.array(x_list,dtype=float)
		
		#store the y one in a dictionary (key = condition)	
		y_arrays[condition] = y_array
	
	# get the results out of the dictionary
	instrumental = y_arrays['i']
	lyric = y_arrays['l']
	
	# process the results (for this timestep)
	mean_diff = numpy.mean(lyric) - numpy.mean(instrumental)
	var_sum = numpy.var(lyric)/len(lyric) + numpy.var(instrumental)/len(instrumental)
	tstat = mean_diff / (var_sum**0.5) 
	pval = stats.t.sf(abs(tstat), len(lyric)-1)
	pval_list.append(pval)
	
	print "At time = %.1fs lyric mean is %f more arousing than instrumental mean"%(
			t, lyric.mean()-instrumental.mean() )
	print "  T statistic = %f which corresponds to p = %.3f"%(tstat, pval)
	
	row_data = {  't': t,
			'imy': instrumental.mean(), 
			'ivy': numpy.var(instrumental), 
			'iny': len(instrumental),
			'lmy': lyric.mean(),
			'lny': len(lyric),
			'lvy': numpy.var(lyric),
			'tstat': tstat,
			'pval': pval }
	csv_out.writerow(row_data)
	
csv_file.close()


#differencelist = list()
#timelist = list()
#for i in range (0, sample_file.get_frame_count(),1):
#	for condition in ['i','l']:
#		differencelist.append(lyric.mean()-instrumental.mean() )
#for i in range(0, sample_file.get_frame_count(), 1):

	


# do a Y verses time plot
#pylab.figure(1)
#for df in ds.filter(songno=105):
#	 t = df.data['t']
#	 DotX = df.data['DotX']
#	 DotY = df.data['DotY']	   
#	 col = colours[df.metadata['condition']]
#	 pylab.title('Y vs t')
#	 pylab.plot(t,DotY, col+'-', label=df.metadata['subject'])
#pylab.legend()
#pylab.show()
