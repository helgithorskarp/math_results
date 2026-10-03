"""All42 ordered low-friend pairs times all56 whole normalized anchors."""
import argparse, hashlib, itertools, json, time
from pathlib import Path
START=time.monotonic();STATES=0

def require(ok,message):
    if not ok:raise ValueError(message)
def tick():
    global STATES
    STATES += 1
    if STATES > 500000 or time.monotonic() - START > 20:
        raise RuntimeError('INCOMPLETE: original500000/20 guard')


def baseline(root):
    raw=(root/'FIXTURES.json').read_bytes();e=json.loads((root/'EXPECTED.json').read_text())
    require(hashlib.sha256(raw).hexdigest()==e['published_fixture_file_sha256'],'whole public fixture source')
    stars=json.loads(raw)['stars'];require(len(stars)==23,'reviewed generic23 carrier')
    qualified=[]
    for index,words in enumerate(stars):
        tick();blocks=list(map(frozenset,words))
        require(len(blocks)==20 and len(set(blocks))==20 and all(len(q)==4 and q<=set(range(17)) for q in blocks),'literal positive star')
        require(all(len(a&b)<=1 for a,b in itertools.combinations(blocks,2)),'literal star pair packing')
        rep=[sum(p in q for q in blocks) for p in range(17)]
        if sorted(rep)!=[3,4,4,4]+[5]*13:continue
        heavy=rep.index(3);high=[p for p in range(17) if rep[p]<5]
        if any(not any({heavy,h}<=q for q in blocks) for h in high if h!=heavy):continue
        friends=[p for p in range(17) if p!=heavy and not any({heavy,p}<=q for q in blocks)]
        require(len(friends)==7 and all(rep[p]==5 for p in friends),'seven actual LOW heavy friends')
        qualified.append((index,words,heavy,friends))
    require(len(qualified)==1,'exact positive unique-C-fixture baseline, not a new census')
    return qualified[0]

def normalize(words,heavy,a,b):
    shared=next(q for q in words if a in q and b in q)
    extras=sorted(set(shared)-{a,b});require(len(extras)==2 and heavy not in shared,'actual B extras')
    first=sorted(tuple(sorted(set(q)-{a})) for q in words if a in q and b not in q)
    second=sorted(tuple(sorted(set(q)-{b})) for q in words if b in q and a not in q)
    require(len(first)==len(second)==4,'two literal four-triple classes')
    absent=[next(i for i,row in enumerate(first) if not(set(row)&set(col))) for col in second]
    require(sorted(absent)==list(range(4)),'first/second missing perfect matching')
    cells=[(i,j) for i in range(4) for j in range(4) if i!=j]
    image={heavy:0,a:2,b:3,extras[0]:4,extras[1]:5}
    for p in set(range(17))-set(image):
        i=next(i for i,row in enumerate(first) if p in row)
        j=absent[next(j for j,col in enumerate(second) if p in col)]
        image[p]=6+cells.index((i,j))
    require(sorted(image.values())==[p for p in range(18) if p!=1],'whole actual17-to18 map, root1 omitted')
    fixed=sorted(sorted([1]+[image[p] for p in q]) for q in words)
    require(all(len(set(x)&set(y))<=2 for x,y in itertools.combinations(fixed,2)),'literal20-word root star')
    return [image[p] for p in range(17)],fixed

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();root=Path(__file__).parent
    index,words,heavy,friends=baseline(root)
    inp=json.loads((root/'INPUT.json').read_text());expect=json.loads((root/'EXPECTED.json').read_text())
    digest=hashlib.sha256(json.dumps(inp,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    require(digest==expect['input_math_sha256'] and len(inp['records'])==56,'whole anchor input')
    cases=[];bits=[]
    for a,b in itertools.permutations(friends,2):
        image,fixed=normalize(words,heavy,a,b);positives=[]
        for anchor_index,rec in enumerate(inp['records']):
            tick();added=rec['anchor'][9:]
            require(all(w in fixed for w in rec['anchor'][:9]),'all nine anchor words are actual star words')
            valid=all(len(set(x)&set(y))<=2 for x in added for y in fixed)
            bits.append(str(int(valid)))
            if valid:
                full=sorted(fixed+added)
                require(len({tuple(w) for w in full})==24 and all(len(set(x)&set(y))<=2 for x,y in itertools.combinations(full,2)),'whole literal24-word subpacking')
                positives.append(dict(anchor_index=anchor_index,additional_words=added,full24=full))
        cases.append(dict(old_C_pair=[a,b],point_image=image,fixed_star=fixed,positive_anchors=positives))
    math=dict(cases=2352,input_math_sha256=digest,fixture_index=index,fixture_star=words,fixture_heavy=heavy,
              fixture_friends=friends,coverage=''.join(bits),pair_cases=cases)
    common=hashlib.sha256(json.dumps(math,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    result=dict(agent='six-code-3',role='researcher',status='COMPLETE_ALL_FULL_STAR_ANCHOR_INTERSECTION_TESTS',
                mathematics=math,common_math_sha256=common,states=STATES,guard_states=500000,guard_seconds=20)
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(dict(status=result['status'],positive_pairs=sum(bool(c['positive_anchors']) for c in cases),
                          positive_anchors=sum(len(c['positive_anchors']) for c in cases),common_math_sha256=common),sort_keys=True))
if __name__=='__main__':main()
