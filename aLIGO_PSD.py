import pycbc.psd
import pycbc.types.frequencyseries
import matplotlib.pyplot as plt
import numpy

# List the available analytic psds
print(pycbc.psd.get_lalsim_psd_list())

delta_f = 1.0 / 4
flen = int(1024 / delta_f)
low_frequency_cutoff = 30.0

# PSD of detector
psd = pycbc.psd.aLIGOZeroDetHighPower(flen, delta_f, low_frequency_cutoff)
psd_1 = pycbc.psd.aLIGOZeroDetLowPower(flen, delta_f, low_frequency_cutoff)
psd_2 = pycbc.psd.eLIGOModel(flen, delta_f, low_frequency_cutoff)
psd_3 = pycbc.psd.iLIGOModel(flen, delta_f, low_frequency_cutoff)

# ASD of the PSD
asd = pycbc.types.frequencyseries.FrequencySeries(numpy.sqrt(psd.numpy()), delta_f=psd.delta_f)
asd_1 = pycbc.types.frequencyseries.FrequencySeries(numpy.sqrt(psd_1.numpy()), delta_f=psd_1.delta_f)
asd_2 = pycbc.types.frequencyseries.FrequencySeries(numpy.sqrt(psd_2.numpy()), delta_f=psd_2.delta_f)
asd_3 = pycbc.types.frequencyseries.FrequencySeries(numpy.sqrt(psd_3.numpy()), delta_f=psd_3.delta_f)

# Potting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.loglog(asd.sample_frequencies, asd, linewidth = 3, label = 'aLIGO High Power Design')
ax.loglog(asd_1.sample_frequencies, asd_1, linewidth = 3, label = 'aLIGO, Low Power Design')
ax.loglog(asd_2.sample_frequencies, asd_2, linewidth = 3, label = 'eLIGO')
ax.loglog(asd_3.sample_frequencies, asd_3, linewidth = 3, label = 'iLIGO')
ax.set_ylabel('Strain', fontsize = 25)
ax.set_xlabel('Frequency (Hz)', fontsize = 25)
ax.set_xlim(30.0, 1000.0)
ax.xaxis.set_tick_params(labelsize=20)
ax.yaxis.set_tick_params(labelsize = 20)
ax.legend(loc = 'best', fontsize = 20)
ax.grid()
plt.show()
