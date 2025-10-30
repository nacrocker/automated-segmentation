from skimage.morphology import max_tree
xsp_to_anal=xsp.sel(dict(time=slice(0.250,.35),freq=slice(0,.1e6)))
image=np.array(xsp_to_anal)
P, S = max_tree(image, connectivity=1)
P_rav=P.ravel()
image_rav = image.ravel()

####
from OMFITlib_max_tree_utils import accumulate_vs_index_along_axis
from OMFITlib_max_tree_utils import accumulate_other_index_vs_index_along_axis
from OMFITlib_max_tree_utils import accumulate_other_index2_vs_index_along_axis
from OMFITlib_max_tree_utils import accumulate_other_index12_vs_index_along_axis
from OMFITlib_max_tree_utils import first_at_index_accumlator
from OMFITlib_max_tree_utils import mark_component

#icomp=Spp[-10]
#faiacc=first_at_index_accumlator(P,axis=1)
#mk=mark_component(icomp,image,P,S,accumulator=faiacc)
#print(image)
#print(P)
#print(S)
#print(mk)
##print(acc.accumulation)

#firstind=np.full_like(image,fill_value=-1,dtype=int)
#firstind_rav=firstind.ravel()
#firstind_rav[list(faiacc.accumulation.values())] = [k[0] for k in faiacc.accumulation.keys()]
#print(firstind)

#branchfirstind=np.full_like(image,fill_value=(-1,),dtype=tuple)
#branchfirstind_rav=branchfirstind.ravel()
#branchfirstind_rav[list(faiacc.accumulation.values())] = [k[1:] for k in faiacc.accumulation.keys()]
#print(branchfirstind)

#print()
#print('####')
#print()

####
from OMFITlib_max_tree_utils import interval_timer
inttm=interval_timer()

axis=1
#accumoiviaa,accumoiviaa_count = accumulate_other_index_vs_index_along_axis(P,S,axis=axis)
#print('timer_dt',inttm.delta_time())

#accumoi2viaa,_ = accumulate_other_index2_vs_index_along_axis(P,S,axis=axis)
#print('timer_dt',inttm.delta_time())

accumoi12viaa,accumoiviaa_count = accumulate_other_index12_vs_index_along_axis(P,S,axis=axis)
print('timer_dt',inttm.delta_time())

accumoiviaa = accumoi12viaa[:,:,0]
accumoi2viaa = accumoi12viaa[:,:,1]

faiacc=first_at_index_accumlator(P,axis=axis)
print('timer_dt',inttm.delta_time())

icomp=S[-200]
print(np.log10(image_rav[icomp]))
mk=mark_component(icomp,image,P,S,accumulator=faiacc)
print('timer_dt',inttm.delta_time())

nacc=image.shape[axis]
acccomp=np.zeros(nacc)
acccomp2=np.zeros(nacc)
acccomp_count=np.zeros(nacc)
accumoiviaa_rav=accumoiviaa.ravel()
accumoi2viaa_rav=accumoi2viaa.ravel()
accumoiviaa_count_rav=accumoiviaa_count.ravel()

np.add.at(acccomp,[k[0] for k in faiacc.accumulation.keys()],accumoiviaa_rav[list(faiacc.accumulation.values())])
np.add.at(acccomp2,[k[0] for k in faiacc.accumulation.keys()],accumoi2viaa_rav[list(faiacc.accumulation.values())])
np.add.at(acccomp_count,[k[0] for k in faiacc.accumulation.keys()],accumoiviaa_count_rav[list(faiacc.accumulation.values())])

acccompav = np.divide(acccomp,acccomp_count, where=acccomp_count!=0,out=np.zeros_like(acccomp))
acccomp2av = np.divide(acccomp2,acccomp_count, where=acccomp_count!=0,out=np.zeros_like(acccomp))
acccompvar=acccomp2av-acccompav**2
acccompstd=np.sqrt(acccompvar)

plt.figure()
plt.imshow(np.log10(image),origin='lower')
plt.colorbar()
plt.contour(mk)
plt.plot(np.arange(acccompav.size),np.where(acccomp_count > 0,acccompav,None),'r')

plt.figure()
im1,cb1=imshow_DataArray(xsp_to_anal,norm=matplotlib.colors.LogNorm(),cmap=cmstd)
ax1=im1.axes
time=np.array(xsp_to_anal.time)
freq=np.array(xsp_to_anal.freq)
plt.contour(time,freq,mk)
fmin=np.amin(freq)
fmax=np.amax(freq)
tmin=np.amin(time)
tmax=np.amax(time)
tfav=np.arange(acccompav.size)/time.size*(tmax-tmin)+tmin
fav=np.where(acccomp_count > 0,acccompav*(fmax-fmin)/freq.size+fmin,None)
#plt.figure()
plt.plot(tfav,fav,'g')
plt.title('ch %02d, shot %d'%(ch,shot))