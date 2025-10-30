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
    mode1 = dict(amp=1.0,  envrisetime=5.0, tsnorm=1.0/32, tfnorm=25.0/32, toffnorm=1.0/16, f0=0.7*fN , f1=0.8*fN, noise_std=0.5*np.pi, noise_bw=0.2*fN, nmode=1),
    mode2 = dict(amp=1.0, envrisetime=5.0, tsnorm=3.0/16 , tfnorm=15.0/16  , toffnorm=1.0/8 , f0=0.55*fN, f1=0.7*fN, noise_std=0.5*np.pi, noise_bw=0.2*fN, nmode=2),
    levels=[1e-6,7e-5,.005],#3,
    #mode1 = dict(amp=1.0,  envrisetime=1.0, tsnorm=1.0/16, tfnorm=13.0/16, toffnorm=1.0/16, f0=0.35*fN , f1=0.9*fN, noise_std=0.5*np.pi, noise_bw=0.2*fN, nmode=1),
    #mode2 = dict(amp=1.0, envrisetime=1.0, tsnorm=1.0/8 , tfnorm=7.0/8  , toffnorm=1.0/8 , f0=0.2*fN, f1=0.8*fN, noise_std=0.5*np.pi, noise_bw=0.2*fN, nmode=2),
    #levels=[1.3e-7,4e-5,.005],#3,
    cmap='viridis',
    colors=None,
    spquantrange = None,#[0.77,.99],
    vlim = [1e-9,2.6e-2],#None,
    xlimv = None,
    ylimv = [500.,850.0],
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
from OMFITlib_plot_utils import imshowxy, specim

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

if isinstance(cmap,str) and cmap == 'Standard_Gamma_II':
    from OMFITlib_plot_utils import cmapIDL_Standard_Gamma_II as cmapIDL_Standard_Gamma_II
    cmstd=cmapIDL_Standard_Gamma_II()
    cmap=cmstd

def apply_lims_and_labels(ax=plt):
    if not xlimv is None: ax.xlim(xlimv)
    if not ylimv is None: ax.ylim(ylimv)
    ax.xlabel('time [msec]')
    ax.ylabel('freq [kHz]')

if saveTag is None:
    saveTag=''
if saveTag != '': saveTag='_'+saveTag
figs_to_save=[]
def add_figure_to_save(fig=None,name=None):
    if not fig is None:
        figs_to_save.append(dict(fig=fig,name=name))

ncols=1
nrows=3
fighierarchy=plt.figure(figsize=(ncols*4, nrows*3),layout='constrained')
add_figure_to_save(fig=fighierarchy,name='figure_spcgsynth_levels_tree'+saveTag)

gs = fighierarchy.add_gridspec(ncols=ncols, nrows=nrows)
gsarr = np.asarray([[gs[r,c] for c in range(gs.ncols)] for r in range(gs.nrows)])
fighierarchy_panels={}
fighierarchy_panels['spec']=dict(gs=gsarr.ravel()[0],label='(a)',lablecol='r',labelpos=(.05,.9))
fighierarchy_panels['cntr']=dict(gs=gsarr.ravel()[1],label='(b)',lablecol='k',labelpos=(.05,.9))
fighierarchy_panels['tree']=dict(gs=gsarr.ravel()[2],label='(c)',lablecol='k',labelpos=(.05,.9))
def addpanellabel(ax,panelspec):
    ax.text(*panelspec['labelpos'],panelspec['label'],color=panelspec['lablecol'],transform=ax.transAxes)


ax=fighierarchy.add_subplot(fighierarchy_panels['spec']['gs'])
addpanellabel(ax,fighierarchy_panels['spec'])
imspec,cbspec = specim(tsp,fsp,sp,norm=norm,cmap=cmap)
apply_lims_and_labels()

if np.isscalar(levels):
    levels = np.int(np.round(levels))
    levels=vlim[0]*(vlim[1]/vlim[0])**(np.arange(0,levels)/(levels-1))

levelscf=np.append(levels,np.maximum(np.max(sp),np.max(levels))*1.00001)


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

