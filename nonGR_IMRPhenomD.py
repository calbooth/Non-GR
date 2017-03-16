import numpy as np
import pycbc
import pycbc.waveform.waveform
from pycbc.waveform import parameters
from pycbc.waveform import td_approximants, fd_approximants
from pycbc.filter import match
from pycbc.psd import aLIGOZeroDetHighPower
import matplotlib.pyplot as plt

# get the default args:
default_args = (parameters.fd_waveform_params.default_dict() + \
    parameters.td_waveform_params).default_dict()

q = default_args
q['mass1'] = 10
q['mass2'] = 50
q['spinx1'] = 0.5
q['spinx2'] = -0.5
q['delta_t'] = 1./4096
q['f_lower'] = 40
q['approximant'] = 'IMRPhenomD'

hp, hc = pycbc.waveform.waveform._lalsim_td_waveform(**q)

#########################################################
##--------------------NON GR PARAMS--------------------##
#########################################################

p = default_args
p['mass1'] = 10
p['mass2'] = 50
q['spinx1'] = 0.5
q['spinx2'] = -0.5
p['delta_t'] = 1./4096
p['f_lower'] = 40
p['approximant'] = 'IMRPhenomD'


# dchi non-GR
p['dchi0'] = 1

'''
p['dchi1'] = 1
p['dchi2'] = 1
p['dchi3'] = 1
p['dchi4'] = 1
p['dchi5'] = 1
p['dchi5l'] = 1
p['dchi6'] = 1
p['dchi6l'] = 1
p['dchi7'] = 1

# phi non-GR
p['phi1'] = 1
p['phi2'] = 1
p['phi3'] = 1
p['phi4'] = 1

# xi non-GR
p['dxi1'] = 1
p['dxi2'] = 1
p['dxi3'] = 1
p['dxi4'] = 1
p['dxi5'] = 1
p['dxi6'] = 1

# dsigma non-GR
p['dsigma1'] = 1
p['dsigma2'] = 1
p['dsigma3'] = 1
p['dsigma4'] = 1

# dalpha non-GR
p['dalpha1'] = 1
p['dalpha2'] = 1
p['dalpha3'] = 1
p['dalpha4'] = 1
p['dalpha5'] = 1

# beta non-GR
p['dbeta1'] = 1
p['dbeta2'] = 1
p['dbeta3'] = 1

# alpha PPE non-GR
p['alphaPPE'] = 1
p['alphaPPE0'] = 1
p['alphaPPE1'] = 1
p['alphaPPE2'] = 1
p['alphaPPE3'] = 1
p['alphaPPE4'] = 1
p['alphaPPE5'] = 1
p['alphaPPE6'] = 1
p['alphaPPE7'] = 1

# beta PPE non-GR
p['betaPPE'] = 1
p['betaPPE0'] = 1
p['betaPPE1'] = 1
p['betaPPE2'] = 1
p['betaPPE3'] = 1
p['betaPPE4'] = 1
p['betaPPE5'] = 1
p['betaPPE6'] = 1
p['betaPPE7'] = 1
'''

sp, sc = pycbc.waveform.waveform._lalsim_td_waveform(**p)

# Define lower frequency
f_low = 40

# Resize the waveforms to the same length
tlen = max(len(sp), len(hp))
sp.resize(tlen)
hp.resize(tlen)

# Generate the aLIGO ZDHP PSD
delta_f = 1.0 / sp.duration
flen = tlen/2 + 1
psd = aLIGOZeroDetHighPower(flen, delta_f, f_low)

# Note: This takes a while the first time as an FFT plan is generated
# subsequent calls are much faster.
m, i = match(hp, sp, psd=psd, low_frequency_cutoff=f_low)
print 'The match is: %1.3f' % m

plt.figure()
plt.plot(hp.sample_times, hp, label = 'GR IMRPhenomD')
plt.plot(sp.sample_times, hp, label = 'Non-GR IMRPhenomD')
plt.xlabel('Time(s)', fontsize = 20)
plt.ylabel('h$_+$(m)', fontsize = 20)
plt.title('IMRPhenomD, All non-GR, $M_1 = 10 M_\odot, M_2 = 50 M_\odot, S_{x_1} = 0.5, S_{x_2} = -0.5 $', fontsize = 20)
plt.legend(loc = 'best')
plt.grid()
plt.show()
