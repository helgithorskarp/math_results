"""Independent exception-tuple/type-composition/literal-endpoint verifier.

No import of producer or earlier researcher code. Certificates are public
claims of coverage/deletions, not trusted initial domains.
"""
import argparse,copy,hashlib,itertools,json,math
from pathlib import Path

PAIR_TYPES=(3,5,9,6,10,12)
ALL22=(1<<22)-1

def require(value,message):
    if not value:raise ValueError(message)

def integer(value,lo,hi,message):
    require(type(value) is int and lo<=value<=hi,message)

def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'))

def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()

def recover_profiles():
    result=[]
    for counts in itertools.product(range(5),repeat=6):
        if sum(counts)!=14:continue
        types=[1,2,7,11]
        for mask,count in zip(PAIR_TYPES,counts):types.extend([mask]*count)
        if any(sum(bool(t>>i&1) for t in types)!=9 for i in range(4)):continue
        if any(sum(bool(t>>i&1) and bool(t>>j&1) for t in types)>4 for i in range(4) for j in range(i)):continue
        r,s,t=counts[:3]
        require(counts[3:]==(t,s,r+2),'ordinary pair-count bridge mismatch')
        result.append(((r,s,t),tuple(types)))
    return sorted(result)

def recover_exceptions(types):
    groups={t:[x for x,u in enumerate(types) if u==t] for t in set(types)}
    neighbors=[[x for x,t in enumerate(types) if t>>i&1] for i in range(4)]
    require(all(len(row)==9 for row in neighbors),'low degree mismatch')
    templates=set();accepted=0;raw=0
    for word in itertools.product(*neighbors):
        raw+=1
        if any(bool(types[word[i]]>>j&1)!=bool(types[word[j]]>>i&1) for i in range(4) for j in range(i)):continue
        accepted+=1;images={};next_index={};normal=[]
        for point in word:
            typ=types[point]
            if point not in images:
                position=next_index.get(typ,0)
                images[point]=groups[typ][position]
                next_index[typ]=position+1
            normal.append(images[point])
        templates.add(tuple(normal))
    require(raw==6561,'incomplete9^4 exception coverage')
    return sorted(templates),accepted,raw

def low_rows(types):
    rows=[sum(1<<(x+4) for x,t in enumerate(types) if t>>i&1) for i in range(4)]
    require(all(row.bit_count()==9 for row in rows),'literal low-degree mismatch')
    return rows

def endpoint(x,star,types):
    integer(star,0,(1<<18)-1,'star encoding')
    require(not star>>x&1,'star self loop')
    red=types[x]|(star<<4)
    require(red.bit_count()==10,'actual endpoint degree must be ten')
    return red,ALL22^(red|(1<<(x+4)))

def mixed_spines(x,star,exception_mask,types,low):
    red,blue=endpoint(x,star,types)
    for i in range(4):
        if red>>i&1:
            require((red&low[i]).bit_count()==3-((exception_mask>>i)&1),'literal red mixed spine mismatch')
        else:
            low_blue=ALL22^(low[i]|(1<<i))
            require((blue&low_blue).bit_count()==6,'literal saturated blue mixed spine mismatch')

def make_domain(x,exception_mask,types):
    integer(exception_mask,0,15,'exception column mask')
    require(exception_mask&~types[x]==0,'exception on blue low-high spine')
    needs=tuple(3-((exception_mask>>i)&1) if types[x]>>i&1 else 5 for i in range(4))
    groups=[(typ,tuple(y for y,u in enumerate(types) if u==typ and y!=x)) for typ in sorted(set(types))]
    remaining_count=[sum(len(points) for _,points in groups[p:]) for p in range(len(groups)+1)]
    remaining_low=[tuple(sum(len(points) for typ,points in groups[p:] if typ>>i&1) for i in range(4)) for p in range(len(groups)+1)]
    words=[]
    def visit(position,budget,demands,counts):
        if position==len(groups):
            if budget==0 and not any(demands):words.append(tuple(counts))
            return
        typ,points=groups[position]
        maximum=min(len(points),budget,min(demands[i] for i in range(4) if typ>>i&1))
        for count in range(maximum+1):
            rest=tuple(demands[i]-count*((typ>>i)&1) for i in range(4))
            if budget-count>remaining_count[position+1] or any(v<0 or v>remaining_low[position+1][i] for i,v in enumerate(rest)):continue
            visit(position+1,budget-count,rest,counts+[count])
    visit(0,10-types[x].bit_count(),needs,[])
    low=low_rows(types);domain=[]
    for word in words:
        choices=[tuple(itertools.combinations(points,count)) for (_,points),count in zip(groups,word)]
        for selections in itertools.product(*choices):
            star=0
            for selection in selections:
                for point in selection:star|=1<<point
            mixed_spines(x,star,exception_mask,types,low)
            domain.append(star)
    require(len(domain)==len(set(domain)),'duplicate independently expanded star')
    return tuple(sorted(domain))

