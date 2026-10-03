"""Independent five-subset partitioning and repeated covered-triple certificates."""
import argparse,hashlib,itertools,json,time
from pathlib import Path
START=time.monotonic();STATES=0
def require(ok,message):
    if not ok:raise ValueError(message)
def tick():
    global STATES
    STATES += 1
    if STATES > 500000 or time.monotonic() - START > 20:
        raise RuntimeError('INCOMPLETE: original500000/20 guard')


def mask(points):return sum(1<<p for p in points)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();base=Path(__file__).parent
    inp=json.loads((base/'INPUT.json').read_text());groups={(g['anchor'],g['root']):g['candidates'] for g in inp['groups']}
    codes=['0']*349488;records=[];summaries=[];offset=0
    for rep in [0,10]:
        for r,t in itertools.combinations([1,2,3],2):
            left,right=groups[rep,r],groups[rep,t];partition=[]
            for candidates in [left,right]:
                by_missing={}
                for i,c in enumerate(candidates):
                    tick();covered=0
                    for w in c['full20']:
                        if 0 in w:covered|=mask(w)
                    F=tuple(p for p in range(4,18) if not(covered&(1<<p)))
                    require(len(F)==5,'actual missing five-set');by_missing.setdefault(F,[]).append(i)
                partition.append(by_missing)
            same=positive=0
            for F in itertools.combinations(range(4,18),5):
                tick()
                for i in partition[0].get(F,[]):
                    a=left[i]['full20'];owners={}
                    for u,w in enumerate(a):
                        for triple in itertools.combinations(w,3):
                            require(triple not in owners,'left actual triples never repeat');owners[triple]=u
                    a_set=set(map(tuple,a))
                    for j in partition[1].get(F,[]):
                        tick();same+=1;b=right[j]['full20'];conflicts=set()
                        for v,w in enumerate(b):
                            if tuple(w) in a_set:continue
                            for triple in itertools.combinations(w,3):
                                if triple in owners:conflicts.add((owners[triple],v))
                        conflict=list(min(conflicts)) if conflicts else None
                        require(len(a_set&set(map(tuple,b)))==5,'five whole shared pair words')
                        repeated=sorted(set(a[conflict[0]])&set(b[conflict[1]]))[:3] if conflict else None
                        union=[list(w) for w in sorted(a_set|set(map(tuple,b)))] if conflict is None else None
                        if union is not None:
                            require(len(union)==35,'physical35-word union');positive+=1
                        case=offset+i*len(right)+j;codes[case]='1' if conflict else '2'
                        records.append(dict(case=case,anchor=rep,roots=[r,t],star_ids=[i,j],missing_W=list(F),
                                            conflict=conflict,repeated_triple=repeated,full35=union))
            summaries.append(dict(anchor=rep,roots=[r,t],start=offset,cases=len(left)*len(right),equal_missing=same,positive35=positive))
            offset+=len(left)*len(right)
    require(offset==349488,'all six pair products');records.sort(key=lambda p:p['case'])
    math=dict(cases=offset,coverage=''.join(codes),eligible_cases=records,groups=summaries,
              input_sha256=hashlib.sha256((base/'INPUT.json').read_bytes()).hexdigest())
    common=hashlib.sha256(json.dumps(math,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    out=dict(agent='six-code-3',role='researcher',status='COMPLETE_INDEPENDENT_FIVE_SET_TRIPLE_DOMAIN',mathematics=math,
             common_math_sha256=common,states=STATES,guard_states=500000,guard_seconds=20)
    args.output.write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps(dict(status=out['status'],groups=summaries,common_math_sha256=common),sort_keys=True))
if __name__=='__main__':main()
