def Vec2Cov(X,axis=-1):
    # make outer product of specified axis with itself to make "covariance"
    import numpy as np
    axis = X.ndim+axis if axis < 0 else axis
    return np.conj(np.expand_dims(X,axis+1))*np.expand_dims(X,axis)

nvar=10
cov=np.eye(nvar)
mean = np.zeros(nvar)
nsamp=10000
randnumgen = np.random.default_rng()
x = randnumgen.multivariate_normal(mean, cov, (nsamp,))
xcov=Vec2Cov(x)
def effective_nuclear_rank(m,axis1=-2,axis2=-1):
    """Calculates effective nuclear rank for positive semidefinite hermitian matrix, 
    given by trace(m)**2/trace(m**2) == sum(eigenvalues(m))**2/sum(eigenvalues(m)**2)"""
    return np.sum(np.real(np.diagonal(m,axis1=axis1,axis2=axis2)),axis=-1)**2/np.sum(np.abs(m)**2,axis=(axis1,axis2))

xdim=effective_nuclear_rank(np.mean(xcov,axis=0))
print(xdim)
