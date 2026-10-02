"""Complete necessary CaseI projections, corroborating the ordinary proof."""
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import argparse, hashlib, json, time

START=time.monotonic()
CYCLE=((0,4),(4,3),(3,1),(1,2),(2,5),(5,0))
OWN=(40,20)
MINIMUM=(2,2,1,1,1,1)
K14=tuple(i for i in range(16) if i not in (11,12))

def guard():
    if time.monotonic()-START>30:raise RuntimeError('unchanged30s phase guard; incomplete')
def encode(x):return json.dumps(x,separators=(',',':'))
def digest(x):return hashlib.sha256(encode(x).encode()).hexdigest()
def bit_graph(rows,sy=(0,0)):
    nr=[0]*16
    def e(i,j):nr[i]|=1<<j;nr[j]|=1<<i
    for j in (1,2,*range(3,11)):e(0,j)
    for j in (2,11,12):e(1,j)
    for j in range(9,16):e(2,j)
    for i,j in CYCLE:e(i+3,j+3)
    for s in range(2):
        for i in range(6):
            if OWN[s]>>i&1:e(s+9,i+3)
    for s,w in enumerate((5,3)):
        for t in range(3):
            if w>>t&1:e(s+9,t+13)
    for s in range(2):
        for t in (1,2):e(s+11,t+13)
    for t,m in enumerate(rows):
        for i in range(6):
            if m>>i&1:e(i+3,t+13)
    for s,m in enumerate(sy):
        for i in range(6):
            if m>>i&1:e(i+3,s+11)
    D=(10,10,9,*([10]*8),6+sy[0].bit_count(),6+sy[1].bit_count(),7+rows[0].bit_count(),6+rows[1].bit_count(),6+rows[2].bit_count())
    return nr,D

def bit_valid(nr,D,vertices):
    mask=sum(1<<i for i in vertices);outside=22-len(vertices)
    q={i:D[i]-(nr[i]&mask).bit_count() for i in vertices}
    if any(z<0 or z>outside for z in q.values()):raise ValueError('outside degree')
    return all((nr[i]&nr[j]&mask).bit_count()+max(0,q[i]+q[j]-outside)<=
               (3 if nr[i]>>j&1 else D[i]+D[j]-14) for i,j in combinations(vertices,2))

def literal_graph(rows,sy=(0,0)):
    # Build directly from the literal old ten-point neighborhood, with a separate
    # edge list rather than importing or decoding the producer graph.
    red=[set() for _ in range(16)]
    def e(i,j):red[i].add(j);red[j].add(i)
    old=(2,1,3,4,5,6,7,8,9,10)
    adjacency=((1,8,9),(0,),(6,7),(4,5),(3,7,9),(3,6,8),(2,5,9),(2,4,8),(0,5,7),(0,4,6))
    for i in range(10):
        e(0,old[i])
        for j in adjacency[i]:
            if i<j:e(old[i],old[j])
    for j in (11,12):e(1,j)
    for j in (11,12,13,14,15):e(2,j)
    for i,j in ((9,13),(9,15),(10,13),(10,14),(11,14),(11,15),(12,14),(12,15)):e(i,j)
    for i in range(6):
        for t in range(3):
            if rows[t]>>i&1:e(i+3,t+13)
        for s in range(2):
            if sy[s]>>i&1:e(i+3,s+11)
    D=(10,10,9,*([10]*8),len(red[11])+2,len(red[12])+2,len(red[13])+4,len(red[14])+2,len(red[15])+2)
    return red,D

def literal_valid(red,D,vertices):
    K=frozenset(vertices);outside=22-len(K)
    r={i:K&red[i] for i in K}
    b={i:K-red[i]-{i} for i in K}
    q={i:D[i]-len(r[i]) for i in K}
    if any(z<0 or z>outside for z in q.values()):raise ValueError('literal outside degree')
    for i,j in combinations(vertices,2):
        if j in red[i]:
            if len(r[i]&r[j])+max(0,q[i]+q[j]-outside)>3:return False
        elif len(b[i]&b[j])+max(0,outside-q[i]-q[j])>6:return False
    return True

