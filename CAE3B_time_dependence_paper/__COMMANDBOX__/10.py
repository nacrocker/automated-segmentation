rt=root # rt=OMFIT['ModeTimeDependence']

from OMFITlib_utils import assigntoarr as asgn
from OMFITlib_max_tree_class import max_tree as max_tree_cl
stftroot=rt['OUTPUTS'][130335]['bdot']['HN']['stft'][(0.43, 0.53)]

sp=abs(stftroot[0])**2
fsp=stftroot['freq']
tsp=stftroot['time']

spmxtr=max_tree_cl(sp)
self=spmxtr


signaltonoise=self.volume/(self.area*self.image)
#signaltonoise=self.volume/(self.area*self.peak)
avspecdens=self.volume/self.area*self.extents[...,1]


#paths=[]
#gain=signaltonoise.copy()
gain=avspecdens.copy()
gain_rav=gain.ravel()


maxgain,maxgain_nodes=self.maxattrclosing(gain,return_nodes=True)

argsort_masked = lambda arr,mask: np.nonzeros(mask.ravel())[np.argsort(arr.ravel()[mask.ravel()])]
sort_masked = lambda arr,mask: np.sort(arr.ravel()[mask.ravel()])