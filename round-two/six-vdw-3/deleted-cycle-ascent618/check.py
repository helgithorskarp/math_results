#!/usr/bin/env python3
"""Separate actual-cyclic pattern projection and field-five literal checking."""
import argparse
import hashlib
import itertools
import json
import math
import time
from pathlib import Path

def need(condition,message):
    if not condition:raise ValueError(message)

def parameters(q,lam):
    need(q>=7 and all(q%d for d in range(2,math.isqrt(q)+1)),'Prime q>=7 required')
    need(1<lam<q,'Bad holes')
    holes=(0,1,lam);outside=tuple(x for x in range(q) if x not in holes)
    pairs=tuple(itertools.combinations(outside,2));index={pair:i+1 for i,pair in enumerate(pairs)}
    return holes,outside,pairs,index

def parse(path,n):
    lines=path.read_text().splitlines();need(bool(lines),'Empty DIMACS')
    header=lines[0].split();need(len(header)==4 and header[:2]==['p','cnf'] and int(header[2])==n,'Bad DIMACS variable domain')
    rows=[]
    for line in lines[1:]:
        entries=list(map(int,line.split()));need(entries and entries[-1]==0,'Missing terminator')
        row=tuple(sorted(entries[:-1]));need(all(0<abs(x)<=n for x in row),'Bad literal')
        need(len(row)==len(set(row)) and not any(-x in row for x in row),'Repeated/tautological literal')
        rows.append(row)
    need(len(rows)==int(header[3]) and len(rows)==len(set(rows)),'Count or duplicate mismatch')
    return set(rows)

