from OMFITlib_plot_utils import imshowxy
from OMFITlib_math_utils import peaks


import scipy.sparse as sp
def calculate_index_moment_along_axis(P,S,axis=0,order=1,weight=None,jwght=None):
    P_rav=P.ravel()
    if weight is None: weight=np.ones(P.shape)
    weight_rav=weight.ravel()
    ij=np.unravel_index(np.arange(S.size),P.shape)
    ii=ij[axis]
    jj=ij[1-axis]*1.0
    ni=P.shape[axis]
    nj=P.shape[1-axis]
    iwnz=np.nonzero(weight_rav)[0]
    jav=sp.csr_array(((jj[iwnz]**order)*weight_rav[iwnz],(iwnz,ii[iwnz])),shape=(S.size,ni))
    dojwghtcalc=jwght is None
    if dojwghtcalc: jwght=sp.csr_array((weight_rav[iwnz],(iwnz,ii[iwnz])),shape=(S.size,ni))
    for p in S[:0:-1]:
        pp=P_rav[p]
        jav[[pp],:]+=jav[[p],:] # "[pp],:" required because "pp,:" fails since "1D sparse slices" are not yet implemented
        if dojwghtcalc: jwght[[pp],:]+=jwght[[p],:]
    jav=jav*((jwght*1.0).power(-1))
    return jav,jwght


def calculate_index_variance_along_axis(P,S,axis=0,weight=None):
    jav,jwght=calculate_index_moment_along_axis(P,S,axis=axis,order=1,weight=weight)
    jvar,_=calculate_index_moment_along_axis(P,S,axis=axis,order=2,weight=weight,jwght=jwght)
    jvar=jvar-jav.power(2)
    return jvar,jav,jwght

def calculate_average_component_index_variance_along_axis(P,S,axis=0,weight=None):
    jvar,jav,jwght=calculate_index_variance_along_axis(P,S,axis=axis,weight=weight)
    wght=jwght.sum(axis=1)
    var=(jvar*jwght).sum(axis=1)/wght
    return var,wght,dict(var=jvar,av=jav,wght=jwght)


nx,ny=31,31
npeaks=3
pksdesc0=dict(nx=nx,ny=ny,npeaks=npeaks,cents=[(0.0,0,0)],widths=[2],heights=[1.0],aspects=[2.0],angles=[.5])
#pksdesc=pksdesc0
genpksdesc=False
if genpksdesc: 
    pks,X,Y,pksdesc=peaks(nx=nx,ny=ny,npeaks=npeaks,return_parameters=True)
else:
    pks,X,Y,pksdesc=peaks(**pksdesc,return_parameters=True)

figure()
imshowxy(X,Y,pks)
image = pks

P, S = max_tree(image, connectivity=1)
image_rav=image.ravel()
P_rav=P.ravel()

weight=image
axis=1
ij=np.unravel_index(np.arange(S.size),P.shape)
ii=ij[axis]
jj=ij[1-axis]*1.0
inttm=interval_timer()
imgarea = calculate_area(image,P,S)
imgvol = calculate_volume(image,P,S)
imgdynrng = calculate_height(log10(image),P,S)
imgav = imgvol/imgarea
imgSN = imgav/image.ravel()
mximgSN = propagate_max_to_leaves(imgSN,P,S)
print('timer_dt',inttm.delta_time())
var,wght,jstatsperindex=calculate_average_component_index_variance_along_axis(P,S,axis=axis,weight=image)
print('timer_dt',inttm.delta_time())


ni=np.max(ii)
iroot=next(p for i,p in enumerate(P_rav) if p==i)
ya=jstatsperindex['av'].toarray()
yv=jstatsperindex['var'].toarray()
yw=jstatsperindex['wght'].toarray()
yad=np.zeros((ni,),dtype=np.float64)
yvd=np.zeros((ni,),dtype=np.float64)
ywd=np.zeros((ni,),dtype=np.float64)
for i in range(ni):
    iall=ii==i
    imgi=image[:,i]
    ywd[i]=ywi=np.sum(imgi)
    yad[i]=yavi=np.sum(imgi*np.arange(imgi.size))/ywi
    yvd[i]=yvari=np.sum(imgi*(np.arange(imgi.size)-yavi)**2)/ywi
    #print(i,ya[iroot,i],yavi,yv[iroot,1],yvari)
vard=np.sum(ywd*yvd)/np.sum(ywd)
print(var[iroot],vard)
figure()
subplot(2,1,1)
plot(ya[iroot,:].T,'.-',label='calc')
plot(yad,'.-',label='direct')
subplot(2,1,2)
plot(yv[iroot,:].T,'.-',label='calc')
plot(yvd,'.-',label='direct')