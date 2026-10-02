"""Full fresh literal checker; flat row products rather than producer recursion."""
from itertools import combinations, product
from pathlib import Path
import argparse, json, time
from verify import graph, domain14, domain16, canonical, sha, guard

ALL=frozenset(range(22))
ENDPOINTS=tuple(range(9,16))
XPAIRS=tuple(combinations(range(6),2))
SUBSETS={m:frozenset(16+i for i in range(6) if m>>i&1) for m in range(64)}

def complete(i,red,mask):
    nr=frozenset(red[i])|SUBSETS[mask]
    return nr,ALL-nr-{i}

def valid(i,j,a,b,red):
    color=0 if j in red[i] else 1
    return len(a[color]&b[color])<=(3 if color==0 else 6)

def bases(xs):
    answer=[]
    for r,rows,c,sy,beta,D in xs:
        red=graph(r,c,sy)
        degrees=(10,10,9,*([10]*8),len(red[11])+2,len(red[12])+2,
                 len(red[13])+3,len(red[14])+2,len(red[15])+3)
        if tuple(degrees[11:])!=tuple(D):raise ValueError('literal endpoint degrees')
        answer.append((red,degrees))
    return answer

def endpoints(xs,base):
    start=time.monotonic();triples=[]
    # Enumerate every six-column nonzero T word, independently of SX masks.
    for columns in product(range(1,8),repeat=6):
        ranks=tuple(sum(bool(c>>t&1) for c in columns) for t in range(3))
        if ranks==(3,2,3):
            triples.append(tuple(sum(int(bool(columns[i]>>t&1))<<i for i in range(6)) for t in range(3)))
    triples.sort();pools={n:tuple(m for m in range(64) if m.bit_count()==n) for n in (2,3)}
    answer=[]
    for index,(red,degrees) in enumerate(base):
        for intersection,b in ((2,51),(3,23)):
            sx=(complete(9,red,15),complete(10,red,b))
            if not valid(9,10,*sx,red):raise ValueError('canonical SX pair')
            tr=[{m:complete(13+t,red,m) for m in pools[(3,2,3)[t]]} for t in range(3)]
            sy=[{m:complete(11+s,red,m) for m in pools[2]} for s in range(2)]
            allowed=[frozenset(m for m,n in tr[t].items() if all(valid(9+s,13+t,sx[s],n,red) for s in range(2))) for t in range(3)]
            for ts in triples:
                if any(ts[t] not in allowed[t] for t in range(3)):continue
                whole_t=tuple(tr[t][ts[t]] for t in range(3))
                if any(not valid(13+i,13+j,whole_t[i],whole_t[j],red) for i,j in combinations(range(3),2)):continue
                choices=[tuple(m for m,n in sy[s].items() if all(valid(9+z,11+s,sx[z],n,red) for z in range(2))
                               and all(valid(11+s,13+t,n,whole_t[t],red) for t in range(3))) for s in range(2)]
                for p,q in product(*choices):
                    if not valid(11,12,sy[0][p],sy[1][q],red):continue
                    selected=(sy[0][p],sy[1][q],*whole_t)
                    # Four-regular B_u gives a nonnegative remaining Q-degree.
                    if any(sum(16+j in n[0] for n in selected)>4 for j in range(6)):continue
                    answer.append((index,intersection,*ts,p,q))
        guard(start)
    guard(start);answer.sort()
    return answer,time.monotonic()-start

def masks(frame):
    _,intersection,t0,t1,t2,p,q=frame
    return (15,51 if intersection==2 else 23,p,q,t0,t1,t2)

def rows(frames,base):
    start=time.monotonic();answer=[];products=0
    for frame_index,frame in enumerate(frames):
        red,D=base[frame[0]]
        ep=tuple(complete(i,red,m) for i,m in zip(ENDPOINTS,masks(frame)))
        choices=[]
        for i in range(3,9):
            rank=D[i]-len(red[i])
            candidates=[]
            for m in range(64):
                if m.bit_count()!=rank:continue
                n=complete(i,red,m)
                if all(valid(i,j,n,ep[e],red) for e,j in enumerate(ENDPOINTS)):candidates.append(m)
            choices.append(tuple(candidates))
        if all(choices):
            answer.append((frame_index,tuple(choices)))
            size=1
            for c in choices:size*=len(c)
            products+=size
        if frame_index%128==0:guard(start)
    guard(start)
    return answer,time.monotonic()-start,products

