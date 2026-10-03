"""Literal certificate checks; imports neither enumeration implementation."""
import argparse, copy, hashlib, itertools, json, time
from pathlib import Path
START=time.monotonic(); STATES=0

def require(ok,message):
    if not ok: raise ValueError(message)

def tick():
    global STATES
    STATES += 1
    if STATES > 500000 or time.monotonic() - START > 20:
        raise RuntimeError('INCOMPLETE: original500000/20 guard')


def validate(math,inp,stars,controls):
    require(math['cases']==12096 and len(math['maps'])==12096 and len(math['groups'])==6,'whole declared raw domain')
    require(math['fixture_index']==9 and math['fixture_heavy']==13 and math['fixture_friends']==[0,1,3,4,8,9,10], 'credited unique C carrier')
    source=stars[9];friends=math['fixture_friends'];all_cases=[];groups=[]
    for anchor_rec in inp['anchors']:
        anchor=anchor_rec['anchor'];rep=anchor_rec['representative']
        require(len(anchor)==len(set(map(tuple,anchor)))==13 and all(len(w)==5 for w in anchor),'literal13-anchor')
        require(all(len(set(x)&set(y))<=2 for x,y in itertools.combinations(anchor,2)),'anchor packing')
        for root in [1,2,3]:
            left,right=[p for p in [1,2,3] if p!=root]
            target=sorted(tuple(p for p in w if p not in [root,left]) for w in anchor if root in w and left in w and right not in w)
            dedup={}; ids=[]
            for a,b in itertools.permutations(friends,2):
                first=sorted(tuple(sorted(set(w)-{a})) for w in source if a in w and b not in w)
                shared=next(w for w in source if a in w and b in w);extras=sorted(set(shared)-{a,b})
                for permutation in itertools.permutations(range(4)):
                    for swap in [0,1]:
                        tick();mid=len(all_cases); rec=math['maps'][mid];image=rec['point_image']
                        require(rec['id']==mid and rec['anchor']==rep and rec['root']==root and rec['old_C_pair']==[a,b]
                                and rec['first_class_permutation']==list(permutation) and rec['B_extra_order']==swap,'exact full parameter coverage and labels')
                        require(len(image)==17 and all(type(p) is int for p in image) and sorted(image)==[p for p in range(18) if p!=root], 'point image literal bijection')
                        require(image[13]==0 and image[a]==left and image[b]==right and image[extras[0]]==4+swap
                                and image[extras[1]]==5-swap,'literal marked-point transport')
                        require(all(sorted(image[p] for p in first[i])==list(target[permutation[i]]) for i in range(4)), 'first-class block image')
                        fixed=sorted(sorted([root]+[image[p] for p in w]) for w in source)
                        require(rec['full20']==fixed and len(set(map(tuple,fixed)))==20,'entire original20-word image')
                        sets=list(map(frozenset,fixed))
                        require(all(len(w)==5 and root in w for w in sets) and all(len(x&y)<=2 for x,y in itertools.combinations(sets,2)),'full positive root star')
                        require(sum(w in fixed for w in anchor)==9,'nine pair-anchor words')
                        conflict=next(([i,j] for i,w in enumerate(sets) for j,q in enumerate(anchor)
                                       if root not in q and len(w&set(q))>2),None)
                        require(rec['compatible']==(conflict is None) and rec['conflict']==conflict,'every positive/negative whole-word bit')
                        missing=[p for p in range(4,18) if not any(0 in w and p in w for w in sets)]
                        require(rec['missing_W']==missing and len(missing)==5,'literal missing heavy W set')
                        all_cases.append(mid);ids.append(mid)
                        if conflict is None:
                            union=set(sets)|set(map(frozenset,anchor))
                            require(len(union)==24 and all(len(x&y)<=2 for x,y in itertools.combinations(union,2)),'actual positive24 packing')
                            dedup.setdefault(tuple(map(tuple,fixed)),[]).append(mid)
            candidates=[dict(full20=[list(w) for w in key],map_ids=dedup[key],missing_W=math['maps'][dedup[key][0]]['missing_W']) for key in sorted(dedup)]
            groups.append(dict(anchor=rep,root=root,map_ids=ids,candidates=candidates))
    require(math['groups']==groups,'whole literal deduplication preserves every actual map')
    for control in controls:
        tick();matches=[m for m in math['maps'] if m['anchor']==control['anchor_representative'] and m['root']==control['C_root']
                       and m['point_image']==control['original17_point_image']]
        require(len(matches)==1 and matches[0]['compatible'] and matches[0]['full20']==control['full20_star'],'existing positive geometry map reproduced')
        anchor=next(a['anchor'] for a in inp['anchors'] if a['representative']==control['anchor_representative'])
        actual=sorted(map(list,set(map(tuple,anchor))|set(map(tuple,matches[0]['full20']))))
        require(actual==control['full24_control'],'whole existing24-word control')
    return [dict(anchor=g['anchor'],root=g['root'],raw=2016,
                 compatible_raw=sum(math['maps'][i]['compatible'] for i in g['map_ids']),
                 distinct_full20=len(g['candidates']),distinct_missing_W=len({tuple(c['missing_W']) for c in g['candidates']})) for g in groups]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--force-incomplete-damage-control',action='store_true')
    for name in ['literal','dual','expected','output']: ap.add_argument('--'+name,type=Path,required=True)
    args=ap.parse_args();base=Path(__file__).parent
    expected=json.loads(args.expected.read_text()); inp=json.loads((base/'INPUT.json').read_text())
    raw=(base/'FIXTURES.json').read_bytes(); require(hashlib.sha256(raw).hexdigest()==expected['fixture_file_sha256'],'entire public fixture input')
    stars=json.loads(raw)['stars']; controls=json.loads((base/'GEOMETRY_CONTROLS.json').read_text())
    left=json.loads(args.literal.read_text());right=json.loads(args.dual.read_text())
    require(left['mathematics']==right['mathematics'],'every raw map/word/coverage/group agrees')
    common=hashlib.sha256(json.dumps(left['mathematics'],sort_keys=True,separators=(',',':')).encode()).hexdigest()
    require(left['common_math_sha256']==right['common_math_sha256']==common,'whole common mathematical hash')
    require(left['mathematics']['input_sha256']==hashlib.sha256((base/'INPUT.json').read_bytes()).hexdigest(),'declared actual anchor input')
    global STATES
    if args.force_incomplete_damage_control:
        STATES=500000
        try: validate(left['mathematics'],inp,stars,controls)
        except ValueError: raise ValueError('INCOMPLETE was wrongly swallowed as semantic damage')
        raise ValueError('forced guard should have propagated')
    summary=validate(left['mathematics'],inp,stars,controls)
    damages=[]
    for label in ['missing-map','wrong-point','false-word','false-bit','wrong-W','dropped-dedup-origin','false-parameter']:
        damaged=dict(left['mathematics'])
        damaged['maps']=list(left['mathematics']['maps'])
        damaged['maps'][0]=copy.deepcopy(left['mathematics']['maps'][0])
        damaged['groups']=list(left['mathematics']['groups'])
        damaged['groups'][0]=copy.deepcopy(left['mathematics']['groups'][0])
        if label=='missing-map':damaged['maps'].pop()
        elif label=='wrong-point':damaged['maps'][0]['point_image'][0]=18
        elif label=='false-word':damaged['maps'][0]['full20'][0][0]=18
        elif label=='false-bit':damaged['maps'][0]['compatible']=not damaged['maps'][0]['compatible']
        elif label=='wrong-W':damaged['maps'][0]['missing_W'][0]=0
        elif label=='dropped-dedup-origin':damaged['groups'][0]['candidates'][0]['map_ids'].pop()
        elif label=='false-parameter':damaged['maps'][0]['old_C_pair']=[0,0]
        try: validate(damaged,inp,stars,controls)
        except ValueError:damages.append(label)
        else:raise ValueError('semantic damage accepted: '+label)
    require(len(damages)==7,'every semantic control rejected')
    out=dict(agent='six-code-3',role='researcher',status='COMPLETE_AUTHOR_CHECKED_FULL_C_STAR_IMAGE_DOMAIN',
             cases=12096,common_math_sha256=common,groups=summary,
             geometry_controls=6,semantic_rejections=damages,states=STATES,
             independent_person_review=False,ordinary_bridges_formalized=False,
             guard_states=500000,guard_seconds=20,no_K17_or_endpoint_verdict=True)
    args.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,sort_keys=True))

if __name__=='__main__':main()
