rt=root # rt=OMFIT['ModeTimeDependence']
from OMFITlib_max_tree_class import max_tree as max_tree_cl
from OMFITlib_plot_utils import specim
sproot=rt['OUTPUTS']['synth1']['sp']

sp=sproot['sp']
fsp=sproot['freq']
tsp=sproot['time']

spmxtr=max_tree_cl(sp)
self=spmxtr


fig=figure(layout='tight')
#fig=figure(layout='constrained')

ax=subplot(3,1,1)
_,cb=specim(fsp,tsp,self.area)
title('area')
print(ax,cb.ax,ax.get_subplotspec().get_topmost_subplotspec(),cb.ax.get_subplotspec().get_topmost_subplotspec())

ax=subplot(3,1,2)
_,cb=specim(fsp,tsp,self.area/self.extents[...,1])
title('average vertical extent')
print(ax,cb.ax,ax.get_subplotspec().get_topmost_subplotspec(),cb.ax.get_subplotspec().get_topmost_subplotspec())

ax=subplot(3,1,3)
_,cb=specim(fsp,tsp,self.extents[...,1])
title('horizontal extent')
print(ax,cb.ax,ax.get_subplotspec().get_topmost_subplotspec(),cb.ax.get_subplotspec().get_topmost_subplotspec())

#plt.tight_layout()
#fig.set_constrained_layout(True)