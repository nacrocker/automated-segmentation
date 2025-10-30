#this is a fork of root['PROJECT']['SCRIPTS']['maxtree_noise_project - Haowen Sun summer 2024']
import numpy as np
from scipy.signal import chirp
import matplotlib.pyplot as plt
from scipy.signal import stft
from skimage.morphology import max_tree
from matplotlib.colors import LogNorm
from OMFITlib_max_tree_class import max_tree as max_tree_cl

def blackman_vs_tau(tau):
    """Blackman window vs normalized time (0 <= tau <= 1)
       This gives numpy.blackman(M) == blackman_vs_tau(taus) for taus = (numpy.arange(1-M, M, 2)/(M-1)/2) + 0.5
    """
    return 0.42 + 0.5*cos(2*np.pi*(tau-0.5)) + 0.08*cos(4*np.pi*(tau-0.5)) #0 <= tau <= 1

import typing
class ChirpDesc(typing.NamedTuple):
    amp: float = 1.0
    envlf: typing.Callable[...,typing.Any] = blackman_vs_tau
    tstart: float = 0.0  #seconds
    tlen: float = 1.0  #seconds
    toff: float = 0.0 # seconds
    f0: float = 1000.0 #Hz
    f1: float  = 11000.0 #Hz
    method: str = 'quadratic'
    vertex_zero: bool = True

    def make_chirp_signal(self,t,phi=0.0):
        """make chirp, c(t):
           for t < self.tstart, c(t) = 0
           for t >= self.tstart & t < self.tstart+self.tlen, c(t) = amp*envl((t-self.tstart)/self.tlen)*
               scipy.signal.chirp(tshift+self.toff, self.f0, self.tlen+self.toff, self.f1, method=self.method, phi=phi, vertex_zero=self.vertex_zero)
               where envl is a continuous function inspired by the blackmann window where, for 0 <= tau <= 1:
                   envl(tau) = 0.42 + 0.5*cos(2*np.pi*(tau-0.5)) + 0.08*cos(4*np.pi*(tau-0.5))
              self.method defaults to quadratic and self.vertex_zero defaults to true.
           for t > self.tstart+self.tlen, c(t) = 0
        """
        import numpy as np
        from scipy.signal import chirp
        t = np.asarray(t).flatten()
        nt = t.size
        sig=np.zeros((nt,),dtype=float)
        inchirp = (t >= self.tstart) & (t <= (self.tstart + self.tlen))
        #print('it0',np.flatnonzero(inchirp)[0],'ntch',np.count_nonzero(inchirp))
        if np.count_nonzero(inchirp) > 0:
            tshift = t[inchirp]-self.tstart
            envl=self.envlf(tshift/self.tlen)     # window function
            sig[inchirp] = self.amp*envl*chirp(tshift+self.toff, self.f0, self.tlen+self.toff, self.f1, method=self.method, phi=phi, vertex_zero=self.vertex_zero)
        return sig

class ChirpModeDesc(typing.NamedTuple):
    chirpdesc: ChirpDesc = ChirpDesc()
    nmode: int = 0

    def make_chirpmode_signal_array(self,t,locations):
        import numpy as np
        locations = np.asarray(locations).flatten()
        nsig = locations.size
        t = np.asarray(t).flatten()
        nt = t.size
        sigarr = np.zeros((nsig,nt),dtype=float)
        for isig,loc in enumerate(locations):
            sigarr[isig,:] = self.chirpdesc.make_chirp_signal(t,phi=self.nmode*loc)
        return sigarr

def make_chirpmodes_sigarray(t,chirpmodedescs,locations=(0.0,)):
    sigarray = chirpmodedescs[0].make_chirpmode_signal_array(t,locations)
    for c in chirpmodedescs[1:]:
        sigarray += c.make_chirpmode_signal_array(t,locations)
    return sigarray

def make_noise(mean, std, shape, noise_generator = np.random.normal):
    return noise_generator(mean, std, shape)



###Generating Histograms###

t=np.arange(0,1024/1000,0.001)
locations=[0.0]#,0.1,0.5,np.pi/2]
nsig=len(locations)
nt=len(t)
dt=t[1]-t[0]
fs=1/dt
fN = fs/2.0
nfft=int(np.ceil(np.sqrt(nt)))
noise_mean=0
noise_std=0.001

chirpmodedescs=[]

#modes to match Hawowen Sun's noise_histograms_v2.
ts=t[int(nt/16)]
tl=t[int(nt/16)+int(nt*3/4)-1] - ts
chirpmodedescs.append(ChirpModeDesc(nmode=1,chirpdesc=ChirpDesc(amp=2.0, tstart=ts, tlen=tl, toff=ts, f0=0.3*fN, f1=0.9*fN)))

