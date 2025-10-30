comp=np.zeros(mk.shape,dtype=int)
comp_rav=comp.ravel()
mk_rav=mk.ravel()
comp_rav[S] = arange(image.size)[::-1]
comp_rav[~mk_rav]=0
comp = propagate_max_to_leaves(comp,P,S)
comp_rav=comp.ravel()
comp_rav[mk_rav]=S.size-1-comp_rav[mk_rav]
comp_rav[~mk_rav]=0
ucomp,iucomp=unique(comp,return_inverse=True)
complevs=iucomp.reshape(comp.shape)
figure()
cmstd=cmapIDL_Standard_Gamma_II()
plt.contourf(time,freq,complevs,unique(complevs),cmap=cmstd)
colorbar()
comp_rav=comp.ravel()
tot=0
for i in unique(comp_rav): 
    sm=sum(comp_rav == i)
    if i > 0: tot+=sm
    print(i,': ',sm,imgarea[S[i]])
print(tot,sum(mk))