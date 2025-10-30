#this seems to work for gain = avspecdens=self.volume/self.area*self.extents[...,1].  
#A question remains for how many top modes to keep.


rt=root # rt=OMFIT['ModeTimeDependence']

from OMFITlib_max_tree_class import max_tree as max_tree_cl
stftroot=rt['OUTPUTS'][130335]['bdot']['HF']['stft'][(0.43, 0.53)]
stftarr=np.stack([stftroot[i] for i in np.sort([k for k in stftroot.keys() if isinstance(k,int)])],axis=2)

#sp=abs(stftroot[0])**2
sp=np.mean(abs(stftarr)**2,axis=2)
fsp=stftroot['freq']
tsp=stftroot['time']

spmxtr=max_tree_cl(sp,connectivity=2)
self=spmxtr


signaltonoise=self.volume/(self.area*self.image)
#signaltonoise=self.volume/(self.area*self.peak)
avspecdens=self.volume/self.area*self.extents[...,1]
#avspecdens=self.volume/self.area


#gain=signaltonoise.copy()
gain=avspecdens.copy()
gain_rav=gain.ravel()


mxgnnds = self.maxattrnodes(gain) # for each node, find maxixum gain of itself and its ancecstors
mxgnnds = self.optimummaxattrnodes(gain,maxattrnodes=mxgnnds) #prune gain-maximum nodes to leave only nodes with no descencdent having higher gain.
mxgnndinds = np.flatnonzero(mxgnnds)
mxgnndinds = mxgnndinds[np.argsort(gain.ravel()[mxgnndinds])]
mxgn=gain*(mxgnnds > 0)

from OMFITlib_utils import assigntoarr as asgn, boolindices

ntop=100
mxgnndindstop = mxgnndinds[-ntop:]
mxgnndslabeltop = asgn(np.zeros(self.image.shape),mxgnndindstop,range(ntop,0,-1)).reshape(self.image.shape)
mxgnndslabeltopfill = self.fill_components_from_markers(mxgnndslabeltop)
mxgntop=gain*(mxgnndslabeltop > 0)
mxgntopfill = self.fill_components_from_markers(mxgntop)




from OMFITlib_plot_utils import cmapIDL_Standard_Gamma_II as cmapIDL_Standard_Gamma_II
from OMFITlib_plot_utils import specim as specim
cmstd=cmapIDL_Standard_Gamma_II()
cmap=cmstd
CSS4 = matplotlib.colors.CSS4_COLORS

#bgcolor = CSS4['aliceblue']
#bgcolor = CSS4['lightcyan']
bgcolor = CSS4['lightgray']

def zerotonan(arr):
    return np.where(arr == 0,np.nan,arr)

fig = plt.figure(figsize=(12,9),layout='constrained')
gs = GridSpec(2,2, figure=fig)


kwextra={}
vlimdict={}

gsc=gs[0,0]
normfunc=matplotlib.colors.LogNorm
norm=normfunc(**vlimdict)
ax = fig.add_subplot(gsc)
im,cb=specim(tsp,fsp/1e6,sp,xlabel='time [sec]',ylabel='freq [MHz]',cmap=cmstd,norm=norm,**kwextra)
title('sp')
ax1,im1,cb=ax,im,cb

gsc=gs[1,0]
normfunc=matplotlib.colors.LogNorm
norm=normfunc(**vlimdict)
ax = fig.add_subplot(gsc)
im,cb=specim(tsp,fsp/1e6,mxgntopfill,xlabel='time [sec]',ylabel='freq [MHz]',cmap=cmstd,norm=norm,**kwextra)
title(f'top {ntop} component gain')
ax.set_facecolor(bgcolor)
ax.sharex(ax1)
ax.sharey(ax1)
ax2,im2,cb2=ax,im,cb

gsc=gs[0, 1]    
norm=None
cmap=cmstd.reversed()
ax = fig.add_subplot(gsc)
im,cb=specim(tsp,fsp/1e6,zerotonan(mxgnndslabeltopfill),xlabel='time [sec]',ylabel='freq [MHz]',cmap=cmap,norm=norm,**kwextra)
title(f'top {ntop} components')
cb.ax.invert_yaxis()
ax.set_facecolor(bgcolor)
ax.sharex(ax1)
ax.sharey(ax1)
ax3,im3,cb3=ax,im,cb

gsc=gs[1, 1]    
normfunc=matplotlib.colors.LogNorm
norm=normfunc(**vlimdict)
ax = fig.add_subplot(gsc)
im,cb=specim(tsp,fsp/1e6,zerotonan(gain),xlabel='time [sec]',ylabel='freq [MHz]',cmap=cmstd,norm=norm,**kwextra)
title('gain')
ax.set_facecolor(bgcolor)
ax.sharex(ax1)
ax.sharey(ax1)
ax4,im4,cb4=ax,im,cb
  

def _():
    gsc=gs[1, 1]    
    norm=None
    cmap=cmstd.reversed()
    ax = fig.add_subplot(gsc)
    im,cb=specim(tsp,fsp/1e6,zerotonan(mxgnndslabeltop),xlabel='time [sec]',ylabel='freq [MHz]',cmap=cmap,norm=norm,**kwextra)
    title(f'top {ntop} max nodes')
    ax.set_facecolor(bgcolor)
    ax.sharex(ax1)
    ax.sharey(ax1)
    ax4,im4,cb4=ax,im,cb
    

def _():
    gsc=gs[1, 1]    
    norm=None
    cmap=cmstd.reversed()
    ax = fig.add_subplot(gsc)
    im,cb4=specim(tsp,fsp/1e6,mxgnnds,xlabel='time [sec]',ylabel='freq [MHz]',cmap=cmap,norm=norm,**kwextra)
    title('all max nodes')
    ax.set_facecolor(bgcolor)
    ax.sharex(ax1)
    ax.sharey(ax1)
    ax4,im4,cb4=ax,im,cb