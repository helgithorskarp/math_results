"""Complete actual-color rank/row projections for the corrected T2 forcing."""
from pathlib import Path
from itertools import combinations,product
import hashlib,json,os,sys,time
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[name]='1'
import literal as L,reference as R
start=time.monotonic()
def require(t,m):
    if not t:raise ValueError(m)
def guard():
    if time.monotonic()-start>30:raise RuntimeError('30s mathematical guard; incomplete, no exclusion')
def canonical(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def digest(x):return hashlib.sha256(canonical(x)).hexdigest()
mixed=((0,4),(0,5),(1,2),(1,3))
covers=[w for w in range(64) if all(w>>i&1 or w>>j&1 for i,j in mixed)]
def core(r,rows,sy,e=(0,0,0)):
    red,d,q=L.build(r,rows,sy,e);bits,bd,bq=R.build(r,rows,sy,e)
    require(tuple(sum(1<<j for j in a) for a in red)==bits and d==bd and q==bq,'whole literal/coordinate core')
    caps=L.allowances(red,d);require(caps==R.allowances(bits,bd),'all120 actual pair allowances')
    return red,d,q,caps
mixed=tuple(mixed)

def mixed_cover(w):return all(w>>i&1 or w>>j&1 for i,j in mixed)

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
allowed=[(q,w) for q,w in product(range(3,7),range(64)) if mixed_cover(w) and all(q+(w&own).bit_count()<=4 for own in R.OWN)]
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
for r,x,k0,k1 in product((0,1),(2,3),range(3,5),range(2,5)):
    records=[];accepted=[]
    for u,v,t0,t1 in product((0,1),repeat=4):
        _,_,q,c=core(r,(L.C|(t0<<x),L.C|(t1<<x),L.P),(u<<x,v<<x),(k0-3,k1-2,0))
        z=10 if x==2 else 9
        require(c[z,15]==q[z]+q[15]-6==1,'P SX/T2 covering Q pair')
        if c[2,3+x]>=0:
            require(q[3+x]>=3,'blue a-X supplies Q-rank floor')
            if q[3+x]<=c[z,3+x]+c[15,3+x]:accepted.append([u,v,t0,t1,q[3+x]])
        records.append([u,v,t0,t1,q[3+x],c[2,3+x],c[z,3+x],c[15,3+x]])
    want=[0,1,int((x==3) != bool(r)),int((x==2) != bool(r)),3]
    require(accepted==[want],'whole own-leaf incidence forcing')
    own.append({'r':r,'leaf':x,'T_Q':[k0,k1,3],'accepted':accepted,'records':len(records),'sha256':digest(records)})

U=[w for w in covers if not(w>>2&1 or w>>3&1)]
V=[w for w in covers if w>>2&1 and w>>3&1]
A=[w for w in covers if w>>3&1 and not(w>>2&1)]
D=[w for w in covers if w>>2&1 and not(w>>3&1)]
require([len(z) for z in (U,V,A,D)]==[5,10,5,5],'full valid own-leaf/mixed-cover domains')
records=[];survivors=[];pairpass=[]
for u,v,a,d,k0,k1 in product(U,V,A,D,range(3,5),range(2,5)):
    n,degs,q=L.build(0,(a,d,L.P),(u,v),(k0-3,k1-2,0))
    b,bd,bq=R.build(0,(a,d,L.P),(u,v),(k0-3,k1-2,0))
    require(tuple(sum(1<<j for j in z) for z in n)==b and degs==bd and q==bq,'entire repaired-domain original16 model')
    caps=L.allowances(n,degs);require(caps==R.allowances(b,degs),'all actual colored allowances')
    cut=None
    for i,j in combinations(range(16),2):
        lower=max(0,q[i]+q[j]-6)
        if lower>caps[i,j]:cut=['pair',i,j,lower,caps[i,j]];break
    if cut is None:
        pairpass.append([u,v,a,d,k0,k1])
        for i,j in combinations(range(16),2):
            if q[i]+q[j]-caps[i,j]!=6:continue
            for k in range(16):
                if k in (i,j):continue
                if q[k]>caps[k,i]+caps[k,j]:
                    cut=['joint',i,j,k,q[k],caps[k,i],caps[k,j]];break
            if cut is not None:break
    key=[u,v,a,d,k0,k1]
    records.append([key,cut])
    if cut is None:survivors.append({'key':key,'degrees':degs,'Q_ranks':q,'known16':[sorted(z) for z in n]})
    guard()
require(len(records)==7500,'all full-domain P-row/rank combinations')
transports=[]
for e0,e1,which in product(range(4),range(5),('phi','psi')):
    e=(e0,e1,0);nn,dd,qq,_=core(0,(L.H,L.K,L.P),(L.C,L.L),e);p=R.permutation(which)
    nb,nd,nq,_=core(int(which=='psi'),tuple(R.transport(w,p) for w in (L.H,L.K,L.P)),
                  tuple(R.transport(w,p) for w in (L.C,L.L)),e)
    require(all(nb[p[i]]=={p[j] for j in nn[i]} and nd[p[i]]==dd[i] and nq[p[i]]==qq[i] for i in range(16)),
            'whole variable-rank P/S/r free-frame transport')
    transports.append([e,which]);guard()
n,d,q=L.build(0,(L.H,L.K,L.P),(L.C,L.L));c=L.allowances(n,d)
out={'agent':'six-books-1','role':'researcher','complete':True,
     'scope':'Exact local necessary projections for the stated shell; written reduction unformalized',
     'assumed_SY1_X0_blue':False,'assumed_SY1_Q_disjoint_T2_Q':False,
     'SY1_T2_is_red':15 in n[12],'literal_SY1_T2_known_pages':sorted(n[12]&n[15]),
     'literal_SY1_T2_actual_degrees':[d[12],d[15]],'literal_SY1_T2_Q_overlap_allowance':c[12,15],
     'full_domains':{'SY0':U,'SY1':V,'T0':A,'T1':D,'T0_Q':[3,4],'T1_Q':[2,3,4]},
     'mixed_cells':[len(cells),digest(cells)],'T2_rank_row_candidates':allowed,
     'proper_C_supercuts':supercuts,'all384_own_leaf_cells':own,'whole40_variable_P_S_frame_transports':transports,
     'all7500_first_exact_cuts':records,'whole_pair_survivors':pairpass,'whole_joint_survivors':survivors}
raw=canonical(out);p=Path(sys.argv[1]);p.write_bytes(raw)
print(json.dumps({'complete':True,'domain':len(records),'pair_survivors':len(pairpass),'joint_survivors':len(survivors),
 'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'seconds':time.monotonic()-start,
 'surviving_keys':[z['key'] for z in survivors]}))
