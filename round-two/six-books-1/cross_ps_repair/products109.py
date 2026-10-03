"""Complete column products and every literal known16 colored spine."""
from pathlib import Path
from itertools import product,combinations
import hashlib,json,os,sys,time
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[name]='1'
import literal as L,reference as R
start=time.monotonic()
def require(t,m):
    if not t:raise ValueError(m)
def guard():
    if time.monotonic()-start>30:raise RuntimeError('30s guard incomplete, no exclusion')
def canonical(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def digest(x):return hashlib.sha256(canonical(x)).hexdigest()
inputraw=Path(sys.argv[1]).read_bytes()
require(json.loads(inputraw)['complete'] is True,'complete regenerated point input')
prior=json.loads(inputraw);results=[]
for entry in prior['results']:
    u,v,a,d,k0,k1=entry['key'];n,degs,q=L.build(0,(a,d,L.P),(u,v));records=[];survivors=[];raw_count=0;rank_count=0
    for key,roles,domains,total in entry['whole_nonempty_column_packets']:
        aa,bb,cc,tt=key;eqrows=(set(aa),set(bb),set(cc),{4,5},set(tt))
        expected=1
        for dom in domains:expected*=len(dom)
        require(expected==total,'whole point Cartesian size')
        for choice in product(*domains):
            raw_count+=1
            ranks=[sum((z[0]>>i)&1 for z in choice) for i in range(8)]
            rankok=ranks==list(q[3:11])
            if not rankok:continue
            rank_count+=1
            graph=[set(z) for z in n]+[set() for _ in range(6)]
            for z,(word,h,D) in enumerate(choice):
                nq={1}|{3+i for i in range(8) if word>>i&1}|{11+i for i,row in enumerate(eqrows) if z in row}
                require(len(nq)+h==D,'actual original-Q degree correspondence')
                for i in nq:graph[i].add(16+z);graph[16+z].add(i)
            require(all(len(graph[i])==degs[i] for i in range(16)),'all16 original degrees complete')
            pages,bad=L.known_spines(graph)
            bits=[sum(1<<j for j in row) for row in graph]
            other=[]
            for i,j in combinations(range(16),2):
                edge=(bits[i]>>j)&1
                physical=bits[i]&bits[j] if edge else ((1<<22)-1)&~(bits[i]|bits[j]|(1<<i)|(1<<j))
                other.append([i,j,edge,[z for z in range(22) if physical>>z&1]])
            require(pages==other,'all120 COMPLETE original known-spine physical page records')
            record=[key,list(choice),None if not bad else bad[0]];records.append(record)
            if not bad:survivors.append(record)
            if raw_count%1024==0:guard()
        guard()
    results.append({'key':entry['key'],'raw_products':raw_count,'rank_matching_products':rank_count,
                    'whole_rank_matching_first_spine_records':records,'whole_known_spine_survivors':survivors})
out={'agent':'six-books-1','role':'researcher','complete':True,
     'scope':'Exact E109 P-domain known-spine exclusion; no QQ graph used',
     'input_sha256':hashlib.sha256(inputraw).hexdigest(),'results':results}
require([(z['raw_products'],z['rank_matching_products'],len(z['whole_known_spine_survivors'])) for z in results]==[(768,48,0),(0,0,0),(115200,0,0)],'whole complete products and all survivor sets empty')
raw=canonical(out);Path(sys.argv[2]).write_bytes(raw)
print(json.dumps({'complete':True,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'seconds':time.monotonic()-start,
 'cases':[{'key':x['key'],'raw':x['raw_products'],'rank_matches':x['rank_matching_products'],
          'survivors':len(x['whole_known_spine_survivors'])} for x in results]}))
