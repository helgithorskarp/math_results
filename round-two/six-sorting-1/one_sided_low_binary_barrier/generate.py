"""Produce a first-LOW-binary normal form and compact semantic obstruction.
Packed conditional cubes use six-sorting-2's pinned profile.py. Carrier
pruning is adapted from our actual9285 producer, source2b8d0d2b5766ecb8775c72db231fa5eb06ee512a
(original source df4e3aa03d6bf96c21e7bdab1330b98db7e0fad2). No solver is used.
"""
import hashlib,importlib.util,json,os
from itertools import combinations
from pathlib import Path
import resource,time
ROOT=Path(__file__).resolve().parent
SOURCE=Path(os.environ.get('SORTING_SOURCE_ROOT',ROOT.parents[2]))
FIXTURE_PIN='c75eb6b8d98d94f824def44c6ce13a7d09700e04d7422fea6c70522c99c3b43f'
PROFILE_PIN='dca9c8d6331c3fc548c514ca8f5f1cd170f4a0bb39a3c05250876247d0362719'

def need(test,message):
    if not test:raise ValueError(message)

def digest(obj):return hashlib.sha256(json.dumps(obj,separators=(',',':')).encode()).hexdigest()

def scalar(values,gates):
    row=list(values)
    for a,b in gates:
        if row[a]>row[b]:row[a],row[b]=row[b],row[a]
    return row

def mass(classes):return sum(1<<d for p,d in classes)

def route(classes,gate):
    out={}
    for p,d in classes:
        row=[0]*13;row[0]=-2;row[p]=-1;a,b=gate
        cost=d+int(row[a]<0 or row[b]<0)
        if row[a]>row[b]:row[a],row[b]=row[b],row[a]
        q=row.index(-1);out[q]=max(out.get(q,-1),cost)
    return tuple(sorted(out.items()))

def normalize(initial):
    todo=[initial];paths={initial:[]};first=[];controls=0
    while todo:
        state=todo.pop()
        for gate in combinations(range(1,12),2):
            child=route(state,gate);controls+=1;hits=sum(p in gate for p,d in state)
            need(mass(child)>=448,'ordinary mass decreased')
            if mass(child)==448 and hits and child not in paths:
                paths[child]=paths[state]+[list(gate)];todo.append(child)
            if hits==2 and 448<mass(child)<=512:
                costs=sorted(d for p,d in state if p in gate)
                need(costs==[6,7] and 3 in gate,'first LOW binary type differs')
                p=next(p for p in gate if p!=3);need(p in (1,2,4),'first partner differs')
                prior=paths[state];need(all(p not in g and 3 not in g for g in prior),'first endpoint was touched')
                normal=route(initial,gate);tail=[]
                while len(normal)>1:
                    candidates=[(tuple(sorted((a,b))),route(normal,tuple(sorted((a,b)))))
                                for (a,da),(b,db) in combinations(normal,2)
                                if mass(route(normal,tuple(sorted((a,b)))))<=512]
                    need(len(candidates)==1,'forced tail differs')
                    g,normal=candidates[0];tail.append(list(g))
                need(normal==((1,9),) and len(tail)==2,'final LOW root differs')
                need(not prior or tail[:len(prior)]==prior,'prior LOW gate was dropped')
                first.append({'prior_LOW_word':prior,'first_binary':list(gate),'partner':p,'canonical_suffix':[list(gate)]+tail})
    first.sort(key=lambda x:(len(x['prior_LOW_word']),x['prior_LOW_word'],x['first_binary']))
    need(len(paths)==4 and len(first)==6 and controls==220,'complete first binary census differs')
    return {'zero_slack_states':[list(map(list,c)) for c in sorted(paths)],'local_gate_controls':controls,'first_binary_cases':first}

def pruning(gates, low, high, semantic):
    free = [i for i in range(13) if not (low | high) >> i & 1]
    columns = iter(semantic.truth_columns(len(free)))
    values = ["L" if low >> i & 1 else "H" if high >> i & 1 else next(columns) for i in range(13)]
    carrier = [free.index(i) if i in free else None for i in range(13)]
    word, d, r, redundant = [], 0, 0, 0
    for t, (a, b) in enumerate(gates):
        x, y = values[a], values[b]
        if isinstance(x, str) or isinstance(y, str):
            rank = lambda z: -1 if z == "L" else 1 if z == "H" else 0
            d += 1
            if rank(x) > rank(y):
                values[a], values[b] = y, x
                carrier[a], carrier[b] = carrier[b], carrier[a]
        else:
            if not x & ~y:
                r += 1
                redundant |= 1 << t
            else:
                word.append([carrier[a], carrier[b]])
            values[a], values[b] = x & y, x | y
    current = semantic.marked_ports(values)
    output = [i for i in range(13) if isinstance(values[i], int)]
    rename = {carrier[i]: j for j, i in enumerate(output)}
    return {"outer_record": [low, high, *current, d, r, redundant],
            "input_free_wires": free, "output_free_wires": output,
            "input_to_output_wire": [rename[i] for i in range(len(free))],
            "retained_prefix": [[rename[a], rename[b]] for a, b in word]}




