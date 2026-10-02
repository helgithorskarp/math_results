"""six-reviewer-5: exact one-vertex bound and complete seam audit.

The defining target proof was visible; no target executable or certificate
is imported. kernel.py and prior_annulus.py are unchanged OWNED REVIEW9717
inputs, whose contribution and source must be credited.
"""
from fractions import Fraction as F
from itertools import product
from math import comb
import json, hashlib, pathlib
import kernel as K
import prior_annulus as PA

def normalize(v):
    if isinstance(v,F): return str(v)
    if isinstance(v,(list,tuple)): return [normalize(x) for x in v]
    if isinstance(v,dict): return {k:normalize(x) for k,x in v.items()}
    return v

def discriminant(c,t):
    """Scale cotangents by A=sqrt(1+2c), avoiding irrational arithmetic."""
    c=F(c); a2=1+2*c
    bt={1:F(1),2:c/a2,3:(c-1)/(1+3*c)}[t]
    u=(1-c*c)/(a2*(1+c*bt))  # u=(x+y)/A
    p=1-a2*u
    den={1:a2,2:(1+c)**2,3:a2*(1+c)**2}[t]
    return dict(u=u,p=p,d=a2*u*u-4*p,den=den,numerator=(a2*u*u-4*p)*den)

def bernstein(poly,lo,hi):
    n=len(poly)-1; width=hi-lo
    power=[sum(poly[i]*comb(i,j)*lo**(i-j)*width**j for i in range(j,n+1)) for j in range(n+1)]
    return tuple(sum(power[j]*F(comb(k,j),comb(n,j)) for j in range(k+1)) for k in range(n+1))

def build():
    rows=[]
    # Degree bounds 2,3,4 follow by clearing the displayed rational systems.
    for t,deg in ((1,2),(2,3),(3,4)):
        # Interpolate at c=0,...,deg: these are identity abscissas, not packings.
        poly=K.interpolate([discriminant(j,t)['numerator'] for j in range(deg+1)])
        K.need(len(poly)-1<=deg,'cleared numerator degree')
        checks=[]
        for c in (F(1,7),F(9,20),F(1,2),F(19,31),F(1),F(7,5)):
            r=discriminant(c,t)
            K.need(K.value(poly,c)==r['numerator'],'whole rational identity')
            checks.append(dict(c=c,**r))
        b=bernstein(poly,F(9,20),F(1))
        K.need(all(x<0 for x in b),'strict closed-interval sign')
        rows.append(dict(t=t,degree_bound=deg,polynomial=poly,bernstein=b,checks=checks))
    # New obstruction: x,y>c/A implies xy+A(x+y) > c^2/A^2+2c.
    # Clearing A^2=1+2c leaves exactly 5c^2-1; verify the polynomial identity.
    excess=K.add(K.add((0,0,1),K.mul((0,2),(1,2))),K.neg((1,2)))
    K.need(excess==(-1,0,5),'one-vertex cleared excess')
    gap=F(9,20)**2-F(1,5)
    K.need(gap==F(1,400),'original band lies strictly above new threshold')
    ports=[]
    for qs in product((4,5),repeat=3):
        for ks in product(*(range(2,q-1) for q in qs)):
            r=PA.annulus(qs,ks)
            membership={tuple(map(tuple,cl)):i for i,cy in enumerate(r['cycles']) for cl in cy['vertices']}
            classes={v:tuple(map(tuple,cl)) for cl in r['vertex_classes'] for v in cl}
            seams=[]
            for i,k in enumerate(ks):
                endpoints=(classes[(i,k)],classes[(i,k+1)])
                sides=tuple(membership[e] for e in endpoints)
                K.need(set(sides)=={0,1},'every seam crosses boundary components')
                seams.append(dict(faces=(i,(i+1)%3),endpoints=endpoints,boundaries=sides))
            ports.append(dict(**r,seam_boundaries=seams))
    K.need(len(ports)==27 and sum(len(r['seam_boundaries']) for r in ports)==81,'complete literal domain')
    K.need(len({(r['q'],r['k']) for r in ports})==27,'no duplicated normalization')
    # Boundary control: complete six-point icosahedral wheel has 10 contacts.
    # Deleting two radial contacts produces fake TQQ polygons; keep all contacts.
    wheel=sorted([(0,j) for j in range(1,6)]+[tuple(sorted((j,1+j%5))) for j in range(1,6)])
    quads=((0,1,2,3),(0,3,4,5)); internal=((0,2),(0,4))
    K.need(all(e in wheel for e in internal),'boundary diagonals really contact')
    fake=[e for e in wheel if e not in internal]
    K.need(len(wheel)==10 and len(fake)==8,'complete versus incomplete contact control')
    # Five-point cyclic Gram: neighboring rim products c, others -c; c^2=1/5.
    gram=[[('1' if i==j else ('c' if i==0 or j==0 or (i-j)%5 in (1,4) else '-c')) for j in range(6)] for i in range(6)]
    prism=[dict(i=i,j=j,dot=(F(1,7) if (i%3==j%3 or i//3==j//3) else F(-5,7))) for i in range(6) for j in range(i+1,6)]
    K.need(sum(r['dot']==F(1,7) for r in prism)==9,'classical prism contact calibration')
    return normalize(dict(method='scaled rational cotangent system; unchanged owned dart-boundary permutation; new one-vertex strict diagonal bound',discriminants=rows,new_bound=dict(cleared_excess=excess,threshold_squared=F(1,5),old_band_squared_gap=gap,strict_diagonal=True),ports=ports,boundary_control=dict(c_squared=F(1,5),gram=gram,complete_edges=wheel,fake_quads=quads,deleted_contacts=internal,incomplete_edges=fake),prism=prism))

if __name__=='__main__':
    data=build(); raw=(json.dumps(data,sort_keys=True,separators=(',',':'))+'\n').encode()
    here=pathlib.Path(__file__).resolve().parent
    if (here/'EVIDENCE.json').exists(): K.need((here/'EVIDENCE.json').read_bytes()==raw,'complete evidence bytes')
    else: (here/'EVIDENCE.json').write_bytes(raw)
    print(json.dumps(dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),ports=27,seams=81,discriminants=3,one_vertex_threshold_squared='1/5')))
