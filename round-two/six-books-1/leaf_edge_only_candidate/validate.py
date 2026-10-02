"""Compact bindings, literal assigned-book checks and adverse controls.

Completeness is established by the separate full checker, not by a hash.
This layer checks its completed receipts and all physical frozen witnesses.
"""
from collections import Counter
from copy import deepcopy
from itertools import combinations,product
from pathlib import Path
import argparse,hashlib,json,sys,tempfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
sys.path.insert(0,str(ROOT/'cross_edge_only'))
from verify import graph

FROZEN_SHA='6b980ecc0427342ebfa647db36a14bc4513d11521e67d4cd69463751940e0db3'
SCOPE='specified literal one-nine leaf; root10/mark9/other neighbors10; E<=108; cross omissions'
LOCAL=((1,8,9),(0,),(6,7),(4,5),(3,7,9),(3,6,8),(2,5,9),(2,4,8),(0,5,7),(0,4,6))
KINDS=('projection14','projection16','endpoints','rows','joins')
COUNTS=(1154,682,29876,2250,180)

def fail(message):raise ValueError(message)
def require(test,message):
    if not test:fail(message)
def canonical(x):return json.dumps(x,separators=(',',':'))
def sha(x):return hashlib.sha256(canonical(x).encode()).hexdigest()
def file_sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def unique(pairs):
    d={}
    for k,v in pairs:
        if k in d:fail('duplicate JSON key')
        d[k]=v
    return d
def load(path):
    return json.loads(path.read_text(),object_pairs_hook=unique,
                      parse_constant=lambda _:fail('nonfinite JSON value'))
def same(a,b,message):
    # Object key order is serialization, not part of the mathematical record.
    require(json.dumps(a,sort_keys=True,separators=(',',':'))==
            json.dumps(b,sort_keys=True,separators=(',',':')),message)

def check_sources(root):
    manifest=load(root/'leaf_edge_only_candidate/SOURCE.json')
    for path,expected in manifest['files'].items():
        require(file_sha(root/path)==expected,'source binding: '+path)
    require(file_sha(root/'cross_edge_only/CANDIDATE.json')==FROZEN_SHA,'historical frozen fixture bytes')
    frozen=load(root/'cross_edge_only/CANDIDATE.json')
    for name,expected in frozen['mathematical_source_sha256'].items():
        require(file_sha(root/'cross_edge_only'/name)==expected,'frozen mathematical source: '+name)
    return frozen

def expected_claim():
    return {'schema':'specified-one-nine-leaf-edge-bound-v1','agent':'six-books-1','role':'researcher',
            'vertices':22,'red_page_cap':3,'blue_page_cap':6,'ordinary_books':True,
            'literal_root_neighborhood':[list(x) for x in LOCAL],
            'root_degree':10,'mark_label':0,'mark_global_degree':9,
            'other_neighbor_global_degrees':[10]*9,'outside_degree_restriction':None,
            'conclusion':'red_edges >= 109','omission_coverage':{'X_repeated':6,'Y_repeated':6,'cross':24},
            'external_premises':{'pair_core':'bafkreiesfsfe44lvytykz4oczwidosjpdxf4g3imjfnw7pxdllkmqsfqwu',
                                 'X_repeated_only':'bafkreibfuwpcdg7ifqkupycjbywe3lq7kwmqmm3knxummn2kxjpimwfzzu'},
            'status':'author-checked exact computer-assisted lemma; ordinary Y proof; unformalized bridges; new peer review pending'}

def check_claim(claim):same(claim,expected_claim(),'exact hypothesis/scope binding')

def check_domain(d,kind,r):
    require(d['schema']=='cross-edge-only-'+('projection14' if kind=='projection14' else 'projection16' if kind=='projection16' else kind)+'-v1','domain schema')
    require(d['scope']==SCOPE,'domain scope')
    require(type(d['core']) is int and d['core']==r,'actual labeled core')
    require(d['complete'] is True,'incomplete enumeration')
    require(d['count']==len(d['domain']),'domain cardinality')
    require(sha(d['domain'])==d['domain_sha256'],'domain digest')

