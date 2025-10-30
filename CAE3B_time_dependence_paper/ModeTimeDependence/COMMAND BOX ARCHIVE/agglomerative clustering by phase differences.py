#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
#from omfit.omfit_tree import *
#from omfit_classes import *
import matplotlib as mpl
#mpl.use('agg')


# In[2]:


#don't use %matplotlib inline.  It messes with omfit
def show_fig(filename='jupyter_plot.png'):
    return # short circuiting because using in OMFIT
    # all below if for using in Jupyter
    import matplotlib.pyplot as plt
    from IPython.display import Image, display
    plt.savefig(filename)
    display(Image(filename=filename))

def test_show_fig():
    import matplotlib.pyplot as plt
    plt.figure()
    plt.plot([3,2,1])
    show_fig()


# In[3]:


import scipy.signal as signal
shot = 141398
bdotarray='HN'
bdotnames = ['\\OPS_PC::BDOT_L1DMIVVHN3_RAW', '\\OPS_PC::BDOT_L1DMIVVHN2_RAW', '\\OPS_PC::BDOT_L1DMIVVHN1_RAW', '\\OPS_PC::BDOT_L1DMIVVHN16_RAW', '\\OPS_PC::BDOT_L1DMIVVHN15_RAW', '\\OPS_PC::BDOT_L1DMIVVHN14_RAW', '\\OPS_PC::BDOT_L1DMIVVHN13_RAW', '\\OPS_PC::BDOT_L1DMIVVHN10_RAW', '\\OPS_PC::BDOT_L1DMIVVHN7_RAW', '\\OPS_PC::BDOT_L1DMIVVHN6_RAW', '\\OPS_PC::BDOT_L1DMIVVHN5_RAW', '\\OPS_PC::BDOT_L1DMIVVHN4_RAW']
rt = OMFIT['ModeTimeDependence']
#rt = root # use this line if this a module script

shotsholder = rt['OUTPUTS']
shotoutputs=shotsholder[shot]=OMFITtree('')
bdotoutputs=shotoutputs['bdot']=OMFITtree('')
arrayoutputs=bdotoutputs[bdotarray]=OMFITtree('')
data=arrayoutputs['data']=OMFITtree('')
stftoutputs=arrayoutputs['stft']=OMFITtree('')

bdottimes = [0.15,0.30]
stft=stftoutputs[tuple(bdottimes)]=OMFITtree('')

window='hann'
window_time=0.001
overlap_time= window_time*0.5
usepow2nfft = False # if True, use zero padding for ffts to bring nfft up to a power of 2
detrend='constant'
boundary=None
padded=None

for ib,bname in enumerate(bdotnames):
    data[ib] = OMFITmdsValue(server='NSTX', shot=141398, TDI=bname, treename='OPS_PC')
    if ib is 0:
        time = data[ib].dim_of(0)
        fsamp = (len(time)-1)/ (time[-1] - time[0])
        fsamp = 100 * np.round(fsamp/100)
        window_length = int(window_time * fsamp)
        overlap_length = int(overlap_time * fsamp)
        nfft=None
        if usepow2nfft: nfft=2**np.ceil(np.log2(window_length))

        ibdot = np.argwhere(numpy.logical_and(bdottimes[1]>=time,bdottimes[0]<=time))[[0,-1]]
        nsamp = ibdot[1][0]-ibdot[0][0]

    fZ, tZ, Z = signal.stft(array(data[ib].data()[ibdot[0][0]:ibdot[1][0]]), nperseg=window_length, noverlap=overlap_length, window=window, fs=fsamp, nfft=nfft, detrend=detrend, boundary=boundary, padded=padded)
    tZ = tZ + time[ibdot[0][0]]
    stft[ib] = Z

    if ib is 0:
        stft.insert(0,'freq',fZ)
        stft.insert(1,'time',tZ)

print('Sampling rate: {} samples/second'.format(fsamp))
print('Signal size: {} samples'.format(nsamp))
print('Signal duration: {:.3f} seconds'.format(nsamp/fsamp))


# In[4]:


# Plotting the spectrogram
import matplotlib.pyplot as plt

ipltbdot=0
tmbdot,bdot = data[ipltbdot].dim_of(0)[ibdot[0][0]:ibdot[1][0]],data[ipltbdot].data()[ibdot[0][0]:ibdot[1][0]]
fsp,tsp,sp = stft['freq'], stft['time'],np.abs(stft[ipltbdot])**2

fig, ax = plt.subplots(figsize=(10, 6))
plt.plot(tmbdot,bdot)
plt.xlabel('time [sec]')
plt.tight_layout()
show_fig()

