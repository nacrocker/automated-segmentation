from OMFITlib_max_tree_utils import interval_timer

inttm=interval_timer()
faiacc=first_at_index_accumlator(image,axis=axis)
print('timer_dt',inttm.delta_time())

image_rav=image.ravel()
icomp=S[-100]
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