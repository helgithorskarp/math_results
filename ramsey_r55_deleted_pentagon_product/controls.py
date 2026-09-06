#!/usr/bin/env python3
"""Finite controls and physical decoder tests; no exhaustive43-graph claim."""
from collections import Counter
from copy import deepcopy
from itertools import combinations
from pathlib import Path
import json,random
import check,derive,extract,verify

ROOT=Path(__file__).resolve().parent

def need(ok,msg):
    if not ok:raise ValueError(msg)


def graph(seed,admissible,orientation=1):
    rng=random.Random(seed);cert,stars=derive.derive();choices=sorted(stars)
    red={tuple(e) for e in cert['core_red_edges']}
    for v in range(24,43):
        mask=rng.choice(choices) if admissible else rng.getrandbits(24)
        red.update((u,v) for u in range(24) if mask>>u&1)
    red.update((u,v) for u,v in combinations(range(24,43),2) if rng.getrandbits(1))
    labels=list(range(43));rng.shuffle(labels)
    if orientation==0:red=set(combinations(range(43),2))-red
    return {'n':43,'core_embedding':labels[:24],'core_color':orientation,
            'red_edges':sorted([list(sorted((labels[u],labels[v]))) for u,v in red])}


def main():
    cert=json.loads((ROOT/'certificate.json').read_text());check.verify(cert)
    rng=random.Random(24043);dpll=0
    for n in range(8):
        for _ in range(64):
            clauses=[]
            for __ in range(rng.randrange(17)):
                pos=neg=0
                for v in range(n):
                    value=rng.randrange(3)
                    if value==1:pos|=1<<v
                    elif value==2:neg|=1<<v
                clauses.append((pos,neg))
            got,_=check.model_set(n,clauses)
            truth={m for m in range(1<<n) if all(pos&m or neg&~m for pos,neg in clauses)}
            need(got==truth,'complete DPLL versus all assignments');dpll+=1
    counts=Counter();fixtures=[]
    for admissible in (False,True):
        for orientation in (0,1):
            for seed in range(16):
                g=graph(seed+240430,admissible,orientation);w=extract.extract(g)
                answer=verify.verify(g,w);counts[answer['mechanism']]+=1
                if seed==0:fixtures.append({'graph':g,'certificate':w,'verified':answer})
    # Save no new state in controls: fixtures are regenerated for byte comparison.
    expected=json.loads((ROOT/'fixtures.json').read_text())
    need(expected==fixtures,'fixture reproduction')
    mutations=0
    for alter in (lambda c:c['core_red_edges'].pop(),lambda c:c.update(complete_star_count=14640),
                  lambda c:c.update(forced_red=[20,22]),lambda c:c.update(feasible_positive_weight_words=[])):
        bad=deepcopy(cert);alter(bad)
        try:check.verify(bad)
        except (ValueError,KeyError):mutations+=1
        else:raise ValueError('bad kernel certificate accepted')
    sample=fixtures[0];bad_witnesses=[]
    bad=deepcopy(sample['certificate']);bad['color']=1-bad['color'];bad_witnesses.append(bad)
    bad=deepcopy(sample['certificate']);bad['five'][1]=bad['five'][0];bad_witnesses.append(bad)
    bad=deepcopy(sample['certificate']);bad['five'][0]=43;bad_witnesses.append(bad)
    bad=deepcopy(sample['certificate']);bad['mechanism']='wrong';bad_witnesses.append(bad)
    for bad in bad_witnesses:
        try:verify.verify(sample['graph'],bad)
        except ValueError:mutations+=1
        else:raise ValueError('bad physical certificate accepted')
    malformed=[]
    for f in (lambda g:g.update(n=42),lambda g:g['core_embedding'].__setitem__(1,g['core_embedding'][0]),
              lambda g:g.update(core_color=True),lambda g:g['red_edges'].append(g['red_edges'][0]),
              lambda g:g['red_edges'].append([0,43]),lambda g:g['red_edges'].append([1,0]),
              lambda g:g['red_edges'].append([0,0]),lambda g:g['core_embedding'].__setitem__(0,True)):
        bad=deepcopy(sample['graph']);f(bad);malformed.append(bad)
    for bad in malformed:
        for fn in (extract.extract,lambda g:verify.verify(g,sample['certificate'])):
            try:fn(bad)
            except ValueError:pass
            else:raise ValueError('malformed graph accepted')
    return {'status':'VERIFIED_H24_GLOBAL_FAMILY_CONTROLS','dpll_complete_truth_comparisons':dpll,
            'physical43_graphs':sum(counts.values()),'decoder_mechanisms':dict(sorted(counts.items())),
            'certificate_mutations_rejected':mutations,'malformed_graphs_rejected_by_both':len(malformed),
            'fixture_count':len(fixtures)}

if __name__=='__main__':print(json.dumps(main(),indent=2))
