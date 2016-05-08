#!/usr/bin/python
# -*- coding: utf-8 -*-
##
# fid.py: Functions to extract FID 


#use __all__ to restrict what globals are visible to external modules.
__all__ = [
	'read_fid','FID'
]

## IMPORTS ####################################################################
import numpy as np
import matplotlib.pyplot as plt 
from topspin_to_python import FT


def read_fid(fp,times=None,sfo=0):
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
	fid =  d[:,0]+1j*d[:,1]
	return FID(fid,times,sfo)


class FID(object):
	
	def __init__(self,fid,times=None,sfo=0):
		self._fid = np.copy(fid)
		if times is None:
			times = self.arange(fid.shape)
		self._times = np.copy(times)
		if self.times.shape != self.fid.shape:
			raise ValueError('FID and associated times must have same shape')

		self._sfo = sfo

	@property
	def times(self):
	    return self._times
	@times.setter
	def times(self,times):
		if times.shape != self.times.shape:
			raise ValueError('New times must have same shape')
		self.times = times 

	@property
	def fid(self):
	    return self._fid
	@fid.setter
	def fid(self,fid):
		if fid.shape != self.fid.shape:
			raise ValueError('New fid must have same shape')
		self.fid = fid 

	@property
	def sfo(self):
	    return self._sfo
	@sfo.setter
	def sfo(self,sfo):
		self._sfo = sfo
	
	def ft(self,phase=0):
		"""
		Fourier transform of FID, with applied phase. 

		:param phase: Phase to apply to fourier transform  
		:type phase: float
		:return: The phased fourier transform of the fid 
		:rtype: :class:`FT`
		"""
		ft = np.fft.fftshift(np.fft.fft(self.fid*np.exp(1j*phase)))
		freqs = np.fft.fftfreq(self.fid.size,d=(self.times[1]-self.times[0]))
		freqs_shifted = np.fft.fftshift(freqs)
		return FT(ft,freqs_shifted,phase=phase,sfo=self.sfo,fid=self)

	def drop_points(self,n):
		"""
		Return a new fid with the first n points dropped 
		:param n: number of points to drop
		:type n: int

		:return: A new fid with the first n points dropped
		:rtype: :class:`FID`
		"""
		shifted_fid = self.fid[n:,...]
		shifted_times = self.times[n:,...]-self.times[n-1,...]
		return FID(shifted_fid,shifted_times)

	
	def plot(self,real=True,imag=True,drop_points=0,
		real_label="Reals",imag_label="Imaginaries",x_label='time(s)',
		y_label='arb units',*plotting_args,
		**plotting_kwargs):
		if real:
			plt.plot(self.times[drop_points:],np.real(self.fid[drop_points:]),
				*plotting_args,**plotting_kwargs)
		if imag: 
			plt.plot(self.times[drop_points:],np.imag(self.fid[drop_points:]),
				*plotting_args,**plotting_kwargs)
		plt.xlabel(x_label)
		plt.ylabel(y_label)

	def __repr__(self):
		return {'fid':self.fid,'times':self.times}.__repr__()[1:-1]

	def __str__(self):
		return {'fid':self.fid,'times':self.times}.__str__()[1:-1]



