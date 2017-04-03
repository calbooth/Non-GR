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

nGR = ['dchi0','dchi1','dchi2','dchi3','dchi4','dchi6','dchi7']#,'phi1',
#'phi2','phi3','phi4','dxi1','dxi2','dxi3','dxi4','dxi5','dxi6','dsigma1','dsigma2','dsigma3',
#'dsigma4','dalpha1','dalpha2','dalpha3','dalpha4','dalpha5','dbeta1','dbeta2','dbeta3','alphaPPE',
#'alphaPPE0','alphaPPE1','alphaPPE2','alphaPPE3','alphaPPE4','alphaPPE5','alphaPPE6','alphaPPE7',
#'betaPPE','betaPPE0','betaPPE1','betaPPE2','betaPPE3','betaPPE4','betaPPE5','betaPPE6','betaPPE7']


# Looping through the list
for nonGR in nGR:
	# Setting the non-GR value to zero
	j = 0
	while True:
		# Setting the non-GR parameter to have some value
		p[str(nonGR)] = j
	
		sp, sc = pycbc.waveform.waveform.get_td_waveform(**p)
		
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
		
		# Re-setting the non-GR parameter to zero.
                p[str(nonGR)] = 0

		# If the match is less than 0.97 then break from the loop
		if m < 0.97:
			print '%s = %.2f'%(nonGR, j)
			break
		# Increasing the non-GR value
		j += 0.01

	'''
	Plotting and saving the waveforms
	'''
	plt.figure('%s'%nonGR)
	plt.plot(hp.sample_times, hp, label = 'GR IMRPhenomD')
	plt.plot(sp.sample_times, hp, label = 'Non-GR IMRPhenomD')
	plt.xlabel('Time(s)', fontsize = 20)
	plt.ylabel('h$_+$(m)', fontsize = 20)
	plt.title(('IMRPhenomD,$ %s = %.2f, M_1 = 20 M_\odot, M_2 = 30 M_\odot$'%(nonGR,j)), fontsize = 20)	
	plt.legend(loc = 'best')
	plt.grid()
	plt.savefig('%s'%nonGR+'.png')
