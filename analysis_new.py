# this file is written as a script. 
# Suggested use: load ipython with ipython -pylab
# then run this with 
# %run analysis.py
# all the data will then be in memory for you to play with

import csv
import os
import pylab
import numpy

from scipy import stats

import joystick
from joystick import Dataset, Datafile

data_folder = "data"


ds = Dataset(data_folder)

colours={'i': 'b', 
		 'l': 'r'} # instrumental = blue, lyrics = red
print "Reminder: Lyrics = Red, Instrumental = Blue"

pylab.figure()
pylab.show()

for figureno,songno in enumerate(ds.metadata['songno']):
	# figureno will increment from 0
	# songno will go through all the available songno's in the Dataset ds
	#pylab.figure(figureno)
		
	sample_file = ds.filter(songno=songno).next()
	
	pval_list = list() # list of P values (one for each time step)
	mean_diff_list = list()
	
	# set up a CSV file writer
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
		
		# loop over condition (instrumental/lyric)
		for condition in ['i','l']:
			col = colours[condition]
			y_list=list()
			x_list=list()
			differencelist=list()
				
			# loop over subjects' responses (to this song and condition at this timestep)
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
			
			#store the y results in a dictionary (key = condition)	
			y_arrays[condition] = y_array
		
		# get the results back out of the dictionary
		instrumental = y_arrays['i']
		lyric = y_arrays['l']
		
		# process the results (for this timestep)
		mean_diff = numpy.mean(lyric) - numpy.mean(instrumental)
		var_sum = numpy.var(lyric)/len(lyric) + numpy.var(instrumental)/len(instrumental)
		tstat = mean_diff / (var_sum**0.5) 
		pval = stats.t.sf(abs(tstat), len(lyric)-1 )
		pval_list.append(pval)
		mean_diff_list.append(mean_diff)
		
# 		print "At time = %.1fs lyric mean is %f more arousing than instrumental mean"%(
# 				t, lyric.mean()-instrumental.mean() )
# 		print "  T statistic = %f which corresponds to p = %.3f"%(tstat, pval)
 		
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
	#sample_file.metadata['artist']+['.csv'], (0,1,4))

	#convert to arrays
	pval_array = numpy.array(pval_list)
	mean_diff_array = numpy.array(mean_diff_list)
	
	# do a pval versus time plot
	# pylab.clf()
	t = df.data['t']
	
	#pylab.plot(t,mean_diff_array, colours['l'])
	
	pylab.subplot(4,4,figureno)
	pylab.plot(t,mean_diff_array, colours['l'])
	pylab.title("%s - %s"%(df.metadata['artist'], df.metadata['songname']))
	pylab.xlabel('Time (s)')
	pylab.ylabel('Diff value')	
		# put coloured dots on the points for which instrumental was more arousing
	for i,diff in enumerate(mean_diff_array):
		if diff<0:
			 pylab.plot(t[i],mean_diff_array[i], colours['i']+'.')
	
	# put coloured dashes on the points for which p < 0.005		 
	for i,diff in enumerate(pval_array):
		if pval<0.005:
			pylab.plot(t[i],mean_diff_array[i], linestyle='-', color='g')
	# draw the horizontal line of p=0.005
	#pylab.axhline(y=0.005, linestyle=':', color='k')
	#pylab.text(max(t)/2, 0.005, "p=0.005", color='k')
	
	#pylab.legend()
	pylab.show()

#p = plt.axhspan(0.25, 0.75, facecolor='0.5', alpha=0.5)


#differencelist = list()
#timelist = list()
#for i in range (0, sample_file.get_frame_count(),1):
#	for condition in ['i','l']:
#		differencelist.append(lyric.mean()-instrumental.mean() )
#for i in range(0, sample_file.get_frame_count(), 1):

