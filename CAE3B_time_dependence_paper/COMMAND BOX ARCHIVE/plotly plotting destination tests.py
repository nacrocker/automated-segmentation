#demof plotly plotting in OMFIT
import site
site.main()
#import sys
#print(sys.path)

#import plotly.io as pio
#pio.renderers.default = "browser"
import kaleido
import plotly.express as px
doPDF=True
doPDFinTree=True
doBrowser=False # not going to work from portal

# List arguments
fig = px.line(x=[1, 2, 3, 4], y=[3, 5, 4, 8])
#fig.show()
if doBrowser:
    plotfile="/u/ncrocker/omfit_plot.html"
    plotlink=OMFITwebLink('file://'+plotfile)
    fig.write_html(plotfile)
    plotlink.run()

if doPDF:
    if doPDFinTree:
        omfit_plot=OMFITpath("omfit_plot.pdf")
        plotfile=omfit_plot.filename
    else:
        plotfile="/u/ncrocker/omfit_plot.pdf"
    fig.write_image(plotfile,format='pdf')
    OMFITx.Open(plotfile)
