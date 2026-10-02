#!/usr/bin/env python3
"""Independent literal full-cyclic audit, small positives, and witness decoding."""
import argparse
import hashlib
import itertools
import json
import math
import time
from pathlib import Path

def need(condition,message):
    if not condition:raise ValueError(message)

def parameters(q,case):
    need(q>=7 and all(q%d for d in range(2,math.isqrt(q)+1)),'Prime q>=7 required')
    need(1<=case<=3,'Invalid case')
    if q==103:
        # Deliberately separate core construction from the proposer.
        hole_lists={1:(5,53,101),2:(5,53,102),3:(5,54,101)}
        holes=hole_lists[case]
        local=(0,1,2,3,4,5,6,52,53,54,55,101,102)
        seed=tuple(x for x in local if x not in holes)
    else:
        need(q in (7,11,13),'Small control prime required')
        holes=(0,1,case+1)
        seed=tuple(x for x in range(q) if x not in holes)[:3]
    outside=tuple(x for x in range(q) if x not in holes)
    pairs=tuple(itertools.combinations(outside,2));index={pair:i+1 for i,pair in enumerate(pairs)}
    need(outside[0] in seed and set(seed)<=set(outside),'Root absent from core')
    return holes,seed,outside,pairs,index

def parse(path,n):
    lines=path.read_text().splitlines();need(bool(lines),'Empty DIMACS')
    header=lines[0].split();need(len(header)==4 and header[:2]==['p','cnf'] and int(header[2])==n,'Bad variable domain')
    rows=[]
    for line in lines[1:]:
        entries=list(map(int,line.split()));need(entries and entries[-1]==0,'Missing clause terminator')
        row=tuple(sorted(entries[:-1]));need(all(0<abs(x)<=n for x in row),'Out-of-domain literal')
        need(len(row)==len(set(row)) and not any(-x in row for x in row),'Repeated/tautological literal')
        rows.append(row)
    need(len(rows)==int(header[3]) and len(rows)==len(set(rows)),'Clause count/duplicate mismatch')
    return set(rows)