def cycle_cover():
    records=[]
    # Every two-coloring, first with no overlap, then with each single overlap.
    for overlap in (None,*range(6)):
        remaining=tuple(i for i in range(6) if i!=overlap)
        for word in product((0,1),repeat=len(remaining)):
            c=dict(zip(remaining,word))
            if any(i!=overlap and j!=overlap and c[i]==c[j] for i,j in CYCLE):continue
            sets=[{i for i in remaining if c[i]==s} for s in (0,1)]
            if overlap is not None:
                for z in sets:z.add(overlap)
            records.append((3,*tuple(sum(1<<i for i in z) for z in sets)))
    return sorted(records)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    state=Path('/scratch/research-team-sol61-six-20260929/state')
    if any((state/n).exists() for n in ('PAUSED','PAUSED.json')):raise RuntimeError('active pause')
    h=state/'monitor/HANDOVER.json'
    if h.exists() and json.loads(h.read_text()).get('phase')!='completed':raise RuntimeError('incomplete handover')
    rank_domains=[tuple(m for m in range(64) if m.bit_count()==r) for r in (3,4)]
    tested=0;direct=[]
    for ranks in ((3,3),(3,4),(4,3)):
        for x,y in product(rank_domains[ranks[0]-3],rank_domains[ranks[1]-3]):
            tested+=1;rows=(3,x,y);nr,D=bit_graph(rows)
            if bit_valid(nr,D,K14):direct.append(rows)
    direct.sort();cover=cycle_cover()
    if len(cover)!=14 or len(set(cover))!=14:raise ValueError('cycle cover count')
    # Independently validate every cover member literally. The whole census,
    # not just cardinalities or digests, must recover the same necessary set.
    literal=sorted(rows for rows in cover if literal_valid(*literal_graph(rows),K14))
    if direct!=literal:raise ValueError('entire1000 vs cycle-cover projection mismatch')
    if any(rows not in cover for rows in direct):raise ValueError('cover loses a valid14-point record')
    guard()
    fast=[];slow=[];fast_tests=0;literal_tests=0
    for rows in direct:
        k=tuple(sum(bool(w>>i&1) for w in rows)-MINIMUM[i] for i in range(6))
        options=[tuple(c for c in (1,2,3) if c.bit_count()+k[i]<=2) for i in range(6)]
        for c in product(*options):
            fast_tests+=1
            sy=tuple(sum(((c[i]>>s)&1)<<i for i in range(6)) for s in range(2))
            nr,D=bit_graph(rows,sy)
            if bit_valid(nr,D,tuple(range(16))):fast.append((rows,sy,tuple(D[11:])))
        for sy in product(range(64),repeat=2):
            literal_tests+=1
            if sy[0]|sy[1]!=63:continue
            if any(k[i]+int(bool(sy[0]>>i&1))+int(bool(sy[1]>>i&1))>2 for i in range(6)):continue
            red,D=literal_graph(rows,sy)
            if literal_valid(red,D,tuple(range(16))):slow.append((rows,sy,tuple(D[11:])))
        guard()
    fast.sort();slow.sort()
    if fast!=slow:raise ValueError('entire column/row16-point necessary domain mismatch')
    result={'schema':'caseI-edge-only-projections-v1','agent':'six-books-1','role':'researcher','scope':'given literal Nu with its stated root/neighborhood degrees; E<=108; Y-repeated; arbitrary outside degrees','complete_rank_filtered_domain':tested,'cycle_cover':cover,'projection14':direct,'projection14_sha256':digest(direct),'column_SY_candidates':fast_tests,'full_row_SY_candidates':literal_tests,'projection16':fast,'projection16_sha256':digest(fast),'actual_endpoint_degree_histogram':sorted(Counter(x[2] for x in fast).items()),'status':'complete necessary projections corroborating ordinary proof; not a host construction','elapsed_seconds':time.monotonic()-START,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2)+'\n')
    print(encode({k:v for k,v in result.items() if k not in ('cycle_cover','projection14','projection16')}))

if __name__=='__main__':main()
