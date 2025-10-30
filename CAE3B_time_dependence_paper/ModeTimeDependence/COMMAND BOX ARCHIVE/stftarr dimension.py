rt=root # rt=OMFIT['ModeTimeDependence']

from OMFITlib_sigarraycov_utils import Vec2Cov
from OMFITlib_max_tree_class import max_tree as max_tree_cl
#stftroot = rt['OUTPUTS'][130335]['bdot']['HF']['stft'][(0.43, 0.53)]
stftroot = rt['OUTPUTS'][130335]['bdot']['HN']['stft'][(0.43, 0.53)]
stftarr0 = np.stack([stftroot[i] for i in np.sort([k for k in stftroot.keys() if isinstance(k,int)])],axis=2)
fsp0=stftroot['freq']
tsp0=stftroot['time']


nms=stftroot['bdotshortnames']
nmsexcl=['HN13']
inmsin = np.array([n not in nmsexcl for n in nms])
stftarr0=stftarr0[...,inmsin]
fsp0=stftroot['freq']
tsp0=stftroot['time']

freqrng=[.4e6,1.2e6]
print(type(fsp0))
infreqrng=(lambda x,r:(x >= r[0]) & (x < r[1]))(fsp0,freqrng)
stftarr0=stftarr0[infreqrng,...]
fsp0 = fsp0[infreqrng]
print(np.sum(infreqrng),np.min(fsp0),np.max(fsp0))

stftarr=stftarr0/np.sqrt(np.mean(np.abs(stftarr0)**2,axis=(0,1)))
stftcov=Vec2Cov(stftarr)

#sp=abs(stftroot[0])**2
sp=np.mean(abs(stftarr)**2,axis=2)
fsp,tsp=fsp0,tsp0

 
spmxtr=max_tree_cl(sp)
self=spmxtr
#print('same result: ',np.array_equiv(self.area,accumulate_attribute_from_leaf_to_root(self,self.P*0+1)))

stftcovacc = self.accumulate_attribute_from_leaf_to_root(stftcov)
#dimstftarr = np.sqrt(np.sum(np.real(np.diagonal(stftcovacc,axis1=2,axis2=3)),axis=2)**2/np.sum(np.sum(np.abs(stftcovacc)**2,axis=-1),axis=-1))
def effective_nuclear_rank(m,axis1=-2,axis2=-1):
    """Calculates effective nuclear rank for positive semidefinite hermitian matrix, 
    given by trace(m)**2/trace(m**2) == sum(eigenvalues(m))**2/sum(eigenvalues(m)**2)"""
    #return np.sum(np.real(np.diagonal(m,axis1=axis1,axis2=axis2)),axis=-1)**2/np.sum(np.abs(m)**2,axis=(axis1,axis2))
    return np.abs(np.trace(m,axis1=axis1,axis2=axis2))**2/np.sum(np.abs(m)**2,axis=(axis1,axis2))

def largest_eigenvalue_dominance(m):
    """Calculates dominance of largest eigenvalue for positive semidefinite hermitian matrix,
    given by ratio of trace to largest eigenvalue """
    from numpy import linalg as LA
    return np.abs(np.trace(m,axis1=-2,axis2=-1))/(LA.eigvalsh(m)[:,:,-1])

#dimstftarr = np.sum(np.real(np.diagonal(stftcovacc,axis1=2,axis2=3)),axis=2)**2/np.sum(np.abs(stftcovacc)**2,axis=(-2,-1)))
#dimstftarr = effective_nuclear_rank(stftcovacc)
dimstftarr = largest_eigenvalue_dominance(stftcovacc)

signaltonoise=self.volume/(self.area*self.image)
#signaltonoise=self.volume/(self.area*self.peak)
avspecdens=self.volume/self.area*self.extents[...,1]
#avspecdens=self.volume/self.area

#gain=signaltonoise.copy()
gain=avspecdens.copy()

gain_rav=gain.ravel()
mxgnnds = self.maxattrnodes(gain) # for each node, mark nodes which are maxima of gain along lineage
mxgnnds = self.optimummaxattrnodes(gain,maxattrnodes=mxgnnds) #prune (by setting False) gain-maximum nodes to leave only nodes with no descencdent or ancestor having higher gain.
mxgnndinds = np.flatnonzero(mxgnnds)
mxgnndinds = mxgnndinds[np.argsort(gain.ravel()[mxgnndinds])]
mxgn=gain*(mxgnnds > 0)

from OMFITlib_utils import assigntoarr as asgn, boolindices

figure()
plot(mxgnndinds,'o')
ntop=30
mxgnndindstop = mxgnndinds[-ntop:]
mxgnndslabeltop = asgn(np.zeros(self.image.shape),mxgnndindstop,range(ntop,0,-1)).reshape(self.image.shape)
mxgnndslabeltopfill = self.fill_components_from_markers(mxgnndslabeltop)
mxgntop=gain*(mxgnndslabeltop > 0)
mxgntopfill = self.fill_components_from_markers(mxgntop)

dimstftarrfill = self.fill_components_from_markers(dimstftarr*(mxgnndslabeltop > 0))


