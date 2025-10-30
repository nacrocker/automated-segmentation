rt=root # rt=OMFIT['ModeTimeDependence']

from OMFITlib_sigarraycov_utils import Vec2Cov
from OMFITlib_max_tree_class import max_tree as max_tree_cl
#stftroot = rt['OUTPUTS'][130335]['bdot']['HF']['stft'][(0.43, 0.53)]
stftroot = rt['OUTPUTS'][130335]['bdot']['HN']['stft'][(0.43, 0.53)]
stftarr0 = np.stack([stftroot[i] for i in np.sort([k for k in stftroot.keys() if isinstance(k,int)])],axis=2)
nms=rt['OUTPUTS'][130335]['bdot']['HN']['stft'][(0.43, 0.53)]['bdotshortnames']
nmsexcl=['HN13']
inmsin = np.array([n not in nmsexcl for n in nms])
stftarr0=stftarr0[...,inmsin]
stftarr=stftarr0/np.sqrt(np.mean(np.abs(stftarr0)**2,axis=(0,1)))
stftcov=Vec2Cov(stftarr)

#sp=abs(stftroot[0])**2
sp=np.mean(abs(stftarr)**2,axis=2)
fsp=stftroot['freq']
tsp=stftroot['time']


spmxtr=max_tree_cl(sp)
self=spmxtr
#print('same result: ',np.array_equiv(self.area,self.accumulate_attribute_from_leaf_to_root(self.P*0+1)))

stftcovacc = self.accumulate_attribute_from_leaf_to_root(stftcov)


from numpy import linalg as LA
from scipy.sparse import linalg as LSA

import timeit
from OMFITlib_utils import tmfun


find_mxev_from_ev=lambda m: np.max(LA.eigvalsh(m),axis=-1)
find_mxev_from_norm = lambda m: LA.norm(m,ord=2,axis=(-2,-1))
find_mxev_from_evs = lambda m: np.stack([LSA.eigsh(m[i], k=1, which='LM', return_eigenvectors=False) for i in np.ndindex(m.shape[:-2])],axis=0).reshape(m.shape[:-2])

tm_mxev_from_ev = tmfun(find_mxev_from_ev,stftcovacc)
tm_mxev_from_evs = tmfun(find_mxev_from_evs,stftcovacc)
tm_mxev_from_norm = tmfun(find_mxev_from_norm,stftcovacc)

print('speed of max eigval from eig values: ',timeit.timeit(tm_mxev_from_ev,number=1))
print('speed of max eigval from sparse eig values: ',timeit.timeit(tm_mxev_from_evs,number=1))
print('speed of max eigval from norm: ',timeit.timeit(tm_mxev_from_norm,number=1))

print('same result eig values and norm: ',np.allclose(tm_mxev_from_ev.result,tm_mxev_from_norm.result))
print('same result sparse eig values and norm: ',np.allclose(tm_mxev_from_evs.result,tm_mxev_from_norm.result))
print('max normalized difference eig values and norm: ',np.max(np.abs(2*(tm_mxev_from_ev.result-tm_mxev_from_norm.result)/(tm_mxev_from_ev.result+tm_mxev_from_norm.result))))
print('max normalized difference sparse eig values and norm: ',np.max(np.abs(2*(tm_mxev_from_evs.result-tm_mxev_from_norm.result)/(tm_mxev_from_evs.result+tm_mxev_from_norm.result))))


if True:
    find_mnev_from_ev=lambda m: np.min(LA.eigvalsh(m),axis=-1)
    find_mnev_from_norm = lambda m: LA.norm(m,ord=-2,axis=(-2,-1))

    tm_mnev_from_ev = tmfun(find_mnev_from_ev,stftcovacc)
    tm_mnev_from_norm = tmfun(find_mnev_from_norm,stftcovacc)

    print('speed of min eigval from eig values: ',timeit.timeit(tm_mnev_from_ev,number=1))
    print('speed of min eigval from norm: ',timeit.timeit(tm_mnev_from_norm,number=1))

    rnorm_mnev_from_ev = tm_mnev_from_ev.result/tm_mxev_from_ev.result
    rnorm_mxev_from_ev = tm_mnev_from_norm.result/tm_mxev_from_norm.result

    print('same result: ',np.allclose(rnorm_mnev_from_ev,rnorm_mxev_from_ev,atol=1e-7))
    print('max normalized difference: ',np.max(np.abs(rnorm_mnev_from_ev-rnorm_mxev_from_ev)))

    figure()
    plot(rnorm_mnev_from_ev.ravel(),rnorm_mxev_from_ev.ravel(),'.')
