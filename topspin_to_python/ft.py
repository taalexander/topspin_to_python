#!/usr/bin/python
# -*- coding: utf-8 -*-
##
# ft.py: Functions to manipulate Fourier transform of FID


#use __all__ to restrict what globals are visible to external modules.
__all__ = [
    'FT'
]

## IMPORTS ####################################################################
import numpy as np
import matplotlib.pyplot as plt 
import scipy.optimize as opt
from topspin_to_python import FID

class FT(object):
    """
    Fourier transform data object. 

    :param ft: Numpy array of fourier transform
    :type ft: :class:`numpy.ndarray`
    :param freqs: Numpy array of frequencies centered at 0
    :type freqs: :class:`numpy.ndarray` 
    :param phase: Relative phase to original FID data
    :type phase: float 
    :param auto_phase: Whether to apply automatic phasing (APK)
    :type auto_phase: bool
    :param fid: Original fid of fourier transform
    :type fid: :class:`FID`
    """
    def __init__(self,ft,freqs=None,phase=0,sfo=0,auto_phase=False,fid=None):
        self._ft = ft
        if freqs is None:
            freqs = self.arange(ft.shape)
        self._freqs = freqs
        if self.freqs.shape != self.ft.shape:
            raise ValueError('FT and associated freqs must have same shape')

        self._phase = phase 
        self._sfo = sfo
        self._fid = fid

    @property
    def freqs(self):
        return self._freqs
    @freqs.setter
    def freqs(self,freqs):
        if freqs.shape != self.freqs.shape:
            raise ValueError('New freqs must have same shape')
        self.freqs = freqs

    @property
    def ft(self):
        return self._ft
    @ft.setter
    def ft(self,ft):
        if ft.shape != self.ft.shape:
            raise ValueError('New ft must have same shape')
        self.ft = ft

    @property
    def sfo(self):
        return self._sfo
    @sfo.setter
    def sfo(self,sfo):
        self._sfo = sfo

    @property
    def phase(self):
        return self._phase
    @phase.setter
    def phase(self,phase):
        self._phase = phase 

    @property
    def fid(self):
        return self._fid
    

    def ift(self):
        """
        Inverse Fourier Transform, with undone phasing

        :return: The inverse fourier transform of the fourier transform (FID)
        :rtype: :class:`FID`

        """
        n_fid = np.fft.ifft(np.fft.ifftshift(self.ft))*np.exp(-1j*self.phase)
        times = np.linspace(0,float(len(n_fid))/(self.freqs[-1]-self.freqs[0]),len(n_fid))
        return FID(n_fid,times=times,sfo=self.sfo)




    def plot(self,real=True,imag=True,ppm=True,centered=True,x_label='ppm',
        y_label='arb units',real_label="Reals",imag_label="Imaginaries",
        *plotting_args,**plotting_kwargs):

        if x_label=='ppm' and ppm==False:
            x_label='Hz'
        p_freqs = self.freqs
        if not centered and not ppm:
            p_freqs = p_freqs+self.sfo
        if ppm:
            p_freqs = p_freqs*1E6/self.sfo
        if real:
            plt.plot(p_freqs,np.real(self.ft),
                *plotting_args,**plotting_kwargs)
        if imag: 
            plt.plot(p_freqs,np.imag(self.ft),
                *plotting_args,**plotting_kwargs)

        plt.xlabel(x_label)
        plt.ylabel(y_label)


    def fid_region(self,left=None,right=None,ppm=False):
        """
        Extract region of the FID. 

        :param left: The left offset in kHz (or ppm if ppm is True)
        :type left: float
        :param right: The right offset in kHz (or ppm if ppm is True)
        :type right: float
        :param ppm: Determine if offsets will be given in kHz(False) or ppm(True)
        :type ppm: bool
        :return: Extracted fid, with frequencies 
        :rtype: np.ndarry,np.ndarray
        """
        if left is None:
            left = self.freqs[0]
        elif ppm:
            left = left*self.sfo/1E6
        if right is None:
            right = self.freqs[-1]
        elif ppm:
            right = right*self.sfo/1E6 
        indexes = np.where(np.logical_and(self.freqs>left,self.freqs<right))
        return self.ft[indexes],self.freqs[indexes]

    def integrate(self,left=None,right=None,real=True,ppm=False):
        """
        integrate the spectrum over a given region

        :param left: The left offset in kHz (or ppm if ppm is True)
        :type left: float
        :param right: The right offset in kHz (or ppm if ppm is True)
        :type right: float
        :param real: Whether to integrate the real portion of the spectrum (True),
                    or imaginary (False)
        :type real: bool
        :param ppm: Determine if offsets will be given in kHz(False) or ppm(True)
        :type ppm: bool
        """
        ft,_ = self.fid_region(left,right,ppm)
        ft = ft.real if real else self.ft.imag
        return np.sum(ft)

    def fit_lorentzian(self,left=None,right=None,ppm=False,gen_data=False,width_guess=1000.,**opt_pars):
        """
        Fit the spectrum to a lorentzian function. 
        
        :param method: Optimization method to use, see `Scipy minimize 
        http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html#scipy.optimize.minimize`
        :type method: str
        :param left: The left offset in kHz (or ppm if ppm is True) not used with use_lorentzian
        :type left: float
        :param right: The right offset in kHz (or ppm if ppm is True) not used with use_lorentzian
        :type right: float
        :param real: Whether to integrate the real portion of the spectrum (True),
                    or imaginary (False)
        :param ppm: Determine if offsets will be given in kHz(False) or ppm(True) not used with use_lorentzian
        :type ppm: bool
        :param \**kwargs: Additional minimize parameters see `Scipy minimize 
        http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html#scipy.optimize.minimize`

        :param gen_data: Whether to generate a :class:`FT` from fitted lorentzian parameters 
        :type gen_data: bool

        :return: popt(Amplitude,phase,width,location), fitted parameter covariances, generated spectrum by fit (optional, controlled
                                        by gen_data)
        :rtype:popt(Amplitude,phase,width,location),pcov,:class:`FT`(optional)
        """
        def lorentzian(x,A,phase,w,x0):
            absorption = A*1/(np.pi*w/2)/(1+((x-x0)/(w/2))**2)
            dispersion = 1j*A*((x-x0)/(w/2))/(np.pi*w/2)/(1+((x-x0)/(w/2))**2)
            return np.exp(1j*phase)*(absorption+dispersion)

        
        def fit_fun(x,A,phase,w,x0): 
            l = lorentzian(x,A,phase,w,x0)
            #add in quadrature
            return l.real**2+l.imag**2
        ft,freqs = self.fid_region(left,right,ppm)
        A = np.absolute(ft[np.argmax(np.absolute(ft))])
        a_ft = ft.real**2+ft.imag**2
        popt,pcov = opt.curve_fit(fit_fun,freqs,a_ft,p0=[A,0,width_guess,0])

        if gen_data:
            gen_ft = FT(lorentzian(freqs,*popt),freqs,phase=popt[2],fid=self.fid)
            return popt,pcov,gen_ft

        return popt,pcov


    def apk(self,use_lorentzian=False,left=None,right=None,ppm=False,**opt_pars):
        """
        Automatically phase the fourier transform to maximize the integral over a region.
        
    
        :param use_lorentzian: Whether to do phasing by fitting spectrum to lorentzian. 
        :type use_lorentzian: bool
        :param left: The left offset in kHz (or ppm if ppm is True) not used with use_lorentzian
        :type left: float
        :param right: The right offset in kHz (or ppm if ppm is True) not used with use_lorentzian
        :type right: float
        :param real: Whether to integrate the real portion of the spectrum (True),
                    or imaginary (False)
        :param ppm: Determine if offsets will be given in kHz(False) or ppm(True) not used with use_lorentzian
        :type ppm: bool
        :param \**kwargs: Additional minimize parameters see `Scipy minimize 
        http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html#scipy.optimize.minimize`

        :return: Phased spectrum
        :rtype: :class:`FT`
        """
        if self.fid is not None:
            fid = self.fid
        else:
            fid = self.ift()

        if use_lorentzian:
            min_func = lambda phase: -fid.ft(phase[0]).fit_lorentzian(left=left,right=right,ppm=ppm,gen_data=False,width_guess=1000.,**opt_pars)[0][0]
        else:
            min_func = lambda phase: -fid.ft(phase[0]).integrate(left,right).real
        
        res = opt.minimize(min_func,[np.pi],**opt_pars) 
        return fid.ft(res.x[0])


    def __repr__(self):
        return {'ft':self.ft,'freqs':self.freqs,'phase':self.phase,'sfo':self.sfo}.__repr__()[1:-1]

    def __str__(self):
        return {'ft':self.ft,'freqs':self.freqs,'phase':self.phase,'sfo':self.sfo}.__str__()[1:-1]
