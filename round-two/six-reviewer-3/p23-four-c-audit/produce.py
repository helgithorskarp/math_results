"""Independent labelled row-to-edge search; no campaign helper/fixture imports."""
import itertools, json, sys
from pathlib import Path
PAIRS=list(itertools.combinations(range(4),2))
def build(carrier):
    special=(0,1) if carrier=='A' else (1,2)
    lam=[3 if p==special else 4 for p in PAIRS]
    D=[70-4*r+sum(lam[e] for e,p in enumerate(PAIRS) if a in p)
       for a,r in enumerate([18,19,19,19])]
    return lam,D,[14-3*x for x in lam]
def configurations(n,m,lam,cap):
    rows=[a for a in range(4) for _ in range(m[a])]
    domains=[]
    for a in rows:
        allowed=[e for e,p in enumerate(PAIRS) if a in p and
                 not any(b!=a and b in p and b>0 and n[b]==2 and lam[e]==4
                         for b in range(4))]
        domains.append(list(itertools.combinations(allowed,max(0,8-n[a]))))
    def descend(k,left,word):
        if k==4:
            yield word
            return
        for star in domains[k]:
            if all(left[e]>0 for e in star):
                z=left[:]
                for e in star:z[e]-=1
                yield from descend(k+1,z,word+[list(star)])
    return descend(0,cap[:],[])
def admissible(n,m,D):
    for a in range(4):
        # A star at hub a has 17 vertices and total leave degree 56 or 44.
        low=14-n[a]; high=n[a]+3
        needed=(56 if a==0 else 44)-low
        if needed>high*(high-1)+low:return False
        if m[a]>n[a] or m[a]>D[a]-n[a] or m[a]>0 and n[a]<5:return False
    return True
def main(out):
    out.mkdir(parents=True,exist_ok=True)
    flags=bytearray();records=[];equal=[];count={}
    ms=[m for m in itertools.product(range(5),repeat=4) if sum(m)==4]
    for carrier in ['A','B']:
        lam,D,cap=build(carrier);total=0
        for n in itertools.product(*(range(d+1) for d in D)):
            for m in ms:
                total+=1;word=None
                if admissible(n,m,D):
                    word=next(configurations(n,m,lam,cap),None)
                flags.append(int(word is not None))
                if word is not None:
                    records.append({'carrier':carrier,'n':n,'m':m,'witness':word})
                    if sum(n)==17:
                        equal.append({'carrier':carrier,'n':n,'m':m,
                                      'all_stars':list(configurations(n,m,lam,cap))})
        count[carrier]=total
    (out/'flags.bin').write_bytes(flags)
    result={'cases':count,'records':records,'equality':equal}
    (out/'records.json').write_text(json.dumps(result,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({'cases':len(flags),'feasible':len(records),'minimum':min(sum(r['n']) for r in records),'equality':equal},sort_keys=True))
if __name__=='__main__':main(Path(sys.argv[1]))
