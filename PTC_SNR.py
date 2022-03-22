# -*- coding: utf-8 -*-
"""
=========
PTC, SNR
=========

This code is used to characterize image sensors and cameras. More specifically, it focuses on two main parameters: firstly, the PTC (Photon Transfer Curve) 
which allows us to calculate the Gain of the camera in e-/ADU, the FWC (Full Well Capacity) in e- and the Dynamic Range in dB or bit; secondly, the SNR (Signal to Noise Ratio) 
which is essentially the ratio of the measured signal to the overall measured noise on a pixel.
"""

# Import required libraries
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
#import os
from PIL import Image
from colorama import Fore, Style, deinit, init

def loadImage(path):
   # Load image with PIL
   im = Image.open(path)
   return np.array(im, np.float32)
   
def sdtDiffImage(frame1, frame2):
    # Difference of frames
    frame = frame1 - frame2
    # Standard deviation diff
    sigma = np.std(frame)
    # Variance
    var = np.var(frame)/2  
    return sigma, var, frame

def sdtAddImage(frame1, frame2):
    # Sum of frames & average
    frame = (frame1 + frame2)/2 
    # Mean value
    mu = np.mean(frame)
    return mu, frame
    
def noiseRoutine(folder_path, scan_list):
    n_frames = len(scan_list)
    for idx, value in enumerate(scan_list):
        frame1 = loadImage(folder_path.format(value, 1))
        frame2 = loadImage(folder_path.format(value, 2))
        sigma, var, frame = sdtDiffImage(frame1, frame2)
        mu, frame = sdtAddImage(frame1, frame2)
        if idx==0:
           frame_stack = np.zeros((frame.shape[0], frame.shape[1], n_frames))
           mu_stack = np.zeros(n_frames)
           sigma_stack = np.zeros(n_frames)
           var_stack = np.zeros(n_frames)
        frame_stack[:, :, idx] = frame
        mu_stack[idx] = mu
        sigma_stack[idx] = sigma
        var_stack[idx] = var
        
    return frame_stack, mu_stack, sigma_stack, var_stack  
             
if __name__ == "__main__":
    # main code
    folder_path = r"E:\CCD_CMOS\Basler acA1920-40gm CMOS\Basler_LED\{}s\{}.tiff"  
    scan_list = ['40u', '100u', '500u', '1m', '5m', '10m', '15m', '20m', '25m', '30m', '35m', '40m', '45m', '50m', '55m', '60m', '65m', '70m', '75m', '77,5m', '80m', '82,5m', '85m', '87,5m', '90m', '92,5m', '95m', '97,5m', '100m']
    
    frame_stack, mu_stack, sigma_stack, var_stack = noiseRoutine(folder_path, scan_list)
    
    exp_time = np.array([40e-6, 100e-6, 500e-6, 1e-3, 5e-3, 10e-3, 15e-3, 20e-3, 25e-3, 30e-3, 35e-3, 40e-3, 45e-3, 50e-3, 55e-3, 60e-3, 65e-3, 70e-3, 75e-3, 77.5e-3, 80e-3, 82.5e-3, 85e-3, 87.5e-3, 90e-3, 92.5e-3, 95e-3, 97.5e-3, 100e-3])
    
    init()
    print(Fore.GREEN + Style.BRIGHT, "\033[4m\nPhoton transfer curve (12-bit):\n\033[0m")
    res1 = stats.linregress(mu_stack[0:17], var_stack[0:17]) # R-squared calculation
    res2 = np.polyfit(mu_stack[0:17], var_stack[0:17], 1) # linear regression
    coeff2 = round(res2[0], 1) # slope (gain)
    origine2 = round(res2[1], 1) # y-intercept
    print("- slope :", coeff2/16)
    print("- y-intercept :", origine2/16)
    print(f"- R-squared : {res1.rvalue**2:.4f}\n")
    FWC = (mu_stack[17]/16)/(coeff2/16) 
    print("- FWC (Full well capacity):", round(FWC, 2),"e-") 
    deinit()
     
    #--------------------------------------------------
    
    res3 = stats.linregress(exp_time[0:17], mu_stack[0:17]) # R-squared calculation
    res4 = np.polyfit(exp_time[0:17], mu_stack[0:17], 1) # linear regression
    coeff4 = round(res4[0], 1) # slope (gain)
    origine4 = round(res4[1], 1) # y-intercept\
        
    plt.figure(dpi=300)
    plt.plot(exp_time, mu_stack[0:], '-s', linewidth=0.5, label='Data') 
    plt.plot(exp_time[0:], origine4 + coeff4*exp_time[0:], '--k', label='Linear regression')  
    plt.legend(loc='lower right')
    plt.xlabel('t [s]')
    plt.ylabel('Mean signal [ADU]')
    box_style=dict(boxstyle='square', facecolor='silver', alpha=0.7)
    plt.text(-0.0025,80000, "y = {:0.2f}x + {:0.2f} \n"f"R-squared = {res3.rvalue**2:.4f}". format(coeff4, origine4),{'color':'black','weight':'heavy','size':10}, bbox=box_style)
    plt.grid(color='grey', linestyle='-.', linewidth=0.5)
    plt.title('Full-Frame average. 16-bit')
    plt.show() 
    
    #--------------------------------------------------
    
    plt.figure(dpi=300)
    plt.plot(mu_stack[0:], var_stack[0:], '-s', linewidth=0.5, label='Data') # plt.loglog : log scaling on both the x and y axis --> see noise regimes
    plt.plot(mu_stack[0:], origine2 + coeff2*mu_stack[0:], '--k', label='Linear regression')  
    plt.legend(loc='lower right')
    plt.xlabel('Mean pixel value [ADU]') # Logscale
    plt.ylabel('$Variance$ [$ADU^2$]') # Logscale
    box_style=dict(boxstyle='square', facecolor='silver', alpha=0.7)
    plt.text(1500,116000, "y = {:0.2f}x + {:0.2f} \n"f"R-squared = {res1.rvalue**2:.4f}". format(coeff2, origine2),{'color':'black','weight':'heavy','size':10}, bbox=box_style)
    plt.grid(color='grey', linestyle='-.', linewidth=0.5)
    plt.title('Photon Transfer Curve (PTC). Full-Frame. 16-bit')
    plt.xlim([0, 70000])
    plt.show() 
    
    SNR = 20*np.log10((mu_stack[:17])/(sigma_stack[:17])) # Linear to dB, 16-bit or 12-bit, ratio is the same
    x = mu_stack[:17]
    plt.figure(dpi=300)
    plt.loglog(x/(1.90), SNR, '--s', label='Data') # ADU->e- conversion 
    plt.loglog(x/(1.90), np.sqrt(x/(1.90)), label='ideal')
    plt.legend(loc='lower right')
    plt.grid(color='grey', linestyle='-.', linewidth=0.5)
    plt.xlabel('Average value [$e^-$]')
    plt.ylabel('SNR [dB]')
    plt.title('Input SNR')
    
    

