# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 10:52:54 2019

@author: chengjw
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize, signal

folder = r'C:/Users/'

sample = r''
spin = [r'',]
#        r'', 
#        r'', 
#        r'', 
#        r'']
fit_params = pd.DataFrame()
output = pd.DataFrame()
goodness = pd.DataFrame()


for u in spin:
    print(sample + ' ' + u)
    filepath = folder + sample + '-' + u + r'.csv'
    
    data = pd.DataFrame()
    data = pd.read_csv(filepath, header = 0)
        
    data_vis = data.loc[(data['Wavelength nm.'] >= 450) & (data['Wavelength nm.'] <= 750)]
    
    x = data_vis['Wavelength nm.']
    y = data_vis['Abs.']
    y = y*100
    y = signal.savgol_filter(y, 5, 2)
    
    def _1gaussian(x, amp1,cen1,sigma1,offset):
        return (amp1*np.exp(-(x - cen1)**2/(2*sigma1**2)) + offset)
    
    def _3gaussian(x, amp1,cen1,sigma1, amp2,cen2,sigma2, amp3,cen3,sigma3, offset):
        return (_1gaussian(x, amp1,cen1,sigma1,offset=0) + _1gaussian(x, amp2,cen2,sigma2,offset=0) + _1gaussian(x, amp3,cen3,sigma3,offset=0) + offset)
    
    amp1 = 100
    sigma1 = 50
    cen1 = 520
    
    amp2 = 20
    sigma2 = 10
    cen2 = 550
    
    amp3 = 50
    sigma3 = 10
    cen3 = 610
    
    errfunc3 = lambda p, x, y: (_3gaussian(x, *p) - y)**2
    
    guess3 = [amp1, cen1, sigma1, amp2, cen2, sigma2,amp3, cen3, sigma3,0 ] 
    
    optim3, success = optimize.leastsq(errfunc3, guess3[:], args=(x, y))
    
    optim = optim3.round(decimals=2)
    
    residuals = (_3gaussian(x, *optim3) - y)
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y-np.mean(y))**2)
    r_squared = 1 - (ss_res / ss_tot)
    
    fit_params[sample + '-' + u]=optim3
    goodness.loc[0,sample + '-' + u]=r_squared
    
   
    output['Wavelength'] = x
    output['Raw data']=y
    output['Fit']=_3gaussian(x, *optim3)
    output['Residuals']=residuals    
    output.to_csv(folder + sample + '-' + u + '_fitted.csv')
    
    plt.title(sample)
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Intensity (a.u)')
    plt.plot(x,y, '#2F4F4F', label = u)
    plt.plot(x, _3gaussian(x, *optim3), 'k--', label='fit')
    plt.plot(x, _1gaussian(x, *optim3[0:3],0), '#FFD700', label = optim[0:3] )
    plt.fill_between(x, _1gaussian(x, *optim3[0:3],0).min(), _1gaussian(x, *optim3[0:3],0), facecolor='#FFD700', alpha=0.9)
    plt.plot(x, _1gaussian(x, *optim3[3:6],0), '#32CD32', label = optim[3:6])
    plt.fill_between(x, _1gaussian(x, *optim3[3:6],0).min(), _1gaussian(x, *optim3[3:6],0), facecolor='#32CD32', alpha=0.9)
    plt.plot(x, _1gaussian(x, *optim3[6:9],0), '#008080', label = optim[6:9])
    plt.fill_between(x, _1gaussian(x, *optim3[6:9],0).min(), _1gaussian(x, *optim3[6:9],0), facecolor='#008080', alpha=0.9)
    plt.legend()
    plt.show


fit_params.append(goodness).to_csv(folder + sample + '_fit parameters.csv')