def main():
    start=time.monotonic();raw=(ROOT/'fixture.json').read_bytes()
    need(hashlib.sha256(raw).hexdigest()==FIXTURE_PIN,'fixture changed');f=json.loads(raw)
    pp=SOURCE/'round-two/six-sorting-2/semantic-pruning/profile.py'
    need(hashlib.sha256(pp.read_bytes()).hexdigest()==PROFILE_PIN,'credited profiler changed')
    s=importlib.util.spec_from_file_location('one_low_packed_profile',pp);semantic=importlib.util.module_from_spec(s);s.loader.exec_module(semantic)
    base=f['B23'];profile=semantic.analyze_family(13,base,2,0)
    initial=tuple((lo.bit_length()-1,d) for lo,hi,d,c in profile['envelope'])
    need([list(x) for x in initial]==f['initial_LOW'],'base ordinary LOW classes differ')
    normal=normalize(initial);cases=[]
    for p in (1,2,4):
        suffix=f['suffixes'][str(p)];gates=base+suffix;image=set();full=set()
        for x in range(8192):
            row=scalar([x>>i&1 for i in range(13)],gates);ordered=sorted(row)
            need(all(row[i]==ordered[i] for i in (0,1,12)),'three held output ranks differ')
            full.add(sum(v<<i for i,v in enumerate(row)));image.add(sum(row[i]<<(i-2) for i in range(2,12)))
        image=sorted(image)
        need([suffix]==[x['canonical_suffix'] for x in normal['first_binary_cases'] if x['partner']==p][:1],'fixture normal form differs')
        cases.append({'partner':p,'suffix_after_B23':suffix,'prefix_sha256':digest(gates),'full_image_size':len(full),
                      'ten_core_image':image,'ten_core_image_sha256':digest(image),'ten_core_image_size':len(image),'ten_core_budget':18})
    middle=base+f['suffixes']['2'];early=middle[:25]
    selected=[pruning(early,mask,0,semantic) for mask in f['selected_original_LOW']]
    need([x['outer_record'] for x in selected]==[[40,0,5,0,8,1,1<<24],[9,0,3,0,8,0,0]],'early selected pair rows differ')
    need(len({tuple(x['outer_record'][2:4]) for x in selected})==2,'selected classes overlap')
    early_mass=sum(1<<sum(x['outer_record'][4:6]) for x in selected)
    single=pruning(middle,f['single_C10_original_LOW'],0,semantic)
    need(single['outer_record']==[40,0,3,0,9,1,1<<24],'single-domain C10 differs')
    need(len(single['retained_prefix'])==16 and early_mass==768,'strict certificate differs')
    control=pruning(early,5,0,semantic);need(control['outer_record']==[5,0,5,0,8,0,0],'active-domain record differs')
    free=[i for i in range(13) if i not in (0,2)];row=[0]*13;row[0]=-2;row[2]=-1
    for j,i in enumerate(free):row[i]=f['same_configuration_active_control']['assignment']>>j&1
    after=scalar(row,early[:-1]);need(after[1]>after[4] and min(after[1],after[4])>=0,'same-configuration gate is not active')
    cert={'schema':'first-low-binary-semantic-barrier-v1','agent':'six-sorting-1','role':'researcher',
      'fixture_sha256':FIXTURE_PIN,'base_LOW_records_sha256':digest(profile['records']),
      'base_LOW_envelope':profile['envelope'],'normalization':normal,'canonical_cases':cases,
      'earliest_selected_pruning':selected,'earliest_selected_mass':early_mass,'ordinary_pair_size44_ceiling':512,
      'single_C10_pruning':single,'same_configuration_active_pruning':control,'same_configuration_active_row':after,
      'excluded_first_LOW_binary':[2,3],'remaining_first_LOW_binary_partners':[1,4],
      'size_lower_bound_of_middle_stem':f['imported_S11_lower_bound']+sum(single['outer_record'][4:6])}
    target=ROOT/'certificate.json';target.write_text(json.dumps(cert,indent=2)+'\n')
    print(json.dumps({'agent':'six-sorting-1','role':'researcher','status':'ONE_LOW_BINARY_CERTIFICATE_REGENERATED',
      'certificate_bytes':target.stat().st_size,'certificate_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
      'prefix26_C':sum(single['outer_record'][4:6]),'prefix25_mass':early_mass,'minimum_total':45,
      'seconds':time.monotonic()-start,'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},sort_keys=True))

if __name__=='__main__':main()
