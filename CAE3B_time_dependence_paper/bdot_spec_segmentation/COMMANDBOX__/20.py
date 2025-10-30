from OMFITlib_max_tree_utils import interval_timer
from OMFITlib_max_tree_utils import parent_tree_along_axis
from OMFITlib_max_tree_utils import calculate_area
from OMFITlib_max_tree_utils import calculate_index_moment_along_axis

import numpy as np
from skimage.morphology import max_tree
xsp_to_anal=xsp.sel(dict(time=slice(0.100,.35),freq=slice(0,.2e6)))

image=np.array(xsp_to_anal)
P, S = max_tree(image, connectivity=1)
image_rav=image.ravel()
P_rav=P.ravel()


#imgarea = calculate_area(image,P,S)
#Pa=parent_tree_along_axis(P,S,axis=axis)


#old and broken 
def calculate_index_variance_along_axis(P,S,Pa=None,axis=0,weight=None):
    if weight is None: weight=np.ones(P.shape)
    weight_rav=weight.ravel()
    ij=np.unravel_index(np.arange(S.size),P.shape)
    ii=ij[axis]
    jj=ij[1-axis]*1.0
    if Pa is None: Pa=parent_tree_along_axis(P,S,axis=axis)
    jav_unrav,jwght0_unrav,_=calculate_index_moment_along_axis(P,S,Pa=Pa,axis=axis,weight=weight)
    jav=jav_unrav.ravel()
    jwght0=jwght0_unrav.ravel()
    Pa_rav=Pa.ravel()
    jvsum=(jj**2 - jav)*weight_rav
    jwght=weight_rav.copy()
    #for ip,p in enumerate(S[:0:-1]):
    for p in S[:0:-1]:
        ppa=Pa_rav[p]
        if ppa != p:
            if jwght[p] != jwght0[p]: print('unmatached weigth at p: ',p)
            jvsum[ppa]+=jvsum[p] - jwght[p]*(jav[ppa]-jav[p])**2
            jwght[ppa]+=jwght[p]
    jvar=jvsum/jwght
    return jvar.reshape(P.shape),jav_unrav,jwght.reshape(P.shape),Pa

#old and broken 
def accumulate_values_calculated_along_axis(value_along_axis,P,S,Pa=None,weight=None):
    if weight is None: weight=np.ones(P.shape)
    value_rav=value_along_axis.ravel()
    wghtaccum=weight.ravel().copy()
    accum=value_rav*wghtaccum
    if Pa is None: Pa=parent_tree_along_axis(P,S,axis=axis)
    P_rav=P.ravel()
    Pa_rav=Pa.ravel()
    for p in S[:0:-1]:
        pp=P_rav[p]
        accum[pp]+=accum[p]
        wghtaccum[pp]+=wghtaccum[p]
        ppa=Pa_rav[p]
        if ppa != p: 
            accum[ppa]-=accum[p]
            wghtaccum[ppa]-=wghtaccum[p]
    accum/=wghtaccum
    return accum.reshape(P.shape),wghtaccum.reshape(P.shape),Pa

#old and broken 
def calculate_average_component_index_variance_along_axis(P,S,Pa=None,axis=0,weight=None):
    if weight is None: weight=np.ones(P.shape)
    weight_rav=weight.ravel()
    ij=np.unravel_index(np.arange(S.size),P.shape)
    ii=ij[axis]
    jj=ij[1-axis]*1.0
    if Pa is None: Pa=parent_tree_along_axis(P,S,axis=axis)
    jvar,jav,jwght,_=calculate_index_variance_along_axis(P,S,Pa=Pa,axis=axis,weight=weight)
    accum,wghtaccum,_=accumulate_values_calculated_along_axis(jvar,P,S,Pa=Pa,weight=jwght)
    return accum,wghtaccum,dict(var=jvar,av=jav,wght=jwght),Pa

weight=image
axis=1
inttm=interval_timer()
Pa=parent_tree_along_axis(P,S,axis=axis)
print('timer_dt',inttm.delta_time())
varaccum,wghtvaraccum,jstatsalongaxis,_=calculate_average_component_index_variance_along_axis(P,S,Pa=Pa,axis=axis,weight=image)
print('timer_dt',inttm.delta_time())



#ws=sum(w)
#ws1=sum(w[:i])
#ws2=sum(w[i:])
#xa=sum(w*x)/ws
#xa1=sum(w[:i]*x[:i])/ws1
#xa2=sum(w[i:]*x[i:])/ws2
#xv=sum(w*(x-xa)**2)/ws
#xv1=sum(w[:i]*(x[:i]-xa1)**2)/ws1
#xv2=sum(w[i:]*(x[i:]-xa2)**2)/ws2

#xa==sum(w[i:]*x[i:] + w[:i]*x[:i])/ws = xav1*ws1/ws + xav2*ws2/ws

#xv==sum(w[:i]*((x[i:]-xa1)**2 + 2*(x[i:]-xa1)*(xa1-xa) + (xa1-xa)**2) +
#        w[i:]*((x[i:]-xa2)**2 + 2*(x[i:]-xa2)*(xa2-xa) + (xa2-xa)**2))/ws
#xv==sum(w[:i]*(x[i:]-xa1)**2)/ws + (xa1-xa)**2*ws1/ws +
#    sum(w[i:]*(x[i:]-xa2)**2)/ws + (xa2-xa)**2*ws2/ws
#xv==(xv1 + (xa1-xa)**2)*ws1/ws + (xv2 + (xa2-xa)**2)*ws2/ws

#xv == sum(w*(x-xav)**2)/ws == sum(w*(x-x0)**2+2*(x-x0)*(x0-xa)+(x0-ax)**2))/ws
#xv == sum(w*(x-x0)**2))/ws - (x0-xa)**2

#sum(w*(x-x0)**2)/ws == sum(w*(x-x1)**2+2*(x-x1)*(x1-x0)+(x1-x0)**2))/ws
#                    == sum(w*(x-x1)**2)/ws + 2*(xa-x1)*(x1-x0) + (x1-x0)**2
#                    == sum(w*(x-x1)**2)/ws + (2*xa-(x1+x0))*(x1-x0)
#                    == sum(w*(x-x1)**2)/ws + 2*xa*(x1-x0) + x0**2 - x1**2
#                    == sum(w*(x-x1)**2)/ws + (2*xa-x1)*x1 - (2*xa-x0)
#                    == sum(w*(x-x1)**2)/ws - (xa-x1)**2 + (xa-x0)**2