#fig=plt.figure(figsize=(4, 3),layout='constrained')
ax=fighierarchy.add_subplot(fighierarchy_panels['cntr']['gs'])
addpanellabel(ax,fighierarchy_panels['cntr'])
cf = ax.contourf(tsp,fsp,sp,levelscf,norm=norm,**cdict,extend='max')
apply_lims_and_labels()
if True: #ticks at bases of colors
    cb=matplotlib.figure.Figure.colorbar(ax.figure,cf,norm=norm,format=formatter,extend='max')
    #cb=plt.colorbar(cf,norm=norm,format=formatter,extend='max')
    if len(levelscf) > len(levels): plt.setp(cb.ax.yaxis.get_ticklabels()[len(levels)-len(levelscf):],visible=False)
else: # ticks in middle of colors
    ncolors=len(colors)
    cb=matplotlib.figure.Figure.colorbar(ax.figure,
        matplotlib.cm.ScalarMappable(
            cmap=mpl.colors.ListedColormap(colors).with_extremes(under=colors[0], over=colors[-1]), 
            norm=mpl.colors.BoundaryNorm(np.linspace(0,1,ncolors+1), ncolors),
        ), 
        orientation='vertical',extend='max',spacing='uniform',
    )
    cb.set_ticks(np.linspace(.5,ncolors-0.5,ncolors)/ncolors,labels=['%0.2e'%l for l in levels])
    
def label_filled_contours(self,levels):
    filled_contours = np.zeros(self.P.shape,dtype=int)
    filled_contours_rav = filled_contours.ravel()
    P_rav=self.P.ravel()
    S = self.S
    image_rav_S = self.image.ravel()[S]
    levels = np.sort(levels)
    level_nodes = [[] for i in range(len(levels))]
    contour_parents = [[] for i in range(len(levels))]
    iSla = [*list(np.searchsorted(image_rav_S,levels)),len(S)]
    il = ib = 0
    for iiSl in range(len(iSla)-1):
        lvlnds = []
        for inode in S[iSla[iiSl]:iSla[iiSl+1]]:
            p = P_rav[inode]
            if filled_contours_rav[p] > ib:
                filled_contours_rav[inode] = filled_contours_rav[p]
            else:
                contour_parents[iiSl].append(filled_contours_rav[p])
                il = il+1
                level_nodes[iiSl].append(inode)
                filled_contours_rav[inode] = il
        ib = il
    return filled_contours,level_nodes,contour_parents

self = spmxtr = max_tree_cl(sp,connectivity=1)
filled_contours,level_nodes,contour_parents = label_filled_contours(self,levels)
filled_contours_level_indices = np.zeros(filled_contours.shape,dtype=int)
ll0 = 1
for il,ll in enumerate(level_nodes):
    ll = ll0 + np.arange(len(ll))
    filled_contours_level_indices[np.isin(filled_contours,np.array(ll))] = il+1
    ll0 = ll[-1]+1

ax_to_label=[cf.axes]

from OMFITlib_plot_utils import imshowxy
if False:
    figure(figsize=(4, 3),layout='constrained')
    imfc = imshowxy(tsp,fsp,filled_contours)      
    apply_lims_and_labels()
    title('filled contours')
    ax_to_label.append(imfc[0].axes) 
           

if False:
    figure(figsize=(4, 3),layout='constrained')
    imfcli = imshowxy(tsp,fsp,filled_contours_level_indices)      
    apply_lims_and_labels()
    title('filled contours indices')
    ax_to_label.append(imfcli[0].axes) 
    

tl=imspec.axes.get_xlim()
ntpxinlim = (len(tsp)-1)*(tl[1]-tl[0])/(tsp[-1]-tsp[0])
fl=imspec.axes.get_ylim()
nfpxinlim = (len(fsp)-1)*(fl[1]-fl[0])/(fsp[-1]-fsp[0])
fdistscale = 0.5*(ntpxinlim+nfpxinlim)/nfpxinlim
tdistscale = 0.5*(ntpxinlim+nfpxinlim)/ntpxinlim
distfunc = lambda binimg: scipy.ndimage.distance_transform_edt(binimg, sampling=(fdistscale,tdistscale))


labcol='r'
labfontsize=12
nlevs=builtins.sum(map(len,level_nodes))
labelstrs=[chr(ord('A')+i) for i in range(nlevs)]
def ijmax(a):
    i, j = np.unravel_index(a.argmax(), a.shape)
    return i,j

def ijnearmax(a,tol=0.95):
    return np.argwhere(a/a.max() >= tol)

