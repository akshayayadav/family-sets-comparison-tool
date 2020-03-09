#!/usr/bin/python

#Author: Akshay Yadav
#Version: 1.0

import re
import sys
import os
import subprocess
import argparse


################################################################################

def print_famlist_file(set_hmmscan_tblout_fileName, famlist_set_fileName):
	assign_sequences_to_families_using_hmmscan_tblout(set_hmmscan_tblout_fileName, famlist_set_fileName)


## for reading the famlist file format: <famid> <seqid> with new sequence on each line
## reads the famlist file into a 2D dictionary(where 1st key is the family id and second key is the sequence id) and a 1D dictionary (where key is the sequence id and value is family id)
def read_famlist_file(famlist_fileName, famid_seqid_dict, seqid_dict):
	famlist_file=open(famlist_fileName,"r")
	for line in famlist_file:
		line=line.rstrip()
		linearr=re.split(r'\s+', line)
		famid=linearr[0]
		seqid=linearr[1]
		seqid_dict[seqid]=famid
		if(famid_seqid_dict.has_key(famid)):
			famid_seqid_dict[famid][seqid]=1
		else:
			famid_seqid_dict[famid]={}
			famid_seqid_dict[famid][seqid]=1
	
	
	famlist_file.close()

## family set in the first argument to the family set in the second argument
def compare_family_set_dicts(fam_seqid_dict, seqid_dict, comparison_result_outfileName):
	
	comparison_result_outfile=open(comparison_result_outfileName, "w")	
	
	for famid in fam_seqid_dict:
		set2_famid_counts={}
		other_set_famid_counts_dict={}
		get_other_set_famid_counts(fam_seqid_dict[famid], seqid_dict, other_set_famid_counts_dict)
		print_get_other_set_famid_counts_to_file(comparison_result_outfile, other_set_famid_counts_dict, famid)

	comparison_result_outfile.close()

## calculates how many different families for second argument the family in the first argument belongs to.
def get_other_set_famid_counts(seqid_dict_for_famid, seqid_dict, famid_counts_dict):
	for seqid in seqid_dict_for_famid:
		if not (seqid_dict.has_key(seqid)):
			continue
		other_set_famid=seqid_dict[seqid]
		if(famid_counts_dict.has_key(other_set_famid)):
			famid_counts_dict[other_set_famid]+=1
		else:
			famid_counts_dict[other_set_famid]=1

def print_get_other_set_famid_counts_to_file(comparison_result_outfile, other_set_famid_counts_dict, reference_famid):
	for famid in other_set_famid_counts_dict:
		comparison_result_outfile.write(reference_famid+" "+famid+" "+str(other_set_famid_counts_dict[famid])+"\n")


## wrapper for comparing families
def compare_family_sets_using_famlists(family_set1_name, family_set2_name, output_dirName):

	family_set1_famlist_fileName=output_dirName+"/"+family_set1_name+".famlist"
	family_set2_famlist_fileName=output_dirName+"/"+family_set2_name+".famlist"
		
	family_set1_famid_seqid_dict={}
	family_set2_famid_seqid_dict={}

	family_set1_seqid_dict={}
	family_set2_seqid_dict={}

	read_famlist_file(family_set1_famlist_fileName, family_set1_famid_seqid_dict, family_set1_seqid_dict)
	read_famlist_file(family_set2_famlist_fileName, family_set2_famid_seqid_dict, family_set2_seqid_dict)


	compare_family_set_dicts(family_set1_famid_seqid_dict, family_set2_seqid_dict, output_dirName+"/"+family_set1_name+"-"+family_set2_name)
	compare_family_set_dicts(family_set2_famid_seqid_dict, family_set1_seqid_dict, output_dirName+"/"+family_set2_name+"-"+family_set1_name)
#############################################################################################################################################
family_set1_name = "set1"
family_set2_name = "set2"
output_dirName = "/data"
compare_family_sets_using_famlists(family_set1_name, family_set2_name, output_dirName)

