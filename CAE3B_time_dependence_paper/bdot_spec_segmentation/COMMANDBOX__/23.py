#old and broken calculate_index_moment_along_axis
def calculate_index_moment_along_axis(P,S,Pa=None,axis=0,order=1,weight=None):
    if weight is None: weight=np.ones(P.shape)
    weight_rav=weight.ravel()
    ij=np.unravel_index(np.arange(S.size),P.shape)
    ii=ij[axis]
    jj=ij[1-axis]*1.0
    if Pa is None: Pa=parent_tree_along_axis(P,S,axis=axis)
    Pa_rav=Pa.ravel()
    jsum=(jj**order)*weight_rav
    jwght=weight_rav.copy()
    #for ip,p in enumerate(S[:0:-1]):
    for p in S[:0:-1]:
        ppa=Pa_rav[p]
        if ppa != p:
            jwght[ppa]+=jwght[p]
            jsum[ppa]+=jsum[p]
    jav=jsum/jwght
    return jav.reshape(P.shape),jwght.reshape(P.shape),Pa

av,wght,_=calculate_index_moment_along_axis(P,S,axis=axis,weight=image)
imP=image.ravel()[P].reshape(image.shape)
iscanon=(image==imP) & (P != np.arange(P.size).reshape(P.shape))
#print(av[np.nonzero(image==imP) & (P != np.arange(P.size).reshape(P.shape))])
print(av[np.nonzero(iscanon)])