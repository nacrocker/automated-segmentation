#dead end.  See comments below: "the following sort of works..."
rt=root # rt=OMFIT['ModeTimeDependence']

from OMFITlib_max_tree_class import max_tree as max_tree_cl
stftroot=rt['OUTPUTS'][130335]['bdot']['HN']['stft'][(0.43, 0.53)]

sp=abs(stftroot[0])**2
fsp=stftroot['freq']
tsp=stftroot['time']

spmxtr=max_tree_cl(sp)
self=spmxtr


signaltonoise=self.volume/(self.area*self.image)
#signaltonoise=self.volume/(self.area*self.peak)
avspecdens=self.volume/self.area*self.extents[...,1]
#avspecdens=self.volume/self.area


#paths=[]
#gain=signaltonoise.copy()
gain=avspecdens.copy()
gain_rav=gain.ravel()

#the following sort of works. Prominent features are found, but many are lesser features are missing
maxgain=self.maxattrclosing(gain)
mxgnnds = self.leafattrflatnodes(maxgain)
mxgnndinds = np.flatnonzero(mxgnnds)
mxgnndinds = mxgnndinds[np.argsort(maxgain.ravel()[mxgnndinds])]

occluded = self.markancestors(mxgnndinds[::-1])

from OMFITlib_utils import assigntoarr as asgn, boolindices
disjoint=boolindices(self.image.shape,mxgnndinds,raveled_indices=True)
disjoint_orig=disjoint.copy()
disjoint &= self.canonicality & ~occluded
disjoint_rav = disjoint.ravel()

mxgnndindsorig = mxgnndinds
mxgnndsorig = mxgnnds

mxgnndinds = np.flatnonzero(disjoint_rav)
mxgnndinds = mxgnndinds[np.argsort(maxgain.ravel()[mxgnndinds])]

ntop=50
mxgnndindstop = mxgnndinds[-ntop:]
mxgnnds = asgn(np.zeros(self.image.shape),mxgnndindstop,range(1,ntop+1)).reshape(self.image.shape)
mxgnndsfill = self.fill_components_from_markers(mxgnnds)

from OMFITlib_plot_utils import cmapIDL_Standard_Gamma_II as cmapIDL_Standard_Gamma_II
from OMFITlib_plot_utils import specim as specim
cmstd=cmapIDL_Standard_Gamma_II()
cmap=cmstd
bgcolor = 'g'

fig = plt.figure(figsize=(12,9),layout='constrained')
gs = GridSpec(2,2, figure=fig)

kwextra={}
vlimdict={}
normfunc=matplotlib.colors.LogNorm
norm=normfunc(**vlimdict)
ax1 = fig.add_subplot(gs[0, 0])
im1,cb1=specim(tsp,fsp/1e6,sp,xlabel='time [sec]',ylabel='freq [MHz]',cmap=cmstd,norm=norm,**kwextra)
title('sp')

normfunc=matplotlib.colors.LogNorm
norm=normfunc(**vlimdict)
ax2 = fig.add_subplot(gs[1, 0])
im2,cb2=specim(tsp,fsp/1e6,maxgain,xlabel='time [sec]',ylabel='freq [MHz]',cmap=cmstd,norm=norm,**kwextra)
title('maxgain')
ax2.sharex(ax1)
ax2.sharey(ax1)

gsc=gs[0, 1]    
norm=None
cmap=cmstd.reversed()
ax = fig.add_subplot(gsc)
im,cb=specim(tsp,fsp/1e6,mxgnndsfill,xlabel='time [sec]',ylabel='freq [MHz]',cmap=cmap,norm=norm,**kwextra)
title('mxgnndsfill')
ax.sharex(ax1)
ax.sharey(ax1)
ax3,im3,cb3=ax,im,cb
  
def _(): #disabled code
    gsc=gs[0, 1]
    norm=None
    cmap=cmstd.reversed(gsc)
    ax = fig.add_subplot(gs)
    im,cb=specim(tsp,fsp/1e6,disjoint,xlabel='time [sec]',ylabel='freq [MHz]',cmap=cmap,norm=norm,**kwextra)
    title('disjoint')
    ax.set_facecolor(bgcolor)
    ax.sharex(ax1)
    ax.sharey(ax1)
    ax3,im3,cb3=ax,im,cb

gsc=gs[1, 1]    
norm=None
cmap=cmstd.reversed()
ax = fig.add_subplot(gsc)
im,cb=specim(tsp,fsp/1e6,~occluded,xlabel='time [sec]',ylabel='freq [MHz]',cmap=cmap,norm=norm,**kwextra)
title('~occluded')
ax.sharex(ax1)
ax.sharey(ax1)
ax4,im4,cb4=ax,im,cb


def _(): #disabled code
    gsc=gs[1, 1]    
    norm=None
    cmap=cmstd.reversed()
    ax = fig.add_subplot(gsc)
    im,cb4=specim(tsp,fsp/1e6,disjoint_orig,xlabel='time [sec]',ylabel='freq [MHz]',cmap=cmap,norm=norm,**kwextra)
    title('max nodes')
    ax.set_facecolor(bgcolor)
    ax.sharex(ax1)
    ax.sharey(ax1)
    ax4,im4,cb4=ax,im,cb
