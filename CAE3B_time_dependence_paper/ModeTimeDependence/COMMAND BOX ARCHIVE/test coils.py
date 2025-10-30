rt=root # rt=OMFIT['ModeTimeDependence']
stftroot = rt['OUTPUTS'][130335]['bdot']['HN']['stft'][(0.43, 0.53)]
nmsexcl=['HN13']

nms=stftroot['bdotshortnames']
inmsin = np.array([n not in nmsexcl for n in nms])
nmsin = [n for n in nms if n not in nmsexcl ]

stftarr = np.stack([stftroot[i] for i in np.sort([k for k in stftroot.keys() if isinstance(k,int)])],axis=2)
fsp=stftroot['freq']

spfonly = np.mean(np.abs(stftarr[...,inmsin])**2,axis=1)
figure()
plot(fsp,spfonly,label=nmsin)
yscale('log')
legend()
