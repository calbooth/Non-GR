#!/usr/bin/env python

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
from scipy.optimize import leastsq # Levenberg-Marquadt Algorithm #
from scipy.optimize import curve_fit

#########################################################################
########################### DEFINING FUNCTIONS ##########################

def lorentzian(x, gamma, x_0, A):
    numerator =  (gamma**2 )
    denominator = ( x - x_0)**2 + gamma**2
    y = A*(numerator/denominator)
    return y

def residuals(p,y,x):
    err = y - lorentzian(x,p)
    return err

    
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

nGR = ['dbeta3']

ngrparam = np.linspace(-4, 4, 100) # range of nGR params
#mass1 = np.linspace(15, 45, 100) # Range of masses

spin1 = np.linspace(-0.5, 0.5, 100)

# First looping through params
for nonGR in nGR:
	k = 0 # Initialising x coord to zero
	M = np.zeros([100, 100]) # initialising 2D match array to 100x100 of zeros
	
	# Looping through nGR values
	for i in ngrparam:
		# Setting the non-GR parameter to have some value
                p['%s'%nonGR] = i
		l = 0 # Initialising y coord to zero
		
	#	m_chirp = np.zeros(len(mass1))	
	
		# Looping through masses
		for j in spin1:
			p['spin1x'] = j			
			
			# Creating non-GR waveform
        		sp, sc = pycbc.waveform.waveform.get_td_waveform(**p)
			
		#	m_chirp[l] = ((j*30.0)**(3.0/5.0))/((j + 30.0)**(1.0/5.0))		
	
     	  		# Resize the waveforms to the same length
              		sp.resize(tlen)
	
	        	# Note: This takes a while the first time as an FFT plan is generated
	        	# subsequent calls are much faster.
        		m, i = match(hp, sp, psd=psd, low_frequency_cutoff=f_low)
	                M[l, k] = m # Setting the value at this point in the mass array
        	        l += 1
		k +=1

		x = ngrparam
		y = M[50,:]
		
		guess = np.array([1.0, 0.0, 1.0])

		popt, pcov = curve_fit(lorentzian, x, y, guess)
		
		print popt
	
		np.savetxt('/home/c1320229/non-GR/dbeta3_match_optimum_params.txt', popt)
		
		# Match distribution
		plt.figure()
		plt.plot(ngrparam, M[0,:], label = 'Match distribution')
		plt.xlabel('$dbeta_3$', fontsize = 20)
		plt.ylabel('Match', fontsize = 20)
		plt.legend(loc = 'best')
		plt.grid()
		plt.savefig('/home/c1320229/non-GR/dbeta3_match_distribution.png')	
	#	plt.show()

