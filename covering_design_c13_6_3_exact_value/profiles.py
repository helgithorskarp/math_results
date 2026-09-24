"""Uniform excess decorations for degree twelve or degrees eleven and ten."""
from collections import Counter
from math import factorial
import primary_model as balanced
import audit_model as audit_balanced
from catalogue import CAT,point_automorphisms
from row_maps import columns
DEGREES={}
def decorations(profile):
    if profile=='twelve':return {((h,3),) for h in range(12)}
    if profile=='eleven':return {tuple(sorted(((h,2),(q,1)))) for h in range(12) for q in range(12) if h!=q}
    raise ValueError('unknown profile')

def prepare(profile,method):
    roots=[]
    for d in CAT:
        left=decorations(profile)
        actions=point_automorphisms(d) if method=='primary' else None
        while left:
            extra=min(left)
            if actions is None:left.remove(extra)
            else:left-={tuple(sorted((a[p],e) for p,e in extra)) for a in actions}
            high=tuple(p for p,e in extra)
            def score(r):
                through=[b&~(1<<r) for b in d['blocks'] if b>>r&1]
                if method=='audit':return (len(through),-r)
                cells=Counter(columns(through,[p for p in range(12) if p!=r]))
                free=1
                for n in cells.values():free*=factorial(n)
                return (len(through),-free,-r)
            r=max((p for p in range(12) if p not in high),key=score)
            k=d['point_signatures'][r].bit_count();assert k in (4,5)
            roots.append(dict(id=len(roots),design=d['id'],high=high,extra=extra,r=r,k=k))
    return roots

def join(root,templates,method):
    high=set(root['high']);target=[9]*13
    for p,e in root['extra']:target[p]+=e
    if method=='primary':
        records,raw,unique=balanced.uncoloured(root['design'],root['r'],templates)
        # Cache only within one first-link design.
        if DEGREES.get('design')!=root['design']:DEGREES.clear();DEGREES['design']=root['design']
        answers=[]
        for union,second,mandatory,forbidden in records:
            if second>root['design'] or mandatory&~sum(1<<p for p in high):continue
            if union not in DEGREES:DEGREES[union]=tuple(sum(b>>p&1 for b in union) for p in range(13))
            degree=DEGREES[union]
            if any(not 0<=target[p]-degree[p]<=20-len(union) for p in range(13)):continue
            answers.append(union)
    else:
        records,raw=audit_balanced.uncoloured(root['design'],root['r'],templates)
        answers=[]
        for union,second,degree,heavy in records:
            if second>root['design']:continue
            if any(not 0<=target[p]-degree[p]<=20-len(union) for p in range(13)):continue
            if any(not set(t)<=high for t in heavy):continue
            answers.append(union)
    return answers,target,raw