def literal_join(xs,frames,record):
    frame_index,chosen,DY,witness=record
    require(type(frame_index) is int and 0<=frame_index<len(frames),'endpoint frame index')
    frame=frames[frame_index]
    index,intersection,t0,t1,t2,p,q=frame
    require(intersection in (2,3),'ordered SX intersection')
    r,rows,c,sy,beta,D=xs[index]
    nr=graph(r,c,sy)
    degrees=(10,10,9,*([10]*8),len(nr[11])+2,len(nr[12])+2,
             len(nr[13])+3,len(nr[14])+2,len(nr[15])+3)
    same(list(degrees[11:]),D,'actual endpoint degree vector')
    ep=(15,51 if intersection==2 else 23,p,q,t0,t1,t2)
    all_rows=(0,63,0,*chosen,*ep)
    require(len(all_rows)==16,'literal full row shape')
    for i,m in enumerate(all_rows):
        require(type(m) is int and 0<=m<64,'literal row mask')
        require(m.bit_count()==degrees[i]-len(nr[i]),'literal actual row degree')
    nr=[set(n) for n in nr]+[set() for _ in range(6)]
    for i,m in enumerate(all_rows):
        for j in range(6):
            if m>>j&1:nr[i].add(16+j);nr[16+j].add(i)
    h=tuple(4-sum(bool(m>>j&1) for m in ep[2:]) for j in range(6))
    require(min(h)>=0,'nonnegative unknown internal Q degree')
    actual=tuple(len(nr[16+j])+h[j] for j in range(6))
    same(list(actual),DY,'literal ordinary Y degrees')
    require(sum(actual)+sum(degrees)==216,'literal whole edge sum')
    require(len(witness)==4 and witness[0]=='known_red_book','assigned red witness type')
    _,i,j,pages=witness
    require(type(i) is int and type(j) is int and 0<=i<j<22,'literal spine coordinates')
    require(len(pages)==4 and len(set(pages))==4 and all(type(z) is int for z in pages),'four distinct literal pages')
    require(i not in pages and j not in pages and j in nr[i] and all(z in nr[i] and z in nr[j] for z in pages),'assigned red book edges')
    require(not any(j>=16 and i>=16 for i,j in [(i,j)]+[(i,z) for z in pages]+[(j,z) for z in pages]),'no unknown Q edge in book')
    first=next((['known_red_book',a,b,sorted(nr[a]&nr[b])[:4]] for a,b in combinations(range(22),2)
                if b in nr[a] and len(nr[a]&nr[b])>=4),None)
    same(witness,first,'literal first witness')
    return tuple(sorted(Counter(degrees+actual).items()))

def core(work,r,frozen):
    d={k:load(work/f'{k}-r{r}.json') for k in KINDS}
    for k in KINDS:check_domain(d[k],k,r)
    summary=frozen['core_summaries'][r]
    require(summary['core']==r and summary['completed'] is True,'frozen core identity')
    for k,n in zip(KINDS,COUNTS):require(len(d[k]['domain'])==n,'complete expected '+k+' cardinality')
    require(d['projection14']['row_rank_filtered_domain']==84050,'entire T row domain')
    require(d['projection16']['SY_candidates_tested']==727448,'entire SY domain')
    require(d['rows']['raw_row_products']==1009032,'whole row product domain')
    profiles=Counter(literal_join(d['projection16']['domain'],d['endpoints']['domain'],rec) for rec in d['joins']['domain'])
    actual=[[r,*rec] for rec in d['joins']['domain']]
    same(actual,[rec for rec in frozen['assigned_book_witnesses'] if rec[0]==r],'every frozen physical witness')
    for k,key in zip(KINDS,('X14','X16','endpoints','rows','joins')):
        require(d[k]['domain_sha256']==summary['full_domain_digests'][key],'frozen full '+key+' domain')
    independent=load(work/f'full-independent-r{r}.json')
    same({k:v for k,v in independent.items() if k!='phase_seconds'},summary,'entire independent mathematical receipt')
    require(d['projection16']['input14_sha256']==d['projection14']['domain_sha256'],'projection14 parent')
    for k in ('endpoints','rows','joins'):require(d[k]['parent_X_sha256']==d['projection16']['domain_sha256'],'projection16 parent')
    for k in ('rows','joins'):require(d[k]['parent_endpoints_sha256']==d['endpoints']['domain_sha256'],'endpoint parent')
    require(d['joins']['parent_rows_sha256']==d['rows']['domain_sha256'],'rows parent')
    return {'core':r,'summary':summary,'profiles':[[list(z) for z in p]+[n] for p,n in sorted(profiles.items())]},d

CASE_KEYS=('complete_rank_filtered_domain','cycle_cover','projection14','projection14_sha256',
           'column_SY_candidates','full_row_SY_candidates','projection16','projection16_sha256',
           'actual_endpoint_degree_histogram')
def case_record(work,expected):
    data=load(work/'caseI-projections.json');cycle=load(work/'caseI-cycle.json')
    record={'projection':{k:data[k] for k in CASE_KEYS},'cycle':cycle}
    same(record,expected,'entire CaseI projection and cycle records')
    return record