def audit(path,q,case):
    begin=time.monotonic();holes,seed,outside,pairs,index=parameters(q,case);root=outside[0];length=6*q;rows=set()
    for first,second in itertools.combinations(outside[1:],2):
        ids=(index[(root,first)],index[(root,second)],index[(first,second)])
        for bits in itertools.product((0,1),repeat=3):
            if sum(bits)%2:rows.add(tuple(sorted(v if b==0 else -v for v,b in zip(ids,bits))))
    cycle_count=len(rows);groups={};skipped=tautologies=retained=0
    for step in range(1,length):
        for start in range(length):
            residues=tuple((start+j*step)%length for j in range(7));fields=tuple(t%q for t in residues)
            if any(x in holes for x in fields):skipped+=1;continue
            retained+=1;pattern=tuple(int(t%6>=3) for t in residues)
            if len(set(fields))==1:
                need(len(set(pattern))==2,'Unexpected same-column monochromatic row');tautologies+=1;continue
            need(len(set(fields))==7,'Repeated nonzero-slope field point')
            if fields[::-1]<fields:fields=fields[::-1];pattern=pattern[::-1]
            words=groups.setdefault(fields,set());words.add(pattern);words.add(tuple(1-x for x in pattern))
    local_bad=set()
    for word in itertools.product((0,1),repeat=7):
        ladder=[word[j]^word[j+3] for j in range(4)]
        if all(x==ladder[0] for x in ladder):local_bad.add(word)
    need(len(local_bad)==16,'Wrong local parity truth relation')
    ladders=set()
    for fields,patterns in groups.items():
        need(patterns==local_bad,'Literal cyclic blocked words differ from ladder')
        row=tuple(sorted(index[tuple(sorted((fields[j],fields[j+3])))] for j in range(4)))
        need(len(row)==len(set(row))==4,'Collapsed ladder')
        ladders.add(row);rows.add(row);rows.add(tuple(sorted(-x for x in row)))
    units={(-index[(root,x)],) for x in seed if x!=root};rows.update(units)
    actual=parse(path,len(pairs));need(actual==rows,'Full literal cycle/ladder/seed model mismatch')
    need(all(len(row) in (1,3,4) for row in rows),'Unexpected AP ascent or counter restriction')
    return {'q':q,'case':case,'holes':list(holes),'seed':list(seed),'regular_columns':list(outside),'root':root,
            'variables':len(pairs),'root_cycle_clauses':cycle_count,'seven_ladders':len(ladders),'seed_units':len(units),
            'clauses':len(rows),'counter_variables':0,'weight_cap':None,
            'all_actual_cyclic_pairs_checked':length*(length-1),'pairs_skipped_meeting_holes':skipped,
            'pairs_retained_outside_holes':retained,'tautological_retained_pairs':tautologies,
            'literal_seven_orientation_groups_checked':len(groups),
            'hypothesis':'all regular local-core field points have the five-AP seed color',
            'orientation_anchor':'u(root)=0 by global color exchange',
            'cnf_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'seconds':time.monotonic()-begin}

def literal(q,case,bits):
    holes,seed,outside,_,_=parameters(q,case)
    need(len(bits)==len(outside) and all(x in (0,1) for x in bits),'Bad orientations')
    u=dict(zip(outside,bits))
    if any(u[x] for x in seed):return False,{'failure':'Seed color mismatch'}
    length=6*q;colors=[None if t%q in holes else u[t%q]^int(t%6>=3) for t in range(length)];checked=skipped=0
    for step in range(1,length):
        for start in range(length):
            values=[colors[(start+j*step)%length] for j in range(7)]
            if None in values:skipped+=1;continue
            checked+=1
            if all(x==values[0] for x in values):return False,{'failure':'Cyclic seven AP','start':start,'step':step}
    return True,{'outside_seven_pairs_checked':checked,'seven_pairs_skipped':skipped}

def small(path,q,case):
    need(q<=13,'Small control prime required');_,_,outside,pairs,_=parameters(q,case);rows=parse(path,len(pairs));accepted=[];inputs=0
    for tail in itertools.product((0,1),repeat=len(outside)-1):
        bits=(0,)+tail;u=dict(zip(outside,bits));parities=[u[x]^u[y] for x,y in pairs]
        cnf=all(any(parities[abs(v)-1]==int(v>0) for v in row) for row in rows)
        valid,_=literal(q,case,bits);need(cnf==valid,'Small model/literal seed hypothesis mismatch')
        if valid:accepted.append(''.join(map(str,bits)))
        inputs+=1
    return {'q':q,'case':case,'normalized_inputs':inputs,'valid_count':len(accepted),'positive_fixtures':accepted[:3],
            'all_valid_orientations_sha256':hashlib.sha256(('\n'.join(accepted)+'\n').encode()).hexdigest()}

def witness(path,q,case):
    holes,seed,outside,pairs,index=parameters(q,case);entries=json.loads(path.read_text())
    need(isinstance(entries,list) and len(entries)==len(pairs) and all(type(x) is int and x!=0 for x in entries),'Bad pair assignment')
    values={abs(x):int(x>0) for x in entries};need(set(values)==set(range(1,len(pairs)+1)),'Missing/duplicate pair variables')
    u={outside[0]:0}
    for x in outside[1:]:u[x]=values[index[(outside[0],x)]]
    need(all(values[index[(x,y)]]==u[x]^u[y] for x,y in pairs),'Inconsistent pair cycle')
    valid,counts=literal(q,case,tuple(u[x] for x in outside));need(valid,'Literal partial-witness failure: '+str(counts))
    return {'q':q,'case':case,'holes':list(holes),'seed':list(seed),'regular_columns':list(outside),
            'orientation':''.join(str(u[x]) for x in outside),'outside_hole_AP_free':True,
            'local_core_has_one_color':True,'full_coloring_AP_free':False,**counts}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('path',type=Path);p.add_argument('--q',type=int,default=103)
    p.add_argument('--case',type=int,required=True);g=p.add_mutually_exclusive_group();g.add_argument('--small',action='store_true');g.add_argument('--witness',action='store_true')
    a=p.parse_args();f=small if a.small else witness if a.witness else audit;print(json.dumps(f(a.path,a.q,a.case)))
