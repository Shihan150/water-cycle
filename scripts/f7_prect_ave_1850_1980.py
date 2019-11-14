# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 11:04:34 2019

@author: Shihan Li
plot the geographic distribution of average precipitation (1850-1980 AD)
"""
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
#readdata function
from netCDF4 import Dataset
def readdata(file_name):
    file_path_re = r'C:\Users\59506\Desktop\plot\atmosphere'
    b = '/'
    file_path = file_path_re + b + file_name
    file_obj = Dataset(file_path)
    print(file_obj.variables.keys())
    return file_obj

def static_plot(time_index, key_variable, lat, lon, 
                figsize, title1, title2, colorbar_title,figtitle):
    #time_index: time interval filter conditions; key_variable: key variables for ploting
    #lat, lon: coordinates from data
    #figsize: define the size of final figure
    #titles: title name for each element respectively
    time_interval = time[time_index] #make the time interval
    #pick up the key variable value for  correspondent time interval
    key_variable_in_interval = key_variable[time_index[0][0]:time_index[0][-1]+1,:,:] 
    #calculate the average in this time interval
    key_variable_ave = np.empty([len(lat),len(lon)])
    for i in range(len(lat)):
        for j in range(len(lon)):
            key_variable_ave[i,j] = np.mean(key_variable_in_interval[:,i,j])
    #calculate zonal average
    key_variable_zonal = np.empty([len(time_interval),len(lat)])
    for i in range(len(time_interval)):
        for j in range(len(lat)):
            key_variable_zonal[i,j] = np.mean(key_variable_in_interval[i,j,:])
    
    
    upper_limitation = 400
    lower_limitation = 0
    
    #start ploting
    fig = plt.figure(figsize = figsize)

    #plot ax1, average evaporation in last 1kyr
    ax1 = fig.add_subplot(2,1,1, projection=ccrs.PlateCarree())
    ax1.coastlines()
    #plot ax1.controuf map
    contf = ax1.contourf(lon,lat,key_variable_ave, 
                         levels = np.linspace(lower_limitation,upper_limitation,41),
                         extend = 'max',
                         projection=ccrs.PlateCarree())
    #set title for ax1
    ax1.set_title(title1 , fontweight = 'bold', fontsize = 20)
    #plot the contour line
    #levels = range(100,700,200)
    #countour = ax1.contour(lon, lat, evap_ave, levels = levels, colors='r',linestyles = 'dashed')
    #add colorbar
    cb1 = fig.colorbar(contf, ticks = np.linspace(lower_limitation, upper_limitation, 11),  format = '%.0f',
                   orientation = 'horizontal',fraction=0.08, pad=0.12)
    #set ax1.colorbar format
    cb1.set_label(colorbar_title,  fontsize = 16)
    cb1.ax.tick_params(labelsize=16)
    #set ax1 label's and tick's format
    ax1.set_xticks([ -180, -120, -60,0, 60, 120, 180,], crs=ccrs.PlateCarree())
    ax1.set_yticks([-90, -60, -30, 0, 30, 60, 90],  crs=ccrs.PlateCarree())
    ax1.tick_params(axis='both', labelsize=20)
    ax1.xaxis.set_major_formatter(LongitudeFormatter())
    ax1.yaxis.set_major_formatter(LatitudeFormatter())

    #plot ax2, zonal distribution for ax1
    ax2 = fig.add_subplot(2,1,2)
    key_variable_ave_zonal = np.mean(key_variable_ave, axis = 1)
    key_variable_ave_z = ax2.plot(lat, key_variable_ave_zonal, linewidth=3.0, color = 'b')
    #set ax2 format
    ax2.set_title(title2, fontweight = 'bold', fontsize = 20 )
    ax2.set_xlabel('°N',fontsize = 16)
    ax2.tick_params(labelsize=16) 
    ax2.set_ylabel("cm/year",fontsize = 16)

    fig.savefig(figtitle)
    return fig
##read precipitation data
file_name = ('trace.01-36.22000BP.cam2.PRECT.22000BP_decavg_400BCE.nc')
data_prect = readdata(file_name)
lon = data_prect.variables['lon'][:]
lat = data_prect.variables['lat'][:]
time = data_prect.variables['time'][:]
#unit conversion constant
unit_conversion_constant = 60 * 60 * 24 *365 * 100
# convert unit from m/s to cm/year
prect = data_prect.variables['PRECT'][:]* unit_conversion_constant

#fulfill the data gap in 360° lon by appending another column in lon and 
#copying the data at 0° to it
lon = np.append(lon, 360)
prect = np.dstack((prect,prect[:,:,0])) 

#define the time interval: 1850 - 1980 AD
time_index = np.where(time>=-0.1)
figsize = (12,14)
title1 = 'a.Annual precipitation (1850-1980 AD)'
title2 = 'b.Zonal average precipitation (1850-1980 AD)'
colorbar_title = 'Precipitation rate (cm/year)'
figtitle = 'prect_ave_1850_1980.png'
fig = static_plot(time_index, prect, lat, lon, 
                figsize, title1, title2, colorbar_title,figtitle)   

