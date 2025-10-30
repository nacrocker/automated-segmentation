from OMFITlib_max_tree_utils import calculate_area, calculate_height, calculate_volume, propagate_max_to_leaves
from OMFITlib_max_tree_utils import calculate_average_component_variance_along_axis
from skimage.morphology import max_tree

#xsp_to_anal=xsp.sel(dict(time=slice(*[v for v in (0.250,.35)]),freq=slice(0,.1e6)))
xsp_to_anal=xsp.sel(dict(time=slice(0.100,.35),freq=slice(0,.2e6)))
      
image=np.array(xsp_to_anal)
P, S = max_tree(image, connectivity=1)
image_rav=image.ravel()

imgarea = calculate_area(image,P,S)
imgvol = calculate_volume(image,P,S)
imgdynrng = calculate_height(log10(image),P,S)
imgav = imgvol/imgarea
imgSN = imgav/image.ravel()
mximgSN = propagate_max_to_leaves(imgSN,P,S)
#imgvar,_,_,Pa=calculate_average_component_index_variance_along_axis(P,S,axis=1,weight=image)

mkcond=(imgarea>=50) & (imgarea<=300)&(imgdynrng >= 2)
mkcond = propagate_max_to_leaves(mkcond,P,S)
mk=np.zeros(image.shape,dtype=bool)
mk.ravel()[mkcond] = True

plt.figure()
im1,cb1=imshow_DataArray(xsp_to_anal,norm=matplotlib.colors.LogNorm(),cmap=cmstd)
ax1=im1.axes
time=np.array(xsp_to_anal.time)
freq=np.array(xsp_to_anal.freq)
plt.contour(time,freq,mk)