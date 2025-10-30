#functions for transorming between signal array and covariance matrix
def VecSqSum(X,sumaxis=-1):
    #axis gives sum axis. other axes used to make outer product
    import numpy as np
    return np.tensordot(np.conj(X),X,axes=(sumaxis,sumaxis))

def Vec2Cov(X,axis=-1):
    # make outer product of specified axis with itself to make "covariance"
    import numpy as np
    axis = X.ndim+axis if axis < 0 else axis
    return np.conj(np.expand_dims(X,axis+1))*np.expand_dims(X,axis)

#functions to convert between covariance matrix 2D and vector forms
def Cov2CovVec(Xc,axes=-1,newaxis=None):
    #axes specifies pair of "Cov" axes to convert to single "CovVec" axis.
    #newaxis specifies CovVec axis.  Defaults to lower of axes
    #if axes is scalar:
    #  if axes >=0:
    #    use (axes,axes+1)
    #  else:
    #    use (axis-1,axes)
    #else:
    #  should be 2 element tuple of axis values
    import numpy as np
    if np.isscalar(axes):
        if axes >=0:
            assert axes < (len(Xc.shape)-1), "axis too large for number of dimensions in Xc"
            axes=(axes,axes+1)
        else:
            assert len(Xc.shape) > 1, "Xc should be at least 2D"
            axes=(axes-1,axes)
    else:
        assert len(axes) == 2, "axes is not scalar, so should be 2-element tuple"
    assert Xc.shape[axes[0]] == Xc.shape[axes[1]], "axis %d and axis %d of Xc should have equal sizes"%axes
    axes=tuple(a if a >= 0 else Xc.ndim+a for a in axes)
    if not newaxis: newaxis=np.minimum(*axes)
    Xc = np.moveaxis(Xc,axes,(-2,-1))
    dimother=(*Xc.shape[0:-2],)
    itriu = np.ravel_multi_index(np.triu_indices(Xc.shape[-1], k=1),Xc.shape[-2:])
    idiag = np.ravel_multi_index(np.diag_indices(Xc.shape[-1]),Xc.shape[-2:])
    if Xc.ndim > 2:
        Xc=Xc.reshape((-1,Xc.shape[-1]**2))
    else:
        Xc=Xc.reshape((Xc.shape[-1]**2,))
    Xcv=np.concatenate([Xc[...,idiag].real,Xc[...,itriu].real,Xc[...,itriu].imag],axis=-1)
    if len(dimother) > 0:
        Xcv=Xcv.reshape((*dimother,-1))
    if newaxis != Xcv.ndim-1:
        Xcv=np.moveaxis(Xcv,-1,newaxis)
    return Xcv

def CovVec2Cov(Xcv,axis=-1):
    #axes specifies "CovVec" axis to be converted to 2 axes of Cov
    import numpy as np
    if axis < 0: axis = Xcv.ndim+axis
    n=np.sqrt(Xcv.shape[axis]).astype(int)
    assert n**2 == Xcv.shape[axis],"sqrt of length of Xcv axis %d should be integer"%(axis,)
    ntri=int(n*(n-1)/2)
    dimother=tuple(d for id,d in enumerate(Xcv.shape) if id != axis)
    Xcv = np.moveaxis(Xcv,axis,-1)
    Xc = np.empty((*dimother,n**2),dtype=complex)
    itriu = np.ravel_multi_index(np.triu_indices(n, k=1),(n,n))
    idiag = np.ravel_multi_index(np.diag_indices(n),(n,n))
    Xc[...,idiag] = Xcv[...,0:n]
    Xctriu=np.empty((*dimother,ntri),dtype=complex)
    Xctriu.real[...,:] = Xcv[...,n:(n+ntri)]
    Xctriu.imag[...,:] = Xcv[...,n+ntri:]
    Xc[...,itriu] = Xctriu
    Xc=np.reshape(Xc,(-1,n,n))
    Xc=np.conj(np.swapaxes(Xc,-1,-2))
    Xc=np.reshape(Xc,(-1,n**2))
    Xc[...,itriu] = Xctriu
    Xc=np.reshape(Xc,(*dimother,n,n))
    Xc = np.moveaxis(Xc,(-2,-1),(axis,axis+1))
    return Xc

#make sigstftarr from signal list
def sigstftarr_from_siglist(t,siglist,nfft=None,noverlap=None):
    from scipy.signal import stft
    fs=1/(t[1]-t[0])
    nt=len(t)
    if not nfft: nfft=np.ceil(np.sqrt(nt))
    if not noverlap: noverlap=int(nfft/2)
    sigstftlist=[]
    for sig in siglist:
        fstft, tstft, sigstft = stft(sig, fs, nperseg=nfft,noverlap=noverlap)
        sigstftlist.append(sigstft)
    nfstft=len(fstft)
    ntstft=len(tstft)
    sigstftarr=np.stack(sigstftlist,axis=0)
    return fstft, tstft, sigstftarr

#support routines for hierarchical signal structure clustering of sigstftarr
def sigstftarr_to_sigstftCovVec(sigstftarr,sigaxis=0):
    # sigaxis: axis of for iterating over signals
    # CovVec axis (i.e. signal axis or "feature" axis) will be last
    import numpy as np
    if sigaxis < 0: sigaxis = sigstftarr.ndims+sigaxis
    sigstftarr=np.moveaxis(sigstftarr,sigaxis,0)
    nsig=sigstftarr.shape[0]
    sigstftcovvec=Cov2CovVec(Vec2Cov(sigstftarr,axis=0),axes=0).reshape((nsig**2,-1)).T
    return sigstftcovvec# -*-Python-*-
