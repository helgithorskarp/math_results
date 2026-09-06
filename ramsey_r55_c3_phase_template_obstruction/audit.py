"""Definition-level physical checks; no native objective or move code."""
from pathlib import Path
from itertools import combinations
from hashlib import sha256
from collections import Counter
import argparse,csv,json
import physical as p

def structure(base):
    p.family(base)
    out=[]
    for i,j in combinations(range(14),2):
        # Discover the three physical pair orbits by the action itself.
        remaining={(u,v) for u in range(3*i,3*i+3) for v in range(3*j,3*j+3)}
        orbits=[]
        while remaining:
            u,v=min(remaining)
            o={(u,v),(p.ACTION[u],p.ACTION[v]),(p.ACTION[p.ACTION[u]],p.ACTION[p.ACTION[v]])}
            p.need(len(o)==3 and o<=remaining,'pair orbit')
            remaining-=o;orbits.append(sorted(o))
        red=[int(bool(base[o[0][0]]&(1<<o[0][1]))) for o in orbits]
        if sum(red) in (1,2):out.append((orbits,sum(red)))
    return out

def decode(base,groups,word):
    p.need(len(word)==len(groups) and set(word)<={'0','1','2'},'phase word')
    rows=base.copy()
    for (orbits,n),digit in zip(groups,word):
        t=int(digit)
        for j,orbit in enumerate(orbits):
            red=(j==t) if n==1 else (j!=t)
            for u,v in orbit:
                rows[u]&=~(1<<v);rows[v]&=~(1<<u)
                if red:rows[u]|=1<<v;rows[v]|=1<<u
    return rows

def checks(base,groups,word,expected):
    rows=decode(base,groups,word);p.family(rows)
    p.need([x.bit_count() for x in rows]==[x.bit_count() for x in base],'physical degrees')
    ds=p.recursive_defects(rows);p.need(sum(map(len,ds))==expected,'physical score')
    return rows,list(map(len,ds))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('base',type=Path);ap.add_argument('data',type=Path);ap.add_argument('--controls',action='store_true');args=ap.parse_args()
    base=p.read_graph(args.base);groups=structure(base)
    if args.controls:
        records=list(csv.DictReader(args.data.open(),delimiter='\t'));p.need(len(records)==443,'controls complete')
        for i,r in enumerate(records):
            p.need((r['kind'],int(r['index']))==(('cube',i) if i<243 else ('walk',i-243)),'control index')
            checks(base,groups,r['phases'],int(r['score']))
        print(json.dumps({'status':'VERIFIED_443_PHYSICAL_PHASE_CONTROLS','ternary_cube':243,'incremental_walk':200,'table_sha256':sha256(args.data.read_bytes()).hexdigest()},sort_keys=True,indent=2));return
    records=list(csv.DictReader((args.data/'restarts.tsv').open(),delimiter='\t'));p.need(records,'records')
    out=[];graphs=[]
    for i,r in enumerate(records):
        p.need(int(r['restart'])==i,'restart index')
        rows,counts=checks(base,groups,r['phases'],int(r['best']));graphs.append(rows)
        p.need(0<=int(r['best_step'])<=int(r['steps_done']),'step range')
        seed=int(r['seed']);mask=(1<<64)-1
        if i==0:initial=base
        else:
            w=''
            for _ in groups:
                seed=(seed+0x9e3779b97f4a7c15)&mask;z=seed
                z=((z^(z>>30))*0xbf58476d1ce4e5b9)&mask
                z=((z^(z>>27))*0x94d049bb133111eb)&mask;z^=z>>31;w+=str(z%3)
            initial=decode(base,groups,w)
        p.need(sum(map(len,p.recursive_defects(initial)))==int(r['initial']),'physical initial')
        out.append({'restart':i,'blue_red':counts,'best':sum(counts),'graph_sha256':sha256(p.edge_bytes(rows)).hexdigest()})
    best=min(range(len(out)),key=lambda i:out[i]['best']);rows=p.read_graph(args.data/'best.edges')
    p.need(rows==graphs[best],'first winner identity');ds=p.literal_defects(rows);p.need(ds==p.recursive_defects(rows),'literal/recursive full five-set equality')
    status=json.loads((args.data/'status.json').read_text());p.need(status.get('complete') is True or (status.get('candidate_target') is True and not any(ds)),'run completeness')
    print(json.dumps({'status':'VERIFIED_PHASE_TRADE_GRAPH_SCORES','free_ternary_variables':len(groups),'records':out,'winner':best,'blue_red':list(map(len,ds)),'degree_histogram':dict(sorted(Counter(x.bit_count() for x in rows).items())),'all_defects':ds,'target':not any(ds),'search_exhaustive':False},indent=2,sort_keys=True))
if __name__=='__main__':main()
