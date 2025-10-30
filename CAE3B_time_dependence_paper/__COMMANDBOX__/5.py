def s_func(lc, A):
    return A * np.exp(4 * lc)
def r_func(lc,A):
    return A / np.exp(4 * lc)

max_log_contrast = 10
max_area = 100
total_area = OMFIT['commandBox']['out_nc']['total_area']
total_log_contrast = OMFIT['commandBox']['out_nc']['total_log_contrast']


max_plot_a = np.exp(10)
max_plot_lc = 10/4

max_plot_lc = np.min([max_log_contrast,max_plot_lc])
max_plot_a = np.min([max_area,max_plot_a])

max_plot_range=np.min([max_plot_lc*4,np.log(max_plot_a)])
max_plot_a = np.exp(max_plot_range)
max_plot_lc = max_plot_range/4

lc_range=(0.1, max_log_contrast)
a_range=(2, max_area)
log_r_range= [-5,5]

lc_param = np.linspace(0, max_plot_lc, 100)
a_param = np.linspace(1, max_plot_a, 100)
lcg, ag = meshgrid(lc_param, a_param) # grid of point
Sg = s_func(lcg, ag) # evaluation of the function on the grid

#Using "4*log(contrast)" for x variable because 2D hist shows heavy concnetration around log(area) = 4*log(contrast)
n_bins_a_plot = 50
n_bins_r_plot = 50
plt.figure()
plt.hist2d(np.log(total_area),np.log(total_area)-4*np.array(total_log_contrast),  bins=(n_bins_a_plot,n_bins_r_plot), cmap='viridis', range=[np.log(a_range),log_r_range],  norm=matplotlib.colors.LogNorm())
plt.colorbar()

OMFITx.End()
# testing various power relations for area vs log contrast  no surprise that for lc0 = 0.25, plotted line is "y=x"
lc0_all = [0.25]
for lc0 in lc0_all: 
    area_curve = np.exp(lc_param/lc0)
    plt.plot(4 * lc_param, np.log(area_curve), 'r-', label='Area Curve')

mlev=np.log(s_func(max_plot_lc,max_plot_a))
print(mlev)
cset = contour(4*lc_param, np.log(a_param), np.log(Sg), np.arange(1, np.ceil(mlev)),linewidths=2,cmap=cm.Set2)
clabel(cset,inline=True,fmt='%1.1f',fontsize=10)

plt.title('2D Histogram of Contrast and Area')
plt.xlabel('4 * Log of Contrast')
plt.ylabel('Log of Area')
plt.xlim((0, 4*max_plot_lc))
plt.ylim((0, np.log(max_plot_a)))