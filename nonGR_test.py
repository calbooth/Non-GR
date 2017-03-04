import lal, lalsimulation, copy
import numpy as np
import pycbc
import pycbc.waveform.waveform
from pycbc.waveform import utils as wfutils
from pycbc.waveform import parameters
#from pycbc.waveform.waveform import _check_lal_pars
#from pycbc.waveform.waveform import _lalsim_td_waveform
from pycbc.waveform import td_approximants, fd_approximants
import matplotlib.pyplot as plt

hp, hc = pycbc.waveform.waveform._lalsim_td_waveform(approximent = 'IMRPhenomD',
                                mass1 = 20,
                                mass2 = 30,
                                spin1z = 0.9,
                                delta_t = 1.0/4096,
                                f_lower = 40,
                                XLALSimInspiralWaveformParamsLookupNonGRDChi6)

plt.figure()
plt.plot(hp.sample_times, hp, label = 'Non-GR IMRPhenomD')
