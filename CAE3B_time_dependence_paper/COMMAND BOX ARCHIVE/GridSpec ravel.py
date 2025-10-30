fgrc=(2,3) #(num rows, num cols)
fgsz=(fgsz0[0]*fgrc[1],fgsz0[1]*fgrc[0])

fig = plt.figure(figsize=fgsz,layout='constrained')
gs = GridSpec(*fgrc, figure=fig)
gsrav = lambda i: gs[np.unravel_index(i, gs.get_geometry())]
print(gsrav(0))
print(gs[0,0])
