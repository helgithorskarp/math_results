"""Exact corroboration of the ordinary cycle-only finish, no graph imports."""
from itertools import product
from pathlib import Path
import argparse,hashlib,json,time

def bits(m):return frozenset(i for i in range(6) if m>>i&1)
def canonical(x):return json.dumps(x,separators=(',',':'))
start=time.monotonic()
cycle=(0,4,3,1,2,5)
edges=tuple((cycle[i],cycle[(i+1)%6]) for i in range(6))
minimum=(2,2,1,1,1,1)
own=(frozenset((3,5)),frozenset((2,4)))
sx_t=(frozenset((0,2)),frozenset((0,1)))
parser=argparse.ArgumentParser()
parser.add_argument('--projection',type=Path,required=True)
parser.add_argument('--out',type=Path,required=True)
args=parser.parse_args()
p=args.projection
projection=json.loads(p.read_text())
records=[];total=0;before_sx=0
for masks in projection['cycle_cover']:
    t=tuple(bits(m) for m in masks)
    k=tuple(sum(i in z for z in t)-minimum[i] for i in range(6))
    options=tuple(tuple(c for c in (1,2,3) if c.bit_count()+k[i]<=2) for i in range(6))
    old=[];new=[]
    for cols in product(*options):
        total+=1
        sy=tuple(frozenset(i for i,c in enumerate(cols) if c>>s&1) for s in range(2))
        if any(len(sy[s]&t[j])>2 for s in range(2) for j in (1,2)):continue
        if any(cols[i]|cols[j]!=3 for i,j in edges):continue
        old.append(cols)
        if sum(k)==0:
            double=frozenset(i for i,c in enumerate(cols) if c==3)
            opposite=tuple(frozenset((cycle[i],cycle[i+3])) for i in range(3))
            if len(sy[0])!=4 or len(sy[1])!=4 or double not in opposite:
                raise ValueError('ordinary K0 characterization failed')
        beta=tuple(2-k[i]-cols[i].bit_count() for i in range(6))
        if any(beta[i]+len(sx_t[s]&frozenset(j for j,z in enumerate(t) if i in z))>1
               for s in range(2) for i in own[s]):continue
        new.append(cols)
    before_sx+=len(old)
    if sum(k)==1 and old:raise ValueError('ordinary overlap argument has an exception')
    if new:raise ValueError('ordinary finished CaseI has an exception')
    records.append({'T_rows':masks,'K':sum(k),'complete_SY_candidates':len(tuple(product(*options))),
                    'after_cycle_and_SY_T':old,'after_SX_own':new})
    if time.monotonic()-start>30:raise RuntimeError('unchanged phase guard; incomplete')
result={'schema':'caseI-edge-only-ordinary-cycle-audit-v1','agent':'six-books-1','role':'researcher',
        'complete_T_patterns':len(records),'complete_SY_candidates':total,
        'before_SX_own':before_sx,'after_SX_own':0,'records':records,
        'hypotheses':'derived ordinary constraints for E<=108 and given literal Nu only; no outside degree profile',
        'status':'exact corroboration of the ordinary proof; not a host witness or independent review'}
raw=canonical(result)+'\n'
args.out.parent.mkdir(parents=True,exist_ok=True)
args.out.write_text(raw)
print(canonical({'complete_T_patterns':len(records),'complete_SY_candidates':total,'before_SX_own':before_sx,
                 'after_SX_own':0,'whole_record_sha256':hashlib.sha256(raw.encode()).hexdigest(),
                 'elapsed_seconds':time.monotonic()-start}))
