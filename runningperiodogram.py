#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3

This module provides a function for calculating at plotting a running 
periodogram to user specifications given a light curve (time and flux).

@author: keatonb
"""
import numpy as np
import matplotlib.pyplot as plt
import lightkurve as lk
import astropy.units as u
from tqdm import tqdm

def runningperiodogram(time, flux, seglength=5, stepsize=1, frequnit=u.uHz,
                       minfreq=None, maxfreq=None, osample=5, normalization='amplitude',
                       vmin=None, vmax=None, cmap='Blues', figsize=(6,4), colorbar=True,
                       filename=None):
    """Compute and display running Lomb-Scargle periodogram
    
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
    
    #Compute sliding window positions
    delta = stepsize/2. #some tolerance for final window
    winstart = np.arange(np.min(time),np.max(time)-seglength+delta,stepsize)
    winstop = winstart + seglength
    
    #Compute frequency grid
    if minfreq is None:
        minfreq = 0
    if maxfreq is None:
        maxfreq = 0.5 * (1./(np.median(np.diff(time))))*(1/u.day).to(frequnit).value #approx Nyquist
    freqstep = 1./(2.*seglength*osample)*(1/u.day).to(frequnit).value
    frequency = np.arange(minfreq,maxfreq,freqstep)
    
    #Ready to calculate running periodogram
    runningper = np.zeros((len(winstart),len(frequency)))
    for i in tqdm(range(len(winstart)),desc='Computing periodograms'):
        thisseg = np.where((time >= winstart[i]) & (time < winstop[i]))
        lc = lk.LightCurve(time=time[thisseg],flux=flux[thisseg])
        try:
            runningper[i,:] = lc.to_periodogram(frequency=frequency,normalization=normalization,freq_unit=frequnit).power.value
        except:
            pass
    
    #Plot
    fig,ax = plt.subplots(figsize=figsize, constrained_layout=True)
    im = ax.imshow(runningper,origin='lower',cmap=cmap,interpolation='none',aspect='auto',vmin=vmin,vmax=vmax,
              extent=[frequency[0],frequency[-1],(winstart[0]+winstop[0])/2.,(winstart[-1]+winstop[-1])/2.])
    ax.set_xlabel(f'frequency ({frequnit})')
    ax.set_ylabel('time (days)')
    if colorbar:
        fig.colorbar(im, ax=ax,label=normalization)
        
    
    #Display or save
    if filename is None:
        plt.show()
    else:
        plt.savefig(filename)