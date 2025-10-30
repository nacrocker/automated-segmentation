#speed tests of alternative implementations of maxattrnodes
def maxattrnodes(self,attr,allchildren=True):
    """Find nodes which are local maxima of attr value along lineage. A maximum passes two tests:
    First test is: attr.ravel()[parent]< attr.ravel()[node].
    For anychild == True, second test is attr.ravel()[node] >= attr.ravel[child] for any child.
    For anychild == False, second test is attr.ravel()[node] >= attr.ravel[child] for all children."""
    S=self.S
    P_rav=self.P.ravel()
    attr_rav=attr.ravel()
    maxattrnodes=np.zeros(self.image.shape,dtype=bool)
    maxattrnodes_rav = maxattrnodes.ravel()

    ##Vectorized, faster code than for-loops below:
    maxattrnodes_rav[:] = attr_rav[P_rav] < attr_rav
    if allchildren:
        np.logical_and.at(maxattrnodes_rav,P_rav,attr_rav[P_rav]>=attr_rav)
    else:
        np.logical_or.at(maxattrnodes_rav,P_rav,attr_rav[P_rav]>=attr_rav)
    return maxattrnodes

    ##Equivalent to, but slower than, vecotrized code above:
    #for p in S[1:]:
    #    q = P_rav[p]
    #    maxattrnodes_rav[p] = attr_rav[q] < attr_rav[p]
    #
    #if allchildren:
    #    for p in S[1:]:
    #        q = P_rav[p]
    #        maxattrnodes_rav[q] = maxattrnodes_rav[q] and attr_rav[q] >= attr_rav[p]
    #else:
    #    for p in S[1:]:
    #        q = P_rav[p]
    #        maxattrnodes_rav[q] = maxattrnodes_rav[q] or attr_rav[q] >= attr_rav[p]
    #return maxattrnodes


#maxattrnodes_forloop gives identical output to maxattrnodes, but much slower
def maxattrnodes_forloop(self,attr,allchildren=True):
    """Find nodes which are local maxima of attr value along lineage. A maximum passes two tests:
    First test is: attr.ravel()[parent]< attr.ravel()[node].
    For anychild == True, second test is attr.ravel()[node] >= attr.ravel[child] for any child.
    For anychild == False, second test is attr.ravel()[node] >= attr.ravel[child] for all children."""
    S=self.S
    P_rav=self.P.ravel()
    attr_rav=attr.ravel()
    maxattrnodes=np.zeros(self.image.shape,dtype=bool)
    maxattrnodes_rav = maxattrnodes.ravel()
    for p in S[1:]:
        q = P_rav[p]
        maxattrnodes_rav[p] = attr_rav[q] < attr_rav[p]

    if allchildren:
        for p in S[1:]:
            q = P_rav[p]
            maxattrnodes_rav[q] = maxattrnodes_rav[q] and attr_rav[q] >= attr_rav[p]
    else:
        for p in S[1:]:
            q = P_rav[p]
            maxattrnodes_rav[q] = maxattrnodes_rav[q] or attr_rav[q] >= attr_rav[p]
    return maxattrnodes



#class tmfun:
#    def __init__(self,fun,*params):
#        self.params = params
#        self.fun = fun
#    def __call__(self):
#        self.result=self.fun(*self.params)


rt=root # rt=OMFIT['ModeTimeDependence']

from OMFITlib_max_tree_class import max_tree as max_tree_cl
stftroot=rt['OUTPUTS'][130335]['bdot']['HF']['stft'][(0.43, 0.53)]
stftarr=np.stack([stftroot[i] for i in np.sort([k for k in stftroot.keys() if isinstance(k,int)])],axis=2)

#sp=abs(stftroot[0])**2
sp=np.mean(abs(stftarr)**2,axis=2)
fsp=stftroot['freq']
tsp=stftroot['time']

spmxtr=max_tree_cl(sp,connectivity=2)
self=spmxtr

signaltonoise=self.volume/(self.area*self.image)
#signaltonoise=self.volume/(self.area*self.peak)
avspecdens=self.volume/self.area*self.extents[...,1]
#avspecdens=self.volume/self.area


#gain=signaltonoise.copy()
gain=avspecdens.copy()


from OMFITlib_utils import tmfun



tm_mx = tmfun(maxattrnodes,self,gain)
tm_mx_forloop = tmfun(maxattrnodes_forloop,self,gain)
tm_mx_objmeth = tmfun(self.maxattrnodes,gain)


import timeit

print(timeit.timeit(tm_mx_forloop,number=1))
mxgnnds_all_forloop = tm_mx_forloop.result
print(timeit.timeit(tm_mx,number=1))
mxgnnds_all = tm_mx.result
print(timeit.timeit(tm_mx_objmeth,number=1))
mxgnnds_all_objmeth = tm_mx_objmeth.result
print(np.all(mxgnnds_all==mxgnnds_all_forloop))
print(np.all(mxgnnds_all==mxgnnds_all_objmeth))
