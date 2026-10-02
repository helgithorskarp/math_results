"""Independent physical slack, half-domain and literal-endpoint certificate audit."""
import argparse
import collections
import hashlib
import itertools
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
SCOPE='No full-valid22-point completion of canonical three-triple incidence profiles0 or1 from9371; no other profile or Ramsey endpoint exclusion.'

def require(ok,message):
    if not ok:
        raise ValueError(message)

def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'))

def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()

def configuration(index):
    raw=(ROOT/'incidence.json').read_bytes()
    require(hashlib.sha256(raw).hexdigest()=='10c23fac3815df26beb8120854ad46c9a87bd15c1b29fa40514c64e6eb8dbd6f','primitive profile source changed')
    require(type(index) is int and index in (0,1),'bad selected triple profile')
    counts=json.loads(raw)['sectors'][0]['canonical'][index]
    types=tuple(m for m in range(1,16) for _ in range(counts[m-1]))
    red=[tuple(x for x,t in enumerate(types) if t&(1<<i)) for i in range(4)]
    require(len(types)==18 and all(len(row)==9 for row in red),'actual degree margins')
    # Literal total mixed cap72 minus the whole actual H two-walk total.
    budget=[72-sum(10-sum(bool(types[x]&(1<<j)) for j in range(4)) for x in row) for row in red]
    require(sum(budget)==6 and all(1<=d<=3 for d in budget),'actual mixed budgets')
    return counts,types,red,budget

def physical_templates(types,red,budget):
    options=[]
    for i,d in enumerate(budget):
        blue=tuple(x for x in range(18) if x not in red[i]);row_options=[]
        for alpha in range(1,d+1,2):
            for rpoints in itertools.combinations_with_replacement(red[i],alpha):
                for bpoints in itertools.combinations_with_replacement(blue,d-alpha):
                    row=[0]*18
                    for x in rpoints+bpoints:row[x]+=1
                    transport=tuple(sum(row[x] for x in red[j]) for j in range(4))
                    row_options.append((tuple(row),transport))
        require(len({row for row,_ in row_options})==len(row_options),'duplicate physical row')
        options.append(row_options)
    census=0;surviving=0;found=collections.Counter()
    for chosen in itertools.product(*options):
        census+=1
        walk=[rec[1] for rec in chosen]
        if any(walk[i][j]!=walk[j][i] for i in range(4) for j in range(i)):continue
        surviving+=1
        rows=[rec[0] for rec in chosen]
        column=[sum(rows[i][x]*(4**i) for i in range(4)) for x in range(18)]
        cell=collections.defaultdict(list)
        for x,t in enumerate(types):cell[t].append(column[x])
        template=tuple(v for t in sorted(cell) for v in sorted(cell[t]))
        found[template]+=1
    require(census==__import__('math').prod(len(r) for r in options),'incomplete physical matrix census')
    return sorted(found),{'physical_row_options':[len(r) for r in options],'physical_matrices':census,
                          'symmetric_physical_matrices':surviving,'orbit_sizes':[found[r] for r in sorted(found)]}

def half(vertices,types):
    result=[]
    for word in range(1<<len(vertices)):
        points=[v for k,v in enumerate(vertices) if word&(1<<k)]
        result.append((sum(1<<v for v in points),len(points),
                       tuple(sum(bool(types[v]&(1<<i)) for v in points) for i in range(4))))
    return result

def physical_domains(types,budget):
    rows=collections.defaultdict(list);examined=0
    for x,t in enumerate(types):
        right=collections.defaultdict(list)
        for rec in half([v for v in range(9,18) if v!=x],types):right[rec[1]].append(rec)
        size=10-sum(bool(t&(1<<i)) for i in range(4))
        for lm,ln,lc in half([v for v in range(9) if v!=x],types):
            for rm,rn,rc in right[size-ln]:
                examined+=1
                deficits=[(3 if t&(1<<i) else 5)-(lc[i]+rc[i]) for i in range(4)]
                valid=True
                for i,d in enumerate(deficits):
                    red=bool(t&(1<<i))
                    # A positive odd red row sum is1, or3 only at budget3.
                    largest=(3 if budget[i]==3 else 1) if red else budget[i]-1
                    if d<0 or d>largest:valid=False;break
                if not valid:continue
                code=sum(d*(4**i) for i,d in enumerate(deficits))
                rows[(x,code)].append(lm|rm)
    require(all(len(row)==len(set(row)) for row in rows.values()),'duplicate physical neighbor subset')
    return {k:sorted(v) for k,v in rows.items()},examined

