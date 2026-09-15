#!/usr/bin/env python3
"""Independent small-domain oracle and semantic corruption controls."""
from itertools import combinations, product
from pathlib import Path
import copy, json
import verify as v

def main():
    c=json.loads((v.BASE/'certificate.json').read_text())
    expected=json.loads((v.BASE/'EXPECTED.json').read_text())
    v.need(v.verify(c)==expected,'valid baseline must pass')
    pairs=list(combinations(range(4),2));cases=0
    for flags in range(64):
        edges=[e for i,e in enumerate(pairs) if (flags>>i)&1]
        adj=[set() for _ in range(4)]
        for a,b in edges:adj[a].add(b);adj[b].add(a)
        for domains in product((1,3,7),repeat=4):
            brute=next((w for w in product(range(3),repeat=4) if
                        all(domains[i]&(1<<w[i]) for i in range(4)) and
                        all(w[a]!=w[b] for a,b in edges)),None)
            checked=v.extension(adj,domains)
            v.need((brute is None)==(checked is None),'complete-search/brute-force comparison')
            if checked is not None:
                v.need(all(domains[i]&(1<<checked[i]) for i in range(4)) and
                       all(checked[a]!=checked[b] for a,b in edges),'decoded small oracle word')
            cases+=1
    rejected=[]
    mutants=[]
    def changed(name,key,value):
        x=copy.deepcopy(c);x[key]=value;mutants.append((name,x))
    changed('coordinate scale','field_scale',12)
    w=list(c['proper_four_word']);w[29]=w[0]
    changed('violated private unit contact','proper_four_word',''.join(w))
    w=list(c['forbidden_joint_terminal_word']);w[-1]='3'
    changed('altered forbidden terminal prescription','forbidden_joint_terminal_word',''.join(w))
    w=list(c['proper_five_word_for_forbidden_terminals']);w[30]='2'
    changed('proper five-word with different marked terminals','proper_five_word_for_forbidden_terminals',''.join(w))
    for name,x in mutants:
        try:v.verify(x)
        except ValueError:rejected.append(name)
        else:raise ValueError('corruption accepted: '+name)
    print(json.dumps({'valid_baseline_passed':True,'domain_oracle_cases':cases,'semantic_corruptions_rejected':rejected},indent=2))
if __name__=='__main__':main()
