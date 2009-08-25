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
    def __init__(self, folderpath=None):
        pass
        self.data=list()
        if folderpath:
            self.load(folderpath)
        
    def load(self,folderpath='data'):
        print "Loading from",folderpath
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
                

    
class Datafile:
    def __init__(self, filepath=None):
        self.filename=''
        self.data=None
        self.metadata=dict()
        if filepath:
            self.load(filepath)
        
    def parse_filename(self):
        #sm10_ts_subjectcodes1_01-00-songnumber-condition-artist-songtitle.txt
        import re
        match = re.match('sm10_ts_(?P<subject>.+?)_01-00-(?P<songno>\d+)-(?P<condition>[il])-(?P<artist>.+?)-(?P<songname>.+?)\.txt', self.filename)
        if not match: 
            raise FileNameError('Filename %s is not of the expected format'%self.filename)
        for key in ['subject', 'songno', 'condition', 'artist', 'songname']:
            self.metadata[key] = match.group(key)
        
    def load(self, filepath):
        # create new dictionary for data
        this_file_data = dict()
        # read data file
        print "Reading ",filepath

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
        this_file_data['t'] = numpy.array(t)
        this_file_data['DotX'] = numpy.array(DotX)
        this_file_data['DotY'] = numpy.array(DotY)
        
        self.data = this_file_data


class untitledTests(unittest.TestCase):
    def setUp(self):
        pass
    def testLoadDataset(self):
        dataset = Dataset()
        dataset.load('data')

if __name__ == '__main__':
    unittest.main()