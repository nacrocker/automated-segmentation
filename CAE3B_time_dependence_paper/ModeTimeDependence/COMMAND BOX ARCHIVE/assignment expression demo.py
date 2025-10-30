a=np.zeros((10,))
asgnl = lambda out,ind,val: np.put(out,ind,val) is None and out
print(asgnl(np.zeros((10,)),[1],[2]))