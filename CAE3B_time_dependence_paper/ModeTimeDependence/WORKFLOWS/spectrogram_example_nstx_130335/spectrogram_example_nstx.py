defParams=SortedDict(dict(
    bdotarray = 'HN',
    shot=141398,
    plotcoilind=3,
    timerange = [0.0,1.0],
    freqrange = [0.2e6,2.0e6],
    spquantrange = [.03,1],
    window='hann',
    window_time = 0.001, #sec
    overlap = 0.5,
    usepow2nfft = False, # if True, use zero padding for ffts to bring nfft up to a power of 2
    detrend = 'constant',
    saveFIG=True,
    savePDF=False,
    saveLocation=None,
    saveTag=None
    ))

if parent and 'parameters' in parent: defParams.update(parent['parameters'])
defaultVars(**defParams)

bdotarray=bdotarray.upper()
bdotcoilarrays = dict(
    HF = dict(
        names = ['\\OPS_PC::BDOT_L1DMIVVHF1_RAW', '\\OPS_PC::BDOT_L1DMIVVHF2_RAW', '\\OPS_PC::BDOT_L1DMIVVHF4_RAW', '\\OPS_PC::BDOT_L1DMIVVHF5_RAW', '\\OPS_PC::BDOT_L1DMIVVHF9_RAW', '\\OPS_PC::BDOT_L1DMIVVHF11_RAW']
        ),
    HN = dict(
        names = ['\\OPS_PC::BDOT_L1DMIVVHN3_RAW', '\\OPS_PC::BDOT_L1DMIVVHN2_RAW', '\\OPS_PC::BDOT_L1DMIVVHN1_RAW', '\\OPS_PC::BDOT_L1DMIVVHN16_RAW', '\\OPS_PC::BDOT_L1DMIVVHN15_RAW', '\\OPS_PC::BDOT_L1DMIVVHN14_RAW', '\\OPS_PC::BDOT_L1DMIVVHN13_RAW', '\\OPS_PC::BDOT_L1DMIVVHN10_RAW', '\\OPS_PC::BDOT_L1DMIVVHN7_RAW', '\\OPS_PC::BDOT_L1DMIVVHN6_RAW', '\\OPS_PC::BDOT_L1DMIVVHN5_RAW', '\\OPS_PC::BDOT_L1DMIVVHN4_RAW']
        ),
    )
bdotnames = bdotcoilarrays[bdotarray]['names']
bdotshortnames=[re.search(r'('+bdotarray+r'\d+)',b).group(0) for b in bdotnames]
ibdot = 0
if bdotarray+str(plotcoilind) in bdotshortnames: ibdot = bdotshortnames.index(bdotarray+str(plotcoilind))


brnch=root['OUTPUTS'].addBranchPath(f"[{shot}]['bdot']['{bdotarray}']['data']")
shotholder,shotoutputs,bdotoutputs,arrayoutputs=(b[0] for b in  brnch)
arrayoutputs.addBranchPath("['stft']")
data=arrayoutputs['data']
stftoutputs=arrayoutputs['stft']
stft=stftoutputs[tuple(timerange)]=OMFITtree('')

import scipy.signal as signal
overlap_time= window_time*overlap
boundary=None
padded=None

