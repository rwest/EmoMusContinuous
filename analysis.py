# this program should do some analysis

import csv

data = csv.reader(open('../../data/emo mus/phase 2 timeseries/timeseries smooth 10/sm10_ts_aalb1094s1_01-00-063-i-bettemidler-windbeneathmywings.txt'), delimiter=',')
for row in data:
...	print ', '.join(row)