def controls(root,work,frozen,domains):
    failures=[]
    def reject(label,fn,text):
        try:fn()
        except ValueError as e:
            require(text in str(e),'wrong rejection for '+label);failures.append(label)
        else:fail('damaged record accepted: '+label)
    claim=expected_claim();claim['outside_degree_restriction']=[9,10]
    reject('outside profile inserted',lambda:check_claim(claim),'scope')
    claim=expected_claim();claim['literal_root_neighborhood'][1].append(2)
    reject('induced neighborhood changed',lambda:check_claim(claim),'scope')
    claim=expected_claim();claim['ordinary_books']=False
    reject('induced book interpretation',lambda:check_claim(claim),'scope')
    base=domains[0]['projection14']
    for label,key,value,text in (('incomplete','complete',False,'incomplete'),('core swapped','core',1,'core'),('Boolean core','core',False,'core'),('schema changed','schema','other','schema'),('scope changed','scope','four-low only','scope')):
        bad=deepcopy(base);bad[key]=value
        reject(label,lambda b=bad:check_domain(b,'projection14',0),text)
    bad=deepcopy(base);bad['domain'].pop();bad['count']=len(bad['domain']);bad['domain_sha256']=sha(bad['domain'])
    reject('deleted domain with repaired summary',lambda:require(bad['domain_sha256']==frozen['core_summaries'][0]['full_domain_digests']['X14'],'frozen full X14 domain'),'full X14')
    xs=domains[0]['projection16']['domain'];frames=domains[0]['endpoints']['domain'];rec=domains[0]['joins']['domain'][0]
    bad=deepcopy(rec);bad[2][0]+=1
    reject('changed actual outside degree',lambda:literal_join(xs,frames,bad),'ordinary Y degrees')
    bad=deepcopy(rec);bad[3][3][1]=bad[3][3][0]
    reject('duplicate page certificate',lambda:literal_join(xs,frames,bad),'distinct literal pages')
    bad=deepcopy(rec);bad[3][3][0]=bad[3][1]
    reject('spine as page certificate',lambda:literal_join(xs,frames,bad),'assigned red book edges')
    bad=deepcopy(rec);bad[1][0]^=1
    reject('changed actual row rank',lambda:literal_join(xs,frames,bad),'actual row degree')
    with tempfile.TemporaryDirectory(prefix='leaf-damage-',dir=work) as tmp:
        tmp=Path(tmp);p=tmp/'bad.json';p.write_text('{"core":0,"core":1}')
        reject('duplicate JSON key',lambda:load(p),'duplicate')
        p.write_text('{"value":NaN}')
        reject('nonfinite JSON',lambda:load(p),'nonfinite')
        # Copy bytes, not symlinked entry points: reads must target this tree.
        import shutil
        for directory in ('cross_edge_only','caseI_edge_only','leaf_edge_only_candidate'):
            shutil.copytree(root/directory,tmp/directory,ignore=shutil.ignore_patterns('__pycache__'))
        p=tmp/'cross_edge_only/verify.py';p.write_text(p.read_text()+'\n# damaged source binding\n')
        reject('modified literal checker source',lambda:check_sources(tmp),'source binding: cross_edge_only/verify.py')
    return failures

def elementary_controls():
    counts=Counter()
    for word in product(range(3),repeat=4):
        if sorted(Counter(word).values())!=[1,1,2]:continue
        repeated=next(t for t in range(3) if word.count(t)==2)
        counts['X_repeated' if word[0]==word[1]==repeated else 'Y_repeated' if word[2]==word[3]==repeated else 'cross']+=1
    same(dict(counts),{'X_repeated':6,'Y_repeated':6,'cross':24},'all actual omission words')
    checks=0
    for n in (6,8):
        mask=(1<<n)-1
        for a,b in product(range(1<<n),repeat=2):
            require((a&b).bit_count()>=max(0,a.bit_count()+b.bit_count()-n),'red intersection minimum')
            require(((mask^a)&(mask^b)).bit_count()>=max(0,n-a.bit_count()-b.bit_count()),'blue intersection minimum');checks+=1
    require(sum(map(len,LOCAL))==26 and 99-10-26==63 and 10+13+63==86,'literal root edge equality')
    return {'omissions':dict(sorted(counts.items())),'subset_pairs':checks,'root_edges':13,'root_cut':63,'base_edges':86}

def run(root,work):
    frozen=check_sources(root);check_claim(load(root/'leaf_edge_only_candidate/CLAIM.json'))
    records=[];domains=[]
    for r in (0,1):rec,d=core(work,r,frozen);records.append(rec);domains.append(d)
    case=case_record(work,load(root/'leaf_edge_only_candidate/CASE_EXPECTED.json'))
    damaged=controls(root,work,frozen,domains)
    return {'schema':'specified-leaf-edge-only-complete-check-v1','agent':'six-books-1','role':'researcher',
            'cross':records,'CaseI':case,'elementary_controls':elementary_controls(),'rejected_damage_controls':damaged,
            'X_repeated':'explicit imported9414 E-only theorem; not regenerated',
            'status':'author-checked exact result; ordinary/completeness/code bridges unformalized; new peer review pending'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);args=p.parse_args()
    record=run(ROOT,args.work);raw=canonical(record)+'\n'
    (args.work/'RESULT.json').write_text(raw)
    print(canonical({'status':'VALIDATION_PASS','whole_record_sha256':hashlib.sha256(raw.encode()).hexdigest(),
                     'record_bytes':len(raw.encode()),'damaged_records_rejected':len(record['rejected_damage_controls'])}))
