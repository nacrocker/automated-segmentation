#root=OMFIT['ModeTimeDependence']

dt=0.5e-3
fs=1/dt
fN=fs*0.5


defParams=SortedDict(dict(
    t=np.arange(0,300.0,dt),
    nfft=1024,
    locations=[0.0],#,0.1,0.5,np.pi/2]
    tsmooth = 20.0,
    fsmooth = 20.0,
    signal_to_noise=10000.0,
    noise_bw = 0.0,#1500.0, 
    noise_f0 = 0.0,#200.0,
    mode1 = dict(amp=1.0,  envrisetime=1.0, tsnorm=1.0/32, tfnorm=25.0/32, toffnorm=1.0/16, f0=0.7*fN , f1=0.8*fN, noise_std=0.5*np.pi, noise_bw=0.2*fN, nmode=1),
    mode2 = dict(amp=1.0, envrisetime=1.0, tsnorm=3.0/16 , tfnorm=15.0/16  , toffnorm=1.0/8 , f0=0.55*fN, f1=0.7*fN, noise_std=0.5*np.pi, noise_bw=0.2*fN, nmode=2),
    levels=[1e-6,7e-5,.005],#3,
    #mode1 = dict(amp=1.0,  envrisetime=1.0, tsnorm=1.0/16, tfnorm=13.0/16, toffnorm=1.0/16, f0=0.35*fN , f1=0.9*fN, noise_std=0.5*np.pi, noise_bw=0.2*fN, nmode=1),
    #mode2 = dict(amp=1.0, envrisetime=1.0, tsnorm=1.0/8 , tfnorm=7.0/8  , toffnorm=1.0/8 , f0=0.2*fN, f1=0.8*fN, noise_std=0.5*np.pi, noise_bw=0.2*fN, nmode=2),
    #levels=[1.3e-7,4e-5,.005],#3,
    cmap='viridis',
    colors=None,
    spquantrange = None,#[0.77,.99],
    vlim = [1e-9,2.6e-2],#None,
    xlimv = None,
    ylimv = [500.,1000.0],
    saveFIG=True,
    savePDF=False,
    saveLocation=None,
    saveTag=None
    ))

if parent and 'parameters' in parent: defParams.update(parent['parameters'])

#with namespace_environment(OMFIT['Utilities']):
#    from OMFITlib_SCRIPT_utils import forceDefaultVarsGUI
#    forceDefaultVarsGUI()

defaultVars(**defParams)


from OMFITlib_math_utils import ChirpModeDesc, ChirpDesc, make_chirpmodes_sigarray, make_noise, gaussian_spectrum_noise, smooth_rise_square_pulse
from OMFITlib_max_tree_class import max_tree as max_tree_cl
from OMFITlib_plot_utils import imshowxy

nsig=len(locations)
nt=len(t)
dt=t[1]-t[0]
fs=1/dt
fN = fs/2.0

import pdb
import sys
debugger = pdb.Pdb(stdin=sys.__stdin__, stdout=sys.__stdout__)

def make_gaussian_multiplicative_noise_generator(std=0,f0=0.0,bw=0,perturbative=True):
    if std == 0:
        gen = lambda t: 0*t+1.0
    else:
        if bw > 0:
            gen = lambda t: (1.0 if perturbative else 0) + gaussian_spectrum_noise(len(t),std=std,f0=f0,bw=bw,fs=fs)
        else:
            gen = lambda t: (1.0 if perturbative else 0) + make_noise(0.0, std, (len(t),))

    return gen



#modes to match Hawowen Sun's noise_histograms_v2.
chirpmodedescs=[]
def add_chirpmodedesc(mode):
    ts=t[int(nt*mode['tsnorm'])]
    tl=t[int(nt*mode['tsnorm'])+int(nt*(mode['tfnorm']-mode['tsnorm']))-1] - ts
    toff=ts
    mode['tstart']=ts
    mode['tlen']=tl
    mode['toff']=toff
    for k in ['tsnorm','tfnorm','toffnorm']:
        mode.pop(k)

    if 'noise_std' in mode:
        mode['multiplicative_noise_generator'] = make_gaussian_multiplicative_noise_generator(std=mode.get('noise_std',0.0),f0=mode.get('noise_f0',0.0),bw=mode.get('noise_bw',0.0))        
    for k in ['noise_std','noise_f0','noise_bw']:
        if k in mode: mode.pop(k)
    
    
    if 'envrisetime' in mode:       
        mode['envlf'] = (lambda trise: (lambda t: smooth_rise_square_pulse(t-0.5,1.0,trise=trise/tl)))(mode.pop('envrisetime'))

    chirpmodedescs.append(ChirpModeDesc(nmode=mode.pop('nmode'),chirpdesc=ChirpDesc(**mode)))
    
