rt=root # rt=OMFIT['ModeTimeDependence']

def min_eig(m):
    """Find the minimum eigenvalue of m and corresponding eigenvector."""
    #this doesn't work.  not sure why.

    if m.ndim < 2:
        raise ValueError('%d-dimensional array given. Array must be at least two-dimensional' % m.ndim)

    d0, d1 = m.shape[-2:]
    if d0 != d1:
        raise ValueError('Last 2 dimensions of the array must be square')

    if m.shape[-1] == 1:
        return m[...,-1,-1]

    A = m[...,:-1]
    b = m[...,-1]
    Atb = np.tensordot(np.conj(A),b,axes=((-2,),(-1,)))
    AtA = np.tensordot(np.conj(A),A,axes=((-2,),(-2,)))

    from numpy import linalg as LA
    x = LA.solve(AtA,Atb)
    oshape = [*x.shape]
    oshape[0] = 1
    x = np.append(x,np.ones(oshape),axis=-1)
    xnorm = LA.norm(x,axis=-1)
    mxnorm = LA.norm(np.tensordot(m,x,axes=((-1,),(-1,))))
    return mxnorm/xnorm,x/xnorm



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

stftcovav = np.mean(stftcov,axis=(0,1))
print(min_eig(stftcovav))
from numpy import linalg as LA
val,vec=LA.eigh(stftcovav)
imn = np.argmin(abs(val))
print(val[imn],vec[:,imn])
print(val[imn]/np.max(val))