def audit(path,q,lam):
    begin=time.monotonic();holes,outside,pairs,index=parameters(q,lam);root=outside[0];length=6*q
    rows=set()
    for first,second in itertools.combinations(outside[1:],2):
        ids=(index[(root,first)],index[(root,second)],index[(first,second)])
        for bits in itertools.product((0,1),repeat=3):
            if sum(bits)%2:rows.add(tuple(sorted(v if b==0 else -v for v,b in zip(ids,bits))))
    cycle_count=len(rows);groups={};skipped=tautologies=retained=0
    # Reconstruct every actual cyclic AP, retaining all its forbidden point
    # orientations. These are projected only after a full local truth check.
    for step in range(1,length):
        for start in range(length):
            residues=tuple((start+j*step)%length for j in range(7))
            fields=tuple(t%q for t in residues)
            if any(x in holes for x in fields):skipped+=1;continue
            retained+=1;pattern=tuple(int(t%6>=3) for t in residues)
            if len(set(fields))==1:
                need(len(set(pattern))==2,'Unexpected same-column monochromatic row')
                tautologies+=1;continue
            need(len(set(fields))==7,'Nonzero field slope repeated a point')
            if fields[::-1]<fields:fields=fields[::-1];pattern=pattern[::-1]
            words=groups.setdefault(fields,set());words.add(pattern);words.add(tuple(1-x for x in pattern))
    local_bad=set()
    for word in itertools.product((0,1),repeat=7):
        ladder=[word[j]^word[j+3] for j in range(4)]
        if all(x==ladder[0] for x in ladder):local_bad.add(word)
    need(len(local_bad)==16,'Unexpected local parity truth relation')
    ladders=set()
    for fields,patterns in groups.items():
        need(patterns==local_bad,'Literal cyclic blocked words differ from four-pair ladder')
        ladder=tuple(sorted(index[tuple(sorted((fields[j],fields[j+3])))] for j in range(4)))
        need(len(ladder)==4 and len(set(ladder))==4,'Collapsed ladder')
        ladders.add(ladder);rows.add(ladder);rows.add(tuple(sorted(-x for x in ladder)))
    five=set()
    for step in range(1,q):
        for start in range(q):
            values=tuple((start+j*step)%q for j in range(5))
            if any(x in holes for x in values):continue
            five.add(tuple(sorted(values)))
    for support in five:
        root_five=support[0]
        rows.add(tuple(sorted(index[(root_five,x)] for x in support[1:])))
    actual=parse(path,len(pairs));need(actual==rows,'Exact literal cycle/ladders/no-five model mismatch')
    need(all(len(row) in (3,4) for row in actual),'Unexpected seed, anchor or counter restriction')
    return {'q':q,'lambda':lam,'holes':list(holes),'regular_columns':list(outside),'root':root,
            'variables':len(pairs),'root_cycle_clauses':cycle_count,'seven_ladders':len(ladders),
            'no_five_supports':len(five),'clauses':len(rows),'counter_variables':0,
            'all_actual_cyclic_pairs_checked':length*(length-1),'pairs_skipped_meeting_holes':skipped,
            'pairs_retained_outside_holes':retained,'tautological_retained_pairs':tautologies,
            'actual_field_five_pairs_checked':q*(q-1),'literal_seven_orientation_groups_checked':len(groups),
            'orientation_anchor':'u(root)=0 only in decoding; no unit clause',
            'hypothesis':'no monochromatic five-term field AP avoiding holes',
            'cnf_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'seconds':time.monotonic()-begin}

def literal(q,lam,bits):
    holes,outside,_,_=parameters(q,lam);need(len(bits)==len(outside) and all(x in (0,1) for x in bits),'Bad decoded orientations')
    u=dict(zip(outside,bits));length=6*q
    colors=[None if t%q in holes else u[t%q]^int(t%6>=3) for t in range(length)]
    checked=skipped=0
    for step in range(1,length):
        for start in range(length):
            values=[colors[(start+j*step)%length] for j in range(7)]
            if None in values:skipped+=1;continue
            checked+=1
            if all(x==values[0] for x in values):return False,{'failure':'cyclic seven AP','start':start,'step':step}
    for step in range(1,q):
        for start in range(q):
            points=[(start+j*step)%q for j in range(5)]
            if any(x in holes for x in points):continue
            if len({u[x] for x in points})==1:return False,{'failure':'monochromatic field five AP','start':start,'step':step}
    return True,{'outside_seven_pairs_checked':checked,'seven_pairs_skipped':skipped,'all_field_five_pairs_checked':q*(q-1)}

def small(path,q,lam):
    need(q<=13,'Exhaustive controls restricted to q<=13')
    _,outside,pairs,_=parameters(q,lam);rows=parse(path,len(pairs));accepted=[];inputs=0
    for tail in itertools.product((0,1),repeat=len(outside)-1):
        bits=(0,)+tail;u=dict(zip(outside,bits));parities=[u[x]^u[y] for x,y in pairs]
        cnf=all(any(parities[abs(v)-1]==int(v>0) for v in row) for row in rows)
        valid,_=literal(q,lam,bits);need(cnf==valid,'Small pair-projection/literal hypothesis mismatch')
        if valid:accepted.append(''.join(map(str,bits)))
        inputs+=1
    return {'q':q,'lambda':lam,'normalized_inputs':inputs,'valid_count':len(accepted),'positive_fixtures':accepted[:3],
            'all_valid_orientations_sha256':hashlib.sha256(('\n'.join(accepted)+'\n').encode()).hexdigest()}

def witness(path,q,lam):
    holes,outside,pairs,index=parameters(q,lam);entries=json.loads(path.read_text())
    need(isinstance(entries,list) and len(entries)==len(pairs) and all(type(x) is int and x!=0 for x in entries),'Malformed pair assignment')
    values={abs(x):int(x>0) for x in entries};need(set(values)==set(range(1,len(pairs)+1)),'Missing/duplicate pair variables')
    u={outside[0]:0}
    for x in outside[1:]:u[x]=values[index[(outside[0],x)]]
    need(all(values[index[(x,y)]]==u[x]^u[y] for x,y in pairs),'Inconsistent pair cycle')
    bits=tuple(u[x] for x in outside);valid,counts=literal(q,lam,bits);need(valid,'Literal partial witness failure: '+str(counts))
    return {'q':q,'lambda':lam,'holes':list(holes),'regular_columns':list(outside),'orientation':''.join(map(str,bits)),
            'outside_hole_AP_free':True,'no_mono_field_five':True,'full_coloring_AP_free':False,**counts}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('path',type=Path);p.add_argument('--q',type=int,default=103)
    p.add_argument('--lambda',dest='lam',type=int,required=True);g=p.add_mutually_exclusive_group()
    g.add_argument('--small',action='store_true');g.add_argument('--witness',action='store_true')
    a=p.parse_args();f=small if a.small else witness if a.witness else audit;print(json.dumps(f(a.path,a.q,a.lam)))
