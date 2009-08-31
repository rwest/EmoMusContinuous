#!/usr/bin/env python
# encoding: utf-8
"""
joystick.py

A class to load and manage joystick data from emotional response to music tests
Created by Richard West on 2009-08-25.

"""

import sys
import os
import unittest
import csv
import re
import numpy


class untitled:
	def __init__(self):
		pass
		
class FileNameError(ValueError):
	pass
	
class Dataset:
	"""A set of data"""
	def __init__(self, folderpath=None):
		self.metadata = dict()
		self.data = list()
		if folderpath:
			self.load(folderpath)
		
			
	def filter(self,**kwargs):
		"""Filters the dataset based on keyword arguments
		(which are converted to strings before comparison)
		
		It is an iterator (i.e. usage "for df in dataset.filter(songno=105):" )"""
		for datafile in self.data:
			for key in kwargs:
				if datafile.metadata[key] != str(kwargs[key]):
					break
			else: # got to end of kwargs without breaking, so include the file
				yield datafile
		
	def load(self,folderpath='data'):
		print "Loading from",folderpath
		self.folderpath = folderpath
		for subfolder in os.listdir(folderpath):
			subfolderpath = os.path.join(folderpath, subfolder)
			if not os.path.isdir(subfolderpath):
				continue  # it's not a folder; continue to the next one.
			
			print "Loading from",subfolderpath	  
			filenames = os.listdir(subfolderpath)
			
			for filename in filenames:
				filepath = os.path.join(subfolderpath, filename)
				try:
					this_file = Datafile(filepath)
				except FileNameError:
					print "Couldn't parse the filename. Skipping",filename
					continue # to the next file
					
				#store in the master list
				self.data.append(this_file)
				
				for key,value in this_file.metadata.iteritems():
					try:
						self.metadata[key].add(value)
					except KeyError: # metadata[key] not defined yet
						self.metadata[key] = set([value])
				
				
				

	
class Datafile:
	def __init__(self, filepath=None):
		self.filename=''
		self.data=None
		self.metadata=dict()
		if filepath:
			self.load(filepath)
	
	def __repr__(self):
		subject = self.metadata['subject']
		songno = self.metadata['songno']
		condition = self.metadata['condition']
		length = len(self.data['t'])
		time = self.get_last_time()
		return "<Datafile song:%s condition:%s subject:%s time:%ss>"%(
				 songno, condition, subject, time )
		
	def parse_filename(self):
		#sm10_ts_subjectcodes1_01-00-songnumber-condition-artist-songtitle.txt
		import re
		match = re.match('sm10_ts_(?P<subject>.+?)_01-00-(?P<songno>\d+)-(?P<condition>[il])-(?P<artist>.+?)-(?P<songname>.+?)\.txt', self.filename)
		if not match: 
			raise FileNameError('Filename %s is not of the expected format'%self.filename)
		for key in ['subject', 'songno', 'condition', 'artist', 'songname']:
			self.metadata[key] = match.group(key)

	def get_last_time(self):
		"""Get the time of the last datapoint"""
		return self.data['t'][-1]
	def get_frame_count(self):
		"""Get the number of datapoints"""
		return len(self.data['t'])
		
	def load(self, filepath):
		# create new dictionary for data
		this_file_data = dict()
		# read data file
		#print "Reading ",filepath

		(path,filename) = os.path.split(filepath)
		self.filename = filename
		try:
			self.parse_filename()
		except FileNameError:
			# Couldn't parse filename. for now, raise the exception
			# if you don't care that you can't parse the filename, don't raise
			raise
			
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
		this_file_data['t'] = numpy.array(t,dtype=float)
		this_file_data['DotX'] = numpy.array(DotX,dtype=float)
		this_file_data['DotY'] = numpy.array(DotY,dtype=float)
		
		self.data = this_file_data


class loadingTests(unittest.TestCase):
	def setUp(self):
		pass
	def testLoadDatafile(self):
		filepath='data/Barbara Streisand/sm10_ts_vbla1048s2_01-00-069-l-barbrastreisand-thewaywewere.txt'
		assert os.path.isfile(filepath)
		datafile = Datafile()
		datafile.load(filepath)
	def testLoadDataset(self):
		dataset = Dataset()
		dataset.load('data')

class manipulationTests(unittest.TestCase):
	def setUp(self):
		self.dataset = Dataset('data')
	def testFilter(self):
		dataset=self.dataset
		for datafile in dataset.filter(songno=105, condition='i'):
			print datafile.data['DotX'].shape,
			
if __name__ == '__main__':
	# to run unit tests, use the following line
	unittest.main()
	
	
		