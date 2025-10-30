picked=plt.ginput(2)
picked_indices= list(np.searchsorted(c,p)-1 for p,c in zip(np.vstack(picked).T,[tsp,fsp/1e6]))[::-1]
print(picked)
print(picked_indices)

