rt=root # rt=OMFIT['ModeTimeDependence']

from OMFITlib_utils import assigntoarr as asgn
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


#paths=[]
#gain=signaltonoise.copy()
gain=avspecdens.copy()
gain_rav=gain.ravel()


maxgain,maxgain_nodes=self.maxattrclosing(gain,return_nodes=True)

ntop=100
#mxgnthresh = np.unique(maxgain.ravel()[self.leaf_P_indices])[-ntop]
mxgnthresh = np.unique(maxgain[maxgain_nodes])[-ntop]


#mxgnnds = self.leafattrflatnodes(maxgain,mxgnthresh)
#mxgnnds = asgn(np.zeros(self.image.size),np.argsort(gain.ravel())[-ntop:],range(1,ntop+1)).reshape(self.image.shape)

#sort_masked = lambda arr,mask: np.sort(arr.ravel()[mask.ravel()])

argsort_masked = lambda arr,mask: np.nonzero(mask.ravel())[0][np.argsort(arr.ravel()[mask.ravel()])]
mxgnndinds = argsort_masked(maxgain,maxgain_nodes & (maxgain >= mxgnthresh))

#for a in [np.zeros(self.image.size),mxgnndinds]:#,np.arange(mxgnndinds)+1]:
#    print(a.dtype,a.shape)

mxgnnds = asgn(np.zeros(self.image.size),mxgnndinds,np.arange(len(mxgnndinds),0,-1)).reshape(self.image.shape)
mxgnndsfill = self.fill_components_from_markers(mxgnnds,preserve_nesting=True)
print(np.unique(mxgnndsfill))


#markermask = self.leafattrflatzones(maxgain,mxgnthresh)
#print(np.all(markermask==mxgnndsfill))
#print(np.sum(markermask != mxgnndsfill))
#print(np.histogram(markermask+2*mxgnndsfill,bins=4))
#print(np.any(self.image.ravel()[self.P[np.nonzero(mxgnndsfill & ~mxgnnds)]] != self.image[np.nonzero(mxgnndsfill & ~mxgnnds)]))
#print( np.sum(self.image.ravel()[self.P[markermask]] == self.image[markermask]))
#print( np.sum(self.image.ravel()[self.P[mxgnndsfill]] == self.image[mxgnndsfill]))

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

norm=None
cmap3=cmstd.reversed()
ax3 = fig.add_subplot(gs[0, 1])
im3,cb3=specim(tsp,fsp/1e6,zerotonan(mxgnndsfill),xlabel='time [sec]',ylabel='freq [MHz]',cmap=cmap3,norm=norm,**kwextra)
title('mxgnndsfill')
cb3.ax.invert_yaxis()
ax3.set_facecolor(bgcolor)
ax3.sharex(ax1)
ax3.sharey(ax1)

normfunc=matplotlib.colors.LogNorm
norm=normfunc(**vlimdict)
ax4 = fig.add_subplot(gs[1, 1])
im4,cb4=specim(tsp,fsp/1e6,gain,xlabel='time [sec]',ylabel='freq [MHz]',cmap=cmap,norm=norm,**kwextra)
title('gain')
ax4.sharex(ax1)
ax4.sharey(ax1)
