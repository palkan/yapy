#coding: utf-8

import sys
import os
import re
import pprint
import argparse

DELIMETER = '\t'
COLLECT_EMPTY = False

def process_file(input_file,output_file):
	
	"""
		Read input file line by line and write result to output file.
		Output file contains SessionId and actions sequence. Action is a click (C) or query (Q). 
		
		If COLLECT_EMPTY is False take into account only sessions with at leas one action; otherwise empty sessions are also included (i.e. we have only M record).
		
		Note: assume that S record cannot occur without preceding M record (so we may skip S records at all)
		
		Args:
			input_file: input file object
			output_file: output file object
	"""

	sessions = []
	
	current_session = ""
	
	for line in input_file:
		vars = parse_line(line)	
		if vars:
			if not (current_session == vars[0]):
				prefix = '\n' if current_session else ''
				output_file.write(prefix+vars[0]+DELIMETER)
				current_session = vars[0]
			if vars[1]:
				output_file.write(vars[1])
			
			
def parse_line(line):
	"""
		Parse string and extract session id and type of record (Q or C) or only session id if COLLECT_EMPTY is True
		Assume that SESSION_ID contains only latin characters and digits and TimeSpend is a number
		Args:
			line: line to parse
	"""
	matches = re.search('^([\w\d]+)'+DELIMETER+'\d+'+DELIMETER+'([QC])',line)
	if matches:
		return matches.group(1), matches.group(2)
	elif COLLECT_EMPTY:
		matches = re.search('^([\w\d]+)'+DELIMETER+'M',line)
		if matches:
			return matches.group(1), False
	return False
	
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Proccess Yandex log')
	parser.add_argument('-i', dest='inputfile', type=argparse.FileType('r'), help='input file containing Yandex log', required=True)
	parser.add_argument('-o', dest='outputfile', type=argparse.FileType('w'), help='output file to write result', required=True)
	parser.add_argument('-empty', action='store_true', help='collect empty sessions or not')

	args = parser.parse_args()
	
	COLLECT_EMPTY = args.empty
	
	try:
		process_file(args.inputfile,args.outputfile)
		print('Done')
	except:
		print("Failed to process files. Maybe wrong paths or permissions?")
		sys.exit(0)
		