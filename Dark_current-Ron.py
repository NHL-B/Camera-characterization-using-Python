# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 09:10:52 2022

This code is used to characterize image sensors and cameras. More specifically, it focuses on two main parameters, dark current and read noise.
To do so, it calculates the mean value and the standard deviation from averaged and subtracted dark frames for each exposure times and then create plots from these values.
It also contains a function called 'histRoutine' that displays histograms.

@author: BELGHERZ
"""

# Import required libraries
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
# import os
from PIL import Image
from matplotlib.colors import LogNorm
from colorama import Fore, Style, deinit, init
from matplotlib_scalebar.scalebar import ScaleBar

def loadImage(path):
   # Load image with PIL
   im = Image.open(path)
   return np.array(im, np.float32)
   
def sdtDiffImage(frame1, frame2):
    # Difference of frames
    frame = frame1 - frame2
    # Standard deviation
    sigma = np.std(frame)
    # Mean value
    mu = np.mean(frame)
    return mu, sigma, frame

def sdtAddImage(frame1, frame2):
    # Sum of frames
    frame = (frame1 + frame2)/2  
    # Standard deviation
    sigma = np.std(frame)
    # Mean value
    mu = np.mean(frame)
    return mu, sigma, frame
    
def noiseRoutine(folder_path, scan_list):
    n_frames = len(scan_list)
    for idx, value in enumerate(scan_list):
        frame1 = loadImage(folder_path.format(value, 1))
        frame2 = loadImage(folder_path.format(value, 2))
        mu, sigma, frame = sdtDiffImage(frame1, frame2) 
        if idx==0:
           frame_stack = np.zeros((frame.shape[0], frame.shape[1], n_frames))
           mu_stack = np.zeros(n_frames)
           sigma_stack = np.zeros(n_frames)
        frame_stack[:, :, idx] = frame
        mu_stack[idx] = mu
        sigma_stack[idx] = sigma/np.sqrt(2) 
    return frame_stack, mu_stack, sigma_stack
 
def meanRoutine(folder_path, scan_list):
    n_frames = len(scan_list)
    for idx, value in enumerate(scan_list):
        frame1 = loadImage(folder_path.format(value, 1))
        frame2 = loadImage(folder_path.format(value, 2))
        mu, sigma, frame = sdtAddImage(frame1, frame2) 
        if idx==0:
           frame_stack = np.zeros((frame.shape[0], frame.shape[1], n_frames))
           mu_stack = np.zeros(n_frames)
           sigma_stack = np.zeros(n_frames)
        frame_stack[:, :, idx] = frame
        mu_stack[idx] = mu
        sigma_stack[idx] = sigma
    return frame_stack, mu_stack, sigma_stack    
 
def histRoutine(frame_stack, mu_stack, sigma_stack, scan_list):
    for idx in range(mu_stack.shape[0]):
        frame = frame_stack[:, :, idx]
        mu = mu_stack[idx]
        sigma = sigma_stack[idx]*np.sqrt(2) 
        bin_list = np.linspace(-5*sigma + mu, 5*sigma + mu, 12) #bins ? #start ? to be adjusted. 
        plt.figure(dpi=300)
        frame, bin_list, patches = plt.hist(frame.ravel(), bin_list, alpha = 0.7)
        frame = frame.astype('int')
        for i in range(len(patches)):
            patches[i].set_facecolor(plt.cm.coolwarm(frame[i]/max(frame)))
        plt.axvline(mu.mean(), color='k', linestyle='dashed', linewidth=1.5, label='mean')
        plt.xlabel('ADU')
        plt.ylabel('Counts')
        plt.legend(loc='upper right')
        plt.title('Histogram @ {}s. $\mu$: {:.2f} ADU. $\sigma$diff: {:.2f} ADU. 16-bit'.format(scan_list[idx], mu, sigma)) #σdiff or σ 
        plt.show() 

def myplot_mean(idx): 
    """
    This function displays a 16-bit averaged dark image at a certain exposure time (texp) with a logarithmic 
    colorbar which allows a 2D visualization of pixels intensity in ADU (or grey-scale value)
    """
    a = np.abs(frame_mean_stack[:,:, idx])
    plt.figure(num=None, dpi=300, facecolor='w', edgecolor='k')
    plt.imshow(a, cmap='seismic', norm=LogNorm(np.min(a[a>0]), np.max(a))) 
    cbar = plt.colorbar(aspect=15, shrink=0.77)  
    cbar.set_label('Log intensity (ADU)')
    plt.title('Mean dark frame @ %is. 16-bit' %idx)
    plt.xlabel('x-axis (pixels)')
    plt.ylabel('y-axis (pixels)')
    scalebar = ScaleBar(5.86, 'um', location='lower left', box_alpha= 0.95, pad= 0.25, border_pad= 0.25, scale_loc='top', sep=3) # ex: Pixel size = 5.86 μm
    plt.gca().add_artist(scalebar)
    plt.show()
    
    """
    Sensor specifications
    """
    init()
    print(Fore.GREEN + Style.BRIGHT, "\033[4m\nSensor:\n\033[0m")
    print(Style.RESET_ALL + "- Resolution (Height,Width) :", a.shape)
    print("- Area :", a.size)
    deinit()
    
def myplot_diff(idx):
    """
    This function displays a 16-bit subtracted dark image at a certain exposure time (texp) with a logarithmic 
    colorbar which allows a 2D visualization of pixels intensity in ADU (or grey-scale value). The zero is set to 100. 
    """
    b = np.abs(frame_diff_stack[:,:, idx])
    plt.figure(num=None, dpi=300, facecolor='w', edgecolor='k')
    plt.imshow(b, cmap='seismic', norm=LogNorm(100, np.max(b))) 
    cbar = plt.colorbar(aspect=15, shrink=0.77)
    cbar.set_label('Log intensity (ADU)')
    plt.title('Diff. dark frame @ %is. 16-bit' %idx)
    plt.xlabel('x-axis (pixels)')
    plt.ylabel('y-axis (pixels)')
    scalebar = ScaleBar(5.86, 'um', location='lower left', box_alpha= 0.95, pad= 0.25, border_pad= 0.25, scale_loc='top', sep=3) # ex: Pixel size = 5.86 μm 
    plt.gca().add_artist(scalebar)
    plt.show()
    
             
if __name__ == "__main__":
    # main code
    folder_path = r"E:\CCD_CMOS\Basler acA1920-40gm CMOS\Dark2\{}s\{}.tiff" # your path
    scan_list = ['40u', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'] # ex: w/ 11 images, texp [40us;10s], at least six exposure times must be chosen (EMVA 1288)
    
    #noise
    frame_diff_stack, mu_stack, sigma_stack = noiseRoutine(folder_path, scan_list)
    histRoutine(frame_diff_stack, mu_stack, sigma_stack, scan_list) 
    
    #mean
    frame_mean_stack, mu_stack1, sigma_stack1 = meanRoutine(folder_path, scan_list)
    # histRoutine(frame_mean_stack, mu_stack1, sigma_stack1, scan_list)
    
    #--------------------------------------------------
    
    #2D visualization
    texp = 1 
    myplot_mean(texp)
    myplot_diff(texp)
  
    #--------------------------------------------------
  
    exp_time = np.array([40e-6, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) 

    init()
    print(Fore.GREEN + Style.BRIGHT,"\033[4m\nDifferential standard deviation (16-bit):\n\033[0m")
    res1 = stats.linregress(exp_time, sigma_stack[0:])
    coeff1 = round(res1.slope, 3) 
    print (Style.RESET_ALL + "- slope :", coeff1)
    origine1 = round(res1.intercept, 3)
    print ("- y-intercept :", origine1)
    print(f"- R-squared : {res1.rvalue**2:.3f}")
    
    plt.figure(dpi=300)
    plt.plot(exp_time, sigma_stack[0:], 's', label='mono data')
    plt.plot(exp_time, res1.intercept + res1.slope*exp_time, '--k', label='mono fit')
    plt.legend(loc='lower right')
    plt.xlabel('t [s]')
    plt.ylabel('$\sigma$R [ADU]')
    box_style=dict(boxstyle='square', facecolor='silver', alpha=0.7)
    plt.text(0.2,36.5, "y = {:0.2f}x + {:0.2f} \n"f"$R^2$ = {res1.rvalue**2:.3f}". format(coeff1, origine1),{'fontname':'Kozuka Gothic Pr6N','color':'black','weight':'normal','size':10}, bbox=box_style)
    # x,y coordinates need to be adjusted. 
    plt.grid()
    plt.title('Readout noise vs exposure time. Full-Frame average. 16-bit')
    plt.xlim([0, 10])
    plt.xticks(exp_time)
    plt.show()
    
    #--------------------------------------------------
   
    print(Fore.GREEN + Style.BRIGHT,"\033[4m\nDark current from mean (16-bit):\n\033[0m")
    res2 = stats.linregress(exp_time, mu_stack1[0:])
    coeff2 = round(res2.slope, 3)
    print(Style.RESET_ALL + "- slope :", coeff2)
    origine2 = round(res2.intercept, 3)
    print("- y-intercept :", origine2)
    print(f"- R-squared : {res2.rvalue**2:.3f}")    
    
    plt.figure(dpi=300)
    plt.plot(exp_time, mu_stack1[0:], 's', label='mono data')
    plt.plot(exp_time, res2.intercept + res2.slope*exp_time, '--k', label='mono fit')
    plt.legend(loc='lower right')
    plt.xlabel('t [s]')
    plt.ylabel('$\mu$ [ADU]')
    box_style=dict(boxstyle='square', facecolor='silver', alpha=0.7)
    plt.text(0.2,490, "y = {:0.2f}x {:0.2f} \n"f"$R^2$ = {res2.rvalue**2:.3f}". format(coeff2, origine2),{'fontname':'Kozuka Gothic Pr6N','color':'black','weight':'heavy','size':10}, bbox=box_style)
    # x,y coordinates need to be adjusted. 
    plt.grid()
    plt.title('Dark current from mean pixel value. Full-Frame average. 16-bit')
    plt.xlim([0, 10])
    plt.xticks(exp_time)
    plt.show()
    
    #--------------------------------------------------
    
    print (Fore.GREEN + Style.BRIGHT,"\033[4m\n12-bit values:\n\033[0m")

    for i in range(0,11): 
        #noise
        # num1 = mu_stack1[i]/16
        # num2 = (sigma_stack[i]*np.sqrt(2))/16
        # num3 = (sigma_stack[i]/16)*8.2
        # print (Style.RESET_ALL + 'Exp.time :",i,"s")
        # print( 'µ = ', round(num1, 2) , 'ADU')        
        # print('σ diff = ', round(num2, 2), 'ADU')
        # print('σR = ', round(num3, 2), 'e-\n')  
     
        # mean
        num4 = mu_stack1[i]/16
        num5 = (sigma_stack1[i])/16
        print (Style.RESET_ALL + '- Exp.time :',i,'s')
        print('µ =', round(num4, 2), 'ADU') 
        print('σ =', round(num5, 2), 'ADU\n') 
    
    deinit()
          
# plt.plot(exp_time, sigma_stack[0:])  #sigmaDiff
# plt.plot(exp_time, sigma_stack1[0:]) #sigmaMean