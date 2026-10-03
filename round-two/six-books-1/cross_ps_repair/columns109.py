"""All actual-color E109 point domains and complete endpoint-Q roles."""
from pathlib import Path
from itertools import combinations,product
import hashlib,json,os,sys,time
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[name]='1'
import literal as L,reference as R
start=time.monotonic()
def require(t,m):
    if not t:raise ValueError(m)
def guard():
    if time.monotonic()-start>30:raise RuntimeError('30s guard; incomplete no exclusion')
def canonical(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def digest(x):return hashlib.sha256(canonical(x)).hexdigest()
prior=json.loads(Path(sys.argv[1]).read_text())
require(prior['complete'] is True and [e['key'] for e in prior['whole_joint_survivors']]==[[35,60,43,23,3,2],[50,13,43,23,3,2],[50,60,43,23,3,2]],'whole corrected three-core interface')
results=[]
for entry in prior['whole_joint_survivors']:
    u,v,a,d,k0,k1=entry['key'];n,degs,q=L.build(0,(a,d,L.P),(u,v))
    bits,bd,bq=R.build(0,(a,d,L.P),(u,v));require(degs==bd and q==bq,'full degree/rank interface')
    caps=L.allowances(n,degs);table={};tablerecords=[]
    all16=(1<<16)-1;vertices=set(range(16))
    for role in range(32):
        s=(role&3).bit_count();t=(role>>2).bit_count();h=3-s
        if t<1:table[role]=[];tablerecords.append([role,[]]);continue
        fixed={1}|{11+i for i in range(5) if role>>i&1}
        accepted=[];other=[]
        for word in range(256):
            nq=fixed|{3+i for i in range(8) if word>>i&1};D=len(nq)+h
            good=True
            for i,j in combinations(range(16),2):
                bi,bj=int(i in nq),int(j in nq)
                lower=bi*bj+max(0,q[i]-bi+q[j]-bj-5)
                if lower>caps[i,j]:good=False;break
            if good:
                for i in range(16):
                    if i in nq:
                        if len(n[i]&nq)+max(0,q[i]+h-6)>3:good=False;break
                    else:
                        blue=len(vertices-n[i]-nq-{i})+max(0,5-q[i]-h)
                        if blue>6:good=False;break
            if good:accepted.append([word,h,D])
            nb=sum(1<<i for i in nq);ok=True
            for i,j in combinations(range(16),2):
                bi,bj=(nb>>i)&1,(nb>>j)&1
                if bits[i]>>j&1:
                    lower=(bits[i]&bits[j]).bit_count()+bi*bj+max(0,q[i]-bi+q[j]-bj-5)
                    if lower>3:ok=False;break
                else:
                    blue=(all16&~(bits[i]|bits[j]|(1<<i)|(1<<j))).bit_count()
                    blue+=(1-bi)*(1-bj)+max(0,5-(q[i]-bi)-(q[j]-bj))
                    if blue>6:ok=False;break
            if ok:
                for i in range(16):
                    if nb>>i&1:
                        if (bits[i]&nb).bit_count()+max(0,q[i]+h-6)>3:ok=False;break
                    else:
                        blue=(all16&~(bits[i]|nb|(1<<i))).bit_count()+max(0,5-q[i]-h)
                        if blue>6:ok=False;break
            if ok:other.append([word,h,D])
        require(accepted==other,'entire set/bit original-Q point domain')
        table[role]=accepted;tablerecords.append([role,accepted]);guard()
    Q=set(range(6));T1={4,5};small=list(combinations(range(4),2))
    packets=[];survivors=[]
    for aa,bb in product(small,repeat=2):
        sy=(set(aa),set(bb))
        for cc in combinations(sorted(Q-sy[1]),3):
            for tt in combinations(range(6),3):
                rows=(*sy,set(cc),T1,set(tt))
                if any(len(rows[i-11]&rows[j-11])>caps[i,j] for i,j in combinations(range(11,16),2)):continue
                roles=[sum(1<<i for i,row in enumerate(rows) if z in row) for z in range(6)]
                if any((r>>2).bit_count()<1 for r in roles):continue
                domains=[table[r] for r in roles]
                product_size=1
                for dom in domains:product_size*=len(dom)
                key=[list(aa),list(bb),list(cc),list(tt)]
                packets.append([key,roles,[len(z) for z in domains],product_size])
                if product_size:survivors.append([key,roles,domains,product_size])
        guard()
    results.append({'key':entry['key'],'whole32_point_role_table':tablerecords,
                    'whole_end_Q_packets':packets,'whole_nonempty_column_packets':survivors})
out={'agent':'six-books-1','role':'researcher','complete':True,
     'scope':'Exact E109 necessary projections; written original-domain and density bridges unformalized',
     'actual_SY1_T2_color':'BLUE','global_outside_degree_floor_assumed':False,'results':results}
raw=canonical(out);Path(sys.argv[2]).write_bytes(raw)
print(json.dumps({'complete':True,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),
 'seconds':time.monotonic()-start,'cases':[{'key':x['key'],'point_patterns':sum(len(z[1]) for z in x['whole32_point_role_table']),
   'end_Q_packets':len(x['whole_end_Q_packets']),'nonempty_packets':len(x['whole_nonempty_column_packets']),
   'max_product':max([0]+[z[-1] for z in x['whole_nonempty_column_packets']])} for x in results]}))
