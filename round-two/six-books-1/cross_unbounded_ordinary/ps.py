"""Exact local corroboration of the ordinary unbounded-edge P/S obstruction.

Local necessary projections corroborate the separately written argument.
The whole-shell theorem additionally uses the C and terminal components.
"""
import sys,time,json,hashlib
from pathlib import Path
from itertools import product
import literal as L,reference as R
start=time.monotonic()
def require(t,m):
    if not t:raise ValueError(m)
def guard():
    if time.monotonic()-start>30:raise RuntimeError('30s guard; incomplete')
def digest(x):return hashlib.sha256((json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()).hexdigest()
def core(r,rows,sy,e=(0,0,0)):
    red,d,q=L.build(r,rows,sy,e);bits,bd,bq=R.build(r,rows,sy,e)
    require(tuple(sum(1<<j for j in a) for a in red)==bits and d==bd and q==bq,'whole old-label/coordinate core')
    caps=L.allowances(red,d);require(caps==R.allowances(bits,bd),'all120 physical allowances')
    return red,d,q,caps
mixed=((0,4),(0,5),(1,2),(1,3))
def covers(w):return all(w>>i&1 or w>>j&1 for i,j in mixed)

# Every possible local D pair, allowing unprescribed T2 membership.
cells=[]
for i,j in mixed:
    other=1-i
    for di,dj in product(range(32),repeat=2):
        if not 1<=di.bit_count()<=4 or dj.bit_count()>3:continue
        words=[((1<<other) if k==2 else 0)|(1<<i if di>>k&1 else 0)|(1<<j if dj>>k&1 else 0) for k in range(5)]
        red,d,q,cap=core(0,tuple(words[2:]),tuple(words[:2]))
        qi,qj=7-di.bit_count(),6-dj.bit_count();known=1+(di&dj).bit_count()
        require((q[3+i],q[3+j])==(qi,qj) and len(red[3+i]&red[3+j])==known,'generic mixed local pages/ranks')
        possible=known+qi+qj-6<=3
        require(possible==((di|dj)==31),'complete mixed Q-union bridge')
        if possible:require(known+qi+qj-6==3,'mixed Q union tight')
        cells.append([i,j,di,dj,qi,qj,known,possible])
require(len(cells)==3120,'whole mixed local domain')
guard()

# T2 Q floor3 and SX red-spine caps give rank+own-intersection <=4.
allowed=[(q,w) for q,w in product(range(3,7),range(64)) if covers(w) and all(q+(w&own).bit_count()<=4 for own in R.OWN)]
require([w for q,w in allowed if q==4]==[L.C] and not any(q>=5 for q,w in allowed),'rank-four T2 is C; larger ranks impossible')
proper=[w for q,w in allowed if q==3 and w not in (L.C,L.P,L.S)]
require(len(proper)==8 and all(w&L.C==L.C for w in proper),'whole proper-C-superset domain')
supercuts=[]
for w in proper:
    leaf=next(i for i in range(2,6) if w>>i&1);z=9 if leaf in (3,5) else 10
    _,_,q,c=core(0,(L.C,L.C,w),(0,0))
    require(q[z]+q[15]-6==c[z,15]==1,'proper supersets force SX/T2 union')
    require(c[z,3+leaf]<=1 and c[15,3+leaf]<=1,'two red point allowances at most1')
    supercuts.append([w,leaf,z,c[z,3+leaf],c[15,3+leaf],3])

# On the two P leaves, a-X and a tight union force one incidence pattern.
# Center bits in the filler T0/T1 rows do not enter these particular spines;
# the written proof derives their membership later, from mixed covers.
own=[]
for r,x in product((0,1),(2,3)):
    records=[];accepted=[]
    for u,v,t0,t1 in product((0,1),repeat=4):
        _,_,q,c=core(r,(L.C|(t0<<x),L.C|(t1<<x),L.P),(u<<x,v<<x))
        z=10 if x==2 else 9
        require(c[z,15]==q[z]+q[15]-6==1,'P SX/T2 covering Q pair')
        if c[2,3+x]>=0:
            require(q[3+x]>=3,'blue a-X supplies Q-rank floor')
            if q[3+x]<=c[z,3+x]+c[15,3+x]:accepted.append([u,v,t0,t1,q[3+x]])
        records.append([u,v,t0,t1,q[3+x],c[2,3+x],c[z,3+x],c[15,3+x]])
    want=[0,1,int((x==3) != bool(r)),int((x==2) != bool(r)),3]
    require(accepted==[want],'whole own-leaf incidence forcing')
    own.append({'r':r,'leaf':x,'accepted':accepted,'records':len(records),'sha256':digest(records)})

# SY1 must be L or L+1; its red T spines force both T0/T1 centers.
vrows=[w for w in range(64) if covers(w) and w>>2&1 and w>>3&1 and not w&1]
require(vrows==[60,62],'whole SY1 mixed-cover alternatives')
trows=[]
for v in vrows:
    A=[w for w in range(64) if covers(w) and w>>3&1 and not (w>>2&1) and (w&v).bit_count()<=2]
    D=[w for w in range(64) if covers(w) and w>>2&1 and not (w>>3&1) and (w&v).bit_count()<=2]
    require(all(w&L.C==L.C for w in A+D) and bool(A) and bool(D),'both T rows contain C')
    trows.append([v,A,D])

# Every q in SY1-Q is outside T2-Q and hence red to BOTH SX points.
# Test the entire scalar box using literal known page counts and actual D.
scalar=[];survivors=[]
for s0,tword,cword,lword,h,beta in product(range(2),range(4),range(4),range(16),range(6),range(2)):
    n={1,9,10,12}|({11} if s0 else set())
    n|={13+i for i in range(2) if tword>>i&1}
    n|={3+i for i in range(2) if cword>>i&1}
    n|={5+i for i in range(4) if lword>>i&1}
    s=1+s0;t=tword.bit_count();centers=cword.bit_count();leaves=lword.bit_count();D=len(n)+h
    red,d,q,_=core(0,(11,7,L.P),(L.C,60|(beta<<1)))
    require(len(red[1]&n)==s and len(red[2]&n)==3+s+t,'physical v/a known page formulas')
    sy_known=len(red[12]&n)
    require(sy_known==1+t+leaves+beta*((cword>>1)&1),'physical SY1 page formula')
    possible=(s+t+h>=4 and s+h<=3 and sy_known<=3 and 3+s+t<=D-5)
    scalar.append([s0,tword,cword,lword,h,beta,D,possible])
    if possible:
        require((s,t,centers,leaves,h,beta,D)==(1,1,2,1,2,0,10),'complete scalar equality classification')
        ti=13 if tword==1 else 14;sx=10 if ti==13 else 9
        witness=[3,4,sx,12]
        require(len(set(witness))==4 and all(i in red[ti]&n for i in witness),'four literal red pages on Ti-q')
        bits,_,_=R.build(0,(11,7,L.P),(L.C,60))
        require(all(bits[ti]>>i&1 for i in witness),'four-page independent coordinate corroboration')
        survivors.append({'parameters':[s0,tword,cword,lword,h,beta,D],'four_red_pages':witness})
guard();require(len(scalar)==6144 and len(survivors)==8,'entire q box, not a sample')

transports=[]
for e0,e1,which in product(range(4),range(5),('phi','psi')):
    e=(e0,e1,0);a,d,q,_=core(0,(L.H,L.K,L.P),(L.C,L.L),e);p=R.permutation(which)
    b,nd,nq,_=core(int(which=='psi'),tuple(R.transport(w,p) for w in (L.H,L.K,L.P)),tuple(R.transport(w,p) for w in (L.C,L.L)),e)
    require(all(b[p[i]]=={p[j] for j in a[i]} and nd[p[i]]==d[i] and nq[p[i]]==q[i] for i in range(16)),'whole P/S/r variable-rank transports')
    transports.append([e,which])
out={'agent':'six-books-1','role':'researcher','complete':True,
     'status':'Exact local corroboration of the ordinary P/S obstruction without an edge bound',
     'scope':'Full mixed-edge/T2-row cover and ordinary P/S obstruction; C-row and terminal components are separate',
     'mixed_cells':[len(cells),sum(x[-1] for x in cells),digest(cells)],'T2_rank_row_candidates':allowed,
     'proper_C_supercuts':supercuts,'own_leaf_cells':own,'SY1_rows':vrows,'T_center_rows':trows,
     'scalar_box':[len(scalar),digest(scalar)],'eight_scalar_configurations_all_fail_four_red_pages':survivors,
     'whole40_variable_P_S_frame_transports':[len(transports),digest(transports)]}
raw=(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n').encode()
Path(sys.argv[1]).write_bytes(raw)
print(json.dumps({'complete':True,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'seconds':time.monotonic()-start}))
