#should all be copied to OMFITlib_max_tree_utils, and now some may be out of date
def calculate_area(image,P,S):
    area=np.ones(image.size,dtype=np.int)
    P_rav=P.ravel()
    for p in S[:0:-1]:
        pp=P_rav[p]
        area[pp]=area[pp]+area[p]
    return area

def calculate_volume(image,P,S):
    image_rav=image.ravel()
    vol=image_rav.copy()
    P_rav=P.ravel()
    for p in S[:0:-1]:
        pp=P_rav[p]
        vol[pp]=vol[pp]+vol[p]
    return vol

def calculate_height(image,P,S):
    image_rav=image.ravel()
    height=np.zeros(image.size,dtype=np.float64)
    P_rav=P.ravel()
    for p in S[:0:-1]:
        pp=P_rav[p]
        height[pp]=maximum(height[pp],height[p]+image_rav[p]-image_rav[pp])
    return height


def propagate_max_to_leaves(val,P,S):
    P_rav=P.ravel()
    mxval=val.copy()
    mxval_rav=mxval.ravel()
    for p in S[1:]:
        pp=P_rav[p]
        if mxval_rav[pp] > mxval_rav[p]: mxval_rav[p] = mxval_rav[pp]
    return mxval         

#old and broken 
def calculate_moment_along_axis(P,S,Pa=None,axis=0,order=1,weight=None):
    if weight is None: weight=np.ones(P.shape)
    weight_rav=weight.ravel()
    ij=np.unravel_index(np.arange(S.size),P.shape)
    ii=ij[axis]
    jj=ij[1-axis]*1.0
    if Pa is None: Pa=parent_tree_along_axis(P,S,axis=axis)
    Pa_rav=Pa.ravel()
    isum=(jj**order)*weight_rav
    iwght=weight_rav.copy()
    for ip,p in enumerate(S[:0:-1]):
        ppa=Pa_rav[p]
        if ppa != p:
            iwght[ppa]=iwght[ppa]+iwght[p]
            isum[ppa]=isum[ppa]+isum[p]
    iav=isum/iwght
    return iav.reshape(P.shape),iwght.reshape(P.shape),Pa
    
#old and broken 
def calculate_moment_along_axis_alt(P,S,Pa=None,axis=0,order=1,weight=None):
    if weight is None: weight=np.ones(P.shape)
    weight_rav=weight.ravel()
    ij=np.unravel_index(np.arange(S.size),P.shape)
    ii=ij[axis]
    jj=ij[1-axis]*1.0
    if Pa is None: Pa=parent_tree_along_axis(P,S,axis=axis)
    Pa_rav=Pa.ravel()
    iav=(jj**order)
    iwght=weight_rav.copy()
    for ip,p in enumerate(S[:0:-1]):
        ppa=Pa_rav[p]
        if ppa != p:
            iav[ppa]=(iav[ppa]*iwght[ppa]+iav[p]*iwght[p])
            iwght[ppa]=iwght[ppa]+iwght[p]
            iav[ppa]/=iwght[ppa]
    return iav.reshape(P.shape),iwght.reshape(P.shape),Pa

#copied to OMFITlib_max_tree_utils
def accumulate_on_tree(value,P,S):
    value_rav=image.ravel()
    accum=value_rav.copy()
    P_rav=P.ravel()
    for p in S[:0:-1]:
        pp=P_rav[p]
        accum[pp]=accum[p]+accum[p]
    return accum.reshape(P.shape)

#old and broken 
def calculate_average_component_variance_along_axis(P,S,Pa=None,axis=0,weight=None):
    if weight is None: weight=np.ones(P.shape)
    weight_rav=weight.ravel()
    ij=np.unravel_index(np.arange(S.size),P.shape)
    ii=ij[axis]
    jj=ij[1-axis]*1.0
    if Pa is None: Pa=parent_tree_along_axis(P,S,axis=axis)
    iav,iwght,_=calculate_moment_along_axis(P,S,Pa=Pa,axis=axis,weight=weight)
    iav=accumulate_on_tree(((jj-iav.ravel())**2).reshape(P.shape)*weight,P,S)
    iav=iav/iwght
    return iav