ts=t[int(nt/8)]
tl=t[int(nt/8)+int(nt*3/4)-1] - ts
chirpmodedescs.append(ChirpModeDesc(nmode=2,chirpdesc=ChirpDesc(amp=1.5, tstart=ts, tlen=tl, toff=ts, f0=0.15*fN, f1=0.7*fN)))

n_bins = 50
contrast_cum = np.zeros(n_bins)
area_cum = np.zeros(n_bins)
max_log_contrast = 10
max_area = 300
n_tries=100
total_area=[]
total_log_contrast=[]

for _ in range(n_tries):
    noise = make_noise(noise_mean, noise_std, t.shape)
    sigarray = make_chirpmodes_sigarray(t, chirpmodedescs, locations=[0])
    data = noise
    #data = sigarray + noise # haven't tested if broadcasting works properly
    #data = sigarray[0]

    fstft,tstft, sigstft=stft(data,fs,nperseg=nfft,noverlap=None)
    fsp, tsp, sp = fstft, tstft, abs(sigstft)
    self = max_tree_cl(sp,connectivity=1)

    area = self.area[self.canonicality]
    contrast = self.contrast[self.canonicality]

    total_area.extend(area)
    total_log_contrast.extend(np.log(contrast))

    hist_contrast, bin_edges_contrast = np.histogram(np.log(contrast), bins=n_bins, density=False, range=(0, max_log_contrast))
    hist_area, bin_edges_area = np.histogram(area, bins=n_bins, density=False, range=(0, max_area))
    contrast_cum += hist_contrast
    area_cum += hist_area

def pltshow():
    pass

plt.figure()
plot(t,data)
plt.xlabel('time [s]')

plt.figure()
bnds=lambda coord: polyval(polyfit([0,len(coord)-1],[m(coord) for m in [np.min,np.max]],1),[-0.5,len(coord)-0.5])
im1=plt.imshow(sp,aspect='auto',origin='lower',cmap='plasma',extent=(*bnds(tsp),*bnds(fsp)))
plt.colorbar()
plt.xlabel('time [sec]')
plt.ylabel('freq [Hz]')

bin_centers = (bin_edges_contrast[:-1] + bin_edges_contrast[1:]) / 2
bin_width_contrast = np.diff(bin_edges_contrast)
nstft = sigstft.size
#contrast_pdf = contrast_cum / (n_tries * nstft)
contrast_pdf = contrast_cum / (np.sum(contrast_cum)*bin_width_contrast) # get PDF

### Contrast ###

plt.figure()
plt.bar(bin_centers, contrast_cum, width=(bin_centers[1] - bin_centers[0]))
plt.title('Histogram of Contrast Values')
plt.xlabel('Log of Contrast')
plt.ylabel('Count')
plt.legend()
pltshow()

plt.figure()
plt.bar(bin_centers, contrast_cum/(np.sum(contrast_cum)*bin_width_contrast), width=(bin_centers[1] - bin_centers[0]))
plt.title('Histogram of PDF(Contrast)')
plt.xlabel('Log of Contrast')
plt.ylabel('PDF')
plt.legend()
pltshow()

plt.figure()
plt.plot(bin_centers, contrast_pdf, 'r-', label='Probability density')
plt.title('Probability density of Contrast Values')
plt.xlabel('Log of Contrast')
plt.ylabel('Probability density')
plt.legend()
pltshow()

### Area ###

bin_centers = (bin_edges_area[:-1] + bin_edges_area[1:]) / 2
bin_width_area = np.diff(bin_edges_area)
#area_pdf = area_cum / (n_tries * nstft)
area_pdf = area_cum / (np.sum(area_cum)*bin_width_area) # PDF

plt.figure()
plt.bar(bin_centers, area_cum, width=(bin_centers[1] - bin_centers[0]))
plt.title('Histogram of Area Values')
plt.xlabel('Area')
plt.ylabel('Count')
plt.legend()
pltshow()

plt.figure()
plt.bar(bin_centers, area_cum/(np.sum(area_cum)*bin_width_area), width=(bin_centers[1] - bin_centers[0]))
plt.title('Histogram of PDF(area)')
plt.xlabel('Area')
plt.ylabel('PDF')
plt.legend()
pltshow()

plt.figure()
plt.plot(bin_centers, area_pdf, 'r-', label='Probability density')
plt.title('Probability density of Area Values')
plt.xlabel('Area')
plt.ylabel('Probability density')
plt.legend()
pltshow()

