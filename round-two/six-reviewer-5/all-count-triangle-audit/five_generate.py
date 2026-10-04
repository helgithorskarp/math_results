"""Fresh exact leading pivots over QQ(u,v,w), not author certificate replay.

Variable order (u,v,w), lexicographic, characteristic zero. l=2+v,
h=3+u+v, q=3h+w. Entire polynomial coefficient records are portable.
"""
import argparse,hashlib,json,pathlib,sys,time
from sympy.polys.domains import QQ
from sympy import symbols
from forms import build,need

U,V,W=symbols('u v w');F=QQ.frac_field(U,V,W);u,v,w=F.gens
def poly(p):return [[list(m),str(c)] for m,c in sorted(p.to_dict().items())]
def rat(x):return {'n':poly(x.numer),'d':poly(x.denom)}
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',required=True);args=parser.parse_args()
    h=3+u+v;l=2+v;q=3*h+w
    # Five-block reconstruction needs no residual mu/generic field calculations.
    s=q+3*h;d=h-l;ell=3*(h+l)+1;N=2*q+6*(h+l);D=3*h
    G=[4*(q-1),4*D,2*D*(q-2),2*q*D,s*d/(3*h*l)]
    S=[[F.zero for _ in G] for _ in G]
    def outer(x,c=1):
        for i in range(5):
            for j in range(5):S[i][j]+=c*x[i]*x[j]
    for ix,iy,count in ((0,0,q/2-1),(1,0,q/2),(0,1,q/2),(1,1,q/2-1)):
        coord=[1/(2*(q-1)),F.zero,(1-ix-iy)/(q-2),(iy-ix)/q,F.zero]
        outer([G[i]*coord[i] for i in range(5)],count)
    outer([-G[0]/2,G[1]/2,F.zero,F.zero,F.zero])
    outer([F.zero,-2,q-2,q,F.zero],3*h)
    outer([F.zero,-2,q-2,-q,G[4]],3*l)
    outer([-2*(q-1),6*l,-3*(q-2)*(h+l),-3*q*d,-s*d/h],1/ell)
    A=[[(N-1 if i==j else 0)-S[i][j]/G[i] for j in range(5)] for i in range(5)]
    record={'domain':'QQ(u,v,w); order lex; l=2+v,h=3+u+v,q=3h+w',
            'entries':[[rat(x) for x in row] for row in A], 'stages':[], 'pivots':[]}
    B=[row[:] for row in A]
    for i in range(5):
        pivot=B[i][i];need(pivot!=0,'nonzero exact rational pivot')
        # Positivity is checked on every coefficient, not a sample.
        for pp in (pivot.numer,pivot.denom):
            dd=pp.to_dict();need(dd.get((0,0,0),0)>0 and all(c>=0 for c in dd.values()),'positive shifted pivot')
        record['pivots'].append(rat(pivot));updates=[]
        for j in range(i+1,5):
            for k in range(i+1,5):
                new=B[j][k]-B[j][i]*B[i][k]/pivot
                updates.append({'j':j,'k':k,'value':rat(new)})
        record['stages'].append({'column':[rat(B[j][i]) for j in range(i+1,5)],
                                 'row':[rat(B[i][k]) for k in range(i+1,5)],'updates':updates})
        for item in updates:B[item['j']][item['k']]=B[item['j']][item['k']]-B[item['j']][i]*B[i][item['k']]/pivot
        print('completed exact pivot '+str(i+1),flush=True)
    data=(json.dumps(record,sort_keys=True,separators=(',',':'))+'\n').encode();pathlib.Path(args.out).write_bytes(data)
    print(json.dumps(dict(bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),pivots=5,ordered_updates=30,
                         pivot_terms=[len(p['n']) for p in record['pivots']])))
if __name__=='__main__':main()
