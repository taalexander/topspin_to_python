#!/usr/bin/python
# -*- coding: utf-8 -*-
##
# fid.py: Functions to extract FID 


#use __all__ to restrict what globals are visible to external modules.
__all__ = [
	'read_experiment'
]

## IMPORTS ####################################################################
import numpy as np
import os.path
from fid import read_fid
from acqu_pars import read_acqu_pars, prune_acqu_pars, format_acqu_pars
import prune_lists


## METHODS ####################################################################
def read_experiment(exp_fp,prune_acqu=True,format_acqu=True,prune_list=None,format_list=None):
    """
    Read TopSpin Experiment data folder and extract the fid/acquistion parameters. 

    :param exp_fp: File path to experiment folder
    :type exp_fp: str
    :param prune_acqu: Whether to prune the acquisition parameters or not
    :type prune_acqu: bool
    :param format_acqu: Whether to format the acquistion parameters or not
    :type format_acqu: bool
    :param prune_list: List of keys to remove from acquistion parameters. By default 
                    is :any:`prune_lists.DEFAULT_PRUNE_PARS`
    :type prune_list: str
    :param format_list: List of keys to reformat in acquistion parameters. By default 
                    is :any:`prune_lists.DEFAULT_REFORMAT_PARS`
    :type format_list: str
    """
    if prune_list is None:
        prune_list = prune_lists.DEFAULT_PRUNE_PARS
    if format_list is None:
        format_list = prune_lists.DEFAULT_REFORMAT_PARS


    experiment = {}



    acqu_pars = read_acqu_pars(exp_fp+'acqu')
    formatted_acqu = format_acqu_pars(acqu_pars,format_list)

    if prune_acqu:
        acqu_pars = prune_acqu_pars(acqu_pars,prune_list)
    if format_acqu:
        acqu_pars = formatted_acqu

    experiment['acqu'] = acqu_pars

    if os.path.isfile(exp_fp+'fid'):
        
        sfo = formatted_acqu['sfo'][\
            np.nonzero(formatted_acqu['recchan'])[0][0]]*1E6
        td = formatted_acqu['td']
        aq = float(td)/formatted_acqu['sw_h']/2
        experiment['acqu']['aq'] = aq
        times = np.linspace(0,aq,td/2)
        exp_fid = read_fid(exp_fp+'fid',times=times,sfo=sfo)
        experiment['fid'] = exp_fid 

    # perform pruning/formatting

    

    return experiment 