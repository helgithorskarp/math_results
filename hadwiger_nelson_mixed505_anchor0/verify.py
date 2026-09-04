#!/usr/bin/env python3
"""Complete mixed 505-vertex census, fixing vertex 0 of the 214-point source."""

from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import permutations
import importlib.util
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
TRIPLE=HERE.parent/'hadwiger_nelson_nonmono159_moser_triple'
PATH=TRIPLE/'verify.py'
if sha256(PATH.read_bytes()).hexdigest()!='34d251f7e7c2a7d6c4542e260cbab6c9a390373f0eb7073800d70cdba6b271cb':
    raise ValueError('enumeration dependency mismatch')
spec=importlib.util.spec_from_file_location('triple_census',PATH)
T=importlib.util.module_from_spec(spec);spec.loader.exec_module(T)
K=T.K
require=T.require


def construction():
    _,B,_,EB=T.construction()
    raw=(HERE.parent/'hadwiger_nelson_nonmono159_214_lowden2/points214.tsv').read_bytes()
    require(sha256(raw).hexdigest()=='97c9b3a964ed19874ae3fe932eb8c085fd637f618d2481fffaebbd1fbae55c2f','coordinate mismatch')
    lines=raw.decode().splitlines()
    require(lines[0]=='# scale 12','wrong point scale')
    V=[]
    for line in lines:
        if not line or line.startswith('#'):continue
        a=tuple(map(int,line.split()))
        require(len(a)==16 and all(a[i]==0 for i in range(16) if i not in (0,5,9,12)),'point outside E')
        V.append(K.element(*(F(a[i],12) for i in (0,5,9,12))))
    q=V[0]
    require(q==K.element(1,F(-1,6),0,0),'wrong chosen anchor')
    H=[K.add(v,K.negate(q)) for v in V]
    require(len(H)==len(set(H))==214 and H[0]==K.ZERO,'bad centered gadget')
    labels={h:i for i,h in enumerate(H)}
    require(all(K.conjugate(h) in labels for h in H),'reflection changes the point set')
    reflection=[labels[K.conjugate(h)] for h in H]
    require(reflection[0]==0 and all(reflection[reflection[i]]==i for i in range(214)),'bad reflection involution')
    EH=T.C.internal_edges(H)
    require(len(EH)==977,'wrong 214-gadget edge count')
    return B,H,EB,EH,reflection


def main():
    B,H,EB,EH,reflection=construction()
    libB,hashB=T.read_library('colors_B.txt',B,EB)
    libH,hashH=T.read_library(HERE/'colors_H.txt',H,EH)
    require((len(libB),len(libH))==(3,2),'wrong library sizes')
    perms=[(0,)+p for p in permutations((1,2,3))]
    classification,partition,polynomial,coverage=(sha256() for _ in range(4))
    counts,groups=T.enumerate_classes(B,H,False,classification)
    for s in T.C.partition_text(False,groups):partition.update(s.encode())
    maximum=max(map(len,groups.values()))
    sample=None
    for (S,V),ee in sorted(groups.items()):
        key=[[str(x) for x in S],[str(x) for x in V]]
        polynomial.update((json.dumps([key,ee],separators=(',',':'))+'\n').encode())
        witness=next(((i,j,k) for i,cb in enumerate(libB) for j,ch in enumerate(libH)
                      for k,p in enumerate(perms) if all(cb[b]!=p[ch[h]] for b,h in ee)),None)
        require(witness is not None,'uncovered quadratic class')
        i,j,k=witness
        colors=libB[i]+tuple(perms[k][v] for v in libH[j][1:])
        require(len(colors)==505 and all(colors[b]!=colors[291+h] for b,h in ee),'bad union coloring')
        coverage.update((json.dumps([key,witness],separators=(',',':'))+'\n').encode())
        if sample is None and len(ee)==maximum:
            sample={'T':key[0],'V':key[1],'seed_pair':ee[0],'new_cross_edges':len(ee),
                    'witness':witness,'cross_edges':ee}
    result={'B_vertices':len(B),'B_edges':len(EB),'H_vertices':len(H),'H_edges':len(EH),
            'anchor':['1','-1/6','0','0'],'reflection_invariant':True,
            'reflection_sha256':sha256(json.dumps(reflection).encode()).hexdigest(),
            'union_vertices_outside_E':505,'internal_edges_outside_E':len(EB)+len(EH),
            **counts,'quadratic_classes':len(groups),'unit_multipliers':2*len(groups),
            'cross_edge_histogram':dict(sorted(Counter(map(len,groups.values())).items())),
            'uncovered_classes':0,'B_library_size':len(libB),'H_library_size':len(libH),
            'classification_sha256':classification.hexdigest(),'edge_partition_sha256':partition.hexdigest(),
            'polynomial_census_sha256':polynomial.hexdigest(),'coverage_sha256':coverage.hexdigest(),
            'B_library_sha256':hashB,'H_library_sha256':hashH,'max_contact_example':sample}
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
