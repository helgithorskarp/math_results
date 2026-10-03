"""Independent exhaustive bijections of the two literal four-block classes."""
import argparse, hashlib, itertools, json, time
from pathlib import Path
START=time.monotonic(); STATES=0

def require(ok,message):
    if not ok: raise ValueError(message)

def tick():
    global STATES
    STATES += 1
    if STATES > 500000 or time.monotonic() - START > 20:
        raise RuntimeError('INCOMPLETE: original500000/20 guard')


def mask(points): return sum(1<<p for p in points)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    base=Path(__file__).parent; inp=json.loads((base/'INPUT.json').read_text()); expected=json.loads((base/'EXPECTED.json').read_text())
    raw=(base/'FIXTURES.json').read_bytes()
    require(hashlib.sha256(raw).hexdigest()==expected['fixture_file_sha256'],'whole public fixture bytes')
    stars=json.loads(raw)['stars']; require(len(stars)==23,'credited23-star carrier'); qualified=[]
    for k,ws in enumerate(stars):
        tick();blocks=[mask(w) for w in ws]
        require(len(set(blocks))==len(blocks)==20 and all(w.bit_count()==4 and 0<w<1<<17 for w in blocks),'mask positive star')
        require(all((x&y).bit_count()<=1 for x,y in itertools.combinations(blocks,2)),'mask pair intersections')
        rep=[sum(bool(w&(1<<p)) for w in blocks) for p in range(17)]
        if sorted(rep)!=[3,4,4,4]+[5]*13: continue
        heavy=rep.index(3);neighbors=0
        for w in blocks:
            if w&(1<<heavy): neighbors|=w
        if any(not(neighbors&(1<<p)) for p in range(17) if p!=heavy and rep[p]<5): continue
        friends=[p for p in range(17) if p!=heavy and not(neighbors&(1<<p))]
        require(len(friends)==7 and all(rep[p]==5 for p in friends),'heavy friends')
        qualified.append((k,ws,blocks,heavy,friends))
    require(len(qualified)==1,'unique C fixture baseline')
    fixture_index,words,blocks,heavy,friends=qualified[0];maps=[];groups=[]
    permutations=list(itertools.permutations(range(4)))
    for anchor_rec in inp['anchors']:
        anchor=anchor_rec['anchor'];rep=anchor_rec['representative'];anchor_masks=[mask(w) for w in anchor]
        for root in [1,2,3]:
            left,right=[p for p in [1,2,3] if p!=root]
            targetA=sorted(tuple(p for p in w if p not in [root,left]) for w in anchor if root in w and left in w and right not in w)
            targetB=sorted(tuple(p for p in w if p not in [root,right]) for w in anchor if root in w and right in w and left not in w)
            ta=list(map(mask,targetA));tb=list(map(mask,targetB));unique={};ids=[]
            for a,b in itertools.permutations(friends,2):
                shared=next(w for w in blocks if w&(1<<a) and w&(1<<b))
                extras=[p for p in range(17) if shared&(1<<p) and p not in [a,b]]
                sourceA=sorted(tuple(p for p in range(17) if w&(1<<p) and p!=a) for w in blocks if w&(1<<a) and not(w&(1<<b)))
                sourceB=sorted(tuple(p for p in range(17) if w&(1<<p) and p!=b) for w in blocks if w&(1<<b) and not(w&(1<<a)))
                sa=list(map(mask,sourceA));sb=list(map(mask,sourceB))
                incidence=[[(x&y).bit_count() for y in sb] for x in sa]
                targets=[[(x&y).bit_count() for y in tb] for x in ta]
                for first in permutations:
                    second_maps=[]
                    for second in permutations:
                        tick()
                        if all(incidence[i][j]==targets[first[i]][second[j]] for i in range(4) for j in range(4)):
                            second_maps.append(second)
                    require(len(second_maps)==1,'complete second-class bijection search gives one per first map')
                    second=second_maps[0];image=[None]*17;image[heavy]=0;image[a]=left;image[b]=right
                    for i in range(4):
                        for j in range(4):
                            cell=sa[i]&sb[j]
                            if not cell: continue
                            other=ta[first[i]]&tb[second[j]]
                            require(cell.bit_count()==other.bit_count()==1,'actual singleton incidence image')
                            image[cell.bit_length()-1]=other.bit_length()-1
                    for swap in [0,1]:
                        tick();image[extras[0]]=4+swap;image[extras[1]]=5-swap
                        require(sorted(image)==[p for p in range(18) if p!=root],'whole physical point bijection')
                        fixed_masks=sorted(mask([root]+[image[p] for p in w]) for w in words)
                        fixed=sorted([p for p in range(18) if w&(1<<p)] for w in fixed_masks)
                        require(sum(mask(w) in fixed_masks for w in anchor)==9,'nine original pair words retained')
                        conflict=None
                        for i,w in enumerate(fixed):
                            for j,q in enumerate(anchor_masks):
                                if q&(1<<root): continue
                                if (mask(w)&q).bit_count()>2: conflict=[i,j];break
                            if conflict is not None: break
                        heavy_neighbors=0
                        for w in fixed_masks:
                            if w&1: heavy_neighbors|=w
                        missing=[p for p in range(4,18) if not(heavy_neighbors&(1<<p))]
                        require(len(missing)==5,'five missing physical W points')
                        mid=len(maps);ids.append(mid)
                        maps.append(dict(id=mid,anchor=rep,root=root,old_C_pair=[a,b],
                                         first_class_permutation=list(first),B_extra_order=swap,
                                         point_image=list(image),full20=fixed,compatible=conflict is None,
                                         conflict=conflict,missing_W=missing))
                        if conflict is None: unique.setdefault(tuple(map(tuple,fixed)),[]).append(mid)
            require(len(ids)==2016,'raw2016 complete root domain')
            candidates=[dict(full20=[list(w) for w in key],map_ids=unique[key],
                             missing_W=maps[unique[key][0]]['missing_W']) for key in sorted(unique)]
            groups.append(dict(anchor=rep,root=root,map_ids=ids,candidates=candidates))
    math=dict(cases=12096,fixture_index=fixture_index,fixture_heavy=heavy,fixture_friends=friends,
              maps=maps,groups=groups,input_sha256=hashlib.sha256((base/'INPUT.json').read_bytes()).hexdigest())
    require(len(maps)==12096,'all physical maps retained')
    common=hashlib.sha256(json.dumps(math,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    result=dict(agent='six-code-3',role='researcher',status='COMPLETE_INDEPENDENT_BLOCK_BIJECTION_CENSUS',
                mathematics=math,common_math_sha256=common,states=STATES,guard_states=500000,guard_seconds=20)
    args.output.write_text(json.dumps(result,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps(dict(status=result['status'],common_math_sha256=common,
                         groups=[dict(anchor=g['anchor'],root=g['root'],candidates=len(g['candidates'])) for g in groups])))

if __name__=='__main__': main()
