#!/usr/bin/python
# -*- coding: utf-8 -*-
##
# fid.py: Functions to extract FID 


#use __all__ to restrict what globals are visible to external modules.
__all__ = [
	'read_fid'
]

## IMPORTS ####################################################################
import numpy as np




def read_fid(fp):
	"""
	Read an FID file from TopSpin and return data as :type:`numpy.complex128`

	:param fp: File or string of fid
	:type fp: file,str

	:returns: FID as complexnumpy array
	:rtype: :type:`numpy.complex128`  
	"""

	# Topspin FIDs are stored as real/complex interleaved big endian 
	# formatted float32 
	d = np.fromfile(fp,dtype='>i4').reshape(-1,2)
	return d[:,0]+1j*d[:,1]