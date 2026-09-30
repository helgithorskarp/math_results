#!/usr/bin/env python3
"""Independent backward dependency-DAG audit of QR617 seam certificates.

six-reviewer-2, independent mathematical reviewer. Standard library only.
No target checker/generator is imported; the supplied corpus is untrusted.
"""
import argparse
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path

P,N,C,L,R=617,3704,1852,1287,2417

class Invalid(ValueError):
    pass

def need(condition,message):
    if not condition:
        raise Invalid(message)

def integer(x):
    return type(x) is int

def points(record):
    need(isinstance(record,list) and len(record)==2 and all(integer(x) for x in record),'AP format')
    a,d=record
    need(a>=0 and d>0 and a+6*d<N,'AP domain')
    return tuple(range(a,a+7*d,d))

def bits(xs):
    result=0
    for x in xs:
        result|=1<<x
    return result

def positions(mask):
    result=[]
    while mask:
        b=mask&-mask
        result.append(b.bit_length()-1)
        mask-=b
    return result

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def colors():
    # Pair all nonzero square roots, without Euler modular exponentiation.
    need(all(P%d for d in range(2,25)),'617 prime')
    square={(k*k)%P for k in range(1,(P+1)//2)}
    need(len(square)==308 and 0 not in square,'complete square classes')
    q=[None]+[int(r not in square) for r in range(1,P)]
    need(all(q[r]==q[-r%P] for r in range(1,P)),'negative-one square')
    return q

def reference(s,q,outer_only=False):
    need(integer(s) and 0<=s<P,'phase')
    return [None if ((x-C+s)%P==0 or (outer_only and L<=x<R))
            else q[(x-C+s)%P]^int(x>=C) for x in range(N)]

def cut_roots(cut,s,word,erased):
    """Read the whole trace as a DAG, then recursively justify its conclusion.

    Nodes are signed assignments; leaves must be available fixed nonpoles.
    Root masks propagate through dependencies instead of mutating a word.
    """
    need(isinstance(cut,dict) and cut.get('type') in ('opposed','implication'),'cut format')
    if cut['type']=='opposed':
        r=cut['record']
        need(isinstance(r,list) and len(r)==3 and all(integer(x) for x in r),'opposed format')
        v,d0,d1=r
        need(L<=v<R,'opposed center')
        support=[]
        for color,d in enumerate((d0,d1)):
            for x in points([v-3*d,d]):
                if x!=v:
                    need(word[x]==color and not (erased>>x)&1,'opposed initial leaf')
                    support.append(x)
        mask=bits(support)
        need(mask.bit_count()==12,'opposed distinct premises')
        return mask,0
    r=cut['record']
    need(r.get('key')==[s,s,1],'trace phase')
    trace=r.get('steps')
    need(isinstance(trace,list),'trace format')
    nodes={}
    for i,row in enumerate(trace):
        need(isinstance(row,list) and len(row)==4 and all(integer(x) for x in row),'node format')
        x,color,a,d=row
        need(0<=x<N and color in (0,1) and x not in nodes,'distinct node assignment')
        need(word[x] is None or (erased>>x)&1,'forced node was initially free')
        ap=points([a,d]);need(x in ap,'node belongs to premise AP')
        nodes[x]=(i,color,tuple(y for y in ap if y!=x))
    cache={};visited=set()
    def justify(x,wanted,consumer):
        if x not in nodes:
            need(word[x]==wanted and not (erased>>x)&1,'available initial leaf')
            return 1<<x
        index,color,premises=nodes[x]
        need(index<consumer,'acyclic earlier dependency')
        need(color==wanted,'dependency color')
        if x not in cache:
            root=0
            for y in premises:
                root|=justify(y,1-color,index)
            cache[x]=root
        visited.add(x)
        return cache[x]
    terminal=points(r.get('final_ap'))
    first=terminal[0]
    color=nodes[first][1] if first in nodes else word[first]
    need(color in (0,1),'terminal known color')
    roots=0
    for x in terminal:
        roots|=justify(x,color,len(trace))
    # Every supplied node is checked, including potential unused steps. The
    # published pruned corpus has none; union matches its protected support.
    terminal_nodes=len(visited)
    for x,(index,color,premises) in nodes.items():
        roots|=justify(x,color,len(trace))
    need(roots and not (roots&erased),'nonempty new roots')
    return roots,len(trace)-terminal_nodes

def family(cuts,s,q):
    need(isinstance(cuts,list) and len(cuts)==(33 if s in (0,1) else 31),'complete cut count')
    word=reference(s,q,True);used=0;sizes=[];supports=[];unused=0
    for cut in cuts:
        root,junk=cut_roots(cut,s,word,used)
        need(not (root&used),'pairwise disjoint far roots')
        need(all(word[x] in (0,1) for x in positions(root)),'exterior nonpole root domain')
        used|=root;unused+=junk;sizes.append(root.bit_count());supports.append(positions(root))
    return {'key':[s,s,1],'cuts':len(cuts),'support_sizes':sizes,
            'support_sets':supports,'root_union':positions(used)},unused

def reflected(cut,s):
    # Transform signed nodes and APs; the mate is subsequently checked from
    # its independently built word. No inference from a quotient is trusted.
    if cut['type']=='opposed':
        v,d0,d1=cut['record']
        return {'type':'opposed','record':[N-1-v,d1,d0]}
    r=cut['record'];a,d=r['final_ap'];mate=(1-s)%P
    return {'type':'implication','record':{'key':[mate,mate,1],
            'steps':[[N-1-x,1-b,N-1-a-6*d,d] for x,b,a,d in r['steps']],
            'final_ap':[N-1-a-6*d,d]}}

def inner(records,s,q):
    word=reference(s,q);used=0;by_color=[0,0]
    for r in records:
        ap=points(r);need(L<=ap[0] and ap[-1]<R,'inner region')
        mask=bits(ap);need(not(mask&used),'inner disjoint APs')
        color=word[ap[0]];need(color in (0,1) and all(word[x]==color for x in ap),'inner monochromatic nonpoles')
        used|=mask;by_color[color]+=1
    return used,by_color

def controls(q,complete):
    rejected=[]
    def reject(name,call):
        try:call()
        except Invalid:rejected.append(name)
        else:raise Invalid('corruption accepted: '+name)
    reject('zero difference',lambda:points([0,0]))
    reject('out of interval',lambda:points([3698,1]))
    reject('Boolean integer',lambda:points([False,1]))
    w=[None]*N
    for x in range(6):w[x]=0
    for x in range(7,13):w[x]=1
    toy={'type':'implication','record':{'key':[0,0,1],'steps':[[6,1,0,1]],'final_ap':[6,1]}}
    root,junk=cut_roots(toy,0,w,0)
    need(root==bits(list(range(6))+list(range(7,13))) and junk==0,'positive one-step DAG control')
    cyclic=copy.deepcopy(toy);cyclic['record']['steps']=[[6,1,0,1],[5,0,5,1]]
    cyclic_word=w[:];cyclic_word[5]=None
    reject('cyclic or future dependency',lambda:cut_roots(cyclic,0,cyclic_word,0))
    s,cuts=complete[0]
    reject('missing final cut',lambda:family(cuts[:-1],s,q))
    reject('duplicate support',lambda:family([cuts[0]]*len(cuts),s,q))
    word=reference(s,q,True)
    opposed=next(c for c in cuts if c['type']=='opposed')
    support,_=cut_roots(opposed,s,word,0)
    reject('erased initial premise',lambda:cut_roots(opposed,s,word,support&-support))
    previous=0
    for candidate in cuts:
        if candidate['type']=='implication' and candidate['record']['steps']:
            imp=candidate;break
        root,_=cut_roots(candidate,s,word,previous);previous|=root
    baseline,_=cut_roots(imp,s,word,previous)
    need(baseline!=0,'valid mutation baseline')
    bad=copy.deepcopy(imp);bad['record']['steps'][0][1]^=1
    reject('flipped forced value',lambda:cut_roots(bad,s,word,previous))
    bad=copy.deepcopy(imp);bad['record']['steps'][0][0]=bad['record']['steps'][0][2]+7*bad['record']['steps'][0][3]
    reject('forced point outside AP',lambda:cut_roots(bad,s,word,previous))
    bad=copy.deepcopy(imp);bad['record']['steps']=[bad['record']['steps'][0]]*2
    reject('repeated assignment',lambda:cut_roots(bad,s,word,previous))
    bad=copy.deepcopy(imp);bad['record']['final_ap']=[0,0]
    reject('invalid terminal AP',lambda:cut_roots(bad,s,word,previous))
    # Hand-checkable eight-position clauses at a generic partial word:
    # positions0..5 fixed0 force6=1; positions1..6 then contradict fixed0.
    w=[None]*N
    for x in range(6):w[x]=0
    w[7]=0
    toy={'type':'implication','record':{'key':[0,0,1],'steps':[[6,1,0,1]],'final_ap':[1,1]}}
    # This terminal contains opposite6=1, so it must be rejected.
    reject('nonmonochromatic terminal',lambda:cut_roots(toy,0,w,0))
    return rejected

def audit(work):
    q=colors()
    need(all(q[a*r%P]==q[a]^q[r] for a in range(1,P) for r in range(1,P)),'multiplicative affine color identity')
    reps=[s for s in range(P) if s<=(1-s)%P]
    need(len(reps)==309 and [s for s in reps if s==(1-s)%P]==[309],'complete reflection orbits')
    need({p.name for p in work.glob('canonical-*.json')}=={f'canonical-{s}.json' for s in reps},'canonical file coverage')
    rows={};proofs=[];all_cuts=[];types=Counter();unused=0;counts=Counter();steps=Counter()
    for s in reps:
        data=json.loads((work/f'canonical-{s}.json').read_text())
        need(data['key']==[s,s,1],'canonical key')
        cuts=data['cuts'];need(len(cuts)==(33 if s==0 else 31),'canonical corpus completed')
        proofs.append({'key':[s,s,1],'cuts':cuts});all_cuts.append((s,cuts))
        mate=(1-s)%P
        for phase,fam in [(s,cuts)]+([] if mate==s else [(mate,[reflected(c,s) for c in cuts])]):
            need(phase not in rows,'unique phase')
            row,junk=family(fam,phase,q);rows[phase]=row;unused+=junk
            counts.update(row['support_sizes'])
            for cut in fam:
                types[cut['type']]+=1
                if cut['type']=='implication':steps[len(cut['record']['steps'])]+=1
    need(set(rows)==set(range(P)),'all617 phases')
    data=json.loads((work/'inner.json').read_text())
    need(data['format']=='QR617_OPPOSITE_PHASE_INNER_PACKING_V1' and data['region']==[L,R],'inner format')
    direct={}
    for row in data['records']:
        key=row['key'];need(isinstance(key,list) and len(key)==3 and integer(key[0]) and key==[key[0],key[0],1],'inner key')
        s=key[0];need(0<=s<P and s not in direct,'inner unique phase')
        inner(row['aps'],s,q);direct[s]=row['aps']
    need(set(direct)==set(range(P)),'inner coverage')
    chosen=[];phase_profile=[];refined=[];merged_rows=[]
    for s in range(P):
        mate=(1-s)%P;source=s if len(direct[s])>=len(direct[mate]) else mate
        aps=direct[source] if source==s else [[N-1-a-6*d,d] for a,d in direct[source]]
        used,color_count=inner(aps,s,q)
        need(len(aps)>=(38 if s in(0,1) else 40),'claimed inner threshold')
        need(not(used&bits(rows[s]['root_union'])),'joint region disjointness')
        need(len(aps)+rows[s]['cuts']>=71,'claimed joint threshold')
        chosen.append({'key':[s,s,1],'source_phase':source,'aps':aps,'support':positions(used)})
        phase_profile.append([s,len(aps),rows[s]['cuts'],*color_count])
        # Combine complementary color classes. Each original packing is
        # disjoint; APs from different reference colors cannot intersect.
        mirror=[[N-1-a-6*d,d] for a,d in direct[mate]]
        _,dcounts=inner(direct[s],s,q)
        _,mcounts=inner(mirror,s,q)
        word=reference(s,q);merged=[];sources=[];reflections=[]
        for color in (0,1):
            use_direct=dcounts[color]>=mcounts[color]
            source=s if use_direct else mate
            pool=direct[s] if use_direct else mirror
            sources.append(source);reflections.append(not use_direct)
            merged.extend(ap for ap in pool if word[ap[0]]==color)
        new_used,new_counts=inner(merged,s,q)
        need(new_counts==[max(dcounts[b],mcounts[b]) for b in (0,1)],'exact separate-color envelope')
        need(len(merged)>=40 and min(new_counts)>=18,'strong inner/color thresholds')
        need(not(new_used&bits(rows[s]['root_union'])),'merged inner/far disjointness')
        total=len(merged)+rows[s]['cuts']
        need(total>=(73 if s in (0,1) else 71),'strong exceptional total')
        refined.append([s,*new_counts,len(merged),rows[s]['cuts'],total])
        merged_rows.append({'phase':s,'source_by_color':sources,'reflected_by_color':reflections,'aps':merged,'support':positions(new_used)})
    rejection=controls(q,all_cuts)
    for label,bad in [('duplicated inner AP',direct[0]+[direct[0][0]]),
                      ('inner pole AP',[[next(x for x in range(L,R-6) if (x-C)%P==0),1]])]:
        try:inner(bad,0,q)
        except Invalid:rejection.append(label)
        else:raise Invalid('inner corruption accepted: '+label)
    need(refined[309][1:3]==[21,21],'self-reflecting phase positive control')
    try:need(inner(direct[309],309,q)[1]==refined[309][1:3],'self-mate selector ignores reflection')
    except Invalid:rejection.append('self-mate selector ignores reflection')
    else:raise Invalid('fixed-phase selector corruption accepted')
    ordered=[rows[s] for s in range(P)]
    result={'agent':'six-reviewer-2','role':'independent mathematical reviewer',
            'status':'COMPLETE_INDEPENDENT_DAG_AUDIT',
            'prime':P,'length':N,'affine_multiplication_checks':(P-1)**2,
            'interval_AP_count':sum(N-6*d for d in range(1,(N-1)//6+1)),'inner_region':[L,R],'phase_count':len(rows),'canonical_count':len(reps),
            'canonical_certificate_sha256':digest(proofs),'all_phase_support_sha256':digest(ordered),
            'inner_selected_support_sha256':digest(chosen),
            'canonical_cut_count':sum(len(cuts) for s,cuts in all_cuts),
            'far_cut_count':sum(row['cuts'] for row in ordered),
            'selected_inner_AP_count':sum(len(row['aps']) for row in chosen),
            'cut_types':dict(sorted(types.items())),'support_size_histogram':dict(sorted(counts.items())),
            'step_count_histogram':dict(sorted(steps.items())),'unused_trace_nodes':unused,
            'joint_bound_histogram':dict(sorted(Counter(row[1]+row[2] for row in phase_profile).items())),
            'minimum_inner_edits_each_reference_color':[min(row[3] for row in phase_profile),min(row[4] for row in phase_profile)],
            'phase_profile_sha256':digest(phase_profile),
            'refined_inner_minimum':min(row[3] for row in refined),
            'refined_color_minima':[min(row[1] for row in refined),min(row[2] for row in refined)],
            'refined_exceptional_profiles':refined[:2],
            'refined_joint_bound_histogram':dict(sorted(Counter(row[5] for row in refined).items())),
            'refined_weakest_phases':[row[0] for row in refined if row[5]==min(r[5] for r in refined)],
            'refined_phase_profile_sha256':digest(refined),
            'merged_inner_support_sha256':digest(merged_rows),
            'merged_inner_AP_count':sum(row[3] for row in refined),'controls_rejected':rejection,
            'scope':'Equal normalized pole phase and opposite orientation, arbitrary actual coloring/poles. Support packing lower bounds, not edit optima or a W(2,7) resolution.'}
    return result,refined

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--workdir',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True);parser.add_argument('--profile',type=Path)
    args=parser.parse_args();result,profile=audit(args.workdir)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    if args.profile:args.profile.write_text(json.dumps(profile,separators=(',',':'))+'\n')
    print(result['status'],'phases',result['phase_count'],'far supports',result['far_cut_count'],'inner APs',result['selected_inner_AP_count'])

if __name__=='__main__':main()