from OMFITlib_plot_utils import cmapIDL_Standard_Gamma_II as cmapIDL_Standard_Gamma_II
from OMFITlib_plot_utils import specim as specim
cmstd=cmapIDL_Standard_Gamma_II()
cmap=cmstd
CSS4 = matplotlib.colors.CSS4_COLORS

#bgcolor = CSS4['aliceblue']
#bgcolor = CSS4['cyan']
#bgcolor = CSS4['cadetblue']
bgcolor = CSS4['paleturquoise']

def zerotonan(arr):
    return np.where(arr == 0,np.nan,arr)


#fgsz=(12,9) #(horiz,vert)
#fgrc=(2,2) #(num rows, num cols)
#fgsz=(6,4.5) #(horiz,vert)
#fgrc=(1,1) #(num rows, num cols)
#fgsz=(6,9) #(horiz,vert)
#fgrc=(2,1) #(num rows, num cols)
fgsz0=(6,4.5) #single panel (horiz,vert)
fgrc=(2,3) #(num rows, num cols)
fgsz=(fgsz0[0]*fgrc[1],fgsz0[1]*fgrc[0])

fig = plt.figure(figsize=fgsz,layout='constrained')
gs = GridSpec(*fgrc, figure=fig)
gsrav = lambda i: gs[np.unravel_index(i, gs.get_geometry())]
gsit = (gsrav(i) for i in range(np.product(gs.get_geometry())))

axs,ims,cbs=[],[],[]
def save_handles(ax,im,cb):
    axs.append(ax)
    ims.append(im)
    cbs.append(cb)

kwextra={}
vlimdict={}

gsc=next(gsit)
normfunc=matplotlib.colors.LogNorm
norm=normfunc(**vlimdict)
ax = fig.add_subplot(gsc)
im,cb=specim(tsp,fsp/1e6,sp,xlabel='time [sec]',ylabel='freq [MHz]',cmap=cmstd,norm=norm,**kwextra)
title('sp')
save_handles(ax,im,cb)

ax1=axs[0]

gsc=next(gsit)
normfunc=matplotlib.colors.LogNorm
norm=normfunc(**vlimdict)
ax = fig.add_subplot(gsc)
im,cb=specim(tsp,fsp/1e6,zerotonan(gain),xlabel='time [sec]',ylabel='freq [MHz]',cmap=cmstd,norm=norm,**kwextra)
title('gain')
ax.set_facecolor(bgcolor)
ax.sharex(ax1)
ax.sharey(ax1)
save_handles(ax,im,cb)

gsc=next(gsit)
norm=None
#cmap=cmstd.reversed()
cmap=cmstd
ax = fig.add_subplot(gsc)
im,cb=specim(tsp,fsp/1e6,dimstftarr,xlabel='time [sec]',ylabel='freq [MHz]',cmap=cmstd,norm=norm,**kwextra)
title('stftarr max dimension')
ax.set_facecolor(bgcolor)
ax.sharex(ax1)
ax.sharey(ax1)
save_handles(ax,im,cb)

gsc=next(gsit)
norm=None
cmap=cmstd.reversed()
ax = fig.add_subplot(gsc)
#import pdb
#import sys
#debugger = pdb.Pdb(stdin=sys.__stdin__, stdout=sys.__stdout__)
#debugger.set_trace()
im,cb=specim(tsp,fsp/1e6,zerotonan(mxgnndslabeltopfill),xlabel='time [sec]',ylabel='freq [MHz]',cmap=cmap,norm=norm,**kwextra)
title(f'top {ntop} components')
cb.ax.invert_yaxis()
ax.set_facecolor(bgcolor)
ax.sharex(ax1)
ax.sharey(ax1)
save_handles(ax,im,cb)

def _():
    gsc=next(gsit)
    normfunc=matplotlib.colors.LogNorm
    norm=normfunc(**vlimdict)
    cmap=cmstd
    ax = fig.add_subplot(gsc)
    im,cb=specim(tsp,fsp/1e6,zerotonan(mxgntop),xlabel='time [sec]',ylabel='freq [MHz]',cmap=cmap,norm=norm,**kwextra)
    title(f'{ntop} max nodes labeled by gain')
    ax.set_facecolor(bgcolor)
    ax.sharex(ax1)
    ax.sharey(ax1)
    save_handles(ax,im,cb)

gsc=next(gsit)
normfunc=matplotlib.colors.LogNorm
norm=normfunc(**vlimdict)
ax = fig.add_subplot(gsc)
im,cb=specim(tsp,fsp/1e6,mxgntopfill,xlabel='time [sec]',ylabel='freq [MHz]',cmap=cmstd,norm=norm,**kwextra)
title(f'top {ntop} components labled by gain')
ax.set_facecolor(bgcolor)
ax.sharex(ax1)
ax.sharey(ax1)
save_handles(ax,im,cb)


gsc=next(gsit)
norm=None
#cmap=cmstd.reversed()
cmap=cmstd
ax = fig.add_subplot(gsc)
im,cb=specim(tsp,fsp/1e6,zerotonan(dimstftarrfill),xlabel='time [sec]',ylabel='freq [MHz]',cmap=cmstd,norm=norm,**kwextra)
title(f'top {ntop} max nodes labled by stftarr dimension')
ax.set_facecolor(bgcolor)
ax.sharex(ax1)
ax.sharey(ax1)
save_handles(ax,im,cb)