fig, ax = plt.subplots(figsize=(10, 6))
plt.imshow(np.flip(np.log10(sp), axis=0), extent=(np.min(tsp), np.max(tsp), np.min(fsp), np.max(fsp)), aspect='auto')
plt.title('Spectrogram')
plt.ylabel('freq [Hz]')
plt.xlabel('time [sec]')
plt.colorbar()
plt.tight_layout()
show_fig()


# In[5]:


#coilind=np.arange(0,len(bdotnames))
coilind=[0,1]
print([bdotnames[ci] for ci in coilind])

nc=len(coilind)
structure_mat=np.empty_like(stft[0][0],shape=stft[0].shape+(nc**2,))
for i,ic in enumerate(coilind):
    for j,jc in enumerate(coilind[:i+1]):
        k0=np.ravel_multi_index((i,j),(nc,nc))
        structure_mat[...,k0]=stft[ic]*np.conj(stft[jc])
        if (i != j):
            k1=np.ravel_multi_index((j,i),(nc,nc))
            structure_mat[...,k1]=np.conj(structure_mat[...,k0])



# In[6]:


for k in [np.ravel_multi_index((i,j),(nc,nc)) for i,j in [(0,1)]]:
    i,j=np.unravel_index(k,(nc,nc))
    ic,jc=coilind[i],coilind[j]
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.imshow(np.log10(abs(structure_mat[...,k])), origin='lower',extent=(np.min(tsp), np.max(tsp), np.min(fsp), np.max(fsp)), aspect='auto')
    plt.title('Spectrogram (%d,%d)'%(ic,jc))
    plt.ylabel('freq [Hz]')
    plt.xlabel('time [sec]')
    plt.colorbar()
    plt.tight_layout()
    show_fig()
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.imshow(np.angle(structure_mat[...,k]), origin='lower', extent=(np.min(tsp), np.max(tsp), np.min(fsp), np.max(fsp)), aspect='auto', vmin=-np.pi,vmax=np.pi)
    plt.title('Phase (%d,%d)'%(ic,jc))
    plt.ylabel('freq [Hz]')
    plt.xlabel('time [sec]')
    plt.colorbar()
    plt.tight_layout()
    show_fig()


OMFITx.End()
# In[7]:


print(structure_mat.shape)


# In[8]:


from sklearn.cluster import AgglomerativeClustering
from sklearn.feature_extraction.image import grid_to_graph
#n_clusters,distance_threshold=50,None
n_clusters,distance_threshold=None,.05


metric='cosine'
X =np.concatenate((structure_mat.real,structure_mat.imag),axis=-1)
Xind=np.s_[400:2000,0:100,:]
X=X[Xind]
fX=fsp[Xind[0]]
tX=tsp[Xind[1]]
Xshape=X.shape


# In[9]:


X = np.reshape(X, (-1, Xshape[-1]))
connectivity = grid_to_graph(*Xshape[0:2])

model = AgglomerativeClustering(n_clusters=n_clusters,distance_threshold=distance_threshold,connectivity=connectivity,linkage="average",
                                compute_full_tree=True, compute_distances=True,affinity=metric)
model.fit(X)


# In[10]:


def form_linkage_matrix(model):
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count +=1
            else:
                current_count += counts[child_idx-n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack([model.children_, model.distances_,
                                     counts]).astype(float)
    return linkage_matrix


# In[11]:


from skimage.color import label2rgb
label_image = label2rgb(model.labels_.reshape(Xshape[0:2]))
fig, ax = plt.subplots(figsize=(10, 6))
plt.imshow(label_image, origin='lower', extent=(np.min(tX), np.max(tX), np.min(fX), np.max(fX)), aspect='auto')
plt.title('AgglomerativeClustering Labels')
plt.ylabel('freq [Hz]')
plt.xlabel('time [sec]')
plt.tight_layout()
show_fig()


# In[12]:


print(model.children_.shape)
print(model.children_[0:10,:])


# In[13]:


from sklearn.metrics import pairwise_distances as sklmpairdist
def cosdist(X,Y,axis=-1):
    def sm(z,ax):
        return np.expand_dims(z.sum(axis=ax),axis=ax)
    def td(x,y,ax):
        return np.tensordot(x,y,axes=((ax,),(ax,)))
    return 1-td(X,Y,axis)/np.sqrt(td(sm(X**2,axis),sm(Y**2,axis),axis))

def cosdistlist(X,Y,axis=-1):
    return 1-(X*Y).sum(axis=axis)/np.sqrt((X**2).sum(axis=axis)*(Y**2).sum(axis=axis))

X=np.arange(6).reshape((2,-1))
Y=np.arange(1,7).reshape((2,-1))

print(sklmpairdist(X,Y,metric='cosine'))
print(cosdist(X,Y))