def ijmid(dist,tol=0.95):
    ijnmx = ijnearmax(dist,tol).T
    ijnmx = ijnmx[:,np.lexsort(ijnmx)]
    junq = np.unique(ijnmx[1,:])
    jmid = junq[int(len(junq)/2)]
    ijnmxjmid = ijnmx[:,ijnmx[1] == jmid]
    ijnmxijmid = ijnmxjmid[:,int(ijnmxjmid.shape[1]/2)]
    return ijnmxijmid

#ijlabloc = ijmax
ijlabloc = lambda dist: ijmid(dist,tol=0.85)
levijloc = []
for il in range(nlevs):
    levijloc.append(ijlabloc(distfunc(filled_contours == (il+1))))

for ij,lab in zip(levijloc,labelstrs):
    for ax in ax_to_label:
        ax.annotate(lab,[tsp[ij[1]],fsp[ij[0]]],horizontalalignment='center',verticalalignment='center',color=labcol,fontsize=labfontsize)
 
if False:
    il=0
    lab = labelstrs[il]
    figure(figsize=(4, 3),layout='constrained')
    dist=distfunc(filled_contours == (il+1))
    im = imshowxy(tsp,fsp,dist)
    apply_lims_and_labels()
    ij = ijlabloc(dist)
    im[0].axes.annotate(lab,[tsp[ij[1]],fsp[ij[0]]],horizontalalignment='center',verticalalignment='center',color=labcol,fontsize=labfontsize)

cntr=max_tree_cl()
cntr._P = np.array([c-1 if c > 0 else 0 for l in contour_parents for c in l],dtype=int).reshape(1,-1)
cntr._image = np.asarray([v for v,l in zip(np.sort(levels),contour_parents) for c in l]).reshape(1,-1)
cntr._S = np.arange(cntr.P.size,dtype=int)

imagecntr_rav = cntr.image.ravel()
Pcntr_rav = cntr.P.ravel()

xcoord=np.zeros(cntr.S.size)
dxcoord=np.zeros(cntr.S.size)
xcoordroot = 0.0
xccordrootincr = 1.0
dxcoordscalefactor = 2.0*(xccordrootincr/4.0) # should be <= 2.0*xccordrootincr/3.0
xcoord[cntr.S[0]] = xcoordroot
dxcoord[cntr.S[0]] = dxcoordscalefactor

canonicalitycntr_rav = cntr.canonicality.ravel()
numchildcomponentscntr_rav =  cntr.numchildcomponents.ravel()
childhits=np.zeros(cntr.S.size)
for node in cntr.S[1:]:
    p = Pcntr_rav[node]
    if p == node:
        xccordroot += xccordrootincr
        xcoord[node] = xcoordroot
        continue
    if canonicalitycntr_rav[node]:
        nch = numchildcomponentscntr_rav[p]
        xcoord[node] = xcoord[p] 
        if nch > 1:
            xcoord[node] += (childhits[p]/(nch-1)-0.5)*dxcoord[p]
        childhits[p] += 1
        dxcoord[node] = dxcoord[p]
        if nch > 1:
            dxcoord[node]*=dxcoordscalefactor/(nch-1)

_,ycoord=np.unique(cntr.image.ravel(),return_inverse=True)
#figure(figsize=(4, 3),layout='constrained')
ax=fighierarchy.add_subplot(fighierarchy_panels['tree']['gs'])
addpanellabel(ax,fighierarchy_panels['tree'])
plot(np.stack((xcoord,xcoord[cntr.P.ravel()])),np.stack((ycoord,ycoord[cntr.P.ravel()])),color='k',zorder=0)
scatter(xcoord,ycoord,c=np.stack(colors)[ycoord.astype(int)],marker='o',s=1024,zorder=1)
for x,y,l in zip(xcoord,ycoord,labelstrs):
    text(x,y,l,horizontalalignment='center',verticalalignment='center',color='r')
xlim([-1,1])
ax.set_axis_off()

from OMFITlib_utils import saveFigToTree
for ftsdict in figs_to_save:
    figtosave,nametosave = ftsdict['fig'],ftsdict['name']
    saveFigToTree(figtosave,saveLocation=saveLocation,saveName=nametosave,saveFIG=saveFIG,savePDF=savePDF)