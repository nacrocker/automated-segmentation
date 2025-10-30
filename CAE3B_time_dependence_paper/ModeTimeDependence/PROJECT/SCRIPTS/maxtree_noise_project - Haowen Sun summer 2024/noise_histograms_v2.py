#Created by Haowen Sun, Sept. 25, 2024

import numpy as np
from scipy.signal import chirp
import matplotlib.pyplot as plt
from scipy.signal import stft
from skimage.morphology import max_tree
from matplotlib.colors import LogNorm

def make_noise(mean, std, shape, noise_generator = np.random.normal):
    return noise_generator(mean, std, t.shape)

def make_siglist(t, modedescs = None, phisig = [0]):
    nsig=len(phisig)
    nt=len(t)
    siglist=[np.zeros((nt,),dtype=float) for _ in range(nsig)]

    if modedescs is None:
        return siglist

    for imd,md in enumerate(modedescs):
            amp,f0,f1,it0,ntch,nmode=(md[k] for k in ['amp','f0','f1','it0','ntch','nmode'])
            envl=np.blackman(ntch)     # window function
            for isig,phi in enumerate(phisig):
                siglist[isig][it0:it0+ntch]+=amp*envl*chirp(t[it0:it0+ntch], f0, t[it0+ntch], f1, method='quadratic', phi=phi, vertex_zero=True)

    return siglist


def calculate_contrast(image, parent = None, sorted_indices = None):

    image_rav = image.ravel()
    p_root = sorted_indices[0]
    out = image_rav.copy()

    for p in sorted_indices[::-1]:
        if p==p_root:
            continue
        q = parent[p]
        out[q] = max(out[p], out[q])  # search maximum and propagate maximum to parent node


    contrast = np.zeros(len(image_rav), dtype=np.float64)
    for idx in range(len(image_rav)):
        if image_rav[idx] != 0:
            contrast[idx] = out[idx] / image_rav[idx] #compute the ratio

    #print(f'contrast maximal= {np.max(contrast)}')
    return contrast, out

def calculate_area(image, parent = None, sorted_indices = None):

    image_rav = image.ravel()
    p_root = sorted_indices[0]
    area = np.ones(len(image_rav), dtype=np.float64)

    for p in sorted_indices[::-1]:
        if p==p_root:
            continue
        q = parent[p]
        area[q] += area[p]

    return area


###Generating Histograms###

t=np.arange(0,1024/1000,0.001)
phisig=[0]#,0.1,0.5,np.pi/2]
nsig=len(phisig)
nt=len(t)
n_tries=1
fs=1/(t[1]-t[0])
fN = fs/2
nfft=int(np.ceil(np.sqrt(nt)))
n_bins = 50
contrast_cum = np.zeros(n_bins)
area_cum = np.zeros(n_bins)
max_log_contrast = 10
max_area = 100
noise_mean=0
noise_std=0.001
total_area=[]
total_log_contrast=[]
amp1 = 2
amp2 = 1.5
f0_1 = 0.3 * fN
f0_2 = 0.15 * fN
f1_1 = 0.9 * fN
f1_2 = 0.7 * fN
it0_1 = int(nt / 16)
it0_2 = int(nt / 8)
ntch1 = int(nt * 3 / 4)
ntch2 = int(nt * 3 / 4)

modedescs = [
        dict(amp=amp1, f0=f0_1, f1=f1_1, it0=it0_1, ntch=ntch1, nmode=1),
        dict(amp=amp2, f0=f0_2, f1=f1_2, it0=it0_2, ntch=ntch2, nmode=2),
    ]



