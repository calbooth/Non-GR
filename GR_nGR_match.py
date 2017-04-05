#!/usr/bin/env python

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

q = default_args
q['mass1'] = 20
q['mass2'] = 30
q['delta_t'] = 1./4096
q['f_lower'] = 20
q['approximant'] = 'IMRPhenomPv2'

hp, hc = pycbc.waveform.waveform.get_td_waveform(**q) # Generte GR waveform dchi0 = 0
'''
	Creating the PSD
'''
tlen = len(hp) # Create parameter tlen
tlen = math.log(tlen, 2) # Take the log base 2 of tlen
tlen = math.ceil(tlen) # Round up to the nearest integer (result is a float)
tlen = 2.0**tlen # Raise 2 to the nearest integer to help FFT go faster
tlen = int(tlen)

hp.resize(tlen) # Resize hp
f_low = 20 # Lowest frequency

# Generate the aLIGO ZDHP PSD
delta_f = 1.0 / hp.duration # Frequency incirment
flen = tlen/2 + 1
psd = aLIGOZeroDetHighPower(flen, delta_f, f_low) # Creating PSD


#########################################################
##---------------Waveforms for varying M1--------------##
#########################################################
'''
	Non-GR Waveform
'''
p = default_args
p['mass2'] = 30
p['delta_t'] = 1./4096
p['f_lower'] = 20
p['approximant'] = 'IMRPhenomPv2'
p['dchi0'] = 1.0

'''
	GR Waveform
'''
r = default_args
r['mass2'] = 30
r['delta_t'] = 1./4096
r['f_lower'] = 20
r['approximant'] = 'IMRPhenomPv2'

mass1 = np.linspace(5, 35, 100)
pmatch = np.zeros(100)
rmatch = np.zeros(100)

j = 0
for i in mass1:
	p['mass1'] = i
	r['mass1'] = i	

        pp, pc = pycbc.waveform.waveform.get_td_waveform(**p)
        rp, rc = pycbc.waveform.waveform.get_td_waveform(**r)

        # Resize the waveforms to the same length
        pp.resize(tlen)
	rp.resize(tlen)	

        # Note: This takes a while the first time as an FFT plan is generated
        # subsequent calls are much faster.
        mp, ip = match(hp, pp, psd=psd, low_frequency_cutoff=f_low)
        mr, ir = match(hp, rp, psd=psd, low_frequency_cutoff=f_low)

	pmatch[j] = mp	
	rmatch[j] = mr
	
	j += 1

plt.figure()
plt.plot(mass1, pmatch, label = 'Non-GR')
plt.plot(mass1, rmatch, label = 'GR')
plt.xlabel('$M_1(M_{\odot})$', fontsize = 20)
plt.ylabel('Match', fontsize = 20)
plt.title(('Match plot for varying $M_1$'), fontsize = 20)
plt.legend(loc = 'best')
plt.grid()
plt.show()
plt.savefig('dchi0_0.1'+'.png', bbox = 'tight')
