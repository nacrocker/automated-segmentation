smalltest=False
if smalltest:
    image = np.array([[40, 40, 39, 39, 38],
                    [40, 41, 39, 39, 39],
                    [30, 30, 30, 32, 32],
                    [33, 33, 30, 32, 35],
                    [30, 30, 30, 33, 36]], dtype=np.uint8)
else:
    xsp_to_anal=xsp.sel(dict(time=slice(0.250,.35),freq=slice(0,.1e6)))
    image=np.array(xsp_to_anal)

P, S = max_tree(image, connectivity=1)
P_rav=P.ravel()
image_rav = image.ravel()

from OMFITlib_max_tree_utils import parent_tree_along_axis, max_tree_along_axis


from OMFITlib_max_tree_utils import interval_timer
inttm=interval_timer()
Pa,Sa=max_tree_along_axis(P,S,axis=1)
print('timer_dt',inttm.delta_time())
Paa=parent_tree_along_axis(P,S,axis=1)
print('timer_dt',inttm.delta_time())

if smalltest:
    print(Pa)
    print(Paa)
    print(P)
    print(S)

print(np.all(Pa == Paa))