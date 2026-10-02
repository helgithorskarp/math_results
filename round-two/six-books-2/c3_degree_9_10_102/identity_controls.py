"""Literal all-spine controls for the deficit identities and known21 baseline."""
from pathlib import Path
from argparse import ArgumentParser
from itertools import combinations
import hashlib,json,random,time,resource

def pages(rows):
    n=len(rows);blue=[set(range(n))-{u}-rows[u] for u in range(n)]
    return [(u,v,v in rows[u],len(rows[u]&rows[v]) if v in rows[u] else len(blue[u]&blue[v]))
            for u,v in combinations(range(n),2)]

def check(fixture):
    rng=random.Random(180102)
    graphs=[]
    for _ in range(64):
        rows=[set() for _ in range(22)]
        def add(u,v):rows[u].add(v);rows[v].add(u)
        for orbit in range(7):
            if orbit<3:
                for t in range(3):add(21,3*orbit+t)
            if rng.randrange(2):
                for t in range(3):add(3*orbit+t,3*orbit+(t+1)%3)
        for i,j in combinations(range(7),2):
            for shift in range(3):
                if rng.randrange(2):
                    for t in range(3):add(3*i+t,3*j+(t+shift)%3)
        graphs.append(rows)
    graphs += [[set(range(22))-{u} for u in range(22)],[set() for _ in range(22)]]
    spine_count=row_count=root_count=0
    for index,rows in enumerate(graphs):
        data=pages(rows);d=list(map(len,rows));E=sum(d)//2
        weights=[(3 if red else 6)-c for _,_,red,c in data]
        if 2*sum(weights)!=-6468+120*E-3*sum(x*x for x in d):raise ValueError('Literal global deficit identity')
        T=sum(c for _,_,_,c in data)//3
        if 2*T!=3080-sum(x*(21-x) for x in d):raise ValueError('Literal monochromatic triangle identity')
        for v in range(22):
            incident=sum(w for (u,z,_,_),w in zip(data,weights) if v in [u,z])
            symbolic=2*E-294+38*d[v]-d[v]*d[v]-2*sum(d[u] for u in rows[v])
            if incident!=symbolic:raise ValueError('Literal vertex deficit identity')
            if (incident-d[v])%2:raise ValueError('Literal vertex deficit parity')
            row_count+=1
        if index<64:
            DA=sum(d[u] for u in rows[21])
            incident=sum(w for (u,v,_,_),w in zip(data,weights) if 21 in [u,v])
            if len(rows[21])!=9 or incident!=2*(E-DA)-33:raise ValueError('Literal root deficit identity')
            A=rows[21];B=set(range(21))-A
            mixed=sum(w for (u,v,_,_),w in zip(data,weights) if (u in A and v in B) or (u in B and v in A))
            if (mixed-(DA-9))%2:raise ValueError('Literal mixed cut deficit parity')
            root_count+=1
        spine_count+=len(data)
    text=Path(fixture).read_text().splitlines()
    if len(text)!=21 or any(len(r)!=21 or set(r)-{'0','1'} for r in text):raise ValueError('Primary fixture shape')
    rows=[{v for v,c in enumerate(r) if c=='1'} for r in text]
    if any(u in rows[u] or any((v in rows[u])!=(u in rows[v]) for v in range(21)) for u in range(21)):
        raise ValueError('Primary graph semantics')
    data=pages(rows);E=sum(map(len,rows))//2
    cap=[max(c for _,_,red,c in data if red),max(c for _,_,red,c in data if not red)]
    if E!=93 or cap!=[3,6]:raise ValueError('Known ordinary21 baseline')
    return dict(arbitrary_graphs=66,literal22_spines=spine_count,vertex_deficit_rows=row_count,
                vertex_deficit_parities=row_count,root9_deficit_rows=root_count,mixed_cut_deficit_parities=root_count,
                primary21=dict(vertices=21,edges=E,max_red_pages=cap[0],max_blue_pages=cap[1],spines=210),
                trust='Arbitrary graphs may violate page caps; signed identity controls are not witnesses. Primary21 is known prior art.')

def main():
    p=ArgumentParser();p.add_argument('--work',type=Path,required=True);args=p.parse_args()
    start=time.monotonic();record=check(Path(__file__).resolve().parent/'primary21.rows')
    raw=json.dumps(record,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n'
    args.work.mkdir(parents=True,exist_ok=True);(args.work/'identity-controls.json').write_text(raw)
    if time.monotonic()-start>25:raise RuntimeError('INCOMPLETE identity controls')
    print(json.dumps(dict(record=record,bytes=len(raw.encode()),sha256=hashlib.sha256(raw.encode()).hexdigest(),seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),indent=2))

if __name__=='__main__':main()
