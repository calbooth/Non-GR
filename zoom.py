#import matplotlib

#matplotlib.use('Agg')

import numpy as np
import pycbc
import pycbc.waveform.waveform
from pycbc.waveform import parameters
from pycbc.waveform import td_approximants, fd_approximants
from pycbc.filter import match
from pycbc.psd import aLIGOZeroDetHighPower
import matplotlib.pyplot as plt
import matplotlib
import math

# get the default args:
default_args = (parameters.fd_waveform_params.default_dict() + \
    parameters.td_waveform_params).default_dict()

default_args_ngr = (parameters.fd_waveform_params.default_dict() + \
    parameters.td_waveform_params).default_dict()

q = default_args
q['mass1'] = 20
q['mass2'] = 30
#q['spinx1'] = 0.5
#q['spinx2'] = -0.5
q['delta_t'] = 1./4096
q['f_lower'] = 20
q['approximant'] = 'IMRPhenomPv2'

hp, hc = pycbc.waveform.waveform.get_td_waveform(**q) # Generte GR waveform
tlen = len(hp) # Create parameter tlen
tlen = math.log(tlen, 2) # Take the log base 2 of tlen
tlen = math.ceil(tlen) # Round up to the nearest integer (result is a float)
tlen = 2.0**tlen # Raise 2 to the nearest integer to help FFT go faster
tlen = 2.0*tlen
tlen = int(tlen)

hp.resize(tlen) # Resize hp
f_low = 20 # Lowest frequency

# Generate the aLIGO ZDHP PSD
delta_f = 1.0 / hp.duration # Frequency incirment
flen = tlen/2 + 1
psd = aLIGOZeroDetHighPower(flen, delta_f, f_low) # Creating PSD



#########################################################
##--------------------NON GR PARAMS--------------------##
#########################################################

p = default_args_ngr
p['mass1'] = 20
p['mass2'] = 30
#p['spinx1'] = 0.5
#p['spinx2'] = -0.5
p['delta_t'] = 1./4096
p['f_lower'] = 20
p['approximant'] = 'IMRPhenomPv2'

nGR = ['dbeta3']

# Looping through the list
for nonGR in nGR:
        # Setting the non-GR value to zero
        j = 0
        while True:
                # Setting the non-GR parameter to have some value
                p[str(nonGR)] = j

                sp, sc = pycbc.waveform.waveform.get_td_waveform(**p)

                # Resize the waveforms to the same length
                sp.resize(tlen)

                # Note: This takes a while the first time as an FFT plan is generated
                # subsequent calls are much faster.
                m, i = match(hp, sp, psd=psd, low_frequency_cutoff=f_low)

                # If the match is less than 0.97 then break from the loop
                if m <= 0.97:
                        print j
                        break
                # Increasing the non-GR value
                j += 0.01

        # Re-setting the non-GR parameter to zero.
        p[str(nonGR)] = 0

        '''
        Plotting and saving the waveforms
	'''        

        plt.figure('%s'%nonGR, figsize = (10.0, 6.25))
        plt.plot(hp.sample_times, hp, label = 'GR IMRPhenomPv2')
        plt.plot(sp.sample_times, sp, label = 'Non-GR IMRPhenomPv2')
        plt.xlabel('Time(s)', fontsize = 20)
        plt.ylabel('h$_+$(m)', fontsize = 20)
#       plt.title(('$%s = %.2f, M_1 = 20 M_\odot, M_2 = 30 M_\odot$'%(nonGR,j)), fontsize = 20) 
        plt.legend(loc = 'best')
        plt.xlim(-0.25, 0.02)
        plt.grid()
        plt.draw()
        plt.savefig('/home/c1320229/non-GR/%s'%nonGR+'zoom.png', bbox = 'tight')
        plt.show()


