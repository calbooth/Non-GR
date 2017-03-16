import lal, lalsimulation, numpy, copy
from pycbc.types import TimeSeries, FrequencySeries, zeros, Array
from pycbc.types import real_same_precision_as, complex_same_precision_as
import pycbc.scheme as _scheme
import inspect
from pycbc.fft import fft
from pycbc import pnutils
from pycbc.waveform import utils as wfutils
from pycbc.waveform import parameters
from pycbc.filter import interpolate_complex_frequency
import pycbc
#from spa_tmplt import spa_tmplt, spa_tmplt_norm, spa_tmplt_end, \
 #                     spa_tmplt_precondition, spa_amplitude_factor, \
  #                    spa_length_in_time

default_args = (parameters.fd_waveform_params.default_dict() + \
    parameters.td_waveform_params).default_dict()


def _check_lal_pars(p):
	""" 
	Create a laldict object from the dictionary of waveform parameters
	
	Parameters
	----------
	p: dictionary
	The dictionary of lalsimulation paramaters

	Returns
	-------
	laldict: LalDict        
	The lal type dictionary to pass to the lalsimulation waveform functions.
	"""

	lal_pars = lal.CreateDict()
	#nonGRparams can be straightforwardly added if needed, however they have to
	# be invoked one by one
	if p['phase_order']!=-1:
	        lalsimulation.SimInspiralWaveformParamsInsertPNPhaseOrder(lal_pars,int(p['phase_order']))
	if p['amplitude_order']!=-1:
	        lalsimulation.SimInspiralWaveformParamsInsertPNAmplitudeOrder(lal_pars,int(p['amplitude_order']))
	if p['spin_order']!=-1:
	        lalsimulation.SimInspiralWaveformParamsInsertPNSpinOrder(lal_pars,int(p['spin_order']))
	if p['tidal_order']!=-1:
	        lalsimulation.SimInspiralWaveformParamsInsertPNTidalOrder(lal_pars, p['tidal_order'])
	if p['eccentricity_order']!=-1:
	        lalsimulation.SimInspiralWaveformParamsInsertPNEccentricityOrder(lal_pars, p['eccentricity_order'])
	if p['lambda1']:
	        lalsimulation.SimInspiralWaveformParamsInsertTidalLambda1(lal_pars, p['lambda1'])
	if p['lambda2']:
	        lalsimulation.SimInspiralWaveformParamsInsertTidalLambda2(lal_pars, p['lambda2'])
	if p['dquad_mon1']:
	        lalsimulation.SimInspiralWaveformParamsInsertdQuadMon1(lal_pars, p['dquad_mon1'])
	if p['dquad_mon2']:
	        lalsimulation.SimInspiralWaveformParamsInsertdQuadMon2(lal_pars, p['dquad_mon2'])
	if p['numrel_data']:
	        lalsimulation.SimInspiralWaveformParamsInsertNumRelData(lal_pars, str(p['numrel_data']))
	if p['modes_choice']:
		lalsimulation.SimInspiralWaveformParamsInsertModesChoice(lal_pars, p['modes_choice'])
	if p['frame_axis']:
        	lalsimulation.SimInspiralWaveformParamsInsertFrameAxis(lal_pars, p['frame_axis'])
	if p['side_bands']:
		lalsimulation.SimInspiralWaveformParamsInsertSideband(lal_pars, p['side_bands'])


################################################################################################
#####-------------------------------------Non-GR params-----------------------------------######
################################################################################################

