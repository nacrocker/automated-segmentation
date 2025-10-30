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


from numpy import linalg as LA
from scipy.sparse import linalg as LSA

import timeit
from OMFITlib_utils import tmfun

stftcovav = np.mean(stftcov,axis=(0,1))


find_mxev_from_ev_1matrix=lambda m: np.max(LA.eigvalsh(m))
find_mxev_from_norm_1matrix = lambda m: LA.norm(m,ord=2)
find_mxev_from_evs_1matrix = lambda m: LSA.eigsh(m, k=1, which='LM', return_eigenvectors=False)

tm_mxev_from_ev_1matrix = tmfun(find_mxev_from_ev_1matrix,stftcovav)
tm_mxev_from_evs_1matrix = tmfun(find_mxev_from_evs_1matrix,stftcovav)
tm_mxev_from_norm_1matrix = tmfun(find_mxev_from_norm_1matrix,stftcovav)

numtrials=10000

print('speed of max eigval from eig values: ',timeit.timeit(tm_mxev_from_ev_1matrix,number=numtrials))
print('speed of max eigval from sparse eig values: ',timeit.timeit(tm_mxev_from_evs_1matrix,number=numtrials))
print('speed of max eigval from norm: ',timeit.timeit(tm_mxev_from_norm_1matrix,number=numtrials))

print('value of max eigval from eig values: ',tm_mxev_from_ev_1matrix.result)
print('value of max eigval from sparse eig values: ',tm_mxev_from_evs_1matrix.result)
print('value of max eigval from norm: ',tm_mxev_from_norm_1matrix.result)

#speed of max eigval from eig values:  0.4999935426749289
#speed of max eigval from sparse eig values:  8.090903957374394
#speed of max eigval from norm:  0.8600854617543519
#value of max eigval from eig values:  5.767431
#value of max eigval from sparse eig values:  [5.7674303]
#value of max eigval from norm:  5.767431
