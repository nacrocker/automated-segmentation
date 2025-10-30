#speed tests of alternative implementations of optimummaxattrnodes
def optimummaxattrnodes_slow(self,attr,maxattrnodes=None):
    """Given a boolean matrix (maxattrnodes) where nodes with maximum attribute value are True, eliminate subomptimum maxima,
    which have any of these propterties:
    1) an descendent maximum with higher or equal value 
    2) an ancestor maximum with higher value that has no descendent maximum with even higher value        
    If maxattrnodes argument is None, then calculate it."""    
    image_rav=self.image.ravel()
    P_rav=self.P.ravel()
    if maxattrnodes is None: 
        maxattrnodes = self.maxattrnodes(attr)
    else:
        maxattrnodes = maxattrnodes.copy()
    attr_rav=attr.ravel()
    maxattrnodes_rav = maxattrnodes.ravel()
    maxattrndinds = np.flatnonzero(maxattrnodes_rav)
    maxattrndinds = maxattrndinds[np.argsort(attr_rav[maxattrndinds])]
    for p in maxattrndinds[::-1]:
        q = P_rav[p]
        if image_rav[q] == image_rav[p]: # only deal with canonical nodes. no effect if node is actually root.
            p = q 
            q = P_rav[p]
        if ~maxattrnodes_rav[p]: continue # this maximum was eliminated in previous iteration 
        pmax=p
        attrpmax=attr_rav[pmax]
        while q != p: # walk through ancestors to root
            #occluded_rav[q] = True # occlude all ancestors succeccfully reached. 
            p = q
            q = P_rav[p]
            if maxattrnodes_rav[p]: 
                #because outer loop scans through maxima in descending order, ...
                if attr_rav[p] <= attrpmax: 
                    #ancestor maximum with lower value would subsume maximum considered in current iteration of outerloop. 
                    #This is undesirable, so discard it and continue ancestor walk
                    maxattrnodes_rav[p] = False #eliminate lower ancestor
                else:
                    #any ancestor maximum with higher value should subsume maximum considered in current iteration of outerloop,
                    #so discard maximum considered in current iteration of outerloop. Since ancestor is higher, it was 
                    #considered in previous iteration and its ancestors have already been processed. Exit ancestor walk.
                    maxattrnodes_rav[pmax] = False # be eliminated by higher ancestor
                    break
    return maxattrnodes


def optimummaxattrnodes(self,attr,maxattrnodes=None):
    """Given a boolean matrix (maxattrnodes) where nodes with maximum attribute value are True, eliminate subomptimum maxima,
    which have any of these propterties:
    1) an descendent maximum with higher or equal value 
    2) an ancestor maximum with higher value that has no descendent maximum with even higher value        
    If maxattrnodes argument is None, then calculate it."""    

    from collections import deque

    image_rav=self.image.ravel()
    P_rav=self.P.ravel()
    if maxattrnodes is None: 
        maxattrnodes = self.maxattrnodes(attr)
    else:
        maxattrnodes = maxattrnodes.copy()
    attr_rav=attr.ravel()
    maxattrnodes_rav = maxattrnodes.ravel()
    maxattrndinds = np.flatnonzero(maxattrnodes_rav)
    maxattrndinds = maxattrndinds[np.argsort(attr_rav[maxattrndinds])]
    children = self.children
    children_rav=children.ravel()
    occluded_rav=np.zeros(P_rav.shape,dtype=bool)
    
    for p in maxattrndinds[::-1]:
        q = P_rav[p]
        if image_rav[q] == image_rav[p]: # only deal with canonical nodes. no effect if node is actually root.
            p,q = q,P_rav[p]
        if occluded_rav[p]: continue # this maximum was eliminated in previous iteration 
        pmax = p
        while not occluded_rav[q] and q != p: 
            occluded_rav[q] = True
            p = q
            q = P_rav[p]

        #childqueue=children_rav[p][:]
        childqueue=deque(children_rav[pmax])
        while childqueue:
            c = childqueue.popleft()
            occluded_rav[c] = True
            childqueue.extend(children_rav[c])

    maxattrnodes_rav[:]&=~occluded_rav 
     
    return maxattrnodes


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


#paths=[]
#gain=signaltonoise.copy()
gain=avspecdens.copy()
gain_rav=gain.ravel()

mxgnnds = self.maxattrnodes(gain)


from OMFITlib_utils import tmfun

import timeit


tm_op=tmfun(optimummaxattrnodes,self,gain,maxattrnodes=mxgnnds)
print('optimummaxattrnodes: ',timeit.timeit(tm_op,number=1))
mxgnnds_tm = tm_op.result

tm_op_slow=tmfun(optimummaxattrnodes_slow,self,gain,maxattrnodes=mxgnnds)
print('optimummaxattrnodes old and slow: ',timeit.timeit(tm_op_slow,number=1))
mxgnnds_tm_slow = tm_op_slow.result

print(np.count_nonzero(mxgnnds_tm_slow),np.count_nonzero(mxgnnds_tm))
print(np.array_equiv(mxgnnds_tm,mxgnnds_tm_slow))
