"""Complete physical root-star maps by the two missing-matchings."""
import argparse, hashlib, itertools, json, time
from pathlib import Path
START = time.monotonic()
STATES = 0

def require(ok, message):
    if not ok: raise ValueError(message)

def tick():
    global STATES
    STATES += 1
    if STATES > 500000 or time.monotonic() - START > 20:
        raise RuntimeError('INCOMPLETE: original500000/20 guard')


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output', type=Path, required=True)
    args=ap.parse_args(); base=Path(__file__).parent
    inp=json.loads((base/'INPUT.json').read_text()); expected=json.loads((base/'EXPECTED.json').read_text())
    raw=(base/'FIXTURES.json').read_bytes()
    require(hashlib.sha256(raw).hexdigest()==expected['fixture_file_sha256'], 'published whole fixture')
    stars=json.loads(raw)['stars']; qualified=[]
    require(len(stars)==23,'reviewed generic23-star input')
    for k,ws in enumerate(stars):
        tick(); sets=list(map(frozenset,ws))
        require(len(sets)==len(set(sets))==20 and all(len(w)==4 and w<=set(range(17)) for w in sets), 'positive20-star')
        require(all(len(x&y)<=1 for x,y in itertools.combinations(sets,2)), 'positive star pair packing')
        rep=[sum(p in w for w in sets) for p in range(17)]
        if sorted(rep)!=[3,4,4,4]+[5]*13: continue
        h=rep.index(3); hi=[p for p in range(17) if rep[p]<5]
        if any(not any({h,p}<=w for w in sets) for p in hi if p!=h): continue
        friends=[p for p in range(17) if p!=h and not any({h,p}<=w for w in sets)]
        require(len(friends)==7 and all(rep[p]==5 for p in friends), 'seven heavy LOW friends')
        qualified.append((k,ws,h,friends))
    require(len(qualified)==1,'unique C fixture in credited complete carrier')
    fixture_index, words, heavy, friends=qualified[0]
    maps=[]; groups=[]
    for anchor_rec in inp['anchors']:
        anchor=anchor_rec['anchor']; rep=anchor_rec['representative']
        for root in [1,2,3]:
            left,right=[p for p in [1,2,3] if p!=root]
            targetA=sorted(tuple(p for p in w if p not in [root,left]) for w in anchor if root in w and left in w and right not in w)
            targetB=sorted(tuple(p for p in w if p not in [root,right]) for w in anchor if root in w and right in w and left not in w)
            require(len(targetA)==len(targetB)==4,'four actual pair-anchor triples')
            target_absent=[next(i for i,t in enumerate(targetA) if not(set(t)&set(col))) for col in targetB]
            require(sorted(target_absent)==list(range(4)), 'target missing matching')
            unique={}; ids=[]
            for a,b in itertools.permutations(friends,2):
                B=next(w for w in words if a in w and b in w)
                extras=sorted(set(B)-{a,b})
                sourceA=sorted(tuple(sorted(set(w)-{a})) for w in words if a in w and b not in w)
                sourceB=sorted(tuple(sorted(set(w)-{b})) for w in words if b in w and a not in w)
                require(len(sourceA)==len(sourceB)==4 and len(extras)==2 and heavy not in B, 'source pair structure')
                absent=[next(i for i,t in enumerate(sourceA) if not(set(t)&set(col))) for col in sourceB]
                require(sorted(absent)==list(range(4)), 'source missing matching')
                for permutation in itertools.permutations(range(4)):
                    image={heavy:0,a:left,b:right}
                    for p in set(range(17))-set(image)-set(extras):
                        i=next(i for i,t in enumerate(sourceA) if p in t)
                        j=next(j for j,t in enumerate(sourceB) if p in t)
                        col=targetB[target_absent.index(permutation[absent[j]])]
                        meet=set(targetA[permutation[i]])&set(col)
                        require(len(meet)==1,'unique physical cell image')
                        image[p]=next(iter(meet))
                    for swap in [0,1]:
                        tick(); image[extras[0]]=4+swap; image[extras[1]]=5-swap
                        point_map=[image[p] for p in range(17)]
                        require(sorted(point_map)==[p for p in range(18) if p!=root], 'physical17-to18 map')
                        fixed=sorted(sorted([root]+[image[p] for p in w]) for w in words)
                        outside=[i for i,w in enumerate(anchor) if root not in w]
                        require(sum(w in fixed for w in anchor)==9, 'all nine root-anchor words')
                        conflict=next(([i,j] for i,w in enumerate(fixed) for j in outside
                                       if len(set(w)&set(anchor[j]))>2), None)
                        used=set().union(*(set(w)-{0,root} for w in fixed if 0 in w))
                        missing=sorted(set(range(4,18))-used)
                        require(len(missing)==5,'actual heavy0 missing W five-set')
                        mid=len(maps); ids.append(mid)
                        maps.append(dict(id=mid,anchor=rep,root=root,old_C_pair=[a,b],
                                         first_class_permutation=list(permutation),B_extra_order=swap,
                                         point_image=point_map,full20=fixed,compatible=conflict is None,
                                         conflict=conflict,missing_W=missing))
                        if conflict is None: unique.setdefault(tuple(map(tuple,fixed)),[]).append(mid)
            require(len(ids)==2016,'complete2016 raw domain per root')
            candidates=[dict(full20=[list(w) for w in key],map_ids=unique[key],
                             missing_W=maps[unique[key][0]]['missing_W']) for key in sorted(unique)]
            groups.append(dict(anchor=rep,root=root,map_ids=ids,candidates=candidates))
    math=dict(cases=12096,fixture_index=fixture_index,fixture_heavy=heavy,fixture_friends=friends,
              maps=maps,groups=groups,input_sha256=hashlib.sha256((base/'INPUT.json').read_bytes()).hexdigest())
    require(len(maps)==12096,'complete six-root domain')
    common=hashlib.sha256(json.dumps(math,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    result=dict(agent='six-code-3',role='researcher',status='COMPLETE_LITERAL_ROOT_STAR_IMAGE_CENSUS',
                mathematics=math,common_math_sha256=common,states=STATES,guard_states=500000,guard_seconds=20)
    args.output.write_text(json.dumps(result,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps(dict(status=result['status'],common_math_sha256=common,
                         groups=[dict(anchor=g['anchor'],root=g['root'],candidates=len(g['candidates'])) for g in groups])))

if __name__=='__main__': main()
