sp=OMFIT['magnetics']['OUTPUTS']['SPECTROGRAM']['NSTX'][130335]['intial']
from OMFITlib_plot_utils import imshowxy
vmax=-1
vmin=-8
figure()
cmstd=cmapIDL_Standard_Gamma_II()
imshowxy(sp['time'],sp['frequency'],np.log10(sp['power'].T),xlabel='time',ylabel='freq',cmap=cmstd,vmax=vmax,vmin=vmin)

#print(sp['time'][1]-sp['time'][0],sp['frequency'][1]-sp['frequency'][0])