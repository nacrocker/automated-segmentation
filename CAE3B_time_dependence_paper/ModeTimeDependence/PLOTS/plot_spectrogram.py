defaultVars(
    shot = 141398,
    bdotarray = 'HN',
    istft = 0,
    bdottimes = [0.15,0.30],
)

rtnname='plot_spectrogram'
shotsholder = root['OUTPUTS']
if not shot in shotsholder: OMFITexception('%s: shot %d not found.'%(rtnname,shot))
if not 'bdot' in shotsholder[shot]: OMFITexception('%s: no bdot stft found shot %d.'%(rtnname,shot))
if not bdotarray in shotsholder[shot]['bdot']: OMFITexception('%s: stft for bdot array %s not found for shot %d.'%(rtnname,bdotarray,shot))
arrayoutputs=shotsholder[shot]['bdot'][bdotarray]
if not 'stft' in arrayoutputs: OMFITexception('%s: stft for bdot array %s not found for shot %d.'%(rtnname,bdotarray,shot))
stftoutputs=arrayoutputs['stft']
stft=stftoutputs[tuple(bdottimes)]

fsp,tsp,sp = stft['freq'], stft['time'],np.abs(stft[istft])**2

fig, ax = plt.subplots(figsize=(10, 6))
plt.imshow(np.flip(np.log10(sp), axis=0), extent=(np.min(tsp), np.max(tsp), np.min(fsp), np.max(fsp)), aspect='auto')
plt.title('Spectrogram')
plt.ylabel('freq [Hz]')
plt.xlabel('time [sec]')
plt.colorbar()
plt.tight_layout()
