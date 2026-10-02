"""All three-triple equality-three profiles; finite complete necessary domains."""
import argparse
import collections
import datetime
import hashlib
import itertools
import json
import time
from pathlib import Path

ROOT=Path(__file__).resolve().parent
LIMIT=2000000
SCOPE='No full-valid22-point completion of canonical three-triple incidence profiles0 or1 from9371; no other profile or Ramsey endpoint exclusion.'

def require(ok,message):
    if not ok:
        raise ValueError(message)

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def configuration(index):
    source=ROOT/'incidence.json'
    raw=source.read_bytes()
    require(hashlib.sha256(raw).hexdigest()=='10c23fac3815df26beb8120854ad46c9a87bd15c1b29fa40514c64e6eb8dbd6f','source incidence changed')
    require(type(index) is int and index in (0,1),'invalid selected triple profile')
    counts=json.loads(raw)['sectors'][0]['canonical'][index]
    types=[m for m,n in enumerate(counts,1) for _ in range(n)]
    require(len(types)==18,'H order')
    singles=[counts[(1<<i)-1] for i in range(4)]
    omissions=[counts[(15^(1<<i))-1] for i in range(4)]
    budget=[3-s-o for s,o in zip(singles,omissions)]
    require(sum(budget)==6 and sorted(budget) in ([1,1,1,3],[1,1,2,2]),'wrong triple slack budget')
    require(all(sum(bool(t&(1<<i)) for t in types)==9 for i in range(4)),'low margins')
    return counts,types,budget

def partitions(length,capacity):
    def visit(code):
        if len(code)==length:
            yield tuple(code);return
        for k in range(min(capacity,max(code,default=-1)+2)):
            yield from visit(code+[k])
    yield from visit([])

def templates(types,budget):
    cells={m:[x for x,t in enumerate(types) if t==m] for m in sorted(set(types))}
    words=0;symmetric_words=0;matrices=set(); branches=[]
    for alpha in itertools.product(*([1,3] if d==3 else [1] for d in budget)):
        roles=[(i,red) for i in range(4) for red,n in [(True,alpha[i]),(False,budget[i]-alpha[i])] for _ in range(n)]
        require(len(roles)==6,'six units')
        choices=[[m for m in cells if bool(m&(1<<i))==red] for i,red in roles]
        before=len(matrices);wcount=0;scount=0
        for word in itertools.product(*choices):
            words+=1;wcount+=1
            walk=[[sum(bool(m&(1<<j)) for m,(r,_) in zip(word,roles) if r==i) for j in range(4)] for i in range(4)]
            if any(walk[i][j]!=walk[j][i] for i in range(4) for j in range(i)):
                continue
            symmetric_words+=1;scount+=1
            groups=[(m,[r for r,t in enumerate(word) if t==m]) for m in sorted(set(word))]
            for codes in itertools.product(*(list(partitions(len(indices),len(cells[m]))) for m,indices in groups)):
                columns=[0]*18
                for (m,indices),code in zip(groups,codes):
                    for role,label in zip(indices,code):
                        i,_=roles[role];columns[cells[m][label]]+=1<<(2*i)
                canonical=[]
                for m,indices in cells.items():canonical.extend(sorted(columns[x] for x in indices))
                matrices.add(tuple(canonical))
        branches.append({'red_row_sums':list(alpha),'type_words':wcount,'symmetric_type_words':scount,'new_templates':len(matrices)-before})
    return sorted(matrices),{'type_words':words,'symmetric_type_words':symmetric_words,'branches':branches}

def domains(types,budget):
    masks=[sum(1<<x for x,t in enumerate(types) if t&(1<<i)) for i in range(4)]
    rows=collections.defaultdict(list);examined=0
    for x,tx in enumerate(types):
        caps=[3 if tx&(1<<i) else 5 for i in range(4)]
        bounds=[(3 if budget[i]==3 else 1) if tx&(1<<i) else budget[i]-1 for i in range(4)]
        for neighbors in itertools.combinations([y for y in range(18) if y!=x],10-tx.bit_count()):
            examined+=1;star=sum(1<<y for y in neighbors)
            slack=[caps[i]-(star&masks[i]).bit_count() for i in range(4)]
            if any(not 0<=d<=bound for d,bound in zip(slack,bounds)):continue
            signature=sum(d<<(2*i) for i,d in enumerate(slack))
            rows[(x,signature)].append(star)
    return {k:tuple(sorted(v)) for k,v in rows.items()},examined,masks

def atomic(directory,name,value):
    target=directory/name;temp=directory/(name+'.tmp')
    temp.write_text(json.dumps(value,sort_keys=True,separators=(',',':'))+'\n');temp.replace(target)

