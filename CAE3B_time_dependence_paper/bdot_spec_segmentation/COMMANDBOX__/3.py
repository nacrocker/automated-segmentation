#copied to OMFITlib_math_utils
def HighestDensityInterval(x,a=0.6827):
    xs=np.sort(np.asarray(x).flatten())
    a = np.amin([np.amax([a,0]),1])
    nxs=len(xs)
    nHDI=np.amax([1,np.rint(nxs*a).astype(int)])
    print(nHDI,nxs)
    iHDI=np.argmin(xs[nHDI:]-xs[0:-nHDI])
    return (xs[iHDI],xs[iHDI+nHDI-1]),(iHDI,iHDI+nHDI-1,xs)

xHDI,iHDI=HighestDensityInterval(np.log10(xsp_to_plot.data),.95)
vlim,ilim=HighestDensityInterval(xsp_to_plot.data,.95)
print(*xHDI,*iHDI_[0:2],*np.log10(vlim),*ilim[0:2])
xsl=sort(np.log10(xsp_to_plot.data))
xls=np.log10(sort(xsp_to_plot.data))
print(np.amax(xsl-xls))
