"""Definition-level controls and independent integer checks for P82 profiles."""
from pathlib import Path
from itertools import combinations
from functools import lru_cache
import csv
import hashlib
import json
import subprocess

SOURCE=Path(__file__).resolve().parent
PARENT=SOURCE.parent

def run(args):
    result=subprocess.run(list(map(str,args)),capture_output=True,text=True)
    if result.returncode:raise RuntimeError(f'{args}: {result.stderr}')
    return json.loads(result.stdout)

def build(source,target,sanitized=False):
    flags=['-O1','-g','-fsanitize=address,undefined','-fno-omit-frame-pointer']if sanitized else ['-O3']
    subprocess.run(['g++','-std=c++20','-Wall','-Wextra','-Wconversion','-Wshadow','-Werror',*flags,str(source),'-o',str(target)],check=True)

def digest(path):
    h=hashlib.sha256()
    with path.open('rb')as f:
        for block in iter(lambda:f.read(1<<20),b''):h.update(block)
    return h.hexdigest()

def same(a,b):
    with a.open('rb')as f,b.open('rb')as g:
        while True:
            x,y=f.read(1<<20),g.read(1<<20)
            assert x==y,(a,b)
            if not x:return

def mask(a):return sum(1<<x for x in a)

def sidon(a):
    sums=[x+y for i,x in enumerate(a)for y in a[i:]]
    return len(sums)==len(set(sums))

def partition(domain,classes,profile):
    assert sorted(map(len,classes))==sorted(profile)and all(sidon(a)for a in classes)
    assert sorted(x for a in classes for x in a)==sorted(domain)

def profiles(n,total,maximum):
    if n==0:
        if total==0:yield()
        return
    for a in range(min(total,maximum),0,-1):
        if total-a<=a*(n-1):
            for b in profiles(n-1,total-a,a):yield(a,)+b

def rows(path):return [tuple(map(int,l.split()))for l in path.read_text().splitlines()]

def write_rows(path,a):path.write_text(''.join(' '.join(map(str,b))+'\n'for b in a))

def canonical(raw,weights):
    ma={mask(a):a for a in raw};orbits=[]
    assert len(ma)==len(raw)==8214
    for m,a in ma.items():
        b=tuple(sorted(81-x for x in a));r=mask(b)
        assert r in ma and r!=m
        if m<r:orbits.append((sum(weights[x]for x in a),m,a,b))
    orbits.sort(key=lambda a:(-a[0],a[1]))
    return [a for row in orbits for a in row[2:]]

def controls(program,work,generator):
    reports=[]
    def test(name,profile,domains,expected,catalog=None):
        pp=work/(name+'_profile.txt');dp=work/(name+'_domains.txt');write_rows(pp,[profile]);write_rows(dp,domains)
        for method in [0,1]:
            pre=work/f'{name}_{program.name}_{method}'
            args=[program,'complete',method,SOURCE/'weights.txt',pp,dp,pre.with_suffix('.bin'),pre.with_suffix('.jsonl'),pre.with_suffix('.done')]
            if catalog:args.append(catalog)
            r=run(args);a=[json.loads(l)for l in pre.with_suffix('.jsonl').read_text().splitlines()]
            assert r['complete']and r['domains']==len(domains)and [x['found']for x in a]==expected
            for d,x in zip(domains,a):
                if x['found']:partition(d,x['partition'],profile)
            reports.append(dict(name=name,method=method,domains=len(domains),positive=sum(expected),negative=len(domains)-sum(expected),catalog=bool(catalog)))
    family=[mask(a)for a in combinations(range(14),3)if sidon(a)]
    @lru_cache(None)
    def exact(r):
        if not r:return True
        first=r&-r
        return any(a&first and a&r==a and exact(r^a)for a in family)
    domains=list(combinations(range(14),9));test('small333',[3,3,3],domains,[exact(mask(a))for a in domains])
    for profile in [[4,3,2],[4,4,4],[5,4,3],[5,4],[5,5],[6,3,3]]:
        family={k:[mask(a)for a in combinations(range(12),k)if sidon(a)]for k in set(profile)}
        @lru_cache(None)
        def exact(r,i):
            if i==len(profile):return r==0
            return any(a&r==a and exact(r^a,i+1)for a in family[profile[i]])
        domains=list(combinations(range(12),sum(profile)))
        test('small'+''.join(map(str,profile)),profile,domains,[exact(mask(a),0)for a in domains])
    for i,fixture in enumerate(json.loads((SOURCE/'positive27.json').read_text())):
        partition(fixture['points'],fixture['classes'],fixture['sizes'])
        test('positive27_'+str(i),fixture['sizes'],[fixture['points']],[True])
    seed=[[x-1 for x in a]for a in rows(PARENT/'p80_extension_barrier/partition80.txt')]
    partition(range(80),seed,[10]*8)
    padded=work/'weights_padded.txt';padded.write_text((SOURCE/'weights.txt').read_text().strip()+' 0 0\n')
    for shift in [0,2]:
        parts=[[x+shift for x in a]for a in seed[:5]];domain=sorted(x for a in parts for x in a)
        dp=work/f'control50_{shift}.txt';write_rows(dp,[domain]);cp=work/f'control50_{shift}.bin'
        run([generator,0,dp,cp,10,padded])
        for profile in [[10,10,10,8],[10,10,9,9],[10,10,10,10,9]]:
            classes=[a[:k]for a,k in zip(parts,profile)];domain=sorted(x for a in classes for x in a)
            partition(domain,classes,profile)
            test('positive'+''.join(map(str,profile))+'_'+str(shift),profile,[domain],[True],cp)
    return reports

