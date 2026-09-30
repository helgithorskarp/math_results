#!/usr/bin/env python3
"""Exact certificate checker: Euler colors, whole partial words, direct APs.

The elementary AP/checking primitives are adapted from the author's earlier
QR617 exterior-support source (dfe06f622992968dfd3868cb9a78dcd6c5a98c9f).
No generator, unit-propagation state or AP incidence table is imported.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import time

P,N,C,H=617,3704,1852,565
LO,HI=C-H,C+H
FAR,EXCEPTIONAL_FAR=31,33
INNER,EXCEPTIONAL_INNER,TOTAL=40,38,71


def require(test,message):
    if not test:raise ValueError(message)


def qr():
    require(all(P%d for d in range(2,25)),'primality617')
    result=[None]
    for r in range(1,P):
        value=pow(r,(P-1)//2,P)
        require(value in (1,P-1),'Euler criterion')
        result.append(int(value==P-1))
    return result


def check_key(key):
    require(isinstance(key,list) and len(key)==3 and all(type(v) is int for v in key),'integer key')
    require(0<=key[0]<P and key==[key[0],key[0],1],'equal-phase/opposite-orientation key')


def initial_color(x,key,q):
    require(type(x) is int and 0<=x<N,'position bounds')
    if LO<=x<HI:return None
    r=(x-C+key[0])%P
    return None if r==0 else q[r]^(int(x>=HI))


def ap_points(a,d):
    require(type(a) is int and type(d) is int and a>=0 and d>0 and a+6*d<N,'nonconstant AP bounds')
    return [a+j*d for j in range(7)]


def check_cut(cut,key,q,erased=()):
    check_key(key)
    require(cut['type'] in ('opposed','implication'),'cut type')
    if cut['type']=='opposed':
        record=cut['record']
        require(isinstance(record,list) and len(record)==3 and all(type(v) is int for v in record),'opposed record')
        v,d0,d1=record;require(LO<=v<HI,'free bridge center');support=set()
        for b,d in enumerate((d0,d1)):
            for x in ap_points(v-3*d,d):
                if x!=v:
                    require(initial_color(x,key,q)==b,'protected opposed premise')
                    support.add(x)
        require(len(support)==12 and not support.intersection(erased),'opposed support overlap')
        return support
    record=cut['record'];require(record['key']==key,'implication phase key')
    word=[initial_color(x,key,q) for x in range(N)]
    for x in erased:
        require(type(x) is int and 0<=x<N and word[x] is not None,'protected distinct erasure')
        word[x]=None
    initial=word[:];support=set()
    require(isinstance(record['steps'],list),'step list')
    for step in record['steps']:
        require(isinstance(step,list) and len(step)==4 and all(type(v) is int for v in step),'integer implication')
        x,b,a,d=step
        require(0<=x<N and b in (0,1) and word[x] is None,'free forced point')
        points=ap_points(a,d)
        require(x in points and all(word[y]==1-b for y in points if y!=x),'six equal fixed premises')
        support.update(y for y in points if initial[y] is not None);word[x]=b
    final=record['final_ap'];require(isinstance(final,list) and len(final)==2,'final AP')
    points=ap_points(*final);b=word[points[0]]
    require(b in (0,1) and all(word[y]==b for y in points),'fixed monochromatic final AP')
    support.update(y for y in points if initial[y] is not None)
    require(support and not support.intersection(erased),'nonempty disjoint protected support')
    return support


def check_family(cuts,key,q):
    require(isinstance(cuts,list) and cuts,'nonempty family')
    used=set();sizes=[];supports=[]
    for cut in cuts:
        support=check_cut(cut,key,q,used)
        require(not support.intersection(used),'overlapping supports')
        used.update(support);sizes.append(len(support));supports.append(sorted(support))
    return {'key':key,'cuts':len(cuts),'support_sizes':sizes,'support_sets':supports,'root_union':sorted(used)}


def reflect_cut(cut,key):
    check_key(key);s=key[0];mate=(1-s)%P
    if cut['type']=='opposed':
        v,d0,d1=cut['record'];return {'type':'opposed','record':[N-1-v,d1,d0]}
    r=cut['record']
    return {'type':'implication','record':{'key':[mate,mate,1],
            'steps':[[N-1-x,b^1,N-1-a-6*d,d] for x,b,a,d in r['steps']],
            'final_ap':[N-1-r['final_ap'][0]-6*r['final_ap'][1],r['final_ap'][1]]}}


def representatives():
    result=[s for s in range(P) if s<=(1-s)%P]
    require(len(result)==309 and [s for s in result if s==(1-s)%P]==[309],'reflection quotient')
    return result


def stable_hash(value):
    encoded=json.dumps(value,sort_keys=True,separators=(',',':')).encode()
    return hashlib.sha256(encoded).hexdigest()


def target(s):
    return EXCEPTIONAL_FAR if s in (0,1) else FAR


def check_inner_aps(aps,s,q):
    require(isinstance(aps,list),'inner AP list');used=set()
    for record in aps:
        require(isinstance(record,list) and len(record)==2,'inner AP record')
        points=ap_points(*record)
        require(LO<=points[0] and points[-1]<HI,'inner region bounds')
        values=[]
        for x in points:
            require(x not in used,'overlapping inner APs');r=(x-C+s)%P
            require(r!=0,'inner pole');values.append(q[r]^int(x>=C))
        require(all(v==values[0] for v in values),'inner monochromatic AP')
        used.update(points)
    return used


def verify_inner(path,q):
    data=json.loads(path.read_text())
    require(data['format']=='QR617_OPPOSITE_PHASE_INNER_PACKING_V1' and data['region']==[LO,HI],'inner transcript geometry')
    require(isinstance(data['records'],list) and len(data['records'])==P,'inner record count')
    records={}
    for r in data['records']:
        check_key(r['key']);s=r['key'][0];require(s not in records,'duplicate inner phase')
        check_inner_aps(r['aps'],s,q);records[s]=r['aps']
    require(set(records)==set(range(P)),'full inner phase coverage')
    chosen=[]
    for s in range(P):
        mate=(1-s)%P;source=s if len(records[s])>=len(records[mate]) else mate
        aps=records[source] if source==s else [[N-1-a-6*d,d] for a,d in records[source]]
        support=check_inner_aps(aps,s,q)
        require(len(aps)>=(EXCEPTIONAL_INNER if s in (0,1) else INNER),'inner claimed threshold')
        chosen.append({'key':[s,s,1],'source_phase':source,'aps':aps,'support':sorted(support)})
    return chosen


def verify(directory,inner_path):
    start=time.monotonic();q=qr();covered=set();rows=[];size_hist=Counter();steps=Counter();types=Counter();proofs=[]
    expected={f'canonical-{s}.json' for s in representatives()}
    require({p.name for p in directory.glob('canonical-*.json')}==expected,'exact canonical file coverage')
    for s in representatives():
        data=json.loads((directory/f'canonical-{s}.json').read_text());key=[s,s,1]
        require(data['key']==key,'canonical key');cuts=data['cuts']
        minimum=target(s)
        require(len(cuts)>=minimum,'insufficient certified cuts')
        # The claim uses this exact prefix. Additional local experiments do
        # not silently strengthen the certificate hash or uniform claim.
        cuts=cuts[:minimum];proofs.append({'key':key,'cuts':cuts})
        phases=[(s,cuts)]
        mate=(1-s)%P
        if mate!=s:phases.append((mate,[reflect_cut(c,key) for c in cuts]))
        for phase,family in phases:
            require(phase not in covered,'duplicate phase');covered.add(phase)
            result=check_family(family,[phase,phase,1],q)
            size_hist.update(result['support_sizes']);rows.append(result)
            for cut in family:
                types[cut['type']]+=1
                if cut['type']=='implication':steps[len(cut['record']['steps'])]+=1
    require(covered==set(range(P)),'full617 phase coverage')
    rows.sort(key=lambda row:row['key'][0])
    inner=verify_inner(inner_path,q);joint=[]
    for s in range(P):
        require(not set(rows[s]['root_union']).intersection(inner[s]['support']),'near/far overlap')
        joint.append([s,len(inner[s]['aps']),rows[s]['cuts'],len(inner[s]['aps'])+rows[s]['cuts']])
    require(min(row[3] for row in joint)>=TOTAL,'joint claimed threshold')
    return {'agent':'six-vdw-3','role':'researcher','status':'VERIFIED_COMPLETE_OPPOSITE_PHASE_PACKING',
            'length':N,'half_width':H,'free_bridge':[LO,HI],'phase_values':P,'reflection_representatives':309,
            'uniform_far_nonpole_edit_lower_bound':FAR,'exceptional_far_edit_lower_bound':EXCEPTIONAL_FAR,
            'inner_generic_edit_lower_bound':INNER,'inner_exceptional_edit_lower_bound':EXCEPTIONAL_INNER,
            'exceptional_phases':[0,1],'uniform_total_nonpole_edit_lower_bound':TOTAL,
            'checked_cut_count':sum(row['cuts'] for row in rows),
            'support_size_histogram':dict(sorted(size_hist.items())),
            'cut_type_histogram':dict(sorted(types.items())),
            'implication_step_histogram':dict(sorted(steps.items())),
            'canonical_certificate_sha256':stable_hash(proofs),
            'all_phase_support_sha256':stable_hash(rows),
            'inner_transcript_sha256':hashlib.sha256(inner_path.read_bytes()).hexdigest(),
            'inner_selected_support_sha256':stable_hash(inner),
            'inner_AP_count_histogram':dict(sorted(Counter(len(row['aps']) for row in inner).items())),
            'inner_APs_checked_after_selection':sum(len(row['aps']) for row in inner),
            'joint_bound_histogram':dict(sorted(Counter(row[3] for row in joint).items())),
            'minimum_root_union_size':min(len(r['root_union']) for r in rows),
            'maximum_root_union_size':max(len(r['root_union']) for r in rows),
            'seconds':time.monotonic()-start,
            'scope':'Only equal-phase/opposite-orientation QR617 seams. Lower bound, not optimum, extension or unrestricted exclusion.'}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--workdir',type=Path,required=True)
    parser.add_argument('--inner',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    result=verify(args.workdir,args.inner);args.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':main()
