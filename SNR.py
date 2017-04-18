#!/bin/usr/env python

import numpy as np
import matplotlib.pyplot as plt

match = np.linspace(0, 1, 1000)
snr = np.sqrt((-3.12)/(match - 1))

plt.figure()
plt.plot(match, snr, label = 'SNR vs Match')
plt.xlabel('Match', fontsize = 25)
plt.ylabel('$\\rho_{min}$', fontsize = 25)
plt.xlim(0, 1)
plt.ylim(0, 55)
plt.grid()
plt.savefig('snr.png')
plt.show()