def verify(index,work=None,certificate=None):
    out=Path(work).resolve()/str(index) if work is not None else None
    counts,types,low_red,budget=configuration(index)
    templates,physical=physical_templates(types,low_red,budget)
    if out is not None:
        tpacket=json.loads((out/'templates.json').read_text())
        require(tpacket['profile']==index and tpacket['counts']==counts and tpacket['types']==list(types) and tpacket['budget']==budget,'template source/scope mismatch')
        require([list(t) for t in templates]==tpacket['templates'],'entire physical template list differs')
    domain,examined=physical_domains(types,budget)
    if out is not None:
        dpacket=json.loads((out/'domains.json').read_text())
        require([[x,c,s] for (x,c),s in sorted(domain.items())]==dpacket['rows'],'entire high-star lists differ')
        require(examined==dpacket['raw_subsets'] and sum(len(r) for r in domain.values())==dpacket['stored_stars'],'star inventory mismatch')
    packet=json.loads(Path(certificate or ROOT/f'certificate-{index}.json').read_text())
    require(type(packet.get('schema')) is int and packet['schema']==1 and packet.get('scope')==SCOPE,'wrong quantified scope/schema')
    require(type(packet.get('profile')) is int,'noninteger profile')
    require(all(type(v) is int for key in ('counts','types','budget') for v in packet[key]),'noninteger model coordinate')
    require(packet['status']=='COMPLETE_NECESSARY_DOMAIN_CENSUS' and packet['claim_all_empty'] is True,'unfinished/false profile exclusion')
    require(packet['profile']==index and packet['counts']==counts and packet['types']==list(types) and packet['budget']==budget,'certificate scope mismatch')
    require(packet['templates']==len(templates) and len(packet['completed'])==len(templates),'missing/extra case')
    universe=frozenset(range(22));lows=frozenset(range(4))
    low_physical=[frozenset(4+x for x in row) for row in low_red]
    rcache={};bcache={}
    for (x,_),stars in domain.items():
        for star in stars:
            r=frozenset(i for i in range(4) if types[x]&(1<<i)) | frozenset(4+y for y in range(18) if star&(1<<y))
            require(len(r)==10 and 4+x not in r,'bad physical high degree')
            rcache[(x,star)]=r;bcache[(x,star)]=universe-r-{4+x}
    support_tests=0
    def allowed(x,sx,y,sy):
        nonlocal support_tests
        support_tests+=1
        require(support_tests<=2000000,'Operational verifier guard; no exclusion verdict')
        a=rcache[(x,sx)];b=rcache[(y,sy)];red=(4+y in a)
        if red!=(4+x in b):return False
        common=a&b
        if red:
            if len(common)>3:return False
            if any(common&low_physical[i] for i in common&lows):return False
        elif len(bcache[(x,sx)]&bcache[(y,sy)])>6:return False
        return True
    full=[];batches=0;removed=0
    for n,(columns,case) in enumerate(zip(templates,packet['completed'])):
        require(type(case['template']) is int and case['template']==n and case['columns']==list(columns),'wrong case coordinate')
        require(all(type(v) is int for v in case['columns']+case['initial_sizes']),'noninteger case coordinate')
        literal_steps=[]
        current=[set(domain.get((x,columns[x]),())) for x in range(18)]
        require(case['initial_sizes']==[len(r) for r in current],'wrong initial counts')
        initial=[sorted(r) for r in current];empty=[x for x,r in enumerate(current) if not r]
        require(case['status'] in ('INITIAL_EMPTY','ARC_EMPTY'),'unresolved case')
        if case['status']=='INITIAL_EMPTY':
            require(bool(empty) and not case['steps'] and type(case['empty_target']) is int and case['empty_target']==min(empty),'false initial empty')
        else:
            require(not empty,'wrong arc case')
            for step in case['steps']:
                x,y=step['target'],step['other']
                require(type(x) is int and type(y) is int and 0<=x<18 and 0<=y<18 and x!=y,'bad physical pair')
                unsupported=[sx for sx in sorted(current[x]) if not any(allowed(x,sx,y,sy) for sy in sorted(current[y]))]
                require(type(step['count']) is int and bool(unsupported) and len(unsupported)==step['count'] and digest(unsupported)==step['sha256'],'whole regenerated unsupported set count/hash differs')
                literal_steps.append({'target':x,'other':y,'stars':unsupported})
                current[x].difference_update(unsupported);batches+=1;removed+=len(unsupported)
            require(type(case['empty_target']) is int and 0<=case['empty_target']<18 and not current[case['empty_target']],'false final empty')
            require(case['remaining_sizes']==[len(r) for r in current],'remaining sizes mismatch')
        full.append({'columns':list(columns),'initial_domains':initial,'steps':literal_steps,'empty_target':case['empty_target']})
    return {'profile':index,'counts':counts,'budget':budget,'templates':len(templates),'physical':physical,
            'initial_empty':sum(c['status']=='INITIAL_EMPTY' for c in packet['completed']),
            'arc_empty':sum(c['status']=='ARC_EMPTY' for c in packet['completed']),
            'raw_star_subsets':examined,'stored_stars':sum(len(r) for r in domain.values()),
            'deletion_batches':batches,'deleted_stars':removed,'literal_support_tests':support_tests,
            'full_initial_domains_and_deletions_sha256':digest(full),'claim_all_empty':True}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--profile',type=int,choices=(0,1),required=True)
    p.add_argument('--work',type=Path)
    p.add_argument('--certificate',type=Path)
    a=p.parse_args()
    result=verify(a.profile,a.work,a.certificate)
    expected=json.loads((ROOT/'expected.json').read_text())[str(a.profile)]
    require(result==expected,'Whole independent mathematical result differs')
    print(canonical(result))
