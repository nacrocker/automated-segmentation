from OMFITlib_max_tree_utils import interval_timer
from OMFITlib_max_tree_utils import parent_tree_along_axis
import numpy as np
from skimage.morphology import max_tree
xsp_to_anal=xsp.sel(dict(time=slice(0.100,.35),freq=slice(0,.2e6)))

image=np.array(xsp_to_anal)
P, S = max_tree(image, connectivity=1)
image_rav=image.ravel()
P_rav=P.ravel()



from OMFITlib_max_tree_utils import calculate_moment_along_axis, calculate_moment_along_axis_alt
    
weight=image
axis=1
inttm=interval_timer()
Pa=parent_tree_along_axis(P,S,axis=axis)
print('timer_dt',inttm.delta_time())
avcum,weightcum,_=calculate_moment_along_axis(P,S,Pa,axis=1,weight=weight)
print('timer_dt',inttm.delta_time())
avcuma,weightcuma,_=calculate_moment_along_axis_alt(P,S,Pa,axis=1,weight=weight)
print('timer_dt',inttm.delta_time())

print(' ',avcum.ravel()[:5],'\n',weightcuma.ravel()[:5]*1e6,'\n',avcuma.ravel()[:5],'\n',weightcuma.ravel()[:5]*1e6)