def verify(work,jobs):
    weights=list(map(int,(SOURCE/'weights.txt').read_text().split()));orbit=rows(work/'orbit11.txt')
    result={};all_terminals=[]
    for k in [2,3,4]:
        tables=[]
        for m in [0,1]:
            count=[{a:int(b)for a,b in r.items()}for r in csv.DictReader((work/f'count{k}_{m}.csv').open())]
            assert [r['orbit']for r in count]==list(range(len(count)))
            expected_eligible=sum(k*sum(weights[x]for x in orbit[i])>=30884468-(8-k)*4000000 for i in range(0,len(orbit),2))
            assert len(count)==expected_eligible
            tables.append(count)
        assert tables[0]==tables[1]
        summary=dict(eligible_cases=len(tables[0]),nonempty_cases=sum(r['packings']>0 for r in tables[0]),packings=sum(r['packings']for r in tables[0]))
        if k in [2,3]:
            compact=[dict(orbit=r['orbit'],packings=r['packings'])for r in tables[0]]
        else:
            complete=[]
            for m in [0,1]:
                joined=[]
                for shard in range(jobs):
                    pre=work/f'sweep{k}_{m}_{shard}';record=json.loads(pre.with_suffix('.out').read_text())
                    assert pre.with_suffix('.done').read_text()=='complete\n'and record['complete']and record['found']==0
                    part=[{a:int(b)for a,b in r.items()}for r in csv.DictReader(pre.with_suffix('.csv').open())]
                    assert all(r['orbit']%jobs==shard for r in part)and record['packings']==sum(r['packings']for r in part)
                    joined+=part
                joined.sort(key=lambda r:r['orbit']);assert [(r['orbit'],r['packings'])for r in joined]==[(r['orbit'],r['packings'])for r in tables[0]]
                complete.append(joined)
            assert complete[0]==complete[1]
            for shard in range(jobs):
                a=work/f'sweep{k}_0_{shard}';b=work/f'sweep{k}_1_{shard}'
                same(a.with_suffix('.bin'),b.with_suffix('.bin'));same(a.with_suffix('.jsonl'),b.with_suffix('.jsonl'))
                for line in a.with_suffix('.jsonl').read_text().splitlines():
                    t=json.loads(line);ids=t['ids'];chosen=t['chosen'];last=t['residual']
                    assert len(ids)==k and ids==sorted(set(ids))and ids[0]%2==0
                    elevens=[orbit[i]for i in ids]
                    assert all(sidon(a)for a in [*elevens,*chosen])and not t['sidon']and not sidon(last)
                    assert sorted(x for a in [*elevens,*chosen,last]for x in a)==list(range(82))
                    sizes=[len(a)for a in [*chosen,last]]
                    assert sizes in ([[10,10,10,8],[10,10,9,9]]if k==4 else [[10,10,10,10,9]])
                    weighted=[sum(weights[x]for x in a)for a in [*chosen,last]]
                    for i in range(len(sizes)-1):
                        if sizes[i]==sizes[i+1]:assert weighted[i]>=weighted[i+1]
                    all_terminals.append(dict(anchors=k,**t))
            totals={key:sum(r[key]for r in complete[0])for key in ['packings','calls','queries','options','leaves','found']}
            assert totals['found']==0 and totals['calls']==(2 if k==4 else 1)*totals['packings']+totals['options']
            assert totals['leaves']==sum(t['anchors']==k for t in all_terminals)
            summary['totals']=totals
            summary['trace_bytes_per_method']=sum((work/f'sweep{k}_0_{j}.bin').stat().st_size for j in range(jobs))
            compact=complete[0]
        path=work/f'cases_{k}.csv'
        with path.open('w')as f:
            writer=csv.DictWriter(f,fieldnames=list(compact[0]),lineterminator='\n');writer.writeheader();writer.writerows(compact)
        summary['cases_sha256']=digest(path);result[str(k)]=summary
    all_terminals.sort(key=lambda a:(a['anchors'],a['ids'],a['chosen']))
    (work/'all_terminals.json').write_text(json.dumps(all_terminals)+'\n')
    (work/'terminal_examples.json').write_text(json.dumps(all_terminals[:2]+all_terminals[-2:],indent=2)+'\n')
    result['terminal_occurrences']=len(all_terminals)
    result['all_terminals_sha256']=digest(work/'all_terminals.json')
    result['verified']=True
    return result

def audit_pairs(orbit,weights,case_path):
    """Count every unordered pair before taking reflection, without packing DFS."""
    masks=[mask(a)for a in orbit];ws=[sum(weights[x]for x in a)for a in orbit]
    counts=[0]*(len(orbit)//2);fixed=[0]*len(counts);cut=30884468-6*4000000
    for i,a in enumerate(masks):
        for j in range(i+1,len(masks)):
            if not(a&masks[j])and ws[i]+ws[j]>=cut:
                counts[i//2]+=1
                if j==i+1 and i%2==0:fixed[i//2]+=1
    expected=list(csv.DictReader(case_path.open()))
    assert len(expected)==len(counts)==4107
    assert all(counts[i]+fixed[i]==2*int(r['packings'])for i,r in enumerate(expected))
    return dict(unreflected_pairs=sum(counts),reflection_fixed_pairs=sum(fixed),anchored_pairs=sum(int(r['packings'])for r in expected),all_case_counts_verified=True)