add_chirpmodedesc(mode1.copy())
add_chirpmodedesc(mode2.copy())

# #modes to match Hawowen Sun's noise_histograms_v2.
# ts=t[int(nt/16)]
# tl=t[int(nt/16)+int(nt*3/4)-1] - ts
# phase_noise_std = 0.0
# phase_noise_tcorr = 0.1*nfft/fs
# chirpmodedescs.append(ChirpModeDesc(nmode=1,chirpdesc=ChirpDesc(amp=1.0 , tstart=ts, tlen=tl, toff=ts, f0=0.3*fN, f1=0.9*fN)))
# 
# ts=t[int(nt/8)]
# tl=t[int(nt/8)+int(nt*3/4)-1] - ts
# chirpmodedescs.append(ChirpModeDesc(nmode=2,chirpdesc=ChirpDesc(amp=0.75, tstart=ts, tlen=tl, toff=ts, f0=0.25*fN, f1=0.85*fN)))


noise = 0.0
if not signal_to_noise is None:
    noise_std = np.sqrt(np.mean(np.array([cm.chirpdesc.amp for cm in chirpmodedescs])**2))/signal_to_noise*sqrt(nfft)
    if noise_bw > 0:
        noise = gaussian_spectrum_noise(nt,std=noise_std,f0=noise_f0,bw=noise_bw,fs=fs)
    else:
        noise = make_noise(0.0, noise_std, (nt,))


sigarray = make_chirpmodes_sigarray(t, chirpmodedescs, locations=[0])
#data = noise
data = sigarray + noise 
data = data[0]
from scipy.signal import stft
fstft,tstft, sigstft=stft(data,fs,nperseg=nfft,noverlap=0.75*nfft)
fsp, tsp, sp = fstft, tstft, abs(sigstft)**2

from scipy.ndimage import convolve1d
sp0,tsp0,fsp0=sp,tsp,fsp
if tsmooth > 0:
    nsmt = np.int(np.round(tsmooth*fs/nfft))
    nsmt = np.int(nsmt/2)*2+1
    normsmt = convolve1d(np.ones((1,len(tsp))),np.ones(nsmt)/nsmt,mode='constant')
    sp = convolve1d(sp,np.ones(nsmt)/nsmt,mode='constant')/normsmt
    tsp = convolve1d(tsp,np.ones(nsmt)/nsmt,mode='constant')/normsmt.ravel()
if fsmooth > 0:
    nsmf = np.int(np.round(fsmooth*nfft/fs))
    nsmf = np.int(nsmf/2)*2+1
    normsmf = convolve1d(np.ones((len(fsp),1)),np.ones(nsmf)/nsmf,axis=0,mode='constant')
    sp = convolve1d(sp,np.ones(nsmf)/nsmf,mode='constant',axis=0)/normsmf
    fsp = convolve1d(fsp,np.ones(nsmf)/nsmf,mode='constant')/normsmf.ravel()

mxsp=np.max(sp)


#spquantrange = [0.0,1.0]


if vlim is None and not spquantrange is None: 
    vlim=np.quantile(sp,spquantrange)
    if vlim[0] == 0: 
        vlim[0] = np.min(sp.ravel()[sp.ravel() > 0])

if not vlim is None:
    vlimdict=dict(vmin=vlim[0],vmax=vlim[1])
else:
    vlimdict={}


normfunc=matplotlib.colors.LogNorm
norm=normfunc(**vlimdict)

if np.isscalar(levels):
    levels = np.int(np.round(levels))
    levels=vlim[0]*(vlim[1]/vlim[0])**(np.arange(0,levels)/(levels-1))

