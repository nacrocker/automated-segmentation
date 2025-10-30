# coding: utf-8

def getchb(shot=None,ch=1):
    if shot is None: return None
    import pyuda
    client=pyuda.Client()
    b=client.get('/XMC/ACQ216_202/CH%02d'%ch,shot)
    return (b.data,b.time.data)


params45208CAEs={
        'shot':45208,'ch':1,'nperseg':8192,
        'timeslice':slice(0,0.6),'freqslice':slice(1.2e6,2.2e6),
        'significance':2
       }
params44752TAEs={
        'shot':44752,'ch':1,'nperseg':8192,
        'timeslice':slice(0.125,0.25),'freqslice':slice(.25e5,3e5),
        'significance':1.5
       }

params44436EAEs_ch1={
        'shot':44436,'ch':1,'nperseg':8192,
        'timeslice':slice(0.125,0.25),'freqslice':slice(.25e5,4e5),
        'significance':1.5
       }

params44436EAEs_ch3={
        'shot':44436,'ch':3,'nperseg':8192,
        'timeslice':slice(0.125,0.25),'freqslice':slice(.25e5,4e5),
        'significance':1.5
       }

params45272lowf_ch4={
        'shot':45272,'ch':4,'nperseg':8192,
        'timeslice':slice(0.75,0.9),'freqslice':slice(.25e5,4e5),
        'significance':1.5
       }

params45272highf_ch3={
        'shot':45272,'ch':3,'nperseg':8192,
        'timeslice':slice(0.75,0.9),'freqslice':slice(.2e6,2.2e6),
        'significance':1.5
       }

params45272highf_ch1={
        'shot':45272,'ch':1,'nperseg':8192,
        'timeslice':slice(0.75,0.9),'freqslice':slice(.2e6,2.2e6),
        'significance':1.5
       }

params45367lowf_ch4={
        'shot':45367,'ch':4,'nperseg':8192,
        'timeslice':slice(0.1,0.9),'freqslice':slice(0,.2e6),
        'significance':3
       }

paramstemp={
        'shot':45367,'ch':4,'nperseg':8192,
        'timeslice':slice(0.1,0.9),'freqslice':slice(0,.2e6),
        'significance':5
       }

#paramstemp={
#        'shot':48643,'ch':3,'nperseg':8192,
#        'timeslice':slice(0.1,0.9),'freqslice':slice(0,.2e6),
#        'significance':5
#       }

params=paramstemp
shot=params['shot']
ch=params['ch']

sig,time = getchb(shot=shot,ch=ch)
if sig is None: stop

import matplotlib as mp
import matplotlib.pyplot as plt
import numpy as np

plt.figure()
plt.plot(time,sig)
plt.title('ch %02d, shot %d'%(ch,shot))
plt.xlabel('time')
plt.show(block=False)

from scipy.signal import stft

fs=(len(time) - 1)/(time[-1]-time[0])
nperseg=params['nperseg']
noverlap=np.round(nperseg/2)
fsp,tsp,Zsig = stft(sig,fs,nperseg=nperseg,noverlap=noverlap,detrend='constant',boundary=None,padded=False)
sp=np.abs(Zsig)**2

import xarray as xr
timeslice=params['timeslice']
freqslice=params['freqslice']
xsp=xr.DataArray(sp,[('freq',fsp),('time',tsp)],name='bdot^2')
xsp_to_plot=xsp.sel(dict(time=timeslice,freq=freqslice))

def HighestDensityInterval(x,a=0.6827):
    xs=np.sort(np.asarray(x).flatten())
    a = np.amin([np.amax([a,0]),1])
    nxs=len(xs)
    nHDI=np.amax([1,np.rint(nxs*a).astype(int)])
    print(nHDI,nxs)
    iHDI=np.argmin(xs[nHDI:]-xs[0:-nHDI])
    return (xs[iHDI],xs[iHDI+nHDI-1]),(iHDI,iHDI+nHDI-1,xs)

def imshow_DataArray(DA,ax=plt,**kwargs):
    import matplotlib.pyplot as plt
    c=DA.coords
    dy=DA.dims[0]
    dx=DA.dims[1]
    y=c.get(dy)
    x=c.get(dx)
    z=DA.data
    im=ax.imshow(z,origin='lower',extent=(x[0],x[-1],y[0],y[-1]),aspect='auto',**kwargs)
    #splt.contourf(x,y,z,**kwargs)
    print(im.cmap)
    cbar=plt.colorbar()
    cbar.set_label(DA.name)
    plt.xlabel(dx)
    plt.ylabel(dy)
    return im,cbar

def specim(time,freq,spec,ax=plt,**kwargs):
    im=ax.imshow(spec,aspect='auto',origin='lower',extent=(time[0],time[-1],freq[0],freq[-1]),**kwargs)
    plt.ylabel('freq')
    plt.xlabel('time')
    cb=plt.colorbar()
    return im,cb

fig1=plt.figure()
cmstd=cmapIDL_Standard_Gamma_II()
#cmstd='Standard Gamma-II'
vlim,_=HighestDensityInterval(np.log10(xsp_to_plot.data),.95)
vlim=[10.0**v for  v in vlim]
#im1,cb1=imshow_DataArray(xsp_to_plot,vmin=vlim[0],vmax=vlim[1],norm=matplotlib.colors.LogNorm(),cmap=cmstd)
im1,cb1=specim(xsp_to_plot.time,xsp_to_plot.freq,xsp_to_plot.data,vmin=vlim[0],vmax=vlim[1],norm=matplotlib.colors.LogNorm(),cmap=cmstd)
ax1=im1.axes
plt.title('ch %02d, shot %d'%(ch,shot))
plt.show(block=False)

import skimage.morphology as skimor
significance=params['significance']
footprint=None
#footprint=np.zeros((3,3))
#footprint[:,1]=1
#footprint=np.zeros((3,3))
#footprint[1,:]=1
#footprint=np.zeros((3,1))
x=xsp_to_plot
mask=np.log10(x.data)
seed=mask-significance
recon=skimor.reconstruction(seed,mask,footprint=footprint)
peaks=mask-recon

fig2=plt.figure()
im2,cb2=specim(x.time,x.freq,peaks,cmap=cmapIDL_Standard_Gamma_II())
ax2=im2.axes
plt.show(block=False)

ax1.sharex(ax2)
ax1.sharey(ax2)
