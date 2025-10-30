def s_func(lc, A):
    return A * np.exp(4 * lc)
def r_func(lc,A):
    return A / np.exp(4 * lc)

def log_pdf_of_log_data_with_centers_and_fit(data,fitinds=slice(None),**kwargs):
    kwargs['density']=True
    pdf, bin_edges = np.histogram(np.log(np.array(data).ravel()), **kwargs)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    log_pdf = np.log(pdf)
    valid=np.isfinite(log_pdf)
    pfit=np.polyfit(bin_centers[fitinds][valid[fitinds]], log_pdf[fitinds][valid[fitinds]], 1)
    log_pdf_fit = pfit[1] + bin_centers*pfit[0]
    return log_pdf,bin_centers,log_pdf_fit,pfit

total_area = OMFIT['commandBox']['out_nc']['total_area']
total_log_contrast = OMFIT['commandBox']['out_nc']['total_log_contrast']

fitinds=slice(1,None)
nbins=100
data = r_func(np.array(total_log_contrast), np.array(total_area)) # evaluation of the function on the grid
log_pdf,bin_centers,log_pdf_fit,pfit=log_pdf_of_log_data_with_centers_and_fit(data,fitinds=fitinds,bins=nbins)

datalabel='R'
plt.figure()
plt.plot(bin_centers[fitinds], log_pdf_fit[fitinds], 'r-', label=f'fit: PDF(log({datalabel}))={pfit[1]:3.2f}+log({datalabel})*{pfit[0]:3.2f}')
plt.plot(bin_centers, log_pdf, 'b-', label=f'{datalabel} Probability density')
plt.title(f'Probability density of log({datalabel}) Values')
plt.xlabel(f'log({datalabel})')
plt.ylabel('Probability density')
plt.legend()