## 2D Histogram ###

from numpy import exp,arange
from pylab import meshgrid,cm,imshow,contour,clabel,colorbar,axis,title,show

# the function that I'm going to plot
def s_func(lc, A):
    return A * np.exp(4 * lc)

max_plot_a = np.exp(10)
max_plot_lc = 10/4

max_plot_lc = np.min([max_log_contrast,max_plot_lc])
max_plot_a = np.min([max_area,max_plot_a])

max_plot_range=np.min([max_plot_lc*4,np.log(max_plot_a)])
max_plot_a = np.exp(max_plot_range)
max_plot_lc = max_plot_range/4

lc_range=(0.1, max_log_contrast)
a_range=(2, max_area)

lc_param = np.linspace(0, max_plot_lc, 100)
a_param = np.linspace(1, max_plot_a, 100)
lcg, ag = meshgrid(lc_param, a_param) # grid of point
Sg = s_func(lcg, ag) # evaluation of the function on the grid

#Using "4*log(contrast)" for x variable because 2D hist shows heavy concnetration around log(area) = 4*log(contrast)
n_bins_a_plot = 50
n_bins_lc_plot = 100
plt.figure()
plt.hist2d(4 * np.array(total_log_contrast), np.log(total_area), bins=(n_bins_lc_plot, n_bins_a_plot), cmap='viridis', range=[4*np.array(lc_range),np.log(a_range)],  norm=matplotlib.colors.LogNorm())
plt.colorbar()

# testing various power relations for area vs log contrast  no surprise that for lc0 = 0.25, plotted line is "y=x"
lc0_all = [0.25]
for lc0 in lc0_all: 
    area_curve = np.exp(lc_param/lc0)
    plt.plot(4 * lc_param, np.log(area_curve), 'r-', label='Area Curve')

mlev=np.log(s_func(max_plot_lc,max_plot_a))
cset = contour(4*lc_param, np.log(a_param), np.log(Sg), np.arange(1, np.ceil(mlev)),linewidths=2,cmap=cm.Set2)
clabel(cset,inline=True,fmt='%1.1f',fontsize=10)

plt.title('2D Histogram of Contrast and Area')
plt.xlabel('4 * Log of Contrast')
plt.ylabel('Log of Area')
plt.xlim((0, 4*max_plot_lc))
plt.ylim((0, np.log(max_plot_a)))
pltshow()

Sdata = s_func(np.array(total_log_contrast), np.array(total_area)) # evaluation of the function on the grid
S_ravel = Sdata.ravel()
logS_pdf, bin_logS_edges = np.histogram(np.log(S_ravel), bins=100, density=True)
bin_centers = (bin_logS_edges[:-1] + bin_logS_edges[1:]) / 2
log_logS_pdf = np.log(logS_pdf)
valid=np.isfinite(log_logS_pdf)
p_logS=np.polyfit(bin_centers[valid], log_logS_pdf[valid], 1)
logS_pdf_fit = p_logS[1]+bin_centers*p_logS[0]
plt.figure()
plt.plot(bin_centers, np.exp(logS_pdf_fit), 'r-', label=f'fit: PDF(log(S))={np.exp(p_logS[1]):3.2f}*exp(log(S)*{p_logS[0]:3.2f})')
plt.plot(bin_centers, logS_pdf, 'b-', label='S Probability density')
plt.title('Probability density of log(S) Values')
plt.xlabel('log(S)')
plt.ylabel('Probability density)')
plt.yscale('log')
plt.legend()
pltshow()

#valid=~(np.isnan(area_pdf[1:]) | (area_pdf[1:] == 0))
log_area_pdf = np.log(area_pdf)
valid = np.isfinite(log_area_pdf)
bin_centers = (bin_edges_area[:-1] + bin_edges_area[1:]) / 2
#area_fit_slice=slice(1,None)
area_fit_slice=slice(None)
p=np.polyfit(np.log(bin_centers[area_fit_slice][valid[area_fit_slice]]), log_area_pdf[area_fit_slice][valid[area_fit_slice]], 1)
area_pdf_fit = np.exp(p[1])*bin_centers**p[0]
plt.figure()
plt.plot(bin_centers[area_fit_slice],area_pdf_fit[area_fit_slice],'r-',label=f'fit: PDF(area)={np.exp(p[1]):3.2f}*area**{p[0]:3.2f}')
plt.plot(bin_centers, area_pdf, 'b-', label='PDF(area)')

plt.title('Probability density of Area Values')
plt.xlabel('Area')
plt.ylabel('Probability density')
plt.yscale('log')
plt.xscale('log')
plt.legend()
pltshow()
