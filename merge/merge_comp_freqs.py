## Merges two CSV documents.
##

import csv
import sys

class Merged(object):
	def __init__(self):
		self._all_modules_with_complexity = {}
		self._merged = {}

	def sorted_result(self):
		# Sort on descending order:
		ordered = sorted(self._merged.items(), key=lambda item: item[1][0], reverse=True)
		return ordered

	def extend_with(self, name, freqs):
		if name in self._all_modules_with_complexity:
			complexity = self._all_modules_with_complexity[name]
			self._merged[name] = freqs, complexity

	def record_detected(self, name, complexity):
		self._all_modules_with_complexity[name] = complexity
	
def skip_heading(f):
	next(f)
	
def parse_csv(merged, filename, parse_action):
	with open(filename, 'rb') as csvfile:
		r = csv.reader(csvfile, delimiter=',')
		skip_heading(r)
		for row in r:
			parse_action(merged, row)

def write_csv(stats):
	print 'module,revisions,code'
	for s in stats:
		name, (f,c) = s
		print name + ',' + f + ',' + c
	
def parse_complexity(merged, row):
	name = row[1][2:]
	complexity = row[4]
	merged.record_detected(name, complexity)

def parse_freqs(merged, row):
	name = row[0]
	freqs = row[1]
	merged.extend_with(name, freqs)

def merge(revs_file, comp_file):
	merged = Merged()
	parse_csv(merged, comp_file, parse_complexity)
	parse_csv(merged, revs_file, parse_freqs)
	write_csv(merged.sorted_result())

if __name__ == '__main__':
	# TODO: check!
	revs_file = sys.argv[1]
	comp_file = sys.argv[2]
	merge(revs_file, comp_file)