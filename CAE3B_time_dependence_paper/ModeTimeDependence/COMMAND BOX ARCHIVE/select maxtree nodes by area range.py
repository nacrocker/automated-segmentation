rt=root # rt=OMFIT['ModeTimeDependence']

from OMFITlib_max_tree_class import max_tree as max_tree_cl
stftrt=rt['OUTPUTS'][130335]['bdot']['HN']['stft'][(0.43, 0.53)]
sp=abs(stftrt[0])**2
fsp=stftrt['freq']
tsp=stftrt['time']

spmxtr=max_tree_cl(sp)
self=spmxtr

from OMFITlib_plot_utils import cmapIDL_Standard_Gamma_II as cmapIDL_Standard_Gamma_II
from OMFITlib_plot_utils import specim as specim
cmstd=cmapIDL_Standard_Gamma_II()

vlimdict={}
kwextra={}
fig = plt.figure(figsize=(12,3),layout='constrained')
gs = GridSpec(1,3, figure=fig)
gsr = lambda ind: gs[np.unravel_index(ind,gs.get_geometry())]

ax1 = fig.add_subplot(gsr(0))
im1,cb1=specim(tsp,fsp/1e6,sp,xlabel='time [sec]',ylabel='freq [MHz]',norm=matplotlib.colors.LogNorm(**vlimdict),cmap=cmstd,**kwextra)
title('sp')

ax2 = fig.add_subplot(gsr(1), sharex=ax1, sharey=ax1)
im2,cb2=specim(tsp,fsp/1e6,self.area,xlabel='time [sec]',ylabel='freq [MHz]',norm=matplotlib.colors.LogNorm(**vlimdict),cmap=cmstd,**kwextra)
title('area')
ax2.sharex(ax1)
ax2.sharey(ax1)

areathresh=1000
areathreshwidth=4000
#spfilt=sp-spmxtr.direct_filter('area',areathresh)

spfilt=self.fill_components_from_markers((self.area < areathreshwidth+areathresh) & (self.area >= areathresh))*self.image
ax3 = fig.add_subplot(gsr(2), sharex=ax1, sharey=ax1)
im3,cb3=specim(tsp,fsp/1e6,spfilt,xlabel='time [sec]',ylabel='freq [MHz]',norm=matplotlib.colors.LogNorm(**vlimdict),cmap=cmstd,**kwextra)
title('spfilt')
ax3.sharex(ax1)
ax3.sharey(ax1)
