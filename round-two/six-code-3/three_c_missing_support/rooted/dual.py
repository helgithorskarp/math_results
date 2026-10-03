"""Independent full-word-compatible triple search and least-point exact partitions."""
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
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();root=Path(__file__).parent
    e=json.loads((root/'EXPECTED.json').read_text());raw=(root/'FIXTURES.json').read_bytes()
    require(hashlib.sha256(raw).hexdigest()==e['published_fixture_file_sha256'],'exact reader-facing source fixture')
    stars=json.loads(raw)['stars'];require(len(stars)==23,'all generic fixtures')
    qualified=[]
    for index,words in enumerate(stars):
        tick();masks=[sum(1<<p for p in q) for q in words]
        require(len(masks)==len(set(masks))==20 and all(m.bit_count()==4 and 0<m<1<<17 for m in masks),'literal mask20-star')
        require(all((x&y).bit_count()<=1 for x,y in itertools.combinations(masks,2)),'all star intersections')
        counts=[sum(bool(m&(1<<p)) for m in masks) for p in range(17)]
        if sorted(counts)!=[3,4,4,4]+[5]*13:continue
        heavy=counts.index(3);high=[p for p in range(17) if counts[p]<5]
        heavy_neighbors=0
        for m in masks:
            if m&(1<<heavy):heavy_neighbors|=m
        if any(not(heavy_neighbors&(1<<p)) for p in high if p!=heavy):continue
        friends=[p for p in range(17) if p!=heavy and not(heavy_neighbors&(1<<p))]
        require(len(friends)==7 and all(counts[p]==5 for p in friends),'actual missing-heavy LOW points')
        qualified.append((index,words,masks,heavy,friends))
    require(len(qualified)==1,'unique actual C profile after whole fixture validation')
    index,words,masks,heavy,friends=qualified[0]
    inp=json.loads((root/'INPUT.json').read_text());digest=hashlib.sha256(json.dumps(inp,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    require(digest==e['input_math_sha256'] and len(inp['records'])==56,'completed whole input')
    anchor_lookup={tuple(r['colors']):k for k,r in enumerate(inp['records'])};cases=[];bits=[]
    for a,b in itertools.permutations(friends,2):
        shared=next(m for m in masks if (m&(1<<a)) and (m&(1<<b)))
        extras=[p for p in range(17) if shared&(1<<p) and p not in [a,b]]
        first=sorted(tuple(p for p in range(17) if m&(1<<p) and p!=a) for m in masks if m&(1<<a) and not(m&(1<<b)))
        second=sorted(tuple(p for p in range(17) if m&(1<<p) and p!=b) for m in masks if m&(1<<b) and not(m&(1<<a)))
        image=[None]*17;image[heavy]=0;image[a]=2;image[b]=3
        for p,label in zip(extras,[4,5]):image[p]=label
        label=6
        for r in range(4):
            for c in range(4):
                if r==c:continue
                actual_col=next(col for col in second if not(set(first[c])&set(col)))
                meet=set(first[r])&set(actual_col);require(len(meet)==1,'unique literal occupied-cell intersection')
                image[next(iter(meet))]=label;label+=1
        require(sorted(image)==[p for p in range(18) if p!=1],'entire normalized physical point map')
        fixed=sorted(sorted([1]+[image[p] for p in q]) for q in words)
        fixed_masks=[sum(1<<p for p in q) for q in fixed]
        eligible=[]
        for triple in itertools.combinations(range(6,18),3):
            tick();word=sum(1<<p for p in (2,3)+triple)
            if all((word&q).bit_count()<=2 for q in fixed_masks):eligible.append(frozenset(triple))
        partitions=[]
        def visit(remaining,chosen):
            tick()
            if not remaining:partitions.append(chosen);return
            pivot=min(remaining)
            for triple in eligible:
                if pivot in triple and triple<=remaining:visit(remaining-triple,chosen+[triple])
        visit(frozenset(range(6,18)),[])
        positives=[]
        for partition in partitions:
            tick();by_absent={}
            for triple in partition:
                rows={((p-6)//3) for p in triple};require(len(rows)==3,'literal first-class transversal')
                absent=next(r for r in range(4) if r not in rows)
                require(absent not in by_absent,'whole third-class missing-row matching')
                by_absent[absent]=sorted(triple)
            require(sorted(by_absent)==list(range(4)),'all normalized third labels')
            colors=[next(r for r,t in by_absent.items() if p in t) for p in range(6,18)]
            require(tuple(colors) in anchor_lookup,'independently constructed third class in full completed domain')
            anchor_index=anchor_lookup[tuple(colors)]
            added=[[2,3]+by_absent[r] for r in range(4)]
            positives.append(dict(anchor_index=anchor_index,additional_words=added,full24=sorted(fixed+added)))
        positives.sort(key=lambda p:p['anchor_index'])
        require(len({p['anchor_index'] for p in positives})==len(positives),'no duplicate physical partitions')
        accepted={p['anchor_index'] for p in positives};bits+=['1' if k in accepted else '0' for k in range(56)]
        cases.append(dict(old_C_pair=[a,b],point_image=image,fixed_star=fixed,positive_anchors=positives))
    math=dict(cases=2352,input_math_sha256=digest,fixture_index=index,fixture_star=words,fixture_heavy=heavy,
              fixture_friends=friends,coverage=''.join(bits),pair_cases=cases)
    common=hashlib.sha256(json.dumps(math,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    result=dict(agent='six-code-3',role='researcher',status='COMPLETE_FULL_WORD_TRIPLE_PARTITION_ENUMERATION',
                mathematics=math,common_math_sha256=common,states=STATES,guard_states=500000,guard_seconds=20)
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(dict(status=result['status'],positive_anchors=sum(len(c['positive_anchors']) for c in cases),common_math_sha256=common),sort_keys=True))
if __name__=='__main__':main()
