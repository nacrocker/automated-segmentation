from skimage.morphology import max_tree
#from OMFITlib_max_tree_utils import accumulate_vs_index_along_axis, accumulate_other_index_vs_index_along_axis


usetestim=False
if usetestim:
    smalltest=True
    image = np.array([[40, 40, 39, 39, 38],
                    [40, 41, 39, 39, 39],
                    [30, 30, 30, 32, 32],
                    [33, 33, 30, 32, 35],
                    [30, 30, 30, 33, 36]], dtype=np.uint8)
else:
    smalltest=False
    imsc=1e7
    xsp_to_anal=xsp.sel(dict(time=slice(*[v for v in (0.250,.35)]),freq=slice(0,.1e6)))
    image=np.array(xsp_to_anal)

P, S = max_tree(image, connectivity=1)



from OMFITlib_max_tree_utils import interval_timer, accumulate_other_index_vs_index_along_axis, accumulate_vs_index_along_axis, accumulate_vs_index_along_axis_alt
axis=1
inttm=interval_timer()
accum,accumc = accumulate_other_index_vs_index_along_axis(P,S,axis=axis,accumulator=accumulate_vs_index_along_axis)
print('timer_dt',inttm.delta_time())
accuma,accumca = accumulate_other_index_vs_index_along_axis(P,S,axis=axis,accumulator=accumulate_vs_index_along_axis_alt)
print('timer_dt',inttm.delta_time())

if smalltest:
    print(image*imsc)
    print(S)
    print(P)
    print(accumc)
    print(accumca)
    print(accum)
    print(accuma)

print(all(accumc == accumca))
print(all(accum == accuma))