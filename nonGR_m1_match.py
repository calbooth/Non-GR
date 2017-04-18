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

nGR = ['dchi0','dchi1','dchi2','dchi3','dchi4','dchi6',
'dalpha2','dalpha3','dalpha4','dbeta2','dbeta3'] # hashed out to test one param

#nGR = ['dbeta3']

ngrparam = np.arange(-0.5, 0.5, 0.01) # range of nGR params
mass1 = np.linspace(15, 45, 100) # Range of masses

#spin1 = np.linspace(-0.5, 0.5, 100)

# First looping through params
for nonGR in nGR:
	k = 0 # Initialising x coord to zero
	M = np.zeros([100, 100]) # initialising 2D match array to 100x100 of zeros
	
	# Looping through nGR values
	for i in ngrparam:
		# Setting the non-GR parameter to have some value
                p['%s'%nonGR] = i
		l = 0 # Initialising y coord to zero
		
		m_chirp = np.zeros(len(mass1))	
	
		# Looping through masses
		for j in mass1:
			p['mass1'] = j			
			
			# Creating non-GR waveform
        		sp, sc = pycbc.waveform.waveform.get_td_waveform(**p)
			
			m_chirp[l] = ((j*30.0)**(3.0/5.0))/((j + 30.0)**(1.0/5.0))		
	
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
	y = 0.0
	
	fig1 = plt.figure('%s'%nonGR, figsize = (20.0, 13.5))
	ax1 = fig1.add_subplot(1,1,1)
	cont = ax1.contourf(ngrparam, mass1, M, 100)
	ax1.set_ylabel('$M_{1}$', fontsize = 20)
	ax1.set_xlabel('%s'%nonGR, fontsize = 20)
	#ax.set_title('Match plot of varying %s and $M_1$'%nonGR, fontsize = 20)
	ax1.annotate('$\otimes$', (x, y), fontsize = 15)
	colorbar_ax = fig1.add_axes([0.905, 0.11, 0.05, 0.77])
	fig1.colorbar(cont, cax = colorbar_ax)
	con = ax1.contour(ngrparam, mass1, M, 1 ,levels=levels)
	ax1.clabel(con, color = 'k')
	plt.savefig('/home/c1320229/non-GR/%s'%nonGR + 'zerospin.png')
#	plt.show()

	

	fig2 = plt.figure('%s'%nonGR + 'm_chirp', figsize = (20.0, 13.5))
        ax2 = fig2.add_subplot(1,1,1)
        cont = ax2.contourf(ngrparam, m_chirp, M, 100)
        ax2.set_ylabel('$M_{chirp}$', fontsize = 20)
        ax2.set_xlabel('%s'%nonGR, fontsize = 20)
        #ax.set_title('Match plot of varying %s and $M_1$'%nonGR, fontsize = 20)
        ax2.annotate('$\otimes$', (x, y), fontsize = 15)
        colorbar_ax = fig2.add_axes([0.905, 0.11, 0.05, 0.77])
        fig2.colorbar(cont, cax = colorbar_ax)
        con = ax2.contour(ngrparam, m_chirp, M, 1 ,levels=levels)
        ax2.clabel(con, color = 'k')
        plt.savefig('/home/c1320229/non-GR/%s'%nonGR + '2Dm_chirp.png')
#	plt.show()	
	
	p['%s'%nonGR] = 0.0
