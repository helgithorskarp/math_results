"""Whole native sanitizers, repaired damaged data and literal controls."""
from pathlib import Path
from itertools import combinations
import argparse,copy,hashlib,json,os,resource,shutil,subprocess,sys,time
import reproduce

HERE=Path(__file__).resolve().parent

def page_controls():
    checked=0
    for seed in range(64):
        Aword=(101*seed+7)%4096;Bword=(817*seed+17)%(1<<22)
        cols=[]
        for k in range(4):
            mask=(197*seed+59*k+11)&511
            for phase in range(3):
                cols.append({3*i+(t+phase)%3 for i in range(3) for t in range(3) if mask>>(3*i+t)&1})
        def internal(u,v,count,word):
            i,t=divmod(u,3);j,s=divmod(v,3)
            if i==j:return bool(word>>i&1)
            pair=list(combinations(range(count),2)).index(tuple(sorted([i,j])))
            phase=(s-t)%3 if i<j else (t-s)%3
            return bool(word>>(count+3*pair+phase)&1)
        sets=[set() for _ in range(22)]
        for u,v in combinations(range(22),2):
            if v==21:red=u<9
            elif v<9:red=internal(u,v,3,Aword)
            elif u>=9:red=internal(u-9,v-9,4,Bword)
            else:red=u in cols[v-9]
            if red:sets[u].add(v);sets[v].add(u)
        bits=[sum(1<<v for v in row) for row in sets]
        for u,v in combinations(range(22),2):
            red=v in sets[u]
            if red:
                literal=len(sets[u]&sets[v]);bitcount=(bits[u]&bits[v]).bit_count()
            else:
                literal=sum(w not in sets[u] and w not in sets[v] for w in range(22) if w not in [u,v])
                bu=((1<<22)-1)^bits[u]^(1<<u);bv=((1<<22)-1)^bits[v]^(1<<v)
                bitcount=(bu&bv).bit_count()
            component=0
            for block in [range(9),range(9,21),[21]]:
                component+=sum(w not in [u,v] and ((w in sets[u] and w in sets[v]) if red else (w not in sets[u] and w not in sets[v])) for w in block)
            if literal!=bitcount or literal!=component:raise ValueError('Literal/bitset/component page disagreement')
            checked+=1
    # Both sides of the thresholds, on actual simple graphs of smaller orders.
    for n,clique,expected_valid in [(5,True,True),(6,True,False),(8,False,True),(9,False,False)]:
        frame=[set(range(n))-{u} if clique else set() for u in range(n)]
        good=True
        for u,v in combinations(range(n),2):
            if v in frame[u]:
                if len(frame[u]&frame[v])>3:good=False
            elif sum(w not in frame[u] and w not in frame[v] for w in range(n) if w not in [u,v])>6:good=False
        if good!=expected_valid:raise ValueError('Actual graph threshold calibration')
    reproduce.baseline()
    return dict(varied_graphs=64,all_colored_spines=checked,primary21_positive=True)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--replay',type=Path,required=True);parser.add_argument('--work',type=Path,required=True)
    args=parser.parse_args();replay=args.replay.resolve();work=args.work.resolve()
    if work==HERE or HERE in work.parents or work==replay or replay in work.parents:raise ValueError('Separate validation directory')
    if work.exists() and any(work.iterdir()):raise ValueError('Use an EMPTY validation directory')
    work.mkdir(parents=True,exist_ok=True);start=time.monotonic();environment=os.environ.copy()
    for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']:environment[key]='1'
    expected=reproduce.strict_json(HERE/'EXPECTED.json');reproduce.mathematical_summary(replay,expected)
    flags=['-O1','-g','-fno-omit-frame-pointer','-fno-pie','-no-pie','-fsanitize=address,undefined']
    command=['g++','-std=c++17','-Wall','-Wextra','-Wpedantic','-Wconversion','-Wshadow',*flags,str(HERE/'direct.cpp'),'-o',str(work/'direct-sanitized')]
    compiled=subprocess.run(command,env=environment,capture_output=True,text=True,timeout=30);compiled.check_returncode()
    if compiled.stderr:raise ValueError('Sanitizer compiler warnings')
    sanitized={};native_rejections=[];audit_rejections=[]
    for mode in ['M']:
        r=replay/mode;w=work/mode;w.mkdir()
        native=subprocess.run([str(work/'direct-sanitized'),str(r/'frames.txt'),str(w),mode],env=environment,capture_output=True,text=True,timeout=30)
        (w/'sanitizer.stdout').write_text(native.stdout);(w/'sanitizer.stderr').write_text(native.stderr);native.check_returncode()
        if native.stderr:raise ValueError('Sanitizer diagnostic or unexpected valid graph')
        release=reproduce.strict_json(r/'direct-summary.json');san=reproduce.strict_json(w/'direct-summary.json')
        if reproduce.canonical({k:v for k,v in release.items() if k!='seconds'})!=reproduce.canonical({k:v for k,v in san.items() if k!='seconds'}):
            raise ValueError('Every native semantic field differs')
        for name in ['direct-K-words.txt','direct-outcomes.txt']:
            if (r/name).read_bytes()!=(w/name).read_bytes():raise ValueError('Whole sanitizer stream differs')
        sanitized[mode]=san
        lines=(r/'frames.txt').read_text().splitlines();damages={}
        damages['omission']=lines[1:];damages['duplicate']=[lines[0],*lines[:-1]]
        damages['extra-field']=[lines[0]+' 1',*lines[1:]]
        damages['truncation']=[' '.join(lines[0].split()[:-1]),*lines[1:]]
        row=lines[0].split();row[1]='True';damages['noninteger']=[' '.join(row),*lines[1:]]
        row=lines[0].split();row[1]=str(int(row[1])^1);damages['degree-corruption']=[' '.join(row),*lines[1:]]
        row=lines[0].split();row[0]='4096';damages['out-of-domain']=[' '.join(row),*lines[1:]]
        for name,damaged in damages.items():
            file=w/(name+'.txt');file.write_text('\n'.join(damaged)+'\n')
            result=subprocess.run([str(replay/'direct'),str(file),str(w),mode],env=environment,capture_output=True,text=True,timeout=30)
            if result.returncode==0 or not result.stderr:raise ValueError('Accepted native damage '+mode+'/'+name)
            native_rejections.append(dict(mode=mode,name=name,reason=result.stderr.strip()))
        wrong='AA'
        result=subprocess.run([str(replay/'direct'),str(r/'frames.txt'),str(w),wrong],env=environment,capture_output=True,text=True,timeout=30)
        if result.returncode==0 or not result.stderr:raise ValueError('Accepted wrong degree cohort')
        native_rejections.append(dict(mode=mode,name='wrong-cohort',reason=result.stderr.strip()))

        producer=json.loads((r/'projection.json').read_text());inc=json.loads((r/'incidence-records.json').read_text())
        variants=[]
        p=copy.deepcopy(producer);p['records']=p['records'][1:];variants.append(('missing-local-word',p))
        p=copy.deepcopy(producer);key=next(iter(p['canonical_groups']));p['canonical_groups'][key]=p['canonical_groups'][key][1:]
        variants.append(('missing-transport-image',p))
        p=copy.deepcopy(producer);p['records'][0]['row_sums'][0]+=1;variants.append(('forged-row-margin',p))
        for name,p in variants:
            case=w/name;case.mkdir();(case/'projection.json').write_text(json.dumps(p))
            result=subprocess.run([sys.executable,str(HERE/'projection_audit.py'),'--mode',mode,'--work',str(case)],env=environment,capture_output=True,text=True,timeout=30)
            if result.returncode==0 or not result.stderr:raise ValueError('Accepted projection damage '+mode+'/'+name)
            audit_rejections.append(dict(mode=mode,name=name))

        index=next(k for k,r0 in enumerate(inc['results']) if r0['records'])
        variants=[]
        i=copy.deepcopy(inc);i['results'][index]['records']=i['results'][index]['records'][1:];variants.append(('missing-incidence',i))
        i=copy.deepcopy(inc);i['results'][index]['records'][0]['X'][0]=0;variants.append(('forged-X-row',i))
        i=copy.deepcopy(inc);entry=i['column_types']['3'][0]
        entry['columns'][1]^=1;variants.append(('forged-column-phase',i))
        i=copy.deepcopy(inc);entry=i['column_types']['3'][0]
        entry['extra']=1;variants.append(('unknown-column-field',i))
        for name,i in variants:
            case=w/name;case.mkdir();(case/'projection.json').write_text(json.dumps(producer));(case/'incidence-records.json').write_text(json.dumps(i))
            for file in ['frames.txt','frames.json']:shutil.copyfile(r/file,case/file)
            result=subprocess.run([sys.executable,str(HERE/'incidence_audit.py'),'--work',str(case)],env=environment,capture_output=True,text=True,timeout=30)
            if result.returncode==0 or not result.stderr:raise ValueError('Accepted incidence damage '+mode+'/'+name)
            audit_rejections.append(dict(mode=mode,name=name))
    # Independently computed empty L12 projection: forged survivors or
    # transport groups must fail, rather than treating zero as a missing field.
    producer=json.loads((replay/'L12/projection.json').read_text())
    for name,field in [('forged-L12-survivor','records'),('forged-L12-group','canonical_groups')]:
        damaged=copy.deepcopy(producer)
        if field=='records':damaged[field]=[{'word':579}]
        else:damaged[field]={'579':[579]}
        case=work/name;case.mkdir();(case/'projection.json').write_text(json.dumps(damaged))
        result=subprocess.run([sys.executable,str(HERE/'projection_audit.py'),'--mode','L12','--work',str(case)],env=environment,capture_output=True,text=True,timeout=30)
        if result.returncode==0 or not result.stderr:raise ValueError('Accepted false L12 survivor '+name)
        audit_rejections.append(dict(mode='L12',name=name))
    frozen_rejections=[]
    for name in ['omitted-frame','Boolean-valid','unknown-field','wrong-scope','forged-analytic-gap']:
        damaged=copy.deepcopy(expected)
        if name=='omitted-frame':damaged['completions']['frames']=damaged['completions']['frames'][1:]
        elif name=='Boolean-valid':damaged['completions']['direct']['valid']=False
        elif name=='wrong-scope':damaged['scope']='All22 graphs are excluded'
        elif name=='forged-analytic-gap':damaged['analytic']['ordinary_low_neighborhoods'][3]['cases'][0]['gap']=0
        else:damaged['unknown']=1
        try:reproduce.mathematical_summary(replay,damaged)
        except ValueError:frozen_rejections.append(name)
        else:raise ValueError('Accepted typed frozen damage '+name)
    duplicate=work/'duplicate.json';duplicate.write_text('{"a":1,"a":1}')
    try:reproduce.strict_json(duplicate)
    except ValueError:frozen_rejections.append('duplicate-JSON-key')
    else:raise ValueError('Accepted duplicate JSON key')
    controls=page_controls()
    record=dict(status='WHOLE_TWO_PAIR_NATIVE_SANITIZERS_AND_DAMAGES_PASS',
                K_words_checked=sum(s['K_words_checked'] for s in sanitized.values()),
                completion_choices=sum(s['completion_choices'] for s in sanitized.values()),
                every_native_semantic_field_equal=True,entire_native_streams_byte_equal=True,
                sanitizer_flags=flags,sanitized_by_mode=sanitized,native_damage_rejections=native_rejections,
                audit_damage_rejections=audit_rejections,frozen_damage_rejections=frozen_rejections,
                literal_controls=controls,seconds=time.monotonic()-start,
                peak_child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,threads=1,
                trust='Whole finite native censuses, not sampling; same author, ordinary proof/code bridges unformalized.')
    (work/'validation.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n');print(json.dumps(record,indent=2))

if __name__=='__main__':main()
