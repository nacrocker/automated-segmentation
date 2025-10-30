from OMFITlib_max_tree_utils import interval_timer
from OMFITlib_max_tree_utils import parent_tree_along_axis
import numpy as np
from skimage.morphology import max_tree
xsp_to_anal=xsp.sel(dict(time=slice(0.100,.35),freq=slice(0,.2e6)))

image=np.array(xsp_to_anal)
P, S = max_tree(image, connectivity=1)
image_rav=image.ravel()
P_rav=P.ravel()

R=np.array(S.size)
PS=P_rav[S]
imPS=image_rav[PS]
iSRTimPS=np.argsort(imPS,kind='stable')
links=np.core.records.fromarrays([PS[iSRTimPS],S[iSRTimPS]], names='parent,child')


figure()
plot(image_rav[links.parent],image_rav[links.child]-image_rav[links.parent],'.')