stft.insert(0,'parameters',defParams)
stft.insert(1,'bdotnames',bdotnames)
stft.insert(2,'bdotshortnames',bdotshortnames)
data['bdotnames'] = bdotnames
data['bdotshortnames'] = bdotshortnames
for ib,bname in enumerate(bdotnames):
    data[ib] = OMFITmdsValue(server='NSTX', shot=shot, TDI=bname, treename='OPS_PC')
    if ib is 0:
        time = data[ib].dim_of(0)
        fsamp = (len(time)-1)/ (time[-1] - time[0])
        fsamp = 100 * np.round(fsamp/100)
        window_length = int(window_time * fsamp)
        overlap_length = int(overlap_time * fsamp)
        nfft=None
        if usepow2nfft: nfft=2**np.ceil(np.log2(window_length))

        itm = np.argwhere(numpy.logical_and(timerange[1]>=time,timerange[0]<=time))[[0,-1]]
        nsamp = itm[1][0]-itm[0][0]

    fZ, tZ, Z = signal.stft(array(data[ib].data()[itm[0][0]:itm[1][0]]), nperseg=window_length, noverlap=overlap_length, window=window, fs=fsamp, nfft=nfft, detrend=detrend, boundary=boundary, padded=padded)
    tZ = tZ + time[itm[0][0]]
    if ib is 0:
        stft.insert(3,'freq',fZ)
        stft.insert(4,'time',tZ)
    stft[ib] = Z

print('Sampling rate: {} samples/second'.format(fsamp))
print('Signal size: {} samples'.format(nsamp))
print('Signal duration: {:.3f} seconds'.format(nsamp/fsamp))


# Plotting the spectrogram
import matplotlib.pyplot as plt
#plot_utils=OMFIT['ModeTimeDependence']['LIB']['OMFITlib_plot_utils'].importCode()
#cmapIDL_Standard_Gamma_II=plot_utils.cmapIDL_Standard_Gamma_II
#specim=plot_utils.specim

from OMFITlib_plot_utils import cmapIDL_Standard_Gamma_II, specim

#math_utils=OMFIT['ModeTimeDependence']['LIB']['OMFITlib_math_utils'].importCode()
#HighestDensityInterval=math_utils.HighestDensityInterval

from OMFITlib_math_utils import HighestDensityInterval

tmbdot,bdot = data[ibdot].dim_of(0)[itm[0][0]:itm[1][0]],data[ibdot].data()[itm[0][0]:itm[1][0]]
fsp,tsp,sp = stft['freq'], stft['time'],np.abs(stft[ibdot])**2

fig = plt.figure(figsize=(4, 4),layout='constrained')
gs = GridSpec(4, 1, figure=fig)
ax1 = fig.add_subplot(gs[0, 0])

plt.plot(tmbdot,bdot)
plt.title(f"{shot}, {bdotnames[ibdot]}",pad=8.0)
plt.xlim(timerange)
#xlm=ax1.get_xlim()
plt.xticks(visible=False)
plt.ylabel('(volts)')

cmstd=cmapIDL_Standard_Gamma_II()
#cmstd='Standard Gamma-II'
#vlim,_=HighestDensityInterval(np.log10(sp),.95)
#vlim=(lambda mx,o:[mx-o,mx])(np.max(np.log10(sp)),8)
#vlim=[10.0**v for  v in vlim]
vlim=None
if not spquantrange is None: vlim=np.quantile(sp,spquantrange)
if not vlim is None:
  vlimdict=dict(vmin=vlim[0],vmax=vlim[1])
else:
  vlimdict={}
kwextra={}
#kwextra.update(dict(title='Spectrogram'))
ax2=fig.add_subplot(gs[1:,0],sharex=ax1)
im1,cb1=specim(tsp,fsp/1e6,sp,xlabel='time [sec]',ylabel='freq [MHz]',norm=matplotlib.colors.LogNorm(**vlimdict),cmap=cmstd,cbkwargs=dict(extend='both'),**kwextra)
plt.ylim(np.array(freqrange)/1e6)
#ax2.set_xlim(xlm)


intr=lambda x:np.int(np.round(x))
if saveTag is None:
    saveTag=f'{bdotshortnames[ibdot]}_{shot}_t{intr(timerange[0]*1e3):d}_{intr(timerange[1]*1e3):d}_f{intr(freqrange[0]/1e3):d}_{intr(freqrange[1]/1e3):d}'

from OMFITlib_utils import saveFigToTree
saveFigToTree(fig,saveLocation=saveLocation,saveName='figure_spcg_'+saveTag,saveFIG=saveFIG,savePDF=savePDF)
