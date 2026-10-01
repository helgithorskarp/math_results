"""Packed Boolean-column producer for the changed-B28 barrier.
The numeric verifier is standalone and imports none of this machinery.
"""
import hashlib
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import resource
import time
ROOT=Path(__file__).resolve().parent
METRICS={}
def need(test,message):
    if not test:raise ValueError(message)
def count(name,amount=1):
    METRICS[name]=METRICS.get(name,0)+amount
def digest(obj):
    return hashlib.sha256(json.dumps(obj,separators=(',',':')).encode()).hexdigest()
FIXTURE_SHA256='b46d8382fc40a39ffcaad6ed7396318d8efb7efc03692b8bc160568e76dba1bb'

PINS={'../native24-kernel-cover/nested_generate.py': '2574da2080f38a750274771d49609a90cebc99d25a0e97c84fb599246c62a611', '../native24-kernel-cover/minimum_generate.py': 'c4699f5c85be9906f410390538865f5ada0e93e0431c7fe2ac4e2876ee01589c', '../native24-kernel-cover/generate.py': '08a37678a11392ed46907ab30b2463d841e3e068764c09e410244490f2212381', '../native24-kernel-cover/NESTED.md': '3c291c8796cc7586db522d515098debf769482dc5b2d6bf8467fd8aa03322433', '../semantic-pruning/profile.py': 'dca9c8d6331c3fc548c514ca8f5f1cd170f4a0bb39a3c05250876247d0362719', '../semantic-pruning/anchors.py': '0b95573e7e3c446d0b7ca5352f6b5f4b8d92b91d6f3c72e7b4f783cd99d89902'}
for name,pin in PINS.items():
    need(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==pin,'dependency pin differs: '+name)
spec=importlib.util.spec_from_file_location('changed_b28_nested_column',ROOT/'../native24-kernel-cover/nested_generate.py')
q=importlib.util.module_from_spec(spec);spec.loader.exec_module(q)

def ordinary(records):
    entries=sorted(r[:5] for r in records);grouped={}
    for row in entries:
        tag=tuple(row[2:4]);grouped[tag]=max(grouped.get(tag,-1),row[4])
    return {'records_sha256':digest(entries),'envelope':[[*tag,d] for tag,d in sorted(grouped.items())],
            'mass':sum(2**d for d in grouped.values())}

def ordinary_transition(envelope,gate):
    # Direct bit-mask transport rather than scalar tag arrays.
    a,b=gate;ma,mb=1<<a,1<<b;grouped={}
    for lo,hi,d in envelope:
        ta=-1 if lo&ma else 1 if hi&ma else 0
        tb=-1 if lo&mb else 1 if hi&mb else 0
        hit=bool((lo|hi)&(ma|mb))
        if ta>tb:
            if ta==-1 or tb==-1:lo^=ma|mb
            if ta==1 or tb==1:hi^=ma|mb
        tag=(lo,hi);grouped[tag]=max(grouped.get(tag,-1),d+hit)
    return [[*tag,d] for tag,d in sorted(grouped.items())]

def fixture_inputs():
    raw=(ROOT/'fixture.json').read_bytes()
    need(hashlib.sha256(raw).hexdigest()==FIXTURE_SHA256,'literal fixture pin differs')
    f=json.loads(raw)
    need((f['schema'],f['n'],f['size_budget'],f['prefix_length'],f['l'],f['h'],f['free_inputs'])
         ==('changed-b28-fixed-fixture-v1',13,44,28,3,3,7),'fixture parameters differ')
    gates=f['prefix']+f['forced_maximum_word']
    need(len(f['prefix'])==28 and len(f['forced_maximum_word'])==3,
         'literal word lengths differ')
    need(all(type(a)==type(b)==int and 0<=a<b<13 for a,b in gates),'invalid standard gate')
    need(f['forced_maximum_word']==[[7,9],[9,11],[10,11]],'forced word differs')
    originals=f['original_clampings']
    need(1<=len(originals)<=20 and len({tuple(z) for z in originals})==len(originals),
         'selected original domains invalid')
    need(all(type(lo)==type(hi)==int and lo>=0 and hi>=0 and not lo&hi
             and (lo|hi)<2**13 and lo.bit_count()==hi.bit_count()==3 for lo,hi in originals),
         'invalid original clamping')
    return f,gates

def image_summary(rows):
    rows=sorted(set(rows))
    correct=[q for q in range(13)
             if all(((r>>q)&1)==int(q>=13-r.bit_count()) for r in rows)]
    return {'input_count':8192,'output_count':len(rows),'image_sha256':digest(rows),
            'correct_output_wires_on_all_boolean_inputs':correct,
            'weight_counts':[sum(r.bit_count()==w for r in rows) for w in range(14)]}

