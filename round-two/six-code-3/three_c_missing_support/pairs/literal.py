"""All literal star pairs; test the mandatory equal missing-W condition."""
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


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();base=Path(__file__).parent
    inp=json.loads((base/'INPUT.json').read_text());groups={(g['anchor'],g['root']):g['candidates'] for g in inp['groups']}
    codes=[];records=[];summaries=[]
    for rep in [0,10]:
        for r,t in itertools.combinations([1,2,3],2):
            left,right=groups[rep,r],groups[rep,t];start=len(codes);same=positive=0
            left_sets=[list(map(frozenset,c['full20'])) for c in left]
            right_sets=[list(map(frozenset,c['full20'])) for c in right]
            left_missing=[sorted(p for p in range(4,18) if not any(0 in w and p in w for w in ss)) for ss in left_sets]
            right_missing=[sorted(p for p in range(4,18) if not any(0 in w and p in w for w in ss)) for ss in right_sets]
            for i,a in enumerate(left):
                aa=left_sets[i];F=left_missing[i]
                for j,b in enumerate(right):
                    tick();case=len(codes)
                    bb=right_sets[j];G=right_missing[j]
                    if F!=G:codes.append('0');continue
                    same+=1
                    conflict=next(([u,v] for u,x in enumerate(aa) for v,y in enumerate(bb) if x!=y and len(x&y)>2),None)
                    require(len(set(aa)&set(bb))==5,'exact five pair-anchor words shared')
                    triple=sorted(aa[conflict[0]]&bb[conflict[1]])[:3] if conflict else None
                    union=sorted(map(sorted,set(aa)|set(bb))) if conflict is None else None
                    if union is not None:
                        require(len(union)==35,'literal positive35 union');positive+=1
                    codes.append('1' if conflict else '2')
                    records.append(dict(case=case,anchor=rep,roots=[r,t],star_ids=[i,j],missing_W=F,
                                        conflict=conflict,repeated_triple=triple,full35=union))
            summaries.append(dict(anchor=rep,roots=[r,t],start=start,cases=len(left)*len(right),equal_missing=same,positive35=positive))
    require(len(codes)==349488,'all six specified star-pair domains')
    math=dict(cases=len(codes),coverage=''.join(codes),eligible_cases=records,groups=summaries,
              input_sha256=hashlib.sha256((base/'INPUT.json').read_bytes()).hexdigest())
    common=hashlib.sha256(json.dumps(math,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    out=dict(agent='six-code-3',role='researcher',status='COMPLETE_LITERAL_EQUAL_MISSING_STAR_PAIR_DOMAIN',mathematics=math,
             common_math_sha256=common,states=STATES,guard_states=500000,guard_seconds=20)
    args.output.write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps(dict(status=out['status'],groups=summaries,common_math_sha256=common),sort_keys=True))
if __name__=='__main__':main()
