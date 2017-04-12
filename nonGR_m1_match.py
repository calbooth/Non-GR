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
q['f_lower'] = 15
q['approximant'] = 'IMRPhenomPv2'

hp, hc = pycbc.waveform.waveform.get_td_waveform(**q)
# Define lower frequency
f_low = 15

# Resize the waveforms to the same length
tlen = len(hp)
tlen = math.log(tlen, 2)
tlen = math.ceil(tlen)
tlen = 2.0**tlen
tlen = int(tlen)
		
hp.resize(tlen)

# Generate the aLIGO ZDHP PSD
delta_f = 1.0 / hp.duration
flen = tlen/2 + 1
psd = aLIGOZeroDetHighPower(flen, delta_f, f_low)

#########################################################
##--------------------NON GR PARAMS--------------------##
#########################################################

p = default_args
p['mass2'] = 30
p['delta_t'] = 1./4096
p['f_lower'] = 15
p['approximant'] = 'IMRPhenomPv2'

nGR = ['dchi0','dchi1','dchi2','dchi3','dchi4','dchi6',
'dalpha2','dalpha3','dalpha4','dbeta2','dbeta3'] # hashed out to test one param

ngrparam = np.arange(-0.5, 0.5, 0.01) # range of nGR params
mass1 = np.linspace(15, 45, 100) # Range of masses

# First looping through params
for nonGR in nGR:
	k = 0 # Initialising x coord to zero
	M = np.zeros([100, 100]) # initialising 2D match array to 100x100 of zeros
	
	# Looping through nGR values
	for i in ngrparam:
		# Setting the non-GR parameter to have some value
                p['%s'%nonGR] = i
		l = 0 # Initialising y coord to zero

		# Looping through masses
		for j in mass1:
			p['mass1'] = j			
			
			# Creating non-GR waveform
        		sp, sc = pycbc.waveform.waveform.get_td_waveform(**p)

     	  		# Resize the waveforms to the same length
              		sp.resize(tlen)
	
	        	# Note: This takes a while the first time as an FFT plan is generated
	        	# subsequent calls are much faster.
        		m, i = match(hp, sp, psd=psd, low_frequency_cutoff=f_low)
	                M[l, k] = m # Setting the value at this point in the mass array
        	        l += 1
		k +=1

	'''
	Plotting and saving the result
	'''
	levels=np.array([0.97])
	x = 0.0
	y = 20.0
	
	fig = plt.figure('%s'%nonGR)
	ax = fig.add_subplot(1,1,1)
	cont = ax.contourf(ngrparam, mass1, M, 100)
	ax.set_ylabel('$M_1$', fontsize = 20)
	ax.set_xlabel('%s'%nonGR, fontsize = 20)
	#ax.set_title('Match plot of varying %s and $M_1$'%nonGR, fontsize = 20)
	ax.annotate('$\otimes$', (x, y), fontsize = 15)
	colorbar_ax = fig.add_axes([0.905, 0.11, 0.05, 0.77])
	fig.colorbar(cont, cax = colorbar_ax)
	con = ax.contour(ngrparam, mass1, M, 1 ,levels=levels)
	ax.clabel(con, color = 'k')
	plt.savefig('%s'%nonGR + 'mass1.png')
	plt.close()
