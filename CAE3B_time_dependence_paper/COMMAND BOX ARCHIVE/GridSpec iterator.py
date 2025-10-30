fgsz0=(6,4.5) #single panel (horiz,vert)
fgrc=(2,3) #(num rows, num cols)
fgsz=(fgsz0[0]*fgrc[1],fgsz0[1]*fgrc[0])

fig = plt.figure(figsize=fgsz,layout='constrained')
gs = GridSpec(*fgrc, figure=fig)
gsrav = lambda i: gs[np.unravel_index(i, gs.get_geometry())]
gsit = (gsrav(i) for i in range(np.product(gs.get_geometry())))

for i in range(np.product(gs.get_geometry())):
    gsc=next(gsit)#gs[0,0]
    ax = fig.add_subplot(gsc)
    plot(i+np.arange(3),'-o')
    ylim((i-1,3+i))
