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

# get the default args:
default_args = (parameters.fd_waveform_params.default_dict() + \
    parameters.td_waveform_params).default_dict()

# Doing the same for non-GR to fix previous errors
default_args_nGR = (parameters.fd_waveform_params.default_dict() + \
    parameters.td_waveform_params).default_dict()

'''
	Original GR waveform that we will be matching against
'''
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
tlen = 2.0*tlen # Was getting an error for the length being a factor of ~2 smaller than expected
tlen = int(tlen) # Need tlen to be an integer for psd and resizing

hp.resize(tlen) # Resize hp
f_low = 20 # Lowest frequency

# Generate the aLIGO ZDHP PSD
delta_f = 1.0 / hp.duration # Frequency incirment
flen = tlen/2 + 1
psd = aLIGOZeroDetHighPower(flen, delta_f, f_low) # Creating PSD

#########################################################
##---------------------Non-GR Waveform-----------------##
#########################################################

p = default_args_nGR
p['mass1'] = 20
p['mass2'] = 30 
p['delta_t'] = 1./4096
p['f_lower'] = 20
p['approximant'] = 'IMRPhenomPv2'

#M1 = np.linspace(5, 35, 1000) # The mass array
S1 = np.linspace(-0.5, 0.5, 1000)
pmatch = np.zeros(1000) # Non-GR match array
qmatch = np.zeros(1000) # GR match array

val = np.linspace(-0.5, 0.5, 20)

#val = np.array([-0.2])

for ii in val:
	
	p['dalpha3'] = ii # Non-GR parameter
	j = 0 # Counting parameter
	
	for i in S1:

		p['spin1x'] = i
		q['spin1x'] = i	

        	pp, pc = pycbc.waveform.waveform.get_td_waveform(**p)
        	qp, qc = pycbc.waveform.waveform.get_td_waveform(**q)

        	# Resize the waveforms to the same length
        	pp.resize(tlen)
		qp.resize(tlen)	
	
	        # Matching
	        mp, ip = match(hp, pp, psd=psd, low_frequency_cutoff=f_low)
	        mq, iq = match(hp, qp, psd=psd, low_frequency_cutoff=f_low)
	
		# Assigning the matches to an array
		pmatch[j] = mp	
		qmatch[j] = mq
		
		# Increasing counting parameter
		j += 1
	
	# Plotting the points where the curves intersect
	idx = np.argwhere(np.diff(np.sign(pmatch - qmatch)) != 0).reshape(-1) + 0
		
	# Getting rid of unwanted intersection points
	x_int = S1[idx]
	y_int = pmatch[idx]

		
	fig = plt.figure(figsize  = (10.0, 6.25))
	ax = fig.add_subplot(1,1,1)
	k = ax.plot(S1, pmatch, label = 'Non-GR')
	l = ax.plot(S1, qmatch, label = 'GR')	

	# Plotting the point with maximum match  where the curves intersect
#	max_y = np.argmax(y_int)
#	y_max = np.array(max_y)
#	y_index = np.where(y_int == y_int.max())
#	x_max = np.array(x_int[int(y_index)])	

	if len(y_int) > 1:
		max_y = np.argmax(y_int)
		y_int = np.array(max(y_int))
		x_int = np.array(x_int[int(max_y)]) 
	
		m = ax.plot(x_int, y_int, 'ro')
	
		ax.annotate('%.2f, %.2f'%(x_int, y_int), xy=(x_int, y_int), xytext=(x_int + 0.5, y_int + 0.02), fontsize = 15)
			
	# Formatting
	ax.set_xlabel('$S_{1x}$', fontsize = 20)
	ax.set_ylabel('Match', fontsize = 20)
#	ax.set_title(('Match plot for varying $M_1$'), fontsize = 20)
	ax.xaxis.set_tick_params(labelsize=15)
	ax.yaxis.set_tick_params(labelsize=15)
#	ax.set_xlim(5, 35)
	plt.legend(loc = 'best')
	plt.grid()
	plt.savefig('/home/c1320229/non-GR/intercept_dalpha3_' + '%s'%ii + 'spin.png')
#	plt.show()
#	plt.close()
