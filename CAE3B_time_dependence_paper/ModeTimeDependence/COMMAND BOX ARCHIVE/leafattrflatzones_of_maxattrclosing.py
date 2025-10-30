rt=root # rt=OMFIT['ModeTimeDependence']

from OMFITlib_max_tree_class import max_tree as max_tree_cl
stftrt=rt['OUTPUTS'][130335]['bdot']['HN']['stft'][(0.43, 0.53)]

sp=abs(stftrt[0])**2
fsp=stftrt['freq']
tsp=stftrt['time']

spmxtr=max_tree_cl(sp)
self=spmxtr

signaltonoise=self.volume/(self.area*self.height)
#signaltonoise=self.volume/(self.area*self.peak)
avspecdens=self.volume/self.area#*self.extents[...,1]

#paths=[]
#gain=signaltonoise.copy()
gain=avspecdens.copy()
gain_rav=gain.ravel()


maxgain=self.maxattrclosing(gain)
#quantthresh=.9
#mxgnthresh = np.quantile(maxgain.ravel()[self.leaves],quantthresh)
#mxgnthresh=np.amax(maxgain)
ntop=100
mxgnthresh = np.unique(maxgain.ravel()[self.leaf_P_indices])[-ntop]
#mxgnthresh=2
#mxgnmarkers = np.where(maxgain >= mxgnthresh,1,0)
#markermask=self.fill_components_from_markers(mxgnmarkers)
markermask = self.leafattrflatzones(maxgain,mxgnthresh)
print(np.sum(markermask))

from OMFITlib_plot_utils import cmapIDL_Standard_Gamma_II as cmapIDL_Standard_Gamma_II
from OMFITlib_plot_utils import specim as specim
cmstd=cmapIDL_Standard_Gamma_II()
#cmap=cmstd
cmap=None

fig = plt.figure(figsize=(18,4.5),layout='constrained')
gs = GridSpec(1,3, figure=fig)
gsr = lambda ind: gs[np.unravel_index(ind,gs.get_geometry())]

kwextra={}
vlimdict={}
normfunc=matplotlib.colors.LogNorm
norm=normfunc(**vlimdict)
ax1 = fig.add_subplot(gsr(0))
im1,cb1=specim(tsp,fsp/1e6,sp,xlabel='time [sec]',ylabel='freq [MHz]',cmap=cmstd,norm=norm,**kwextra)
title('sp')

ax2 = fig.add_subplot(gsr(1))
im2,cb2=specim(tsp,fsp/1e6,markermask,xlabel='time [sec]',ylabel='freq [MHz]',cmap=cmap,norm=normfunc(**vlimdict),**kwextra)
title('markermask')
ax2.sharex(ax1)
ax2.sharey(ax1)

ax3 = fig.add_subplot(gsr(2))
im3,cb3=specim(tsp,fsp/1e6,gain,xlabel='time [sec]',ylabel='freq [MHz]',cmap=cmap,norm=normfunc(**vlimdict),**kwextra)
title('gain')
ax3.sharex(ax1)
ax3.sharey(ax1)
