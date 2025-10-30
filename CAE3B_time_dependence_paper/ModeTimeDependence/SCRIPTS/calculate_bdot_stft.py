#!/usr/bin/env python
# coding: utf-8


defaultVars(
    shot = 141398,
    bdotarray = 'HN',
    bdottimes = [0.15,0.30],
    window='hann',
    window_time=0.001,
    overlap= 0.5,
    usepow2nfft = False, # if True, use zero padding for ffts to bring nfft up to a power of 2
    detrend='constant',
    boundary=None,
    padded=None,
)

rtnname='calculate_bdot_stft'
shotsholder = root['OUTPUTS']
if not shot in shotsholder: OMFITexception('%s: shot %d not found.'%(rtnname,shot))
if not 'bdot' in shotsholder[shot]: OMFITexception('%s: no bdot data shot %d.'%(rtnname,shot))
if not bdotarray in shotsholder[shot]['bdot']: OMFITexception('%s: data for bdot array %s not found for shot %d.'%(rtnname,bdotarray,shot))
arrayoutputs=shotsholder[shot]['bdot'][bdotarray]
if not 'data' in arrayoutputs: OMFITexception('%s: data for bdot array %s not found for shot %d.'%(rtnname,bdotarray,shot))
data=arrayoutputs['data']
stftoutputs=arrayoutputs.setdefault('stft',OMFITtree(''))
stft=stftoutputs[tuple(bdottimes)]=OMFITtree('')


import scipy.signal as signal

overlap_time=window_time*overlap
ib0=data.keys()[0]
for ib in data.keys():
    if ib is ib0:
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

    if ib is ib0:
        stft.insert(0,'freq',fZ)
        stft.insert(1,'time',tZ)


