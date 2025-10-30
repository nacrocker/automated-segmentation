
import numpy as np

def peaks(nx=11,ny=11,npeaks=1,cents=None,widths=None,heights=None,aspects=None,angles=None,return_parameters=False):
    rndgen = np.random.default_rng()
    if cents is None: cents=list(zip(nx*(rndgen.random(npeaks)-0.5)*0.75,ny*(rndgen.random(npeaks)-0.5)*0.75))
    if widths is None: widths = (rndgen.random(npeaks)+0.5)*np.minimum(nx,ny)/5/npeaks
    if heights is None: heights = (rndgen.random(npeaks)+0.25)/1.25
    if aspects is None: aspects = rndgen.random(npeaks)+1.5
    if angles is None: angles = (rndgen.random(npeaks)-0.5)*np.pi/2

    X,Y=np.meshgrid(np.arange(nx)-(nx-1)/2,np.arange(ny)-(ny-1)/2,sparse=True,indexing='xy')
    pks=np.zeros((nx,ny))
    for c,w,h,asp,ang in zip(cents,widths,heights,aspects,angles):
        Xp,Yp=np.cos(ang)*X+np.sin(ang)*Y,-np.sin(ang)*X+np.cos(ang)*Y
        pks+=np.exp(-(((Xp-c[0])/sqrt(asp))**2+((Yp-c[1])*sqrt(asp))**2)/w**2)
    ret=(pks,X,Y)
    if return_parameters: ret=ret+(dict(nx=nx,ny=ny,npeaks=npeaks,cents=cents,widths=widths,heights=heights,aspects=aspects,angles=angles),)
    return ret


def HighestDensityInterval(x,a=0.6827):
    xs=np.sort(np.asarray(x).flatten())
    a = np.amin([np.amax([a,0]),1])
    nxs=len(xs)
    nHDI=np.amax([1,np.rint(nxs*a).astype(int)])
    iHDI=np.argmin(xs[nHDI:]-xs[0:-nHDI])
    return np.array([xs[iHDI],xs[iHDI+nHDI-1]]),np.array([iHDI,iHDI+nHDI-1])

def safe_divide(a,b):
    a,b=np.broadcast_arrays(a,b)
    return np.divide(a, b, out=np.zeros(b.shape,dtype=np.result_type(a,b,1.0)), where=b!=0)


import numpy as np
#mimic "HN" bdot array on NSTX with comparable but made up paramenters.  Still need to look up actual paremeters.

def view_complex_as_float(arr):
    """Convert complex array arr to floating array. Shape of output will be arr.shape+(2,),
    with last dimension spanning real and imaginary parts."""
    import numpy as np
    arr=np.ascontiguousarray(arr)
    ftype = arr[...,0].real.dtype
    return arr.view(dtype=ftype).reshape(arr.shape+(2,))

def view_float_as_complex(arr):
    """Convert floating array arr to complex array. arr must have arr.shape[-1] = 2,
    with last dimension spanning real and imaginary parts. Shape of output will
    be arr.shape[:-1]."""
    import numpy as np
    arr=np.ascontiguousarray(arr)
    if arr.shape[-1] != 2: raise ValueError("arr must be array with shape[-1] == 2")
    ctype=(arr[...,0]+1j*arr[...,1]).dtype
    return arr.view(dtype=ctype).reshape(arr.shape[:-1])

def complex_multivariate_normal_noise(mean=None,cov=None,size=None,nvars=None):
    import numpy as np
    from scipy.linalg import block_diag

    if not nvars is None:
        if not (np.isscalar(nvars) and isinstance(nvars, (int, np.integer)) and nvars > 0): raise ValueError("if supplied, nvars must be integer > 0")
    elif not mean is None and not np.iscalar(mean):
        nvars = len(mean)
    elif not cov is None and not np.isscalar(cov):
        nvars = len(cov)
    else:
        nvars = 1

    if mean is None:
        mean = np.zeros((nvars,))
    elif np.isscalar(mean):
        mean = np.full((nvars,),mean)
    else:
        mean = np.array(mean)

    if cov is None:
        cov = np.eye(nvars)
    elif np.isscalar(cov):
        cov = np.diag(np.full((nvars,),cov))
    else:
        cov = np.array(cov)

    if (np.issubdtype(mean.dtype, np.complexfloating) or
            np.issubdtype(cov.dtype, np.complexfloating)):
        raise TypeError("mean and cov must not be complex")

    if size is None:
        shape = []
    elif np.isscalar(size) and isinstance(size, (int, np.integer)):
        shape = [size]
    else:
        shape = size

    if len(mean.shape) != 1:
        raise ValueError("mean must be 1 dimensional")
    if (len(cov.shape) != 2) or (cov.shape[0] != cov.shape[1]):
        raise ValueError("cov must be 2 dimensional and square")
    if mean.shape[0] != cov.shape[0]:
        print(mean.shape,cov.shape)
        raise ValueError("mean and cov must have same length")

    randnumgen = np.random.default_rng()
    nvars=len(mean)


    return view_float_as_complex(randnumgen.multivariate_normal(np.hstack((mean,mean)), 0.5*block_diag(cov,cov), shape).reshape(shape+(nvars,2)))

def mode_with_random_phase(modenum,locsrad,areas=None,size=None):
    import numpy as np
    randnumgen = np.random.default_rng()

    if areas is None:
        areas = np.ones(len(locsrad))

    if len(locsrad.shape) != 1:
        raise ValueError("locsrad must be 1 dimensional")
    if len(areas.shape) != 1:
        raise ValueError("areas must be 1 dimensional")
    if locsrad.shape[0] != areas.shape[0]:
        raise ValueError("locsrad and areas must have same length")

    if size is None:
        shape = []
    elif np.isscalar(size) and isinstance(size, (int, np.integer)):
        shape = [size]
    else:
        shape = size

    modephase = randnumgen.uniform(low=0, high=2*np.pi, size=shape+(1,))
    return np.expand_dims(np.exp(1j*modenum*locsrad)*areas,axis=(0,1))*np.exp(1j*modephase)

def blackman_vs_tau(tau):
    """Blackman window vs normalized time (0 <= tau <= 1)
       This gives numpy.blackman(M) == blackman_vs_tau(taus) for taus = (numpy.arange(1-M, M, 2)/(M-1)/2) + 0.5
    """
    return 0.42 + 0.5*cos(2*np.pi*(tau-0.5)) + 0.08*cos(4*np.pi*(tau-0.5)) #0 <= tau <= 1

def taus_for_Mpoint_blackman(M):
    """taus array such that numpy.blackman(M) == blackman_vs_tau(taus)"""  
    return (np.arange(1-M, M, 2)/(M-1)/2) + 0.5


def allclosefortype(a,b,safety_factor=2.0):
    return np.allclose(a,b,1+np.finfo(b[0]).resolution*safety_factor,np.finfo(b[0]).resolution*safety_factor)
