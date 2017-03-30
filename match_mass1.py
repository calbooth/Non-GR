import numpy as np
import pycbc
import pycbc.waveform.waveform
from pycbc.waveform import parameters
from pycbc.waveform import td_approximants, fd_approximants
from pycbc.filter import match
from pycbc.psd import aLIGOZeroDetHighPower
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


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
#p['mass1'] = 20
p['mass2'] = 30
#p['spinx1'] = 0.5
#p['spinx2'] = -0.5
p['delta_t'] = 1./4096
p['f_lower'] = 40
p['approximant'] = 'IMRPhenomD'

dchi0 = np.arange(-0.5, 0.5, 0.01)
mass1 = np.arange(15, 45, 0.3) 

# lower frequency
f_low = 40

# Empty match 2D array
M = np.zeros([100, 100])

k = 0

for i in dchi0:
	p['dchi7'] = i
	l = 0	
	for j in mass1:
		# Iterating through the masses
		p['mass1'] = j
		sp, sc = pycbc.waveform.waveform.get_td_waveform(**p)

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
		#print 'The match is: %1.3f' % m
		M[l, k] = m
		l += 1
	k += 1
'''
Plotting the result
'''
levels=np.array([0.97])
x = 0.0
y = 20.0

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
i = ax.contourf(dchi0, mass1, M, 100)
ax.set_ylabel('$M_1$', fontsize = 20)
ax.set_xlabel('$d\chi_{7}$', fontsize = 20)
ax.set_title('Match plot of varying $d\chi_{7}$ and $M_1$', fontsize = 20)
ax.annotate('$\otimes$', (x, y))
colorbar_ax = fig.add_axes([0.905, 0.11, 0.05, 0.77])
fig.colorbar(i, cax = colorbar_ax)
con = ax.contour(dchi0, mass1, M, 1 ,levels=levels)
ax.clabel(con, color = 'k')
plt.show()