for _ in range(n_tries):
    noise = make_noise(noise_mean, noise_std, t.shape)
    siglist = make_siglist(t, modedescs=modedescs, phisig=[0])
    #data = noise
    data = siglist[0]

    fstft,tstft, sigstft=stft(data,fs,nperseg=nfft,noverlap=None)

    P, S = max_tree(abs(sigstft),connectivity=1)

    area = calculate_area(abs(sigstft), parent=P.ravel(), sorted_indices = S)
    contrast, out = calculate_contrast(abs(sigstft), parent=P.ravel(), sorted_indices = S)

    total_area.extend(area)
    total_log_contrast.extend(np.log(contrast))

    hist_contrast, bin_edges_contrast = np.histogram(np.log(contrast), bins=n_bins, density=False, range=(0, max_log_contrast))
    hist_area, bin_edges_area = np.histogram(area, bins=n_bins, density=False, range=(0, max_area))
    contrast_cum += hist_contrast
    area_cum += hist_area

def pltshow():
    pass

plt.figure()
im1=plt.imshow(abs(sigstft),aspect='auto',origin='lower',cmap='plasma')

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

lc_param = np.linspace(0, max_log_contrast, 100)
a_param = np.linspace(1, max_area, 100)
lcg, ag = meshgrid(lc_param, a_param) # grid of point
S = s_func(lcg, ag) # evaluation of the function on the grid
y_param = np.linspace(0, 4 * max_log_contrast, 100)
yg, ag = meshgrid(y_param, a_param)
Sy = s_func(yg/4, ag)

plt.figure()
plt.hist2d(4 * np.array(total_log_contrast), np.log(total_area), bins=(n_bins, n_bins), cmap='viridis', range=[(4 * 0.1, 4 * max_log_contrast), np.log([2, max_area])],  norm=LogNorm())
plt.colorbar()

lc0_all = [0.25]
for lc0 in lc0_all:
    area_curve = np.exp(lc_param/lc0)
    plt.plot(4 * lc_param, np.log(area_curve), 'r-', label='Area Curve')

cset = contour(y_param, np.log(a_param), np.log(Sy), np.linspace(1, 9, 9),linewidths=2,cmap=cm.Set2)
clabel(cset,inline=True,fmt='%1.1f',fontsize=10)

plt.title('2D Histogram of Contrast and Area')
plt.xlabel('4 * Log of Contrast')
plt.ylabel('Log of Area')
plt.xlim((0, 5))
plt.ylim((0, 5))


#print(np.log(total_area
#print(total_area[0:2])

plt.figure()
S_ravel = S.ravel()
S_hist, bin_edges = np.histogram(S_ravel, bins=100, density=True)
#S_pdf = S_hist / (S_ravel.size)
S_pdf = S_hist # use density = True, then no need normalization
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
print('S_pdf=',len(S_pdf))

p_S=np.polyfit(np.log(bin_centers[1:len(bin_centers)-30]), np.log(S_pdf[1:len(S_pdf)-30]), 1)
S_pdf_fit = np.exp(p_S[1])*bin_centers**p_S[0]
plt.plot(bin_centers[1:len(bin_centers)-30], S_pdf_fit[1:len(S_pdf_fit)-30], 'r-', label=f'fit: PDF(S)={np.exp(p_S[1]):3.2f}*S**{p_S[0]:3.2f}')
plt.plot(bin_centers, S_pdf, 'b-', label='S Probability density')
plt.title('Probability density of S Values')
plt.xlabel('S')
plt.ylabel('Probability density')
plt.yscale('log')
plt.xscale('log')
plt.legend()
pltshow()

plt.figure()
plt.hist(S_ravel, bins = 100, density = True)
plt.yscale('log')
plt.xscale('log')
plt.plot
pltshow()

bin_centers = (bin_edges_area[:-1] + bin_edges_area[1:]) / 2
p=np.polyfit(np.log(bin_centers[1:]), np.log(area_pdf[1:]), 1)

area_pdf_fit = np.exp(p[1])*bin_centers**p[0]
plt.figure()
plt.plot(bin_centers[1:],area_pdf_fit[1:],'r-',label=f'fit: PDF(area)={np.exp(p[1]):3.2f}*area**{p[0]:3.2f}')
plt.plot(bin_centers, area_pdf, 'b-', label='PDF(area)')

plt.title('Probability density of Area Values')
plt.xlabel('Area')
plt.ylabel('Probability density')
plt.yscale('log')
plt.xscale('log')
plt.legend()
pltshow()
