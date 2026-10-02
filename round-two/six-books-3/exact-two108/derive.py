"""Complete exact-two Book108 exception/star producer; standard-library only."""
import argparse,hashlib,itertools,json
from pathlib import Path

PROFILES = [(0,3,3),(1,2,3),(1,3,2),(2,1,3),(2,2,2),(2,3,1)]

def require(value, message):
    if not value:
        raise ValueError(message)

def types_for(profile):
    r,s,t = profile
    types = [1,2,7,11]
    for mask, count in [(3,r),(5,s),(9,t),(6,t),(10,s),(12,r+2)]:
        types += [mask]*count
    require(len(types)==18 and all(sum(bool(m>>i&1) for m in types)==9 for i in range(4)), 'wrong actual incidence')
    return types

def partitions(length, bound):
    def visit(word):
        if len(word)==length:
            yield tuple(word)
            return
        for value in range(min(bound, max(word,default=-1)+2)):
            yield from visit(word+[value])
    yield from visit([])

def exceptions(types):
    available = {m: [x for x,t in enumerate(types) if t==m] for m in sorted(set(types))}
    choices = [[m for m in available if m>>i&1] for i in range(4)]
    result=[]
    for word in itertools.product(*choices):
        if any(bool(word[i]>>j&1)!=bool(word[j]>>i&1) for i in range(4) for j in range(i)):
            continue
        groups = [(m,[i for i in range(4) if word[i]==m]) for m in sorted(set(word))]
        for codes in itertools.product(*(list(partitions(len(indices),len(available[m]))) for m,indices in groups)):
            selected=[None]*4
            for (m,indices),code in zip(groups,codes):
                for i,value in zip(indices,code):selected[i]=available[m][value]
            require(all(selected[i] is not None for i in range(4)), 'incomplete exception')
            result.append(tuple(selected))
    require(len(result)==len(set(result)), 'duplicate canonical template')
    return sorted(result)

def domains(types):
    masks=[sum(1<<x for x,t in enumerate(types) if t>>i&1) for i in range(4)]
    result={}
    examined=0
    for x,tx in enumerate(types):
        caps=[3 if tx>>i&1 else 5 for i in range(4)]
        for neighbors in itertools.combinations([y for y in range(18) if y!=x],10-tx.bit_count()):
            star=sum(1<<y for y in neighbors);examined+=1
            deficits=[caps[i]-(star&masks[i]).bit_count() for i in range(4)]
            if any(d not in (0,1) or (d and not (tx>>i&1)) for i,d in enumerate(deficits)):
                continue
            signature=sum(d<<i for i,d in enumerate(deficits))
            result.setdefault((x,signature),[]).append(star)
    return {k:tuple(sorted(v)) for k,v in result.items()},examined,masks

def compatible(x,sx,y,sy,types,masks,triangle_cut=True):
    red=bool(sx>>y&1)
    if red!=bool(sy>>x&1):return False
    shared=types[x]&types[y]
    common=sx&sy
    if common.bit_count()+shared.bit_count()>(3 if red else 6):return False
    if triangle_cut and red and any(common&masks[i] for i in range(4) if shared>>i&1):return False
    return True

def static_cover(row_domains,types,masks,triangle_cut=True):
    """Each removed target must lack support in a COMPLETE initial other domain."""
    for target in sorted(range(18),key=lambda x:len(row_domains[x])):
        covered=[]
        remaining=set(row_domains[target])
        for other in sorted((y for y in range(18) if y!=target),key=lambda y:len(row_domains[y])):
            gone=[]
            for star in sorted(remaining):
                if not any(compatible(target,star,other,support,types,masks,triangle_cut) for support in row_domains[other]):
                    gone.append(star)
            if gone:
                covered.append({'other':other,'stars':gone})
                remaining.difference_update(gone)
            if not remaining:
                return {'target':target,'groups':covered,'count':len(row_domains[target])}
    return None


