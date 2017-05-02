import matplotlib.pyplot as plt
from pycbc.waveform import get_td_waveform

approximant = 'IMRPhenomPv2'
dt = 1.0/4096
f_low = 20

hp_1, hc_1 = get_td_waveform(approximant = approximant, mass1 = 30, mass2 = 30,
				delta_t = dt, f_lower = f_low) 

hp_2, hc_2 = get_td_waveform(approximant = approximant, mass1 = 15, mass2 = 30,
				delta_t = dt, f_lower = f_low)

hp_3, hc_3 = get_td_waveform(approximant = approximant, mass1 = 15, mass2 = 30,
				spin1z = 0.5, spin2z = 0.5, 
				delta_t = dt, f_lower = f_low)

hp_4, hc_4 = get_td_waveform(approximant = approximant, mass1 = 15, mass2 = 30,
				spin1x = 0.5, spin1y = 0.3, spin2x = -0.4, spin2y = -0.2,
				delta_t = dt, f_lower = f_low)

hp_5, hc_5 = get_td_waveform(approximant = approximant, mass1 = 5, mass2 = 30,
                                delta_t = dt, f_lower = f_low)

'''
plt.figure()
plt.plot(hp_5.sample_times, hp_5, label = 'Mass ratio = 6')
plt.xlabel('Time(s)', fontsize = 20)
plt.ylabel('Strain (m)', fontsize = 20)
plt.grid()
plt.legend(loc = 'best')
plt.savefig('extreme_mass_ratio.png')
#plt.show()

plt.figure()
plt.plot(hp_1.sample_times, hp_1, label = 'Equal Mass ratio')
plt.xlabel('Time(s)', fontsize = 20)
plt.ylabel('Strain (m)', fontsize = 20)
plt.grid()
plt.legend(loc = 'best')
plt.savefig('equal_mass_ratio.png')
#plt.show()

plt.figure()
plt.plot(hp_2.sample_times, hp_2, label = 'Mass ratio = 2')
plt.xlabel('Time(s)', fontsize = 20)
plt.ylabel('Strain (m)', fontsize = 20)
plt.grid()
plt.legend(loc = 'best')
plt.savefig('mass_ratio_2.png')
#plt.show()

plt.figure()
plt.plot(hp_3.sample_times, hp_3, label = 'Mass ratio = 2, Spin alligned')
plt.xlabel('Time(s)', fontsize = 20)
plt.ylabel('Strain (m)', fontsize = 20)
plt.grid()
plt.legend(loc = 'best')
plt.savefig('mass_ratio_2_alligned_spin.png')
#plt.show()

plt.figure()
plt.plot(hp_4.sample_times, hp_4, label = 'Mass ratio = 2, Spin misalliged')
plt.xlabel('Time(s)', fontsize = 20)
plt.ylabel('Strain (m)', fontsize = 20)
plt.grid()
plt.legend(loc = 'best')
plt.savefig('mass_ratio_2_misalligned_spin.png')
#plt.show() 
'''
print max(hp_1), max(hp_2), max(hp_3), max(hp_4), max(hp_5)
