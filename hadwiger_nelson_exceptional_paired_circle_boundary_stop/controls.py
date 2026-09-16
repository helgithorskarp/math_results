"""Enclosure boundary cases, generator algebra, and semantic certificate damage."""
import copy,json
from fractions import Fraction as Q
import verify as V
import geometry as G
from itertools import product
# Producer square extraction checked on every square of a bounded rational grid.
count=0
for a,b in product(range(-4,5),repeat=2):
 x=G.k(Q(a,3),Q(b,5));sq=G.mul(x,x);y=G.square_root(sq)
 V.need(y is not None and G.mul(y,y)==sq and G.sign(y)>=0,'exact square extraction');count+=1
for q in [G.k(2),G.k(0,1),G.k(5,1)]:V.need(G.square_root(q) is None,'nonsquare control')
for x in [Q(0),Q(1),Q(2),Q(1)+Q(1,V.DEN),Q(1)-Q(1,V.DEN)]:
 lo,hi=V.sqrt_interval((x*x,x*x));V.need(lo<=x<=hi,'outward sqrt at exact/near boundary')
V.need(V.square((Q(-1),Q(1)))==(0,1),'interval square across zero')
geo=json.loads((V.HERE/'geometry_certificate.json').read_text());cert=json.loads((V.HERE/'certificate.json').read_text());V.verify(geo,cert)
bad=[]
for key,value in [('four_word','0'*cert['vertices']),('four_word',cert['four_word'][:-1]),('five_word',cert['four_word']),('coordinate_sha256','0'*64),('edge_sha256','0'*64),('edges',cert['edges']-1)]:
 c=copy.deepcopy(cert);c[key]=value;bad.append((geo,c))
x=copy.deepcopy(geo);x['points'].append(x['points'][0]);bad.append((x,cert))
x=copy.deepcopy(geo);x['points'][0][2]=len(x['roots']);bad.append((x,cert))
x=copy.deepcopy(geo);x['roots'][0]=[[-1,1],[0,1]];bad.append((x,cert))
x=copy.deepcopy(geo);x['points'][0][0][0][0][1]=0;bad.append((x,cert))
# Remove an actual non-kernel point; update hash/count/words to test geometric
# completeness, rather than merely a checksum mismatch.
x=copy.deepcopy(geo);i=next(i for i,p in enumerate(x['points']) if p[2]>=0);x['points'].pop(i);c=copy.deepcopy(cert);c['vertices']-=1;c['coordinate_sha256']=V.digest(x)
for key in ('four_word','five_word'):c[key]=c[key][:i]+c[key][i+1:]
bad.append((x,c))
reasons=[]
for x,c in bad:
 try:V.verify(x,c)
 except ValueError as e:reasons.append(str(e))
V.need(len(reasons)==len(bad),'all corruptions rejected')
V.need('complete boundary intersection count' in reasons,'omitted-root completeness rejection')
print(json.dumps({'verified':True,'square_extraction_controls':count,'known_nonsquares':3,'sqrt_enclosure_boundary_controls':5,'interval_square_zero_crossing':True,'corruptions_rejected':len(reasons),'rejection_reasons':reasons},indent=2,sort_keys=True))
