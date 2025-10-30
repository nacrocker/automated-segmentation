mkcond=(imgarea>=50) & (imgarea<=300)&(imgdynrng >= 2)
mkcond = propagate_max_to_leaves(mkcond,P,S)
imkcond=np.zeros(P.shape)
imkcond.ravel()[S]=np.arange(P.size,0,-1)
imkcond.ravel()[~mkcond.ravel()] = 0
imkcond = propagate_max_to_leaves(imkcond,P,S)
imkcond.ravel()[mkcond.ravel()] = P.size-imkcond.ravel()[mkcond.ravel()]
uimkcond,iuimkcond = unique(imkcond,return_inverse=True)
print(uimkcond)
from skimage.measure import label
lbmkcond,nlbmkcond=label(mkcond,connectivity=1,return_num=True)
print(unique(lbmkcond[~mkcond]))
print(unique(lbmkcond[mkcond]))


figure()
subplot(2,1,1)
imshow(iuimkcond.reshape(P.shape),origin='lower',cmap='tab20c')
colorbar()
subplot(2,1,2)
imshow(lbmkcond.reshape(P.shape),origin='lower',cmap='tab20c')
colorbar()