def joins(frames,row_records,base):
    start=time.monotonic();answer=[];literal_products=0;after_pairs=0
    for frame_index,options in row_records:
        frame=frames[frame_index];red,D=base[frame[0]];endpoint_masks=masks(frame)
        ep=tuple(complete(i,red,m) for i,m in zip(ENDPOINTS,endpoint_masks))
        h=tuple(4-sum(16+j in n[0] for n in ep[2:]) for j in range(6))
        candidate=[{m:complete(i+3,red,m) for m in options[i]} for i in range(6)]
        compatible={(i,j):frozenset((m,n) for m in options[i] for n in options[j]
                                   if valid(i+3,j+3,candidate[i][m],candidate[j][n],red)) for i,j in XPAIRS}
        # Every full Cartesian row tuple is examined; no forward column pruning.
        for chosen in product(*options):
            literal_products+=1
            if any((chosen[i],chosen[j]) not in compatible[i,j] for i,j in XPAIRS):continue
            after_pairs+=1
            all_rows=(0,63,0,*chosen,*endpoint_masks)
            nr=[set(red[i])|set(SUBSETS[all_rows[i]]) for i in range(16)]+[set() for i in range(6)]
            for i in range(16):
                for y in SUBSETS[all_rows[i]]:nr[y].add(i)
            # Blue a--y: common blue pages in K are counted literally;
            # common blue pages in Q number5-h_y because a is blue to Q.
            blue_a_K=set(range(16))-nr[2]-{2}
            if any(len(blue_a_K&(set(range(16))-nr[y]))+5-h[y-16]>6 for y in range(16,22)):continue
            DY=tuple(len(nr[y])+h[y-16] for y in range(16,22))
            if sum(D)+sum(DY)!=216:raise ValueError('literal whole108-edge degree sum')
            witness=None
            for i,j in combinations(range(22),2):
                if j in nr[i] and len(nr[i]&nr[j])>=4:
                    witness=('known_red_book',i,j,tuple(sorted(nr[i]&nr[j]))[:4]);break
            if witness is None:raise ValueError('unclosed necessary join; no exclusion established')
            # Four page vertices and every required red edge are literal assigned edges.
            _,i,j,pages=witness
            if len(set(pages))!=4 or i in pages or j in pages or j not in nr[i] or any(p not in nr[i] or p not in nr[j] for p in pages):
                raise ValueError('literal book certificate')
            answer.append((frame_index,tuple(chosen),DY,witness))
            if literal_products%1024==0:guard(start)
        guard(start)
    guard(start);answer.sort()
    return answer,time.monotonic()-start,literal_products,after_pairs

def same(path,domain):
    d=json.loads(path.read_text())
    if not d['complete'] or sha(d['domain'])!=d['domain_sha256']:raise ValueError('parent manifest')
    if canonical(d['domain'])!=canonical(domain):raise ValueError('entire literal domain differs at '+str(path))

def main():
    p=argparse.ArgumentParser();p.add_argument('--core',type=int,choices=(0,1),required=True);p.add_argument('--scratch',type=Path,required=True)
    a=p.parse_args();state=Path('/scratch/research-team-sol61-six-20260929/state')
    if any((state/n).exists() for n in ('PAUSED','PAUSED.json')):raise RuntimeError('pause barrier')
    x14,t14=domain14(a.core);same(a.scratch/f'projection14-r{a.core}.json',x14)
    xs,t16,tested=domain16(a.core,x14);same(a.scratch/f'projection16-r{a.core}.json',xs)
    base=bases(xs)
    frames,te=endpoints(xs,base);same(a.scratch/f'endpoints-r{a.core}.json',frames)
    row_records,tr,raw_products=rows(frames,base);same(a.scratch/f'rows-r{a.core}.json',row_records)
    result,tj,actual_products,after_pairs=joins(frames,row_records,base);same(a.scratch/f'joins-r{a.core}.json',result)
    if raw_products!=actual_products:raise ValueError('entire row Cartesian census')
    d={'agent':'six-books-1','role':'researcher','core':a.core,'completed':True,
       'counts':{'X14':len(x14),'X16':len(xs),'endpoints':len(frames),'row_frames':len(row_records),'known_red_books':len(result)},
       'full_domain_digests':{'X14':sha(x14),'X16':sha(xs),'endpoints':sha(frames),'rows':sha(row_records),'joins':sha(result)},
       'phase_seconds':{'X14':t14,'X16':t16,'endpoints':te,'rows':tr,'joins':tj},
       'SY_candidates_tested':tested,'whole_row_products':actual_products,'after_all_X_pairs':after_pairs,
       'internal_Y_edges_used':0}
    (a.scratch/f'full-independent-r{a.core}.json').write_text(canonical(d)+'\n');print(canonical(d))

if __name__=='__main__':main()
