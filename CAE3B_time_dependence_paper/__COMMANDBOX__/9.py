defaultVars(
    levels=[1e-6,7e-5,.005],#3,
)
cntr=max_tree_cl()
cntr._P = np.array([c-1 if c > 0 else 0 for l in contour_parents for c in l],dtype=int).reshape(1,-1)
cntr._image = np.asarray([v for v,l in zip(np.sort(levels),contour_parents) for c in l]).reshape(1,-1)
cntr._S = np.arange(cntr.P.size,dtype=int)



import networkx as nx
cntrnx = nx.DiGraph()
cntrnx.add_nodes_from(cntr.S)

imagecntr_rav = cntr.image.ravel()
Pcntr_rav = cntr.P.ravel()
for node in cntrnx.nodes():
    print(node)
    cntrnx.nodes[node]['value'] = imagecntr_rav[node]
cntrnx.add_edges_from([(n, Pcntr_rav[n]) for n in cntr.S[1:]])

figure()

nx.draw(cntrnx)