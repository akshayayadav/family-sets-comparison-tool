#!/usr/bin/python

from __future__ import division
import re
import sys
import operator


def read_family_sets_comparison_file(family_sets_comparison_fileName):
	fset_sset_seqcount_dict={}
	family_sets_comparison_file=open(family_sets_comparison_fileName, "r")

	for line in family_sets_comparison_file:
		line=line.strip()
		linearr=re.split(r'\s+',line)
		if(fset_sset_seqcount_dict.has_key(linearr[0])):
			fset_sset_seqcount_dict[linearr[0]][linearr[1]]=int(linearr[2])
		else:
			fset_sset_seqcount_dict[linearr[0]]={}
			fset_sset_seqcount_dict[linearr[0]][linearr[1]]=int(linearr[2])
		
	family_sets_comparison_file.close()
	return(fset_sset_seqcount_dict)

def get_overlapping_families(fset_sset_seqcount_dict, sset_fset_seqcount_dict):
	for ffamid in fset_sset_seqcount_dict:
		sset_famid, soverlap_percent=get_fset_sset_overlap(fset_sset_seqcount_dict[ffamid])
		fset_famid, foverlap_percent=get_fset_sset_overlap(sset_fset_seqcount_dict[sset_famid])
		
		if(ffamid==fset_famid):
			print '{0} {1} {2} {3}'.format(fset_famid, sset_famid, soverlap_percent, foverlap_percent)


def get_fset_sset_overlap(sset_seqcount_dict):
	sset_seqcount_dict_sorted=sorted(sset_seqcount_dict.items(), key=operator.itemgetter(1))
	largest_sset_famid=""
	largest_set_famid_seqcount=0
	total_seqcount=0
	for entry in sset_seqcount_dict_sorted:
		if(entry[1]>largest_set_famid_seqcount):
			largest_sset_famid=entry[0]
			largest_set_famid_seqcount=entry[1]
		total_seqcount=total_seqcount+entry[1]

	sset_overlap_percent = largest_set_famid_seqcount/total_seqcount
	return([largest_sset_famid, sset_overlap_percent])


####################################################################################################################
set1_set2_comparison_fileName=sys.argv[1]
set2_set1_comparison_fileName=sys.argv[2]

set1_set2_seqcount_dict = read_family_sets_comparison_file(set1_set2_comparison_fileName)
set2_set1_seqcount_dict = read_family_sets_comparison_file(set2_set1_comparison_fileName)

get_overlapping_families(set1_set2_seqcount_dict, set2_set1_seqcount_dict)
