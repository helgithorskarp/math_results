"""Standalone numeric checker for the native P23 saturation lift.

No generator, profiler, sibling checker or solver imports. All 78 original
two-minimum domains retain their full eleven-free-input Boolean cubes.
The proof imports the P24 theorem; these tests do not reprove that theorem.
"""
from copy import deepcopy
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import time

ROOT = Path(__file__).resolve().parent
PINS = {'fixture.json': '93b7cda51cc14fa8f53c0ed89c7c1c2150b8ab6b58f823fc69b41ec7035022e6', 'NESTED.md': '3c291c8796cc7586db522d515098debf769482dc5b2d6bf8467fd8aa03322433'}
P24_GRAPH = 'bafkreieelq5auvzgfgmbfzwzvam5canm3neqjv35ybhmnne76bs5ymswpy'
METRICS = {}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def count(name, amount=1):
    METRICS[name] = METRICS.get(name,0) + amount


def digest(obj):
    return hashlib.sha256(json.dumps(obj,separators=(',',':')).encode()).hexdigest()


def checked(name,pin):
    raw=(ROOT/name).read_bytes()
    need(hashlib.sha256(raw).hexdigest()==pin,'dependency pin differs')
    return raw


def simulate(row,gates):
    row=list(row)
    for a,b in gates:
        if row[a]>row[b]:
            row[a],row[b]=row[b],row[a]
    return row


def low_mask(row):
    return sum(2**p for p,v in enumerate(row) if v<0)


def record(gates,lows):
    mask=sum(2**p for p in lows)
    free=[p for p in range(13) if p not in lows]
    touch=final=None
    active=0
    for bits in range(2048):
        row=[0]*13
        row[lows[0]],row[lows[1]]=-2,-1
        for j,p in enumerate(free):
            row[p]=bits>>j&1
        hits=0
        for t,(a,b) in enumerate(gates):
            marked=row[a]<0 or row[b]<0
            if marked:hits |= 2**t
            if row[a]>row[b]:
                if not marked:active |= 2**t
                row[a],row[b]=row[b],row[a]
        if touch is None:touch,final=hits,low_mask(row)
        need((hits,low_mask(row))==(touch,final),'free-dependent marked history')
        count('original_free_assignments')
        count('original_gate_evaluations',len(gates))
    redundant=(2**len(gates)-1)&~(touch|active)
    return [mask,0,final,0,touch.bit_count(),redundant.bit_count(),redundant]


def scalar_transition(envelope,gate):
    buckets={}
    for mask,d in envelope:
        places=[p for p in range(13) if mask>>p&1]
        row=[0]*13
        row[places[0]],row[places[1]]=-2,-1
        a,b=gate
        hit=row[a]<0 or row[b]<0
        out=simulate(row,[gate])
        target=low_mask(out)
        buckets.setdefault(target,[]).append((mask,d+hit,hit))
    result=[]
    for target,fibre in sorted(buckets.items()):
        need(len(fibre)<=2,'ordinary fibre too large')
        if len(fibre)==2:
            need(all(hit for _,_,hit in fibre),'uncharged double fibre')
        result.append([target,max(d for _,d,_ in fibre)])
        count('next_gate_fibres')
    count('standard_next_gates')
    return result


def reconstruct():
    fixture=json.loads(checked('fixture.json',PINS['fixture.json']))
    checked('NESTED.md',PINS['NESTED.md'])
    word=fixture['gates']
    need(len(word)==46 and all(0<=a<b<13 for a,b in word),'native source word differs')
    prefix=word[:23]
    records=sorted(record(prefix,list(lows)) for lows in combinations(range(13),2))
    maxima={}
    for row in records:
        maxima[row[2]]=max(maxima.get(row[2],-1),row[4])
    envelope=[[mask,d] for mask,d in sorted(maxima.items())]
    need(envelope==[[3,8],[5,7],[17,7]],'literal saturation envelope differs')
    cases=[]
    for gate in combinations(range(13),2):
        gate=list(gate)
        out=scalar_transition(envelope,gate)
        mass=sum(2**d for _,d in out)
        if mass>512:
            category='forbidden_by_saturation'
        elif set(gate)&{1,2,4}:
            category='forced_live_merge'
        else:
            category='invisible_to_two_minima'
        cases.append({'gate':gate,'ordinary_envelope':out,'ordinary_mass':mass,'category':category})
    safe=[c['gate'] for c in cases if c['category']=='invisible_to_two_minima']
    forced=[c['gate'] for c in cases if c['category']=='forced_live_merge']
    need(len(safe)==36 and forced==[[2,4]],'complete first-event cover differs')
    need(prefix+forced==word[:24],'forced event does not give the excluded P24')
    need(all(not set(g)&{0,1,2,4} for g in safe),'a preparation touches the live support')
    result={'schema':'native23-saturation-v1','agent':'six-sorting-2','role':'researcher',
            'parent_files_sha256':PINS,'n':13,'size_budget':44,'small_size_lower_bound':35,
            'prefix_length':23,'prefix_sha256':digest(prefix),
            'original_family_records_sha256':digest(records),
            'ordinary_envelope':envelope,'ordinary_mass':512,'forced_gate':[2,4],
            'next_prefix_sha256':digest(word[:24]),'p24_theorem_graph':P24_GRAPH,
            'safe_gates':safe,'forbidden_gate_count':sum(c['category']=='forbidden_by_saturation' for c in cases),
            'cases':cases}
    return result,word


def match(candidate,expected):
    need(candidate==expected,'certificate differs from numeric reconstruction')


def controls(data,word):
    for bits in range(8192):
        row=[bits>>p&1 for p in range(13)]
        need(simulate(row,word)==sorted(row),'46-gate positive control fails')
        count('positive_boolean_inputs')
    for gate in data['safe_gates']:
        ports=sorted(set(gate+[2,4]))
        need(len(ports)==4,'safe gate overlaps forced gate')
        for bits in range(16):
            row=[0]*13
            for j,p in enumerate(ports):row[p]=bits>>j&1
            need(simulate(row,[gate,[2,4]])==simulate(row,[[2,4],gate]),'commutation function differs')
            count('commutation_boolean_controls')
    for field in ('ordinary_mass','small_size_lower_bound'):
        damaged=deepcopy(data);damaged[field]+=1
        try:match(damaged,data)
        except ValueError:count('damages_rejected')
        else:raise ValueError('damaged certificate accepted')
    damaged=deepcopy(data);damaged['cases'][0]['ordinary_envelope'][0][1]+=1
    try:match(damaged,data)
    except ValueError:count('damages_rejected')
    else:raise ValueError('damaged transition accepted')
    damaged=deepcopy(data);damaged['forced_gate']=[1,2]
    try:match(damaged,data)
    except ValueError:count('damages_rejected')
    else:raise ValueError('wrong forced gate accepted')


def main():
    start=time.monotonic()
    data,word=reconstruct()
    match(json.loads((ROOT/'p23-certificate.json').read_text()),data)
    controls(data,word)
    print(json.dumps({'status':'ALL_NATIVE23_SATURATION_CHECKS_PASSED','agent':'six-sorting-2',
                      'role':'researcher','original_domains':78,'ordinary_mass':512,
                      'forced_gate':[2,4],'safe_gates':36,'forbidden_gates':41,
                      'minimum_total_size':45,'imported_p24_graph':P24_GRAPH,**METRICS,
                      'certificate_sha256':hashlib.sha256((ROOT/'p23-certificate.json').read_bytes()).hexdigest(),
                      'seconds':time.monotonic()-start,
                      'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},sort_keys=True))


if __name__=='__main__':
    main()