def propagate(initial,types,masks):
    current=[set(row) for row in initial]
    steps=[];passes=0
    while True:
        changed=False;passes+=1
        for target in sorted(range(18),key=lambda x:len(current[x])):
            for other in sorted((y for y in range(18) if y!=target),key=lambda y:len(current[y])):
                supports=tuple(sorted(current[other]));gone=[]
                for star in sorted(current[target]):
                    if not any(compatible(target,star,other,support,types,masks,True) for support in supports):gone.append(star)
                if gone:
                    steps.append({'target':target,'other':other,'stars':gone})
                    current[target].difference_update(gone);changed=True
                    if not current[target]:
                        return {'status':'EXACT_ARC_EMPTY','empty_target':target,'steps':steps,'passes':passes,'remaining_counts':[len(row) for row in current]}
        if not changed:return {'status':'UNRESOLVED_ARC_FIXED_POINT','steps':steps,'passes':passes,'remaining_counts':[len(row) for row in current]}



def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'))

def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()

def build(domain_record=False):
    packet={'schema':1,'claim':'No valid rootless9^4,10^18 graph has exactly two one-nine roots','profiles':[]}
    full_domains=[]
    summary={'profile_template_counts':[],'templates':0,'empty':0,'static':0,'arc':0,'deletion_batches':0,'deleted_stars':0,'raw_star_subsets':0}
    for profile in PROFILES:
        types=types_for(profile);templates=exceptions(types);saved,examined,masks=domains(types)
        summary['raw_star_subsets']+=examined
        summary['profile_template_counts'].append(len(templates))
        cases=[];full_cases=[]
        for selected in templates:
            columns=[sum(1<<i for i,x in enumerate(selected) if x==y) for y in range(18)]
            initial=[saved.get((x,columns[x]),()) for x in range(18)]
            empty=[x for x,row in enumerate(initial) if not row]
            raw_steps=[]
            if empty:
                kind='empty';target=min(empty)
            else:
                cover=static_cover(initial,types,masks,True)
                if cover is not None:
                    kind='static';target=cover['target']
                    raw_steps=[(target,g['other'],g['stars']) for g in cover['groups']]
                else:
                    arc=propagate(initial,types,masks)
                    require(arc['status']=='EXACT_ARC_EMPTY','Unresolved exact-two template; no complete-exclusion packet')
                    kind='arc';target=arc['empty_target']
                    raw_steps=[(s['target'],s['other'],s['stars']) for s in arc['steps']]
            case={'exceptions':list(selected),'domain_sizes':[len(row) for row in initial],'domain_sha256':digest(initial),'kind':kind,'empty_target':target,'steps':[[x,y,len(stars)] for x,y,stars in raw_steps],'deletions_sha256':digest(raw_steps)}
            cases.append(case)
            if domain_record:full_cases.append({'exceptions':list(selected),'domains':initial,'deletions':raw_steps})
            summary['templates']+=1;summary[kind]+=1
            summary['deletion_batches']+=len(raw_steps)
            summary['deleted_stars']+=sum(len(stars) for _,_,stars in raw_steps)
        packet['profiles'].append({'profile':list(profile),'types':types,'cases':cases})
        if domain_record:full_domains.append({'profile':list(profile),'cases':full_cases})
    summary['certificate_canonical_sha256']=digest(packet)
    return packet,summary,full_domains

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--emit',action='store_true',help='Print freshly produced compact certificate; do not rewrite source')
    parser.add_argument('--domains',action='store_true',help='Print every initial domain and deletion for private independent entry comparison')
    parser.add_argument('--certificate',type=Path,default=Path(__file__).with_name('certificate.json'))
    parser.add_argument('--expected',type=Path)
    args=parser.parse_args();packet,summary,full=build(args.domains)
    if args.emit:print(canonical(packet));return
    if args.domains:print(canonical(full));return
    loaded=json.loads(args.certificate.read_text())
    require(canonical(loaded)==canonical(packet),'Frozen certificate differs from full regenerated producer')
    if args.expected is not None:require(canonical(json.loads(args.expected.read_text()))==canonical(summary),'Expected producer summary mismatch')
    print(canonical(summary))

if __name__=='__main__':main()
