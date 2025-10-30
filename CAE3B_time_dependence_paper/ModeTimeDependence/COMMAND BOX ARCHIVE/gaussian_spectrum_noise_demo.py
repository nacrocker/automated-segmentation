from OMFITlib_math_utils import gaussian_spectrum_noise

t=np.arange(0,300.0,0.5e-3)
nfft=1024
cmap='viridis',
spquantrange = [0.8,.97],


nt=len(t)
dt=t[1]-t[0]
fs=1/dt
fN = fs/2.0


bc_noise_bw = 1500.0 
bc_noise_f0 = 200.0
bc_truncate = 4.0


broadband_coherent_noise = gaussian_spectrum_noise(nt,f0=bc_noise_f0,bw=bc_noise_bw,fs=fs,truncate=bc_truncate)
data = broadband_coherent_noise
from scipy.signal import stft
fstft,tstft, sigstft=stft(data,fs,nperseg=nfft,noverlap=0.75*nfft)
fsp, tsp, sp = fstft, tstft, abs(sigstft)**2

figure()
itm=np.int(len(tsp)/2)
plot(fsp,sp[:,itm])
yscale('log')

from OMFITlib_plot_utils import specim
normfunc=matplotlib.colors.LogNorm
norm=normfunc()
fig=figure()
specim(tsp,fsp,sp,norm=norm)
margins(0, 0)
