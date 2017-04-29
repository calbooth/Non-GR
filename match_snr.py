import matplotlib

matplotlib.use('Agg')

import numpy as np
import pycbc
import pycbc.waveform.waveform
from pycbc.waveform import parameters
from pycbc.waveform import td_approximants, fd_approximants
from pycbc.filter import match
from pycbc.psd import aLIGOZeroDetHighPower
import matplotlib.pyplot as plt
import math

# get the default args:
default_args = (parameters.fd_waveform_params.default_dict() + \
    parameters.td_waveform_params).default_dict()

default_args_ngr = (parameters.fd_waveform_params.default_dict() + \
    parameters.td_waveform_params).default_dict()

q = default_args
q['mass1'] = 20
q['mass2'] = 30
q['spin1x'] = 0.0 
q['delta_t'] = 1./4096
q['f_lower'] = 20
q['approximant'] = 'IMRPhenomPv2'

hp, hc = pycbc.waveform.waveform.get_td_waveform(**q)
# Define lower frequency
f_low = 20

# Resize the waveforms to the same length
tlen = len(hp)
tlen = math.log(tlen, 2)
tlen = math.ceil(tlen)
tlen = 2.0**tlen
tlen = 2.0*tlen
tlen = int(tlen)

hp.resize(tlen)

# Generate the aLIGO ZDHP PSD
delta_f = 1.0 / hp.duration
flen = tlen/2 + 1
psd = aLIGOZeroDetHighPower(flen, delta_f, f_low)

#########################################################
##--------------------NON GR PARAMS--------------------##
#########################################################

p = default_args_ngr
p['mass1'] = 20
p['mass2'] = 30
p['delta_t'] = 1./4096
p['f_lower'] = 20
p['approximant'] = 'IMRPhenomPv2'

# Setting the non-GR parameter to have some value
p['dchi0'] = 10**-3
       
# Creating non-GR waveform
sp, sc = pycbc.waveform.waveform.get_td_waveform(**p)
sp.resize(tlen)
# Note: This takes a while the first time as an FFT plan is generated
# subsequent calls are much faster.
m, i = match(hp, sp, psd=psd, low_frequency_cutoff=f_low)
print m 