class Context:
    def __init__(self):
        self.profiles=recover_profiles();self.types_by_profile=dict(self.profiles);self.low_by_profile={p:low_rows(t) for p,t in self.profiles};self.domains={};self.templates={};self.template_raw={};self.ends={}
        for profile,types in self.profiles:
            templates,accepted,raw=recover_exceptions(types)
            self.templates[profile]=templates;self.template_raw[profile]=(accepted,raw)
    def initial(self,profile,selected):
        types=self.types_by_profile[profile]
        result=[]
        for x in range(18):
            mask=sum(1<<i for i,point in enumerate(selected) if point==x)
            key=(profile,x,mask)
            if key not in self.domains:self.domains[key]=make_domain(x,mask,types)
            result.append(self.domains[key])
        return result
    def compatible(self,profile,x,sx,y,sy):
        types=self.types_by_profile[profile]
        def get(z,star):
            key=(profile,z,star)
            if key not in self.ends:self.ends[key]=endpoint(z,star,types)
            return self.ends[key]
        rx,bx=get(x,sx);ry,by=get(y,sy)
        red=bool(rx>>(y+4)&1)
        if red!=bool(ry>>(x+4)&1):return False
        if not red:return (bx&by).bit_count()<=6
        common=rx&ry
        if common.bit_count()>3:return False
        for i,row in enumerate(self.low_by_profile[profile]):
            if common>>i&1 and common&row:return False
        return True

def verify_case(case,profile,context):
    require(set(case)=={'exceptions','domain_sizes','domain_sha256','kind','empty_target','steps','deletions_sha256'},'case fields')
    require(type(case['exceptions']) is list and len(case['exceptions'])==4,'four exception points required')
    for x in case['exceptions']:integer(x,0,17,'exception point')
    selected=tuple(case['exceptions'])
    require(selected in context.templates[profile],'uncanonical or inadmissible exception template')
    initial=context.initial(profile,selected)
    require(type(case['domain_sizes']) is list and len(case['domain_sizes'])==18,'complete domain sizes required')
    for n in case['domain_sizes']:integer(n,0,24310,'domain count')
    require(case['domain_sizes']==[len(row) for row in initial],'independent initial domain size mismatch')
    require(type(case['domain_sha256']) is str and case['domain_sha256']==digest(initial),'independent entire initial domain fingerprint mismatch')
    integer(case['empty_target'],0,17,'empty target')
    kind=case['kind'];require(kind in ('empty','static','arc'),'unknown proof kind')
    require(type(case['steps']) is list,'deletion steps must be a list')
    current=[set(row) for row in initial];deletions=[]
    if kind=='empty':
        require(not case['steps'] and not initial[case['empty_target']],'false initial empty certificate')
    else:
        require(all(initial) and bool(case['steps']),'nonempty initial domains/deletions required')
        for step in case['steps']:
            require(type(step) is list and len(step)==3,'step needs target, support, count')
            x,y,count=step
            integer(x,0,17,'deletion target');integer(y,0,17,'support target');integer(count,1,24310,'positive deleted count')
            require(x!=y and current[x] and current[y],'invalid self/empty support or step after contradiction')
            if kind=='static':require(x==case['empty_target'],'static cover changes multiple targets')
            gone=[star for star in sorted(current[x]) if not any(context.compatible(profile,x,star,y,support) for support in sorted(current[y]))]
            require(len(gone)==count,'claimed deletion differs from ALL actual unsupported stars')
            deletions.append((x,y,gone));current[x].difference_update(gone)
        require(not current[case['empty_target']],'no verified empty domain at end')
    require(type(case['deletions_sha256']) is str and case['deletions_sha256']==digest(deletions),'full ordered deletion-record fingerprint mismatch')
    return initial,deletions

