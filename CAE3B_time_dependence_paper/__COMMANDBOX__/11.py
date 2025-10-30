rt=root # rt=OMFIT['ModeTimeDependence']
from OMFITlib_max_tree_class import max_tree as max_tree_cl
from OMFITlib_plot_utils import specim
sproot=rt['OUTPUTS']['synth1']['sp']

sp=sproot['sp']
fsp=sproot['freq']
tsp=sproot['time']

spmxtr=max_tree_cl(sp)
self=spmxtr

from OMFITlib_plot_utils import subplot_adder

fig=figure(layout='tight')
#fig=figure(layout='constrained')
sbadder=subplot_adder(fig=fig,horizontal=False)

print(1)
ax=sbadder.add_new_subplot()
_,cb=specim(fsp,tsp,self.area)
cb.remove()
title('area')

print(2)
ax=sbadder.add_new_subplot()
_,cb=specim(fsp,tsp,self.area/self.extents[...,1])
cb.remove()
title('average vertical extent')

print(3)
ax=sbadder.add_new_subplot()
_,cb=specim(fsp,tsp,self.extents[...,1])
cb.remove()
title('horizontal extent')

for ax in sbadder.axes:
    plt.sca(ax)
    plt.colorbar()#use_gridspec=True)