levelscf=np.append(levels,np.maximum(np.max(sp),np.max(levels))*1.00001)

if isinstance(cmap,str) and cmap == 'Standard_Gamma_II':
    from OMFITlib_plot_utils import cmapIDL_Standard_Gamma_II as cmapIDL_Standard_Gamma_II
    cmstd=cmapIDL_Standard_Gamma_II()
    cmap=cmstd

cdict=dict()
if colors is None:
    if isinstance(cmap,str): cmap=matplotlib.cm.get_cmap(cmap)
    #if isinstance(cmap,str): cmap=matplotlib.colormaps[cmap]
    colors=cmap(norm(levels))
    colors=[c[0:3] for c in colors]
    cdict['colors'] = colors
else:
    if isinstance(colors,np.ndarray):
        colors=[c for c in colors]
    cdict['colors'] = colors
formatter=matplotlib.ticker.FormatStrFormatter('%0.2e')

fig=plt.figure(figsize=(4, 3),layout='constrained')
cf = plt.contourf(tsp,fsp,sp,levelscf,norm=norm,**cdict,extend='max')
cb=matplotlib.figure.Figure.colorbar(fig,cf,norm=norm,format=formatter,extend='max')
#cb=plt.colorbar(cf,norm=norm,format=formatter,extend='max')
if len(levelscf) > len(levels): plt.setp(cb.ax.yaxis.get_ticklabels()[len(levels)-len(levelscf):],visible=False)

def apply_lims_and_labels(ax=plt):
    if not xlimv is None: ax.xlim(xlimv)
    if not ylimv is None: ax.ylim(ylimv)
    ax.xlabel('time [msec]')
    ax.ylabel('freq [kHz]')
apply_lims_and_labels()


intr=lambda x:np.int(np.round(x))
if saveTag is None:
    saveTag=''
if saveTag != '': saveTag=saveTag+'_'

from OMFITlib_utils import saveFigToTree
saveFigToTree(fig,saveLocation=saveLocation,saveName='figure_spcgsynth_levels_tree'+saveTag,saveFIG=saveFIG,savePDF=savePDF)



def label_filled_contours(self,levels):
    filled_contours = np.zeros(self.P.shape,dtype=int)
    filled_contours_rav = filled_contours.ravel()
    P_rav=self.P.ravel()
    S = self.S
    image_rav_S = self.image.ravel()[S]
    levels = np.sort(levels)
    level_nodes = [[] for i in range(len(levels))]
    iSla = [*list(np.searchsorted(image_rav_S,levels)),len(S)]
    il = ib = 0
    for iiSl in range(len(iSla)-1):
        lvlnds = []
        for inode in S[iSla[iiSl]:iSla[iiSl+1]]:
            p = P_rav[inode]
            if filled_contours_rav[p] > ib:
                filled_contours_rav[inode] = filled_contours_rav[p]
            else:
                il = il+1
                level_nodes[iiSl].append(inode)
                filled_contours_rav[inode] = il
        ib = il
    return filled_contours,level_nodes

self = spmxtr = max_tree_cl(sp,connectivity=1)
filled_contours,level_nodes = label_filled_contours(self,levels)
filled_contours_level_indices = np.zeros(filled_contours.shape,dtype=int)
ll0 = 1
for il,ll in enumerate(level_nodes):
    ll = ll0 + np.arange(len(ll))
    filled_contours_level_indices[np.isin(filled_contours,np.array(ll))] = il+1
    ll0 = ll[-1]+1

from OMFITlib_plot_utils import imshowxy
figure(figsize=(4, 3),layout='constrained')
imfc = imshowxy(tsp,fsp,filled_contours)      
apply_lims_and_labels()
        
figure(figsize=(4, 3),layout='constrained')
imfcli = imshowxy(tsp,fsp,filled_contours_level_indices)      
apply_lims_and_labels()


