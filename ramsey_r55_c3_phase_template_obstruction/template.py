"""A single deterministic degree-preserving quotient trade."""
from itertools import combinations,product
from collections import Counter
from pathlib import Path
import json
import physical as p

def fixed_rows(counts,hub,color):
    rows=[0]*43
    for u,v in combinations(range(43),2):
        if v==42: val=hub[u//3]
        elif u//3==v//3: val=int(u<21)
        else:
            n=counts[u//3,v//3]
            val=0 if n==0 else 1 if n==3 else None
        if val==color: rows[u]|=1<<v;rows[v]|=1<<u
    return rows

def main():
    a=p.read_graph(Path(__file__).with_name('baseline.edges'));word=p.family(a)
    pairs=list(combinations(range(14),2));index={q:i for i,q in enumerate(pairs)}
    counts={q:word[3*i:3*i+3].count('1') for q,i in index.items()}
    hub=list(map(int,word[273:]))
    forced=[[list(q) for q in p.cliques(fixed_rows(counts,hub,c),5)] for c in (0,1)]
    # The first lexicographic feasible 4-cycle count trade with no fixed K5.
    attempts=[];chosen=None
    for k in range(14):
      for l in range(14):
        if len({2,10,k,l})<4:continue
        signed=[(tuple(sorted(q)),sgn) for q,sgn in [((2,10),1),((k,l),1),((2,k),-1),((10,l),-1)]]
        nxt=counts.copy()
        for q,s in signed:nxt[q]+=s
        if any(n<0 or n>3 for n in nxt.values()):continue
        defects=[len(list(p.cliques(fixed_rows(nxt,hub,c),5))) for c in (0,1)]
        attempts.append({'k':k,'l':l,'fixed_blue_red':defects})
        if not any(defects):chosen=(k,l,signed,nxt);break
      if chosen:break
    p.need(chosen is not None,'no admissible trade')
    k,l,signed,nxt=chosen
    # Among the phase choices for the four single-bit count changes, choose
    # the lexicographically first minimum of the actual full graph objective.
    choices=[]
    for q,s in signed:
        v=3*index[q]
        choices.append([v+t for t in range(3) if int(word[v+t])==(0 if s==1 else 1)])
    evaluated=[];best=None
    for flips in product(*choices):
        w=list(word)
        for v in flips:w[v]='1' if w[v]=='0' else '0'
        w=''.join(w);rows=p.decode(w)
        ds=p.recursive_defects(rows);score=sum(map(len,ds))
        evaluated.append({'flips':list(flips),'score':score})
        if best is None or score<best[0]:best=(score,w,rows)
    score,w,rows=best
    p.need([x.bit_count() for x in a]==[x.bit_count() for x in rows],'degree trade')
    out=Path(__file__).parent
    (out/'traded.edges').write_bytes(p.edge_bytes(rows))
    report={'parent_blue_red':list(map(len,p.recursive_defects(a))),'degree_histogram':dict(sorted(Counter(x.bit_count() for x in a).items())),
      'W':sum(3*(x.bit_count()-21)**2 for x in a),'parent_fixed_blue_red':forced,'attempts':attempts,
      'chosen_k_l':[k,l],'count_trade':[{'pair':list(q),'delta':s} for q,s in signed],
      'parent_mixed_pairs':sum(0<n<3 for n in counts.values()),'traded_mixed_pairs':sum(0<n<3 for n in nxt.values()),
      'phase_initializations':evaluated,'selected_score':score,'selected_bits':w,
      'parent_counts':[counts[q] for q in pairs],'traded_counts':[nxt[q] for q in pairs],
      'hub':hub,'degree_preserved_per_label':True,'no_frozen_five_set':True}
    (out/'template.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('phase_initializations','selected_bits','parent_counts','traded_counts')},indent=2))
if __name__=='__main__':main()
