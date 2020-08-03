# runningperiodogram
Python code to compute a running periodogram with lightkurve

Example usage:
```python
import numpy as np
import matplotlib.pyplot as plt
from runningperiodogram import runningperiodogram

#Dramatic example of sinusoid with sinusoidal frequency modulation
time = np.arange(0,30,1/48.)
flux = 1 + 0.1*np.sin(30*(time + np.sin(0.3*time))) + 0.03*np.random.randn(len(time))

#save periodogram
runningperiodogram(time,flux,filename='example.png')
```

Result:

![Example running periodogram plot.](https://github.com/keatonb/runningperiodogram/blob/master/example.png)

runningperiodogram requires [lightkurve](https://docs.lightkurve.org/) and lightkurve's dependencies.

Here are the parameters for the runningperiodogram function:
```python
"""
Parameters
----------
time : array
    times of time series (in days)
flux: array
    flux of time series (normalized)
seglength: float
    length of sliding window (in days; default 5)
stepsize: float
    steps for sliding window (in days; default 1)
    steps for sliding window (in days; default 1)
frequnit: astropy unit
    frequency unit (default u.uHz)
    for 1/day use (1/u.day).unit
minfreq: float
    minimum frequency in frequnit (default 0)
maxfreq: float
    maximum frequency in frequnit (default Nyquist, approx.)
osample: (float)
    oversample factor (default 5)
normalization: ("amplitude" or "psd")
    normalization (amplitude or power; default amplitude)
vmin,vmax: (float)
    maximum and minimum values of color bar (default: periodogram min,max)
cmap: string
    color map to use (https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html; 
                      default: "Blues")
figsize: tuple
    figure size in inches ((width,height); default (6,4))
colorbar: bool
    whether to display colorbar (default True)
filename: string
    filename to save to. Figure displays if not provided (default None)

"""
```
