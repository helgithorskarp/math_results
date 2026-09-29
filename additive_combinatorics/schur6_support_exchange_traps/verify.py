"""Standard-library witness and CNF auditor, importing no search/encoder code."""
import argparse
from collections import Counter
import hashlib
from itertools import combinations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent


def read_word(name):
    text=(ROOT/(name+'.txt')).read_text().strip()
    assert len(text)==537 and set(text)<=set('0123456')
    return list(map(int,text))


def bad(word):
    return [(a,b,a+b) for a in range(1,538) for b in range(a,538-a)
            if word[a-1] and word[a-1]==word[b-1]==word[a+b-1]]


def check_exchange(old,new):
    for a,b in zip(old,new):
        if a==0:assert b>0
        elif a!=6:assert b in [0,a,6]
    assert new.count(0)<=1 and not bad(new)


def audit_cnf(path,word,excluded,expected):
    raw=path.read_bytes();assert hashlib.sha256(raw).hexdigest()==expected['cnf_sha256']
    actual=Counter();header=None
    for line in raw.decode().splitlines():
        if not line or line.startswith('c'):continue
        if line.startswith('p '):header=tuple(map(int,line.split()[2:]));continue
        values=list(map(int,line.split()));assert values.pop()==0
        actual[tuple(sorted(values))]+=1
    number={};choices={};top=0
    # Derive all allowed states directly from the point operation.
    for x,c in enumerate(word,1):
        choices[x]=[]
        for d in range(7):
            if (d==0 and c!=0) or (d>0 and (c in [0,6] or d in [c,6])):
                top+=1;number[x,d]=top;choices[x].append(d)
    wanted=Counter()
    def clause(values):wanted[tuple(sorted(values))]+=1
    for x,ds in choices.items():
        clause([number[x,d] for d in ds])
        for c,d in combinations(ds,2):clause([-number[x,c],-number[x,d]])
    for a in range(1,538):
        for b in range(a,538-a):
            for c in range(1,7):
                if (a,c) in number and (b,c) in number and (a+b,c) in number:
                    clause({-number[a,c],-number[b,c],-number[a+b,c]})
    for a,b in combinations(range(1,538),2):
        if (a,0) in number and (b,0) in number:clause([-number[a,0],-number[b,0]])
    clause([-number[excluded,0]])
    assert actual==wanted
    assert header==(top,sum(wanted.values()))==(expected['variables'],expected['clauses'])


def main():
    p=argparse.ArgumentParser();p.add_argument('--cnfs',type=Path)
    args=p.parse_args();expected=json.loads((ROOT/'expected.json').read_text())
    words={name:read_word(name) for name in ['initial','traded','initial_exchange','traded_exchange']}
    hole_expected={'initial':322,'traded':161,'initial_exchange':161,'traded_exchange':322}
    rows=[];total_rows=sum(538-2*a for a in range(1,269))
    assert total_rows==72092
    for name,w in words.items():
        holes=[i for i,c in enumerate(w,1) if c==0]
        assert holes==[hole_expected[name]] and not bad(w)
        rows.append({'word':name,'hole':holes[0],'equations':72092,'doublings':268,
                     'assigned_points':536,'sha256':hashlib.sha256((''.join(map(str,w))+'\n').encode()).hexdigest()})
    check_exchange(words['initial'],words['initial_exchange'])
    check_exchange(words['traded'],words['traded_exchange'])
    filled=words['traded'][:];filled[160]=6
    assert bad(filled)==[(161,161,322),(161,322,483)]
    initial_score=[]
    for c in range(1,7):
        filled=words['initial'][:];filled[321]=c;initial_score.append(len(bad(filled)))
    assert initial_score==[32,35,29,26,38,19]
    if args.cnfs:
        for name,excluded in [('initial',161),('traded',322)]:
            audit_cnf(args.cnfs/(name+'.cnf'),words[name],excluded,expected[name])
    print(json.dumps({'status':'PASS','partial_words':rows,'initial_fill_defects':initial_score,
                      'traded_colour6_defects':[[161,161,322],[161,322,483]],
                      'positive_exchange_controls':2,'cnfs_audited':2 if args.cnfs else 0},indent=2))


if __name__=='__main__':main()
