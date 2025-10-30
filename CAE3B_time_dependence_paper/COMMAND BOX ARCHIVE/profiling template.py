#profiling prep
def print_cProfile_stats(pr):
    import pstats, io
    from pstats import SortKey
    s = io.StringIO()
    sortby = SortKey.CUMULATIVE
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())

def start_cProfile():
import cProfile
pr = cProfile.Profile()
pr.enable()

#do code here

#profiling wrap up
pr.disable()
print_cProfile_stats(pr)



##profiling prep
#import cProfile, pstats, io
#from pstats import SortKey
#pr = cProfile.Profile()
#pr.enable()
#
##do code here
#
##profiling wrap up
#pr.disable()
#s = io.StringIO()
#sortby = SortKey.CUMULATIVE
#ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
#ps.print_stats()
#print(s.getvalue())