def cover_structure(f,low,high,root_image,terminal_image,middle):
    need(low['mass']==high['mass']==512,'P28 ordinary masses are not saturated')
    need(low['envelope']==[[3,0,9]],'P28 minimum envelope differs')
    need(high['envelope']==[[0,4224,6],[0,4608,6],[0,5120,8],[0,6144,7]],
         'P28 maximum envelope differs')
    states=[];lo=low['envelope'];hi=high['envelope']
    for cut in range(4):
        controls=[];events=[];preps=[]
        live_mask=0
        for l,h,d in lo+hi:live_mask|=l|h
        for a,b in combinations(range(13),2):
            gate=[a,b]
            nxt_lo=ordinary_transition(lo,gate)
            nxt_hi=ordinary_transition(hi,gate)
            lm=sum(2**r[2] for r in nxt_lo)
            hm=sum(2**r[2] for r in nxt_hi)
            if lm>512 or hm>512:
                kind='forbidden'
            elif nxt_hi!=hi:
                kind='event';events.append(gate)
            else:
                kind='preparation';preps.append(gate)
                need(not ((1<<a)|(1<<b))&live_mask,'preparation touches a live endpoint')
                need(nxt_lo==lo,'preparation changes saturated minimum data')
            controls.append([a,b,lm,hm,kind])
            count('standard_next_gate_controls')
        expected=[f['forced_maximum_word'][cut]] if cut<3 else []
        need(events==expected,'complete next-event list differs')
        free=[q for q in range(13) if not live_mask>>q&1]
        need(preps==[list(z) for z in combinations(free,2)],'preparation list incomplete')
        states.append({'cut':28+cut,'low_envelope':lo,'high_envelope':hi,
                       'allowed_event_gates':events,'preparation_wires':free,
                       'preparation_gate_count':len(preps),'next_gate_controls':controls})
        if cut<3:
            gate=f['forced_maximum_word'][cut]
            lo=ordinary_transition(lo,gate);hi=ordinary_transition(hi,gate)
    need(lo==[[3,0,9]] and hi==[[0,6144,9]],'terminal frozen envelope differs')
    need(middle['size']==80 and middle['image_sha256']
         =='1eb1f208b305e646f34963308548c950af5769446a247a1f7601af313db5e152',
         'literal peer target differs')
    need(all(q in terminal_image['correct_output_wires_on_all_boolean_inputs']
             for q in [0,1,11,12]),'terminal outer output controls fail')
    return {'prefix28_sha256':digest(f['prefix']),'small_size_lower_bound':35,
            'ordinary_ceiling_for_size44':512,'prefix28_low2':low,'prefix28_high2':high,
            'complete_event_states':states,'event_word_count':1,'forced_event_word':f['forced_maximum_word'],
            'prefix28_boolean_image':root_image,'prefix31_sha256':digest(f['prefix']+f['forced_maximum_word']),
            'prefix31_boolean_image':terminal_image,'middle9':middle}

def finish_certificate(f,cover,rows):
    tags=[tuple(r['pruning']['outer_record'][2:4]) for r in rows]
    need(len(tags)==len(set(tags)),'selected current tag classes overlap')
    mass=sum(2**r['nested_label'] for r in rows)
    need(mass>2**44,'selected nested mass is not an exclusion')
    return {'schema':'changed-b28-nested-barrier-v1','agent':'six-sorting-2','role':'researcher',
            'fixture_sha256':FIXTURE_SHA256,'n':13,'size_budget':44,'l':3,'h':3,'free_inputs':7,
            'cover':cover,'selected_original_domains':rows,'selected_classes':len(tags),
            'selected_mass':mass,'total_lower_bound':(mass-1).bit_length(),
            'maximum_individual_label':max(r['nested_label'] for r in rows)}

def build():
    f,gates=fixture_inputs()
    low=ordinary(q.s.analyze_family(13,f['prefix'],2,0)['records'])
    high=ordinary(q.s.analyze_family(13,f['prefix'],0,2)['records'])
    root=image_summary(q.m.base.boolean_image(13,f['prefix']))
    terminal_rows=q.m.base.boolean_image(13,gates);terminal=image_summary(terminal_rows)
    image=sorted({(r>>2)&511 for r in terminal_rows})
    middle={'n':9,'original_wires':list(range(2,11)),'size':len(image),
            'image':image,'image_sha256':digest(image),
            'weight_counts':[sum(r.bit_count()==w for r in image) for w in range(10)]}
    cover=cover_structure(f,low,high,root,terminal,middle)
    rows=[q.witness(gates,lo,hi) for lo,hi in f['original_clampings']]
    return finish_certificate(f,cover,rows)

def main():
    start=time.monotonic();out=build();path=ROOT/'certificate.json'
    path.write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({'status':'CHANGED_B28_CERTIFICATE_REGENERATED','agent':'six-sorting-2','role':'researcher',
                      'selected_domains':out['selected_classes'],'selected_mass':out['selected_mass'],
                      'total_lower_bound':out['total_lower_bound'],
                      'certificate_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                      'bytes':path.stat().st_size,'seconds':time.monotonic()-start,
                      'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},sort_keys=True))
if __name__=='__main__':main()
