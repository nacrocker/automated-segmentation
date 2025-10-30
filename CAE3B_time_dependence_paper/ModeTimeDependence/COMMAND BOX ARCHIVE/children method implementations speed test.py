#speed tests of alternative implementations of children
def children_slower(self):
    S = self.S
    P_rav = self.P.ravel()
    C = np.empty(self.image.shape,dtype=list)
    C_rav=C.ravel()
    C_rav[:]=[[] for _ in range(len(P_rav))]
    for p in S[1:]:
        q = P_rav[p]
        C_rav[q].append(p)
    return C 



def children(self):
    S = self.S
    P_rav = self.P.ravel()
    C_rav = [[] for _ in range(len(P_rav))]
    C = np.empty(self.image.shape,dtype=list)
    for p in S[1:]:
        q = P_rav[p]
        C_rav[q].append(p)
    C.ravel()[:]= C_rav[:]
    return C 


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


#C = children(self)


from OMFITlib_utils import tmfun



import timeit

tm_ch_slower = tmfun(children_slower,self)
print(timeit.timeit(tm_ch_slower,number=1))
Csl = tm_ch_slower.result
print(Csl[0:2,0:2])

tm_ch = tmfun(children,self)
print(timeit.timeit(tm_ch,number=1))
C = tm_ch.result
print(C[0:2,0:2])

print(np.all(Csl == C))
