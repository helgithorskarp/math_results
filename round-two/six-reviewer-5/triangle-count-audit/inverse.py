"""Fresh literal deleted-W inverse energies; stdlib only, own data only."""
import json,pathlib,argparse
from fractions import Fraction as F

def need(ok,why):
    if not ok:raise ValueError(why)

def value(p,h,q):
    def ev(a):return sum(F(c)*h**i*q**j for (i,j),c in a)
    return ev(p['num'])/ev(p['den'])

def solve(a,b):
    a=[list(row)+[z] for row,z in zip(a,b)];n=len(a)
    for i in range(n):
        j=next((j for j in range(i,n) if a[j][i]),None);need(j is not None,'deleted W invertible')
        a[i],a[j]=a[j],a[i];pivot=a[i][i];a[i]=[x/pivot for x in a[i]]
        for j in range(n):
            if j!=i:
                t=a[j][i];a[j]=[x-t*y for x,y in zip(a[j],a[i])]
    return [row[-1] for row in a]

def check(primary,h,q,damage=None):
    h=F(h);q=F(q);hh=int(h);need(h==hh and h>=2 and q>=4,'exact physical/auxiliary control domain')
    alH,beH,alL,beL,nu,muL=[value(p,h,q) for p in primary['scalars']]
    muH=((h-1)*nu+muL/h)/h
    n=3*(hh+1);W=[[F(0)]*n for _ in range(n)]
    coefficients=[(F(1,2),F(-1,2)),(F(-1,2),F(-1,2)),(F(0),F(1))]
    for i in range(n):
        fi,li=divmod(i,3)
        for j in range(n):
            fj,lj=divmod(j,3)
            mean=(muH if fi==fj else (muL/h-muH)/(h-1)) if fi<hh and fj<hh else (muL if fi==fj else -muL/h)
            if fi==fj:
                al,be=(alH,beH) if fi<hh else (alL,beL)
                mean+=al*coefficients[li][0]*coefficients[lj][0]+be*coefficients[li][1]*coefficients[lj][1]
            W[i][j]=mean
    need(all(sum(row)==0 for row in W),'full W constant kernel')
    b=[F(i<3) for i in range(n-1)]
    if damage=='wrong-triple':b[2]=F(0)
    x=solve([row[:-1] for row in W[:-1]],b)
    energy=sum(z*t for z,t in zip(b,x));formula=(h-1)/(h*nu)+1/muL+4/beL
    need(energy==formula,'whole deleted inverse energy')
    xx=x+[F(0)];bb=b+[F(-3)]
    need([sum(z*t for z,t in zip(row,xx)) for row in W]==bb,'full zero-extension inverse equation')
    return dict(h=hh,q=str(q),deleted_dimension=n-1,kappa=str(formula),full_equation=True)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('primary',type=pathlib.Path);ap.add_argument('--damage');a=ap.parse_args();p=json.loads(a.primary.read_text())
    print(json.dumps([check(p,h,F(q),a.damage) for h,q in [(2,4),(3,4),(4,4),(10,4),(3,16),(3,'9/2')]],sort_keys=True,separators=(',',':')))
if __name__=='__main__':main()
