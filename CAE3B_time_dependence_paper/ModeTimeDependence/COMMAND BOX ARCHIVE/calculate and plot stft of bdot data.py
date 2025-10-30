import scipy.signal as signal
shot = 141398
bdotarray='HN'
bdotnames = ['\\OPS_PC::BDOT_L1DMIVVHN3_RAW', '\\OPS_PC::BDOT_L1DMIVVHN2_RAW', '\\OPS_PC::BDOT_L1DMIVVHN1_RAW', '\\OPS_PC::BDOT_L1DMIVVHN16_RAW', '\\OPS_PC::BDOT_L1DMIVVHN15_RAW', '\\OPS_PC::BDOT_L1DMIVVHN14_RAW', '\\OPS_PC::BDOT_L1DMIVVHN13_RAW', '\\OPS_PC::BDOT_L1DMIVVHN10_RAW', '\\OPS_PC::BDOT_L1DMIVVHN7_RAW', '\\OPS_PC::BDOT_L1DMIVVHN6_RAW', '\\OPS_PC::BDOT_L1DMIVVHN5_RAW', '\\OPS_PC::BDOT_L1DMIVVHN4_RAW']
rt = OMFIT['ModeTimeDependence']
#rt = root # use this line if this a module script

shotsholder = rt['OUTPUTS']
shotoutputs=shotsholder[shot]=OMFITtree('')
bdotoutputs=shotoutputs['bdot']=OMFITtree('')
arrayoutputs=bdotoutputs[bdotarray]=OMFITtree('')
data=arrayoutputs['data']=OMFITtree('')
stftoutputs=arrayoutputs['stft']=OMFITtree('')

bdottimes = [0.15,0.30]
stft=stftoutputs[tuple(bdottimes)]=OMFITtree('')

window='hann'
window_time=0.001
overlap_time= window_time*0.5
usepow2nfft = False # if True, use zero padding for ffts to bring nfft up to a power of 2
detrend='constant'
boundary=None
padded=None

for ib,bname in enumerate(bdotnames):
    data[ib] = OMFITmdsValue(server='NSTX', shot=141398, TDI=bname, treename='OPS_PC')
    if ib is 0:
        time = data[ib].dim_of(0)
        fsamp = (len(time)-1)/ (time[-1] - time[0])
        fsamp = 100 * np.round(fsamp/100)
        window_length = int(window_time * fsamp)
        overlap_length = int(overlap_time * fsamp)
        nfft=None
        if usepow2nfft: nfft=2**np.ceil(np.log2(window_length))

        ibdot = np.argwhere(numpy.logical_and(bdottimes[1]>=time,bdottimes[0]<=time))[[0,-1]]
        nsamp = ibdot[1][0]-ibdot[0][0]

    fZ, tZ, Z = signal.stft(array(data[ib].data()[ibdot[0][0]:ibdot[1][0]]), nperseg=window_length, noverlap=overlap_length, window=window, fs=fsamp, nfft=nfft, detrend=detrend, boundary=boundary, padded=padded)
    tZ = tZ + time[ibdot[0][0]]
    stft[ib] = Z

    if ib is 0:
        stft.insert(0,'freq',fZ)
        stft.insert(1,'time',tZ)

print('Sampling rate: {} samples/second'.format(fsamp))
print('Signal size: {} samples'.format(nsamp))
print('Signal duration: {:.3f} seconds'.format(nsamp/fsamp))


# In[4]:


# Plotting the spectrogram
import matplotlib.pyplot as plt
plot_utils=OMFIT['ModeTimeDependence']['LIB']['OMFITlib_plot_utils'].importCode()
cmapIDL_Standard_Gamma_II=plot_utils.cmapIDL_Standard_Gamma_II
imshowxy=plot_utils.imshowxycmstd=cmapIDL_Standard_Gamma_II()
specim=plot_utils.specim

math_utils=OMFIT['ModeTimeDependence']['LIB']['OMFITlib_math_utils'].importCode()
HighestDensityInterval=math_utils.HighestDensityInterval

ipltbdot=0
tmbdot,bdot = data[ipltbdot].dim_of(0)[ibdot[0][0]:ibdot[1][0]],data[ipltbdot].data()[ibdot[0][0]:ibdot[1][0]]
fsp,tsp,sp = stft['freq'], stft['time'],np.abs(stft[ipltbdot])**2

fig = plt.figure(figsize=(5, 3.5),layout='constrained')
gs = GridSpec(3, 1, figure=fig)
ax1 = fig.add_subplot(gs[0, 0])

plt.plot(tmbdot,bdot)
plt.title(f"{shot}, {bdotnames[ipltbdot]}",pad=8.0)
xlm=ax1.get_xlim()
#plt.xlabel('time [sec]')

#sca(axs[1])
#plt.imshow(np.flip(np.log10(sp), axis=0), extent=(np.min(tsp), np.max(tsp), np.min(fsp), np.max(fsp)), aspect='auto')
#plt.title('Spectrogram')
#plt.ylabel('freq [Hz]')
#plt.xlabel('time [sec]')
#plt.colorbar()

cmstd=cmapIDL_Standard_Gamma_II()
#cmstd='Standard Gamma-II'
#vlim,_=HighestDensityInterval(np.log10(sp),.95)
#vlim=(lambda mx,o:[mx-o,mx])(np.max(np.log10(sp)),8)
#vlim=[10.0**v for  v in vlim]
vlim=None
if vlim:
  vlimdict=dict(vmin=vlim[0],vmax=vlim[1])
else:
  vlimdict={}
ax2=fig.add_subplot(gs[1:,0],sharex=ax1)
kwextra={}
#kwextra.update(dict(title='Spectrogram'))
im1,cb1=specim(tsp,fsp/1e6,sp,xlabel='time [sec]',ylabel='freq [MHz]',norm=matplotlib.colors.LogNorm(**vlimdict),cmap=cmstd,**kwextra)
ax2.set_xlim(xlm)