def run(index,work):
    start=time.monotonic();counts,types,budget=configuration(index)
    out=Path(work).resolve()/str(index);out.mkdir(parents=True,exist_ok=True)
    selected,meta=templates(types,budget)
    all_domains,examined,masks=domains(types,budget)
    tpacket={'profile':index,'counts':counts,'types':types,'budget':budget,'templates':[list(t) for t in selected],'metadata':meta}
    dpacket={'rows':[[x,s,list(row)] for (x,s),row in sorted(all_domains.items())],'raw_subsets':examined,'stored_stars':sum(len(r) for r in all_domains.values())}
    atomic(out,'templates.json',tpacket);atomic(out,'domains.json',dpacket)
    tests=0;completed=[]
    def compatible(x,sx,y,sy):
        red=bool(sx&(1<<y))
        if red!=bool(sy&(1<<x)):return False
        common=sx&sy;shared=types[x]&types[y]
        if common.bit_count()+shared.bit_count()>(3 if red else 6):return False
        if red and any(common&masks[i] for i in range(4) if shared&(1<<i)):return False
        return True
    for case_index,columns in enumerate(selected):
        current=[set(all_domains.get((x,columns[x]),())) for x in range(18)]
        sizes=[len(r) for r in current];steps=[];passes=0
        empty=[x for x,r in enumerate(current) if not r]
        if empty:
            completed.append({'template':case_index,'columns':list(columns),'status':'INITIAL_EMPTY','initial_sizes':sizes,'empty_target':min(empty),'steps':[]})
            continue
        status=None
        while status is None:
            passes+=1;changed=False
            order=sorted(range(18),key=lambda x:(len(current[x]),x))
            schedule=[(x,y) for x in order for y in sorted((z for z in range(18) if z!=x),key=lambda z:(len(current[z]),z))]
            for pair_index,(x,y) in enumerate(schedule):
                left=sorted(current[x]);right=sorted(current[y]);gone=[]
                for left_index,sx in enumerate(left):
                    supported=False
                    for right_index,sy in enumerate(right):
                        if tests>=LIMIT:
                            result={'status':'OPERATIONAL_LIMIT_NO_VERDICT','profile':index,'counts':counts,'types':types,'budget':budget,
                                    'templates':len(selected),'completed':completed,'current_template':case_index,
                                    'current_columns':list(columns),'initial_sizes':sizes,'current_domains':[sorted(r) for r in current],'steps':steps,'passes':passes,
                                    'pending':{'schedule':schedule,'pair_index':pair_index,'left_index':left_index,'right_index':right_index,'gone':gone,'changed':changed},
                                    'support_tests':tests,'limit':LIMIT,'seconds':time.monotonic()-start,'claim_all_empty':False}
                            atomic(out,'certificate-full.json',result)
                            return {k:v for k,v in result.items() if k not in ('completed','current_domains','pending','steps','current_columns','initial_sizes')}
                        tests+=1
                        if compatible(x,sx,y,sy):supported=True;break
                    if not supported:gone.append(sx)
                if gone:
                    steps.append({'target':x,'other':y,'stars':gone});current[x].difference_update(gone);changed=True
                    if not current[x]:status='ARC_EMPTY';break
            if status is None and not changed:status='ARC_FIXED_POINT_UNRESOLVED'
        completed.append({'template':case_index,'columns':list(columns),'status':status,'initial_sizes':sizes,
                          'empty_target':next((x for x,r in enumerate(current) if not r),None),
                          'steps':steps,'passes':passes,'remaining_sizes':[len(r) for r in current]})
        atomic(out,'progress.json',{'profile':index,'completed_templates':len(completed),'total_templates':len(selected),'support_tests':tests,'seconds':time.monotonic()-start})
    record={'status':'COMPLETE_NECESSARY_DOMAIN_CENSUS','profile':index,'counts':counts,'types':types,'budget':budget,
            'templates':len(selected),'completed':completed,'support_tests':tests,'limit':LIMIT,'seconds':time.monotonic()-start,
            'claim_all_empty':all(c['status'] in ('INITIAL_EMPTY','ARC_EMPTY') for c in completed)}
    atomic(out,'certificate-full.json',record)
    return {'profile':index,'status':record['status'],'claim_all_empty':record['claim_all_empty'],
            'templates':len(selected),'status_counts':dict(collections.Counter(c['status'] for c in completed)),
            'deletion_batches':sum(len(c['steps']) for c in completed),'deleted_stars':sum(len(s['stars']) for c in completed for s in c['steps']),
            'support_tests':tests,'raw_star_subsets':examined,'stored_stars':dpacket['stored_stars'],'seconds':time.monotonic()-start}

def compact(record):
    result={k:v for k,v in record.items() if k not in ('seconds','support_tests','limit')}
    result['schema']=1
    result['scope']=SCOPE
    for case in result['completed']:
        case['steps']=[dict(target=s['target'],other=s['other'],count=len(s['stars']),sha256=digest(s['stars'])) for s in case['steps']]
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--profile',type=int,choices=(0,1),required=True)
    p.add_argument('--work',type=Path,required=True)
    a=p.parse_args()
    summary=run(a.profile,a.work)
    require(summary['status']=='COMPLETE_NECESSARY_DOMAIN_CENSUS' and summary['claim_all_empty'] is True,'Incomplete computation supplies no exclusion')
    freshly=compact(json.loads((a.work/str(a.profile)/'certificate-full.json').read_text()))
    frozen=json.loads((ROOT/f'certificate-{a.profile}.json').read_text())
    require(freshly==frozen,'Entire freshly reconstructed compact certificate differs')
    summary.pop('seconds',None)
    print(json.dumps(summary,sort_keys=True,separators=(',',':')))
