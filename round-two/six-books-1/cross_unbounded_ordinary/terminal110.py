"""Full labelled110 role cover, two physical column models, empty X margins.

This finite terminal certificate depends on the written ordinary C/density
bridge. It is not a complete22-point host enumeration.
"""
from itertools import combinations,product
import json,hashlib,time,sys
from pathlib import Path
import literal as L
import reference as R

start=time.monotonic()
def require(t,m):
    if not t:raise ValueError(m)
def guard():
    if time.monotonic()-start>30:raise RuntimeError('30s guard; incomplete terminal enumeration')
def digest(x):return hashlib.sha256((json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()).hexdigest()
A,B,C={0,1},{2,3},{4,5}
def case(t0,t2):
    t0,t2=set(t0),set(t2)
    t=[int(z in t0)+int(z in C)+int(z in t2) for z in range(6)]
    return {'SYQ':[[0,1],[2,3]],'TQ':[sorted(t0),[4,5],sorted(t2)],
            'epsilon':[v-1 for v in t],'h':[2,2,2,2,3,3]}
def key(c):return tuple(tuple(a) for a in c['TQ'])

# Set/cardinality producer, with every ordinary role restriction explicit.
produced=[]
for t0,t2 in product(combinations(range(6),3),combinations(range(6),4)):
    if set(t0)&B or not B<=set(t2) or len(set(t2)&A)>1 or len(set(t2)&C)>1:continue
    c=case(t0,t2)
    if min(c['epsilon'])<0:continue
    produced.append(c)
produced.sort(key=key)

# Distinct reference: all4096 bit-word pairs, actual colored known spines.
n,d,q=R.build(0,(R.H,R.K,R.C),(R.P,R.S),(0,0,1))
ref=[];all16=(1<<16)-1
for w0,w2 in product(range(64),repeat=2):
    if w0.bit_count()!=3 or w2.bit_count()!=4:continue
    qrows={11:3,12:12,13:w0,14:48,15:w2}
    for i,j in ((12,13),(11,15),(14,15)):
        if n[i]>>j&1:
            pages=(n[i]&n[j]).bit_count()+(qrows[i]&qrows[j]).bit_count()
            ok=pages<=3
        else:
            pages=(all16&~(n[i]|n[j]|(1<<i)|(1<<j))).bit_count()+(63&~(qrows[i]|qrows[j])).bit_count()
            ok=pages<=6
        if not ok:break
    else:
        if any(not ((w0|48|w2)>>z&1) for z in range(6)):continue
        ref.append(case([z for z in range(6) if w0>>z&1],[z for z in range(6) if w2>>z&1]))
ref.sort(key=key)
require(produced==ref and len(ref)==12,'WHOLE labelled role cover, not only three representatives')
require(all(sum(c['epsilon'])==3 and sum(c['h'])==14 for c in ref),'every actual110 Q excess/internal degree')

perms=[]
for flips in product((0,1),repeat=3):
    p=list(range(6))
    for k,v in enumerate(flips):
        if v:p[2*k],p[2*k+1]=p[2*k+1],p[2*k]
    perms.append(tuple(p))
def image(c,p):
    out=case([p[z] for z in c['TQ'][0]],[p[z] for z in c['TQ'][2]])
    require(all(out['epsilon'][p[z]]==c['epsilon'][z] and out['h'][p[z]]==c['h'][z] for z in range(6)),
            'complete actual role/excess/internal-degree transport')
    return out
canonical=[case(t0,(1,2,3,4)) for t0 in ((0,4,5),(0,1,4),(0,1,5))]
canonkeys={key(c) for c in canonical}
images={key(image(c,p)) for c,p in product(canonical,perms)}
require(images=={key(c) for c in ref},'exact three-orbit cover via all eight pair labels')
catalog_by_key={key(c):c for c in ref}
for c,p in product(ref,perms):
    require(image(c,p)==catalog_by_key[key(image(c,p))],'every complete domain label action stays in the cover')

def audit_packet(candidate,physical):
    require(isinstance(candidate,list) and len(candidate)==12,'whole twelve-case scope required')
    require(candidate==physical,'every case/role/degree/column must match original physical enumeration')
records=[];physical=[]
for c in produced:
    cores=[];direct=[]
    for r,swapped in product((0,1),(False,True)):
        rows=(L.H,L.K,L.C) if r==0 else (L.K,L.H,L.C)
        sy=(L.S,L.P) if swapped else (L.P,L.S)
        red,d,q=L.build(r,rows,sy,(0,0,1));bits,bd,bq=R.build(r,rows,sy,(0,0,1))
        require(tuple(sum(1<<j for j in a) for a in red)==bits and d==bd and q==bq,'literal/coordinate whole core')
        require(L.allowances(red,d)==R.allowances(bits,bd),'all120 known allowances')
        cols=L.column_domains(red,d,q,c);other=R.columns(bits,bd,bq,c)
        require(cols==other,'ENTIRE column sets; independent checker has no C6 missing prefilter')
        balanced=[];directbalanced=[];visited=0
        for choice in product(*cols):
            visited+=1
            if all(sum(w[0]>>i&1 for w in choice)==(3 if i<2 else 2) for i in range(6)):
                balanced.append([list(a) for a in choice])
        for choice in product(*other):
            # Literal actual red Q-neighborhood cardinalities, not missing sums.
            matrix=[[z for z,col in enumerate(choice) if not (col[0]>>i&1)] for i in range(6)]
            if [len(row) for row in matrix]==[3,3,4,4,4,4]:
                directbalanced.append([list(a) for a in choice])
        require(balanced==directbalanced==[],'whole independently enumerated X-row solution sets empty')
        rec={'r':r,'swapped_SY':swapped,'columns':cols,'cartesian':visited,'X_rank_matched':balanced}
        cores.append(rec);direct.append(rec|{'columns':other,'X_rank_matched':directbalanced})
        guard()
    records.append({'case':c,'actual_cores':cores});physical.append({'case':catalog_by_key[key(c)],'actual_cores':direct})
audit_packet(records,physical)

# All pair label actions transport WHOLE column sets; no host symmetry.
bykey={key(a['case']):a for a in records};transports=[]
for c,p in product(canonical,perms):
    source=bykey[key(c)];target=bykey[key(image(c,p))]
    for i in range(4):
        a=source['actual_cores'][i]['columns'];b=target['actual_cores'][i]['columns']
        require(all(a[z]==b[p[z]] for z in range(6)),'whole free-Q column transport')
        transports.append([key(c),p,i])

# Semantic damages are checked against the already complete independent
# physical reference, retaining all values rather than only its digest.
damages=[]
def damaged(name,change):
    candidate=json.loads(json.dumps(records));change(candidate)
    try:audit_packet(candidate,physical)
    except ValueError:damages.append(name)
    else:raise ValueError('actual semantic damage accepted:'+name)
damaged('omit-an-original-labelled-role',lambda x:x.pop())
damaged('duplicate-one-original-role',lambda x:x.__setitem__(1,json.loads(json.dumps(x[0]))))
damaged('wrong-T2-Q-role',lambda x:x[0]['case']['TQ'][2].pop())
damaged('erase-actual-Q-excess',lambda x:x[0]['case']['epsilon'].__setitem__(4,0))
damaged('wrong-internal-Q-degree',lambda x:x[0]['case']['h'].__setitem__(4,2))
damaged('omit-actual-r-SY-core',lambda x:x[0]['actual_cores'].pop())
damaged('omit-valid-physical-column',lambda x:x[0]['actual_cores'][0]['columns'][0].pop())
damaged('insert-invalid-all-missing-column',lambda x:x[0]['actual_cores'][0]['columns'][0].append([63,0,0,2]))
damaged('erase-variable-actual-point-degree',lambda x:x[0]['actual_cores'][0]['columns'][0][0].__setitem__(3,0))
damaged('fabricate-one-balanced-cut',lambda x:x[0]['actual_cores'][0]['X_rank_matched'].append([[0,0,0,10]]*6))
damaged('claim-incomplete-product-complete',lambda x:x[0]['actual_cores'][0].__setitem__('cartesian',0))
damaged('change-SY-marked-pair',lambda x:x[0]['case']['SYQ'][0].__setitem__(0,2))
guard()
out={'agent':'six-books-1','role':'researcher','complete':True,
     'scope':'All twelve labelled110 roles and all48 actual r/SY cores; ordinary rank/density bridge written separately',
     'reference_role_bit_pairs':4096,'labelled_role_cases':produced,'canonical_three_cases':canonical,
     'whole_label_transports':[len(transports),digest(transports)],'all48_physical_column_and_product_records':records,
     'semantic_damage_rejections':damages,'all_X_rank_solution_sets_empty':True}
raw=(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n').encode();Path(sys.argv[1]).write_bytes(raw)
print(json.dumps({'complete':True,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),
                  'roles':len(records),'actual_cores':sum(len(a['actual_cores']) for a in records),
                  'damages':len(damages),'seconds':time.monotonic()-start}))
