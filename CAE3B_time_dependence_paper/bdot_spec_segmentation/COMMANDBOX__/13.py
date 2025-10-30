import secrets
rsd=secrets.randbits(128)
rng=np.random.default_rng(rsd)
x=rng.random(10)
n=x.size
xav1=mean(x[:-1])
xvar1=mean((x[:-1]-xav1)**2)
dx1=(x[-1]-xav1)
xav1p = xav1 + dx1/n
xvar1p = (xvar1 + dx1**2/n)*(n-1)/n
xav=mean(x)
xvar=mean((x-xav)**2)
print(xav1p,xav)
print(xvar1p,xvar)

#x2av1=
#mean((x-x0)**2)=mean(x**2)+x0^2-2*mean(x)*x0
#xav=mean(x); xav1=mean(x[:-1]); x2av1=mean(x[:-1]**2); x2av=mean(x**2)
#dx1=x[-1]-xav1; dx21=x[-1]**2-x2av1
#xav = xav1 + dx1/n; 
#xav-x[1] = -dx1*(n-1)/n
#x2av = x2av1 + dx21/n
#xvar1 = x2av1 - xav1**2
#mean((x-xav)**2) = mean((x[:-1]-xav)**2)*(n-1)/n   + (x[-1]-xav)**2/n
#                 = [xvar1 + (xav1-xav)**2]*(n-1)/n + (x[-1]-xav)**2/n
#                 = xvar1*(n-1)/n + (dx1/n)**2*(n-1)/n + (dx1*(n-1)/n)**2/n
#                 = xvar1*(n-1)/n + dx1**2*[(n-1)/n**3 + (n-1)**2/n**3]
#                 = xvar1*(n-1)/n + (dx1/n)**2*(n-1)
#                 = [xvar1 + dx1**2/n)]*(n-1)/n
#                 = xvar1 + (dx1**2*(n-1)/n-xvar1)/n