#y0=log10(imgrav)
#y0=imgdynrng
#y0=varaccum.ravel()
#y0=wghtvaraccum.ravel()
y0=jstatsperindex['av'].ravel()
#y0=jstatsperindex['var'].ravel()
#y0=jstatsperindex['wght'].ravel()
#y0=imgarea
#y0=log10(image.ravel())

iS=argsort(S)
x0=iS
#x0=log10(image.ravel())
#x0=imgarea

x1=x0[S]
y1=y0[S]

x2=x0[P.ravel()[S]]
y2=y0[P.ravel()[S]]




figure()
plot(x1,y1,'.b')
#plot(stack([x1,x2],axis=1).T,stack([y1,y2],axis=1).T,'b')
#xlim((-10,0))