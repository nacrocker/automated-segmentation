rt=root # rt=OMFIT['ModeTimeDependence']

from OMFITlib_max_tree_class import max_tree as max_tree_cl
stftroot=rt['OUTPUTS'][130335]['bdot']['HN']['stft'][(0.43, 0.53)]

sp=abs(stftroot[0])**2
fsp=stftroot['freq']
tsp=stftroot['time']

spmxtr=max_tree_cl(sp)
self=spmxtr


assert self.isdescendent(self.S[1],self.S[0])
assert self.isdescendent(self.S[-1],self.S[0])
assert not self.isdescendent(self.S[1],self.S[1])
assert not self.isdescendent(self.S[0],self.S[1])
