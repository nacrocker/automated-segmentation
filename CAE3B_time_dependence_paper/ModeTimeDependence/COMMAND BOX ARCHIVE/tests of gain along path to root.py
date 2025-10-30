rt = root # rt = OMFIT['ModeTimeDependence']
from OMFITlib_max_tree_class import max_tree as max_tree_cl
stftrt=rt['OUTPUTS'][130335]['bdot']['HN']['stft'][(0.43, 0.53)]

sp=abs(stftrt[0])**2
fsp=stftrt['freq']
tsp=stftrt['time']

spmxtr=max_tree_cl(sp)
self=spmxtr


#gain=self.volume/(self.area*self.image)
#gain=self.volume/(self.area*self.peak)
gain=self.volume/self.area#*self.extents[...,1]


figure()

for i in range(-1,-10,-1):
    print(i)
#    pth = self.path_to_root(self.S[i])
    pth = self.path_to_root_as_P_indices(self.S[i])
    plot(self.area.ravel()[pth],gain.ravel()[pth],'.-')

imx = np.argmax(gain.ravel())
pth = self.path_to_root_as_P_indices(imx)
print(imx,gain.ravel()[imx])
plot(self.area.ravel()[pth],gain.ravel()[pth],'.-c')

xscale('log')
yscale('log')
