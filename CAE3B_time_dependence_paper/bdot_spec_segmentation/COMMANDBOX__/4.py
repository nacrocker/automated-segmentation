
def HighestDensityInterval(x,a=0.6827):
    xs=np.sort(np.asarray(x).flatten())
    a = np.amin([np.amax([a,0]),1])
    nxs=len(xs)
    nHDI=np.amax([1,np.rint(nxs*a).astype(int)])
    print(nHDI,nxs)
    iHDI=np.argmin(xs[nHDI:]-xs[0:-nHDI])
    return (xs[iHDI],xs[iHDI+nHDI-1]),(iHDI,iHDI+nHDI-1,xs)

def imshow_DataArray(DA,ax=None,**kwargs):
    import matplotlib.pyplot as plt
    c=DA.coords
    dy=DA.dims[0]
    dx=DA.dims[1]
    y=c.get(dy)
    x=c.get(dx)
    z=DA.data
    if ax is None: ax=plt
    im=plt.imshow(z,origin='lower',extent=(x[0],x[-1],y[0],y[-1]),aspect='auto',**kwargs)
    #splt.contourf(x,y,z,**kwargs)
    print(im.cmap)
    cbar=plt.colorbar()
    cbar.set_label(DA.name)
    plt.xlabel(dx)
    plt.ylabel(dy)
    return im,cbar


def show_spec(shot=None,ch=1,nperseg=8192,timeslice=(0.0,0.5),freqslice=slice(.2e6,2.2e6),returnspec=False):

    if shot is None: return  
    sig,time = getchb(shot=shot,ch=ch)
    if sig is None: stop    

    import matplotlib as mp
    import matplotlib.pyplot as plt
    import numpy as np

    #plt.figure()
    #plt.plot(time,sig)
    #plt.title('ch %02d, shot %d'%(ch,shot))
    #plt.xlabel('time')
    #plt.show(block=False)

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


    fig1=plt.figure()
    cmstd=cmapIDL_Standard_Gamma_II()
    #cmstd='Standard Gamma-II'
    vlim,_=HighestDensityInterval(np.log10(xsp_to_plot.data),.95)
    vlim=[10.0**v for  v in vlim]
    im1,cb1=imshow_DataArray(xsp_to_plot,vmin=vlim[0],vmax=vlim[1],norm=matplotlib.colors.LogNorm(),cmap=cmstd)
    ax1=im1.axes
    plt.xlabel('time (sec)')
    plt.ylabel('freq (Hz)')
    plt.title('ch %02d, shot %d'%(ch,shot))
    plt.show(block=False)
    if returnspec: return xsp


params45272highf={
        'shot':45272,'nperseg':8192,
        'timeslice':slice(0.1,0.9),'freqslice':slice(.2e6,2.2e6),
       }

params45272lowf={
        'shot':45272,'nperseg':8192,
        'timeslice':slice(0.1,0.9),'freqslice':slice(0,.2e6)
       }

params45367highf={
        'shot':45367,'nperseg':8192,
        'timeslice':slice(0.1,0.9),'freqslice':slice(.2e6,2.2e6),
       }

params45367lowf={
        'shot':45367,'nperseg':8192,
        'timeslice':slice(0.1,0.9),'freqslice':slice(0,.2e6)
       }

chhighfall=[1,2,3,11,12,13]
chlowfall=[4,5,6,7,8,9]

#params,chall=params45272highf,chhighfall
#params,chall=params45272lowf,chlowfall

#params,chall=params45367lowf,chlowfall
params,chall=params45367highf,chhighfall


for ch in chall:
    show_spec(ch=ch,**params)