xsp_to_anal=xsp.sel(dict(time=slice(0.250,.35),freq=slice(0,.1e6)))

plt.figure()
im1,cb1=imshow_DataArray(xsp_to_anal,norm=matplotlib.colors.LogNorm(),cmap=cmstd)
ax1=im1.axes
sel=plt.ginput(1)[0][::-1]
time=np.array(xsp_to_anal.time)
freq=np.array(xsp_to_anal.freq)
isel=[np.argmin(np.abs(arr-co)) for co,arr in zip(sel,(freq,time))]
sel = [arr[i] for i,arr in zip(isel,(freq,time))]
print(sel)


from OMFITlib_max_tree_utils import accumulate_vs_index_along_axis
from OMFITlib_max_tree_utils import accumulate_other_index_vs_index_along_axis
from OMFITlib_max_tree_utils import accumulate_other_index2_vs_index_along_axis
from OMFITlib_max_tree_utils import accumulate_other_index12_vs_index_along_axis
from OMFITlib_max_tree_utils import first_at_index_accumlator
from OMFITlib_max_tree_utils import mark_component
from OMFITlib_max_tree_utils import interval_timer


image=np.array(xsp_to_anal)
P, S = max_tree(image, connectivity=1)
image_rav=image.ravel()

axis=1

inttm=interval_timer()
faiacc=first_at_index_accumlator(image,axis=axis)
print('timer_dt',inttm.delta_time())

icomp = np.ravel_multi_index(isel,image.shape)
#icomp=S[-100]

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

plt.contour(time,freq,mk)
fmin=np.amin(freq)
fmax=np.amax(freq)
tmin=np.amin(time)
tmax=np.amax(time)
tfav=np.arange(acccompav.size)/time.size*(tmax-tmin)+tmin
fav=np.where(acccomp_count > 0,acccompav*(fmax-fmin)/freq.size+fmin,None)
fstd=np.where(acccomp_count > 0,acccompstd*(fmax-fmin)/freq.size+fmin,None)
#plt.figure()
plt.plot(tfav,fav,'g')
plt.title('ch %02d, shot %d'%(ch,shot))