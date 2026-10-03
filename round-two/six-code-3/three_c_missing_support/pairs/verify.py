"""Independent literal full-star images, pair bits, triples and positive unions."""
import argparse,copy,hashlib,itertools,json,time
from pathlib import Path
START=time.monotonic();STATES=0
def require(ok,message):
    if not ok:raise ValueError(message)
def tick():
    global STATES
    STATES += 1
    if STATES > 500000 or time.monotonic() - START > 20:
        raise RuntimeError('INCOMPLETE: original500000/20 guard')


def validate(inp,math,fixture):
    require(math['cases']==349488 and len(math['coverage'])==349488,'entire paired domain')
    require(len(math['eligible_cases'])==sum(c!='0' for c in math['coverage']),'entire equal-missing list')
    require([(g['anchor'],g['root']) for g in inp['groups']]==[(a,r) for a in [0,10] for r in [1,2,3]],'six original groups')
    groups={};sets={};missing={}
    for g in inp['groups']:
        key=g['anchor'],g['root'];groups[key]=g['candidates'];sets[key]=[];missing[key]=[]
        require(len(g['candidates'])==(60 if g['anchor']==0 else 336),'credited complete candidate coverage')
        require(len({tuple(map(tuple,c['full20'])) for c in g['candidates']})==len(g['candidates']),'all whole candidate images distinct')
        anchor=next(a['anchor'] for a in inp['anchors'] if a['representative']==g['anchor'])
        for i,c in enumerate(g['candidates']):
            tick();words=c['full20'];ss=list(map(frozenset,words))
            require(c['id']==i and words==sorted(words) and len(set(ss))==len(ss)==20,'whole literal candidate')
            require(all(len(w)==5 and g['root'] in w and w<=set(range(18)) and all(type(p) is int for p in w) for w in ss),'actual root20-word shape')
            require(all(len(x&y)<=2 for x,y in itertools.combinations(ss,2)),'candidate star packing')
            require(len(c['origins'])==6,'all six recorded map origins')
            for origin in c['origins']:
                image=origin['point_image'];require(len(image)==17 and all(type(p) is int for p in image) and sorted(image)==[p for p in range(18) if p!=g['root']] and image[13]==0,'whole marked point map')
                require(sorted(sorted([g['root']]+[image[p] for p in w]) for w in fixture)==words,'entire original20-word image')
            union=set(ss)|set(map(frozenset,anchor))
            require(len(union)==24 and all(len(x&y)<=2 for x,y in itertools.combinations(union,2)),'literal anchor24 packing')
            F=sorted(p for p in range(4,18) if not any(0 in w and p in w for w in ss))
            require(len(F)==5 and c['missing_W']==F,'actual missing-W data')
            sets[key].append(ss);missing[key].append(F)
    at=0;eligible=[];summary=[]
    for rep in [0,10]:
        for r,t in itertools.combinations([1,2,3],2):
            start=at;same=positive=0
            for i,aa in enumerate(sets[rep,r]):
                for j,bb in enumerate(sets[rep,t]):
                    tick();F=missing[rep,r][i];G=missing[rep,t][j]
                    if F!=G:require(math['coverage'][at]=='0','unequal missing-set case');at+=1;continue
                    same+=1;conflict=next(([u,v] for u,x in enumerate(aa) for v,y in enumerate(bb) if x!=y and len(x&y)>=3),None)
                    require(math['coverage'][at]==('1' if conflict else '2'),'every equal-missing case bit')
                    triple=sorted(aa[conflict[0]]&bb[conflict[1]])[:3] if conflict else None
                    if conflict:
                        require(len(triple)==3 and set(triple)<=aa[conflict[0]] and set(triple)<=bb[conflict[1]],'literal repeated-triple obstruction')
                        union=None
                    else:
                        both=set(aa)|set(bb);require(len(both)==35 and all(len(x&y)<=2 for x,y in itertools.combinations(both,2)),'entire positive35 packing')
                        union=sorted(map(sorted,both));positive+=1
                    eligible.append(dict(case=at,anchor=rep,roots=[r,t],star_ids=[i,j],missing_W=F,conflict=conflict,repeated_triple=triple,full35=union));at+=1
            summary.append(dict(anchor=rep,roots=[r,t],start=start,cases=len(sets[rep,r])*len(sets[rep,t]),equal_missing=same,positive35=positive))
    require(at==349488 and eligible==math['eligible_cases'] and summary==math['groups'],'every whole pair record and group')
    return summary

def main():
    ap=argparse.ArgumentParser()
    for n in ['literal','dual','expected','output']:ap.add_argument('--'+n,type=Path,required=True)
    args=ap.parse_args();base=Path(__file__).parent;inp=json.loads((base/'INPUT.json').read_text());e=json.loads(args.expected.read_text())
    raw=(base/'FIXTURES.json').read_bytes();require(hashlib.sha256(raw).hexdigest()==e['fixture_file_sha256'],'whole published source fixture')
    fixture=json.loads(raw)['stars'][9];x=json.loads(args.literal.read_text());y=json.loads(args.dual.read_text())
    require(x['mathematics']==y['mathematics'],'every paired bit, full triple witness and35 packing agrees')
    m=x['mathematics'];common=hashlib.sha256(json.dumps(m,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    require(common==x['common_math_sha256']==y['common_math_sha256'],'whole mathematical hash')
    require(m['input_sha256']==hashlib.sha256((base/'INPUT.json').read_bytes()).hexdigest(),'whole declared input')
    summary=validate(inp,m,fixture);damages=[]
    for label in ['missing-case','wrong-first-bit','missing-eligible-record','wrong-point','wrong-star-word','wrong-missing-W']:
        bad=dict(m);badinp=inp
        if label=='missing-case':bad['coverage']=m['coverage'][:-1]
        elif label=='wrong-first-bit':bad['coverage']=('1' if m['coverage'][0]=='0' else '0')+m['coverage'][1:]
        elif label=='missing-eligible-record':bad['eligible_cases']=m['eligible_cases'][:-1] if m['eligible_cases'] else [{}]
        else:
            badinp=dict(inp);badinp['groups']=list(inp['groups']);badinp['groups'][0]=dict(inp['groups'][0]);badinp['groups'][0]['candidates']=list(inp['groups'][0]['candidates']);c=copy.deepcopy(inp['groups'][0]['candidates'][0]);badinp['groups'][0]['candidates'][0]=c
            if label=='wrong-point':c['origins'][0]['point_image'][0]=18
            elif label=='wrong-star-word':c['full20'][0][0]=18
            else:c['missing_W'][0]=0
        try:validate(badinp,bad,fixture)
        except ValueError:damages.append(label)
        else:raise ValueError('semantic corruption accepted: '+label)
    out=dict(agent='six-code-3',role='researcher',status='COMPLETE_AUTHOR_CHECKED_EQUAL_MISSING_C_PAIR_DOMAIN',cases=349488,
             common_math_sha256=common,groups=summary,semantic_rejections=damages,states=STATES,
             positive35=sum(g['positive35'] for g in summary),ordinary_bridges_formalized=False,independent_person_review=False,
             guard_states=500000,guard_seconds=20,no_unrestricted_endpoint_improvement=True)
    args.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
