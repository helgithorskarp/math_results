#!/usr/bin/env python3
"""Complete real-shear exclusion: event regeneration, peeling, physical audit."""
import argparse,importlib.util,json,subprocess
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from math import lcm
from pathlib import Path
from model import HERE,REPO,Z,points,inventory,peel,flat_mul,phase_bytes,require

def literal_coordinates(P,t):
    q=lcm(*(F(x).denominator for x in t));a=tuple(int(F(x)*q)for x in t)
    out=[]
    for x,y in P:
        ty=flat_mul(a,y)
        out.append(tuple(q*u+v for u,v in zip(x,ty,strict=True))+tuple(q*v for v in y))
    den=288*q
    require(len(set(out))==len(P),'shear collision')
    require(den<2**50 and all(abs(v)<2**50 for p in out for v in p),'audit integer bounds')
    return den,out

def write_case(f,P,t,E):
    den,Q=literal_coordinates(P,t)
    f.write(f'{len(P)} {len(E)} {den}\n')
    for p in Q:f.write(' '.join(map(str,p))+'\n')
    for a,b in E:f.write(f'{a} {b}\n')
    return max(abs(v).bit_length()for p in Q for v in p),den.bit_length()

def verify(audit_binary,work):
    work.mkdir(parents=True,exist_ok=True)
    P,labels=points();fixed,events,facts,ys=inventory(P)
    require(Z in events and len(events[Z])==2648,'zero event')
    generic_degree,generic_word=peel(len(P),fixed)
    require(generic_degree<=1,'generic horizontal forest')
    degrees=Counter();edge_counts=Counter();words=[]
    for t,E in events.items():
        if t==Z:continue
        d,w=peel(len(P),E);require(d<=3,('unresolved event',t,d))
        require(set(w)<=set('0123'),'colour domain')
        degrees[d]+=1;edge_counts[len(E)]+=1;words.append(w)
    # This imports positive predecessor verification, not an UNSAT verdict.
    spec=importlib.util.spec_from_file_location('point606_positive',REPO/'hadwiger_nelson_point606_criticality_gate/verify.py')
    parent=importlib.util.module_from_spec(spec);spec.loader.exec_module(parent)
    old_facts,_,_=parent.compute()
    require(old_facts['point_sha256']==sha256(json.dumps(P,separators=(',',':')).encode()).hexdigest(),'same frozen core')
    require(old_facts['all_vertex_deletions_four_colourable'] and old_facts['checked_vertex_deletion_words']==530,'zero coverage')
    require(old_facts['edge_sha256']==sha256(''.join(f'{labels[i]},{labels[j]}\n'for i,j in events[Z]).encode()).hexdigest(),'same zero graph')
    # Rational t=1 represents the generic field case, checked against all roots.
    one=(F(1),)+Z[1:];require(one not in events,'generic audit parameter')
    stream=work/'physical-audit.txt';num_bits=den_bits=0
    with stream.open('w')as f:
        f.write(f'{len(events)+1}\n')
        for t,E in list(events.items())+[(one,fixed)]:
            a,b=write_case(f,P,t,E);num_bits=max(num_bits,a);den_bits=max(den_bits,b)
    with stream.open('rb')as f:
        r=subprocess.run([str(audit_binary.resolve())],stdin=f,capture_output=True,text=True)
    require(r.returncode==0,('physical audit',r.stderr))
    audit=json.loads(r.stdout)
    expected=dict(cases=len(events)+1,pairs=(len(events)+1)*len(P)*(len(P)-1)//2,
                  unit_edges=sum(map(len,events.values()))+len(fixed),status='ALL_PHYSICAL_PAIRS_MATCH')
    require(audit==expected,'audit totals')
    facts.update(points=len(P),zero_edges=len(events[Z]),nonzero_events=len(events)-1,
        nonzero_degeneracy_histogram=dict(sorted(degrees.items())),
        nonzero_edge_min=min(edge_counts),nonzero_edge_max=max(edge_counts),
        generic_degeneracy=generic_degree,zero_deletion_words_checked=530,
        zero_deletion_edge_checks=old_facts['deletion_word_edge_checks'],
        phase_sha256=sha256(phase_bytes(events)).hexdigest(),
        greedy_words_sha256=sha256(('\n'.join(words)+'\n').encode()).hexdigest(),
        max_coordinate_numerator_bits=num_bits,max_coordinate_denominator_bits=den_bits,
        physical_audit=audit,all_at_most_508_supports_four_colourable=True,
        record_candidate=False,non_four_proof_needed=False,
        status='COMPLETE_REAL_SHEAR_CLASS_EXCLUDED')
    return facts

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--audit-binary',required=True,type=Path);ap.add_argument('--work',required=True,type=Path)
    args=ap.parse_args();print(json.dumps(verify(args.audit_binary,args.work),indent=2,sort_keys=True))
