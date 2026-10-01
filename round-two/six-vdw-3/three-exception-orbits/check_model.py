#!/usr/bin/env python3
"""Independent literal full-cyclic reconstruction, without generator imports."""
import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

def need(condition,message):
    if not condition:raise ValueError(message)

def parse(path,q):
    rows=path.read_text().splitlines();header=rows[0].split()
    need(header[:2]==['p','cnf'] and len(header)==4 and int(header[2])==q,'Bad DIMACS header')
    clauses=[]
    for row in rows[1:]:
        entries=list(map(int,row.split()))
        need(entries and entries[-1]==0 and all(0<abs(x)<=q for x in entries[:-1]),'Bad literal or terminator')
        clause=tuple(sorted(entries[:-1]));need(len(set(clause))==len(clause),'Repeated literal')
        clauses.append(clause)
    need(len(clauses)==int(header[3]) and len(clauses)==len(set(clauses)),'Count or duplicate clause error')
    return set(clauses)

def audit(path,q,kind,lam):
    begin=time.monotonic()
    need(q>=7 and kind in ('same','mixed') and 1<lam<q,'Bad model parameters')
    length=6*q;offset=[0]*q;offset[0]=offset[1]=1;offset[lam]=1 if kind=='same' else 2
    # Every actual cyclic start and nonzero step is reconstructed literally.
    # A repeated field coordinate can give a tautology; these are omitted only
    # after checking both opposite literals are present.
    clauses={(-1,)};tautologies=0
    for step in range(1,length):
        for start in range(length):
            literals=set()
            for j in range(7):
                t=(start+j*step)%length;x=t%q;y=t%6
                bit=int((y-offset[x])%6>=3)
                literals.add((x+1) if bit==0 else -(x+1))
            if any(-literal in literals for literal in literals):
                tautologies+=1;continue
            clauses.add(tuple(sorted(literals)))
            clauses.add(tuple(sorted(-literal for literal in literals)))
    actual=parse(path,q)
    need(actual==clauses,'Full cyclic mathematical model differs from supplied CNF')
    need({c for c in actual if len(c)==1}=={(-1,)},'Orientation anchors narrowed')
    need(all(len(c) in (1,7) for c in actual),'Extra constraints or counters')
    return {'q':q,'kind':kind,'lambda':lam,'variables':q,'clauses':len(clauses),
            'all_actual_cyclic_pairs_checked':length*(length-1),'tautological_pairs':tautologies,
            'counter_variables':0,'weight_cap':None,'cnf_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'seconds':time.monotonic()-begin}

def small(path,q,kind,lam):
    clauses=parse(path,q);offset=[0]*q;offset[0]=offset[1]=1;offset[lam]=1 if kind=='same' else 2
    length=6*q;accepted=[];cases=0
    for bits in itertools.product((0,1),repeat=q-1):
        word=(0,)+bits
        satisfiable=all(any(word[abs(lit)-1]==int(lit>0) for lit in clause) for clause in clauses)
        coloring=[word[t%q]^int((t%6-offset[t%q])%6>=3) for t in range(length)]
        valid=True
        for step in range(1,length):
            for start in range(length):
                if len({coloring[(start+j*step)%length] for j in range(7)})==1:
                    valid=False;break
            if not valid:break
        need(satisfiable==valid,'Small literal word/CNF mismatch')
        if valid:accepted.append(''.join(map(str,word)))
        cases+=1
    return {'q':q,'kind':kind,'lambda':lam,'normalized_inputs':cases,'valid_count':len(accepted),
            'valid_fixtures':accepted[:3],
            'all_valid_words_sha256':hashlib.sha256(('\n'.join(accepted)+'\n').encode()).hexdigest()}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('cnf',type=Path)
    parser.add_argument('--q',type=int,default=103);parser.add_argument('--kind',choices=('same','mixed'),required=True)
    parser.add_argument('--lambda',dest='lam',type=int,required=True);parser.add_argument('--small',action='store_true')
    args=parser.parse_args()
    print(json.dumps(small(args.cnf,args.q,args.kind,args.lam) if args.small else audit(args.cnf,args.q,args.kind,args.lam)))

if __name__=='__main__':main()
