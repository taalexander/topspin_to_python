#!/usr/bin/python
# -*- coding: utf-8 -*-
##
# acqu_pars.py: Functions to extract acquisition parameters 


#use __all__ to restrict what globals are visible to external modules.
__all__ = [
	'read_acqu_pars',
	'prune_acqu_pars',
	'format_acqu_pars'
]

## IMPORTS ####################################################################
import numpy as np
from jcamp import JCAMP_reader
import re 
import prune_lists
import copy 
def read_acqu_pars(fp):
	"""
	Read acquisition parameters from JCAMP-DX file 
	:param fp: File or string of fid
	:type fp: file,str

	:returns: FID as complexnumpy array
	:rtype: dict  
	"""
	
	acqu_dict = JCAMP_reader(fp)
	#many parameters have $ prepending
	#we need to remove them 
	acqu_dict = { re.sub('^\$','',k):v for k,v in acqu_dict.items()}


	return acqu_dict

	 
def format_acqu_pars(acqu_dict,reform_pars=prune_lists.DEFAULT_REFORMAT_PARS):
	"""
	Remove what I see as the unneeded acqusition parameters.
	If I did wrong with defaults, please submit a PR explaining what you need
	normally.

	:param acqu_dict: acquisition parameters dictionary
	:type acqu_dict: dict
	:param reform_pars: list of key-strings headers to group together in dicts. 
						Ie. sf01,sfo2,... to sfo:{1:...,2:...,...}
	:type reform_pars: list
	:returns: pruned acquistion parameter dictionary
	:rtype: dict
	"""		
	copied_acqu_dict = copy.deepcopy(acqu_dict)
	for k,v in acqu_dict.iteritems():
		reform = [ i for i,rp in enumerate(reform_pars) if k.startswith(rp)]
		if len(reform) > 0:
			rep_k = reform_pars[reform[0]]
			rep_dict = copied_acqu_dict.get(rep_k,{})
			if type(rep_dict) not in (dict,None):
				rep_dict = {} 
			new_key =  k[len(rep_k):]
			if new_key.isdigit():
				new_key = int(new_key)
			if type(rep_dict) is str:
				import pdb
				pdb.set_trace()
			rep_dict[new_key] = v

			copied_acqu_dict[rep_k] = rep_dict 
			copied_acqu_dict.pop(k)
			

	return copied_acqu_dict


def prune_acqu_pars(acqu_dict,prune_pars=prune_lists.DEFAULT_PRUNE_PARS):
	"""
	Remove what I see as the unneeded acqusition parameters.
	If I did wrong with defaults, please submit a PR explaining what you need
	normally.

	:param acqu_dict: acquisition parameters dictionary
	:type acqu_dict: dict
	:param prune_pars: list of key-strings to remove from acqu_dict
	:type prune_pars: list

	:returns: pruned acquistion parameter dictionary
	:rtype: dict
	"""
	copied_acqu_dict = copy.deepcopy(acqu_dict)
	for par in prune_pars:
		copied_acqu_dict.pop(par, None)

	return copied_acqu_dict