# Phi:
'''
    if p['phi1']:
	lalsimulation.SimInspiralWaveformParamsInsertNonGRPhi1(lal_pars, float(p['phi1']))
    if p['phi2']:
	lalsimulation.SimInspiralWaveformParamsInsertNonGRPhi2(lal_pars, float(p['phi2']))
    if p['phi3']:
	lalsimulation.SimInspiralWaveformParamsInsertNonGRPhi3(lal_pars, float(p['phi3']))
    if p['phi4']:
	lalsimulation.SimInspiralWaveformParamsInsertNonGRPhi4(lal_pars, float(p['phi4']))
# dChi:
'''
#    if p['dchi0']:
#        lalsimulation.SimInspiralWaveformParamsInsertNonGRDChi0(lal_pars, float(p['dchi0']))
'''   
 if p['dchi1']:
        lalsimulation.SimInspiralWaveformParamsInsertNonGRDChi1(lal_pars, float(p['dchi1']))
    if p['dchi2']:
        lalsimulation.SimInspiralWaveformParamsInsertNonGRDChi2(lal_pars, float(p['dchi2']))
    if p['dchi3']:
        lalsimulation.SimInspiralWaveformParamsInsertNonGRDChi3(lal_pars, float(p['dchi3']))
    if p['dchi4']:
        lalsimulation.SimInspiralWaveformParamsInsertNonGRDChi4(lal_pars, float(p['dchi4']))
    if p['dchi5']:
        lalsimulation.SimInspiralWaveformParamsInsertNonGRDChi5(lal_pars, float(p['dchi5']))
    if p['dchi5L']:
        lalsimulation.SimInspiralWaveformParamsInsertNonGRDChi5L(lal_pars, float(p['dchi5L']))
    if p['dchi6']:
        lalsimulation.SimInspiralWaveformParamsInsertNonGRDChi6(lal_pars, float(p['dchi7']))
    if p['dchi6L']:
        lalsimulation.SimInspiralWaveformParamsInsertNonGRDChi6L(lal_pars, float(p['dchi6L']))
    if p['dchi7']:
        lalsimulation.SimInspiralWaveformParamsInsertNonGRDChi7(lal_pars, float(p['dchi7']))

# dXi:
    
    if p['dxi1']:
        lalsimulation.SimInspiralWaveformParamsInsertNonGRDXi1(lal_pars, float(p['dxi1']))
    if p['dxi2']:
        lalsimulation.SimInspiralWaveformParamsInsertNonGRDXi2(lal_pars, float(p['dxi2']))
    if p['dxi3']:
        lalsimulation.SimInspiralWaveformParamsInsertNonGRDXi3(lal_pars, float(p['dxi3']))
    if p['dxi4']:
        lalsimulation.SimInspiralWaveformParamsInsertNonGRDXi4(lal_pars, float(p['dxi4']))
    if p['dxi5']:
        lalsimulation.SimInspiralWaveformParamsInsertNonGRDXi5(lal_pars, float(p['dxi5']))
    if p['dxi6']:
        lalsimulation.SimInspiralWaveformParamsInsertNonGRDXi6(lal_pars, float(p['dxi6']))

# Sigma:

    if p['sigma1']:
        lalsimulation.SimInspiralWaveformParamsInsertNonGRSigma1(lal_pars, float(p['sigma1']))
    if p['sigma2']:
        lalsimulation.SimInspiralWaveformParamsInsertNonGRSigma2(lal_pars, float(p['sigma2']))
    if p['sigma3']:
        lalsimulation.SimInspiralWaveformParamsInsertNonGRSigma3(lal_pars, float(p['sigma3']))
    if p['sigma4']:
        lalsimulation.SimInspiralWaveformParamsInsertNonGRSigma4(lal_pars, float(p['sigma4']))

# Alpha:

    if p['alpha1']:
        lalsimulation.SimInspiralWaveformParamsInsertNonGRAlpha1(lal_pars, float(p['alpha1']))
    if p['alpha2']:
        lalsimulation.SimInspiralWaveformParamsInsertNonGRAlpha2(lal_pars, float(p['alpha2']))
    if p['alpha3']:
        lalsimulation.SimInspiralWaveformParamsInsertNonGRAlpha3(lal_pars, float(p['alpha3']))
    if p['alpha4']:
        lalsimulation.SimInspiralWaveformParamsInsertNonGRAlpha4(lal_pars, float(p['alpha4']))
    if p['alpha5']:
        lalsimulation.SimInspiralWaveformParamsInsertNonGRAlpha5(lal_pars, float(p['alpha5']))

# Beta:

    if p['beta1']:
        lalsimulation.SimInspiralWaveformParamsInsertNonGRBeta1(lal_pars, float(p['beta1']))
    if p['beta2']:
        lalsimulation.SimInspiralWaveformParamsInsertNonGRBeta2(lal_pars, float(p['beta2']))
    if p['beta3']:
        lalsimulation.SimInspiralWaveformParamsInsertNonGRBeta3(lal_pars, float(p['beta3']))

# Alpha PPE:

    if p['alphaPPE']:
        lalsimulation.SimInspiralWaveformParamsInsertNonGRAlphaPPE(lal_pars, float(p['alphaPPE']))
    if p['alphaPPE0']:
        lalsimulation.SimInspiralWaveformParamsInsertNonGRAlphaPPE0(lal_pars, float(p['alphaPPE0']))
    if p['alphaPPE1']:
        lalsimulation.SimInspiralWaveformParamsInsertNonGRAlphaPPE1(lal_pars, float(p['alphaPPE1']))
    if p['alphaPPE2']:
        lalsimulation.SimInspiralWaveformParamsInsertNonGRAlphaPPE2(lal_pars, float(p['alphaPPE2']))
    if p['alphaPPE3']:
        lalsimulation.SimInspiralWaveformParamsInsertNonGRAlphaPPE3(lal_pars, float(p['alphaPPE3']))
    if p['alphaPPE4']:
        lalsimulation.SimInspiralWaveformParamsInsertNonGRAlphaPPE4(lal_pars, float(p['alphaPPE4']))
    if p['alphaPPE5']:
        lalsimulation.SimInspiralWaveformParamsInsertNonGRAlphaPPE5(lal_pars, float(p['alphaPPE5']))
    if p['alphaPPE6']:
        lalsimulation.SimInspiralWaveformParamsInsertNonGRAlphaPPE6(lal_pars, float(p['alphaPPE6']))
    if p['alphaPPE7']:
        lalsimulation.SimInspiralWaveformParamsInsertNonGRAlphaPPE7(lal_pars, float(p['alphaPPE7']))
# Beta PPE:

    if p['betaPPE']:
        lalsimulation.SimInspiralWaveformParamsInsertNonGRBetaPPE(lal_pars, float(p['betaPPE']))
    if p['betaPPE0']:
        lalsimulation.SimInspiralWaveformParamsInsertNonGRBetaPPE0(lal_pars, float(p['betaPPE0']))
    if p['betaPPE1']:
        lalsimulation.SimInspiralWaveformParamsInsertNonGRBetaPPE1(lal_pars, float(p['betaPPE1']))
    if p['betaPPE2']:
        lalsimulation.SimInspiralWaveformParamsInsertNonGRBetaPPE2(lal_pars, float(p['betaPPE2']))
    if p['betaPPE3']:
        lalsimulation.SimInspiralWaveformParamsInsertNonGRBetaPPE3(lal_pars, float(p['betaPPE3']))
    if p['betaPPE4']:
        lalsimulation.SimInspiralWaveformParamsInsertNonGRBetaPPE4(lal_pars, float(p['betaPPE4']))
    if p['betaPPE5']:
        lalsimulation.SimInspiralWaveformParamsInsertNonGRBetaPPE5(lal_pars, float(p['betaPPE5']))
    if p['betaPPE6']:
        lalsimulation.SimInspiralWaveformParamsInsertNonGRBetaPPE6(lal_pars, float(p['betaPPE6']))
    if p['betaPPE7']:
        lalsimulation.SimInspiralWaveformParamsInsertNonGRBetaPPE7(lal_pars, float(p['betaPPE7']))
'''
    return lal_pars


