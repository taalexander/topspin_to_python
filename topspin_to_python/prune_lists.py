#!/usr/bin/python
# -*- coding: utf-8 -*-
##
# prune_lists.py: List of parameters to prune 


#use __all__ to restrict what globals are visible to external modules.


## IMPORTS ####################################################################



DEFAULT_PRUNE_PARS = ['acqt0','anavpt','aq_mod','aqseq','aunm','autopos',
                    'bytorda','cfdgtyp','cfrgtyp','chemstr','cpdprg',
                    'datatype','dbp07','dbpoal','dbpoffs','decbnuc',
                    'decim','decnuc','decstat','digmod','digtyp','dp07',
                    'dbpnam', 'dbpnam3', 'dbpnam4',
                     'dbpnam5','dbpnam6','dbpnam7',                    
                     'decbnuc','decstat','dp07','dpname','dpoal',
                     'dpoffs','dqdmode','dr','ds','dslist','dspfirm','dspfvs',
                     'dtypa','end','f1list','f2list','f3list','fcuchan','fnmode',
                     'fntype','fq1list','fq2list','fq3list','fq4list','fq5list',
                     'fq6list','fq7list','fq8list','frqlo3','frqlo3n','ftlpgn',
                     'gp031','gpnam','grdprog','grpdly','hdduty',
                     'hdrate','holder','hpmod','hpprgn','instrum','l',
                     'lfilter','lgain','linpstp','lockfld','lockgn','locsw',
                     'ltime','masr','masrlst','nbl','nlogch','prgain',
                     'probhd','prosol','sp07','spectr','spnam','subnam',
                     'tp07','tpname','tunhin','tunhout',
                     'tunxout','usera1','usera2','usera3','usera4', 'usera5',
                     'x','y','yl','ymax_a','ymin_a','zgoptns']


DEFAULT_REFORMAT_PARS = ['sfo','bf','cpdprg','dbpnam','subnam','tpname','spnam',
                        'gpnam','dpname','dbpnam','dpname','nuc','o','zl','usera',
                        'te','tun','fl','fq']