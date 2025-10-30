from OMFITlib_max_tree_utils import interval_timer


image=np.array(xsp_to_anal)
P, S = max_tree(image, connectivity=1)
image_rav=image.ravel()


inttm=interval_timer()
tree=dict()
P_rav=P.ravel()
for p in S:
    #tree.setdefault(P_rav[p],[]).append(p)
    tree.setdefault(P_rav[p],dict(children=[]))['children'].append(p)
print('timer_dt',inttm.delta_time())
print(tree)