# add what we need
p = default_args
p['mass1']=10.
p['mass2']=10.
p['delta_t'] = 1./4096
p['f_lower'] = 40.
p['approximant']='IMRPhenomPv2'
lal_pars = _check_lal_pars(p)

# make the waveform
hp1, hc1 = lalsimulation.SimInspiralChooseTDWaveform(
                float(pnutils.solar_mass_to_kg(p['mass1'])),
                float(pnutils.solar_mass_to_kg(p['mass2'])),
                float(p['spin1x']), float(p['spin1y']), float(p['spin1z']),
                float(p['spin2x']), float(p['spin2y']), float(p['spin2z']),
                pnutils.megaparsecs_to_meters(float(p['distance'])),
                float(p['inclination']), float(p['coa_phase']),
                float(p['long_asc_nodes']), float(p['eccentricity']), float(p['mean_per_ano']),
                float(p['delta_t']), float(p['f_lower']), float(p['f_ref']),
                lal_pars,
                _lalsim_enum[p['approximant']])

hp = TimeSeries(hp1.data.data[:], delta_t=hp1.deltaT, epoch=hp1.epoch)
'''
p['dchi0'] = 1
lal_pars = _check_lal_pars(p)
sp1, sc1 = lalsimulation.SimInspiralChooseTDWaveform(
                float(pnutils.solar_mass_to_kg(p['mass1'])),
                float(pnutils.solar_mass_to_kg(p['mass2'])),
                float(p['spin1x']), float(p['spin1y']), float(p['spin1z']),
                float(p['spin2x']), float(p['spin2y']), float(p['spin2z']),
                pnutils.megaparsecs_to_meters(float(p['distance'])),
                float(p['inclination']), float(p['coa_phase']),
                float(p['long_asc_nodes']), float(p['eccentricity']), float(p['mean_per_ano']),
                float(p['delta_t']), float(p['f_lower']), float(p['f_ref']),
                lal_pars,
                _lalsim_enum[p['approximant']])

sp = TimeSeries(sp1.data.data[:], delta_t=sp1.deltaT, epoch=sp1.epoch)

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
'''