def audit(packet,context,domain_record=False):
    require(type(packet) is dict and set(packet)=={'schema','claim','profiles'},'top-level certificate fields')
    require(type(packet['schema']) is int and packet['schema']==1,'schema type')
    require(packet['claim']=='No valid rootless9^4,10^18 graph has exactly two one-nine roots','wrong theorem scope')
    require(type(packet['profiles']) is list,'profile list')
    expected_profiles=[p for p,_ in context.profiles]
    require(len(packet['profiles'])==len(expected_profiles),'incomplete/duplicate profile census')
    summary={'profile_template_counts':[],'templates':0,'empty':0,'static':0,'arc':0,'deletion_batches':0,'deleted_stars':0,'raw_star_subsets':0}
    full=[]
    for record,expected_profile in zip(packet['profiles'],expected_profiles):
        require(type(record) is dict and set(record)=={'profile','types','cases'},'profile fields')
        require(type(record['profile']) is list and len(record['profile'])==3,'three pair parameters required')
        for v in record['profile']:integer(v,0,6,'pair parameter')
        profile=tuple(record['profile']);require(profile==expected_profile,'incomplete/disordered actual profile coverage')
        types=dict(context.profiles)[profile]
        require(type(record['types']) is list and len(record['types'])==18,'eighteen global high types required')
        for t in record['types']:integer(t,1,15,'type mask')
        require(tuple(record['types'])==types,'actual incidence tags differ')
        templates=context.templates[profile]
        require(type(record['cases']) is list and len(record['cases'])==len(templates),'incomplete/duplicate exception case census')
        full_cases=[]
        for case,template in zip(record['cases'],templates):
            require(type(case) is dict and case.get('exceptions')==list(template),'entire ordered exception coverage mismatch')
            initial,deletions=verify_case(case,profile,context)
            summary['templates']+=1;summary[case['kind']]+=1
            summary['deletion_batches']+=len(deletions);summary['deleted_stars']+=sum(len(stars) for _,_,stars in deletions)
            if domain_record:full_cases.append({'exceptions':list(template),'domains':initial,'deletions':deletions})
        summary['profile_template_counts'].append(len(templates))
        # These combinatorial counts are derived independently from endpoint degrees.
        summary['raw_star_subsets']+=sum(math.comb(17,10-t.bit_count()) for t in types)
        if domain_record:full.append({'profile':list(profile),'cases':full_cases})
    summary['certificate_canonical_sha256']=digest(packet)
    return summary,full

def damage_controls(packet,context):
    rejected=[]
    def reject(name,change):
        damaged=copy.deepcopy(packet);change(damaged)
        try:audit(damaged,context)
        except (ValueError,TypeError,KeyError,IndexError):rejected.append(name);return
        raise ValueError('Damaged proof accepted: '+name)
    reject('missing-profile',lambda p:p['profiles'].pop())
    reject('duplicate-profile',lambda p:p['profiles'].__setitem__(1,copy.deepcopy(p['profiles'][0])))
    reject('boolean-schema',lambda p:p.__setitem__('schema',True))
    reject('wrong-global-type',lambda p:p['profiles'][0]['types'].__setitem__(0,3))
    reject('boolean-low-parameter',lambda p:p['profiles'][0]['profile'].__setitem__(0,False))
    reject('missing-exception-case',lambda p:p['profiles'][0]['cases'].pop())
    reject('duplicate-exception-case',lambda p:p['profiles'][0]['cases'].__setitem__(1,copy.deepcopy(p['profiles'][0]['cases'][0])))
    reject('wrong-exception-point',lambda p:p['profiles'][0]['cases'][0]['exceptions'].__setitem__(0,1))
    reject('wrong-domain-count',lambda p:p['profiles'][0]['cases'][0]['domain_sizes'].__setitem__(0,999))
    reject('boolean-domain-count',lambda p:p['profiles'][0]['cases'][0]['domain_sizes'].__setitem__(0,True))
    reject('narrowed-initial-domain-digest',lambda p:p['profiles'][0]['cases'][0].__setitem__('domain_sha256','0'*64))
    static_index=next(i for i,c in enumerate(packet['profiles'][0]['cases']) if c['kind']=='static')
    def static(p):return p['profiles'][0]['cases'][static_index]
    reject('false-initial-empty',lambda p:(static(p).__setitem__('kind','empty'),static(p).__setitem__('steps',[])))
    reject('wrong-batch-count',lambda p:static(p)['steps'][0].__setitem__(2,static(p)['steps'][0][2]+1))
    reject('boolean-batch-count',lambda p:static(p)['steps'][0].__setitem__(2,True))
    reject('self-support',lambda p:static(p)['steps'][0].__setitem__(1,static(p)['steps'][0][0]))
    reject('skipped-deletion-batch',lambda p:static(p)['steps'].pop(0))
    reject('duplicated-deletion-batch',lambda p:static(p)['steps'].insert(1,copy.deepcopy(static(p)['steps'][0])))
    reject('wrong-empty-target',lambda p:static(p).__setitem__('empty_target',(static(p)['empty_target']+1)%18))
    reject('forged-ordered-deletions',lambda p:static(p).__setitem__('deletions_sha256','f'*64))
    return {'rejected_damages':rejected,'count':len(rejected)}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--certificate',type=Path,default=Path(__file__).with_name('certificate.json'));parser.add_argument('--expected',type=Path);parser.add_argument('--domains',action='store_true');parser.add_argument('--self-test',action='store_true')
    args=parser.parse_args();packet=json.loads(args.certificate.read_text());context=Context();summary,full=audit(packet,context,args.domains)
    if args.domains:print(canonical(full));return
    if args.self_test:print(canonical(damage_controls(packet,context)));return
    if args.expected is not None:require(canonical(json.loads(args.expected.read_text()))==canonical(summary),'Independent expected summary mismatch')
    print(canonical(summary))

if __name__=='__main__':main()
