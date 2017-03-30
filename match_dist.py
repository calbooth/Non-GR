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
q['mass1'] = 20
q['mass2'] = 30
#q['spinx1'] = 0.5
#q['spinx2'] = -0.5
q['delta_t'] = 1./4096
q['f_lower'] = 40
q['approximant'] = 'IMRPhenomD'

#hp, hc = pycbc.waveform.waveform._lalsim_td_waveform(**q)

hp, hc = pycbc.waveform.waveform.get_td_waveform(**q)


#########################################################
##--------------------NON GR PARAMS--------------------##
#########################################################

p = default_args
p['mass1'] = 20
p['mass2'] = 30
#p['spinx1'] = 0.5
#p['spinx2'] = -0.5
p['delta_t'] = 1./4096
p['f_lower'] = 40
p['approximant'] = 'IMRPhenomD'

dchi0 = np.arange(-0.5, 0.5, 0.01)
distance = np.linspace(0.0, 450.0, 100)

# lower frequency
f_low = 40

# Empty match 2D array
M = np.zeros([100, 100])

k = 0

for i in dchi0:
        p['sigma1'] = i
        l = 0
        for j in distance:

                p['distance'] = j
                sp, sc = pycbc.waveform.waveform.get_td_waveform(**p)

                                                        
		#Resize the waveforms to the same length
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
                #print 'The match is: %1.3f' % m
                M[k, l] = m
                l += 1
        k += 1

plt.figure()
plt.contourf(dchi0, mass1, M)
plt.ylabel('$\iota$', fontsize = 20)
plt.xlabel('$d\sigma_1$', fontsize = 20)
plt.title('Match plot of varying $d\sigma1$ and $D_L$', fontsize = 20)
plt.colorbar()
plt.show()