def distance_transform_axis(inp,axis=-1,**kwargs):
    if 'metric' in kwargs:
        raise KeyError('invalid keyword: metric')
    if axis < 0: axis = 2+axis
    if axis < 0 or axis > 1:
        raise ValueError('invalid axis value')
    metric = np.zeros((3,3),dtype=bool)
    metric[:,[0,2]] = True
    if axis == 0: metric = metric.T
    return scipy.ndimage.distance_transform_cdt(inp, metric=metric, **kwargs)

tl=imfc[0].axes.get_xlim()
ntpxinlim = (len(tsp)-1)*(tl[1]-tl[0])/(tsp[-1]-tsp[0])
fl=imfc[0].axes.get_ylim()
nfpxinlim = (len(fsp)-1)*(fl[1]-fl[0])/(fsp[-1]-fsp[0])
fdistscale = 0.5*(ntpxinlim+nfpxinlim)/nfpxinlim
tdistscale = 0.5*(ntpxinlim+nfpxinlim)/ntpxinlim


#metric = 0.5*(ntpxinlim+nfpxinlim)*np.arange(-1,2)[:,None]*np.ones((1,3))/nfpxinlim
#metric += 0.5*(ntpxinlim+nfpxinlim)*(np.arange(-1,2)[:,None]*np.ones((1,3))).T/ntpxinlim
#metric = "taxicab"


labcol='r'
labfontsize=12
nlevs=builtins.sum(map(len,level_nodes))
labelstrs=[chr(ord('A')+i) for i in range(nlevs)]
def ijmax(a):
    i, j = np.unravel_index(a.argmax(), a.shape)
    return i,j
levijloc = []
for il in range(nlevs):
    #dist=scipy.ndimage.distance_transform_cdt(filled_contours == (il+1), metric=metric)
    dist = (
            tdistscale*distance_transform_axis(filled_contours == (il+1),axis=0) +
            fdistscale*distance_transform_axis(filled_contours == (il+1),axis=1)
           )
    print(il,np.max(dist),np.count_nonzero(dist==np.max(dist)))
    levijloc.append(ijmax(dist))

for ij,lab in zip(levijloc,labelstrs):
    imfc[0].axes.annotate(lab,[tsp[ij[1]],fsp[ij[0]]],horizontalalignment='center',verticalalignment='center',color=labcol,fontsize=labfontsize)
    imfcli[0].axes.annotate(lab,[tsp[ij[1]],fsp[ij[0]]],horizontalalignment='center',verticalalignment='center',color=labcol,fontsize=labfontsize)

if True:
    ild=0
    ij,lab = levijloc[ild],labelstrs[ild]
    figure(figsize=(4, 3),layout='constrained')
    #dist = scipy.ndimage.distance_transform_cdt(filled_contours == (ild+1), metric="taxicab")
    dist = (
            tdistscale*distance_transform_axis(filled_contours == (ild+1),axis=0) +
            fdistscale*distance_transform_axis(filled_contours == (ild+1),axis=1)
           )
    imd = imshowxy(tsp,fsp,dist)
    apply_lims_and_labels()
    imd[0].axes.annotate(lab,[tsp[ij[1]],fsp[ij[0]]],horizontalalignment='center',verticalalignment='center',color=labcol,fontsize=labfontsize)


if plot_contour_lines:
    levelslab = (lambda a:np.sqrt(a[1:]*a[:-1]))(np.sort(levelscf))
    clab = cf.axes.contour(tsp,fsp,sp,levelslab,norm=norm,extend='max')
else:
    clab=None


from OMFITlib_plot_utils import specim
#normfunc=matplotlib.colors.LogNorm
#norm=normfunc()
if not clab is None: 
    fig=figure(layout='constrained',figsize=(16,4))
    axs=fig.subplots(1,4,sharex=True,sharey=True)
else: 
    fig=figure(layout='constrained',figsize=(4,4))
    axs=[fig.subplots(1,1)]
sca(axs[0])
specim(tsp,fsp,sp,norm=norm)
#csplab = plt.contour(tsp,fsp,sp,levels,norm=norm,colors='white',extend='max')
apply_lims_and_labels()
margins(0, 0)

if not clab is None:
    ai=1
    for s,l in zip(clab.allsegs,clab.levels):
        sca(axs[ai]); ai = ai + 1
        print(f'{l}')
        for p in s:
            plot(p[:,0],p[:,1])