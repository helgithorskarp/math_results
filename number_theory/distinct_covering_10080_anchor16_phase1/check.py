"""Exact literal checks for one prescribed six-class minimum-eight period10080 family.

Actual author six-covering-2, researcher. Standard library only. No LP solver,
private forest, external data or status flag is a premise. The arithmetic
and explicit coordinate transport are the author's earlier literal checker,
ported to a small JSON tree; this is not independent peer review.
"""
import argparse
from collections import Counter, defaultdict
from functools import lru_cache
from hashlib import sha256
import json
from math import gcd, prod
from pathlib import Path
from time import monotonic

BASE=[(8,0),(9,0),(10,1),(14,1),(12,3)]


def need(condition, message):
    if not condition: raise ValueError(message)


def decode_tree(tree):
    phase=tree['phase']; root=tree['root_node']
    need(type(phase) is int and phase==1, 'Unknown prescribed case')
    need(type(root) is int and root>=0, 'Invalid root identifier')
    nodes=tree['nodes']; need(isinstance(nodes,list) and bool(nodes), 'Empty tree')
    identifiers=[n['id'] for n in nodes]
    need(all(type(i) is int and i>=0 for i in identifiers), 'Invalid node identifier')
    need(len(set(identifiers))==len(identifiers), 'Duplicate identifier')
    records={}
    for n in sorted(nodes,key=lambda x:x['id']):
        i=n['id']; parent=n['parent']; status=n['status']; payload=n['payload']
        need(status in ('expanded','uniform','weighted'), 'Unproved terminal status')
        need(isinstance(payload,dict), 'Malformed payload')
        if i==root:
            need(parent is None and n['addition'] is None, 'Invalid root edge')
            A=BASE+[(16,phase)]
        else:
            need(type(parent) is int and parent<i and parent in records, 'Orphan or cycle')
            addition=n['addition']
            need(isinstance(addition,list) and len(addition)==2 and
                 all(type(x) is int for x in addition), 'Invalid added class')
            A=records[parent][1]+[tuple(addition)]
        if status=='weighted':
            need(set(payload).issubset({'demand','capacity','boxes','pairs'}) and
                 {'demand','capacity','boxes'}.issubset(payload), 'Unsupported weighted format')
            need(isinstance(payload['boxes'],list), 'Malformed weight boxes')
            for pair in payload.get('pairs',[]):
                need(isinstance(pair,list) and len(pair)==2 and
                     all(type(m) is int for m in pair), 'Malformed paired resources')
        if status in ('weighted','uniform'):
            need(type(payload.get('demand')) is int and type(payload.get('capacity')) is int,
                 'Noninteger cut total')
        records[i]=(parent,A,status,payload)
    need(root in records, 'Missing root')
    return records

def factor(n):
    result=[]; p=2
    while p*p<=n:
        e=0
        while n%p==0: n//=p; e+=1
        if e: result.append((p,e))
        p+=1
    if n>1: result.append((n,1))
    return tuple(result)


def valuation(n,p):
    e=0
    while n%p==0: n//=p; e+=1
    return e


@lru_cache(None)
def coordinate_transport(p,P,q,source,target,anchor_coordinates):
    """Construct a tree automorphism, then verify its complete finite action."""
    permutation=list(range(P)); current=source; power=1
    while power<q:
        prefix=target%power
        c=current//power%p; d=target//power%p
        if c!=d:
            def swap(r):
                if r%power!=prefix: return r
                digit=r//power%p
                if digit==c: return r+(d-c)*power
                if digit==d: return r+(c-d)*power
                return r
            permutation=[swap(r) for r in permutation]
            current=swap(current)
        power*=p
    if sorted(permutation)!=list(range(P)): raise ValueError('Nonpermutation')
    power=p
    while power<=P:
        images={}
        for r,s in enumerate(permutation):
            prefix=r%power
            if prefix in images and images[prefix]!=s%power:
                raise ValueError('Does not preserve a congruence partition')
            images[prefix]=s%power
        if len(set(images.values()))!=power: raise ValueError('Nonbijective prefix action')
        power*=p
    for depth,phase in anchor_coordinates:
        if any((r%depth==phase)!=(s%depth==phase) for r,s in enumerate(permutation)):
            raise ValueError('Transport fails to fix a placed class coordinate')
    if any(s%q!=target for r,s in enumerate(permutation) if r%q==source):
        raise ValueError('Transport fails to map the proposed phase')
    return tuple(permutation)


def audit_tree(tree):
    start=monotonic()
    structure_only=False; max_nodes=None
    L=10080; root_node=tree['root_node']
    meta={'minimum':8, 'root':'anchor16_'+str(tree['phase'])}
    records=decode_tree(tree)
    factors=factor(L); periods=tuple(p**e for p,e in factors)
    permitted=[m for m in range(8,L+1) if L%m==0]
    children=defaultdict(list)
    for i,(parent,A,status,payload) in records.items():
        if i!=root_node:
            if parent not in records or parent>=i: raise ValueError('Orphan/cyclic node')
            children[parent].append(i)
        if len({m for m,a in A})!=len(A): raise ValueError('Repeated modulus')
        if any(m not in permitted or not 0<=a<m for m,a in A): raise ValueError('Invalid anchor')
        if status not in ('pending','expanded','uniform','weighted','covered'):
            raise ValueError('Unknown status')
    class_masks={}
    def congruence(m,a):
        key=m,a
        if key not in class_masks:
            value=0
            for x in range(a,L,m): value|=1<<x
            class_masks[key]=value
        return class_masks[key]
    residual={root_node:(1<<L)-1}
    for m,a in records[root_node][1]: residual[root_node]&=~congruence(m,a)
    events=[]; checked=Counter(); literal_phases=0; transported_phases=0
    axis_masks={}
    def axis_mask(P,mask):
        if type(mask) is not int or not 0<mask<1<<P: raise ValueError('Invalid axis mask')
        key=P,mask
        if key not in axis_masks:
            value=0
            for x in range(L):
                if mask>>(x%P)&1: value|=1<<x
            axis_masks[key]=value
        return axis_masks[key]
    for count,i in enumerate(sorted(records)):
        parent,A,status,payload=records[i]
        if i!=root_node:
            old=records[parent]
            if old[2]!='expanded' or A[:-1]!=old[1]: raise ValueError('Bad tree edge')
            m,a=A[-1]
            if m!=old[3]['modulus'] or a not in old[3]['phases']: raise ValueError('Unadvertised child')
            residual[i]=residual[parent]&~congruence(m,a)
        U=residual[i]
        assigned={m for m,a in A}
        remaining=[m for m in permitted if m not in assigned]
        if status!='expanded' and children[i]: raise ValueError('Terminal has children')
        if status=='expanded':
            m=payload['modulus']; phases=payload['phases']
            if m not in remaining or not phases or len(set(phases))!=len(phases):
                raise ValueError('Invalid branch')
            if any(type(a) is not int or not 0<=a<m for a in phases): raise ValueError('Invalid phase')
            if sorted(records[j][1][-1][1] for j in children[i])!=sorted(phases):
                raise ValueError('Incomplete advertised child list')
            if not U: raise ValueError('Expanded an already covering node')
            constraints=[]
            for n,b in A:
                for p,e in factor(gcd(m,n)): constraints.append((b,p**e))
            def signature(a): return tuple(gcd(a-b,q) for b,q in constraints)
            targets={}
            for b in phases:
                if not U&congruence(m,b): raise ValueError('Zero-gain child')
                targets.setdefault(signature(b),b)
            for a in range(m):
                literal_phases+=1
                if not U&congruence(m,a): continue
                if signature(a) not in targets: raise ValueError('Unrepresented positive-gain phase')
                b=targets[signature(a)]
                for (p,e),P in zip(factors,periods):
                    q=p**valuation(m,p)
                    fixed=tuple((p**valuation(n,p),c%(p**valuation(n,p))) for n,c in A)
                    coordinate_transport(p,P,q,a%q,b%q,fixed)
                transported_phases+=1
            checked[status]+=1
            events.append([i,status,m,phases])
        elif status=='covered':
            if U: raise ValueError('False covering witness')
            checked[status]+=1
        elif status in ('uniform','weighted') and not structure_only and (max_nodes is None or count<max_nodes):
            if status=='uniform':
                demand=U.bit_count()
                capacity=sum(max((U&congruence(m,a)).bit_count() for a in range(m)) for m in remaining)
            else:
                weights=[0]*L; support=0
                for box in payload['boxes']:
                    if len(box)!=len(periods)+1 or type(box[-1]) is not int or box[-1]<=0:
                        raise ValueError('Invalid positive integer box')
                    points=(1<<L)-1
                    for P,mask in zip(periods,box[:-1]): points&=axis_mask(P,mask)
                    if points&support or points&~U: raise ValueError('Overlapping or covered weight')
                    support|=points
                    while points:
                        least=points&-points; x=least.bit_length()-1
                        weights[x]=box[-1]; points-=least
                demand=sum(weights)
                # Literal arithmetic progressions, no orbit matrices or LP.
                pairs=payload.get('pairs',[])
                paired={m for pair in pairs for m in pair}
                if any(len(pair)!=2 for pair in pairs) or len(paired)!=2*len(pairs) or not paired.issubset(remaining):
                    raise ValueError('Bad joint resource partition')
                capacity=sum(max(sum(weights[a::m]) for a in range(m)) for m in remaining if m not in paired)
                for m,n in pairs:
                    first=[set(range(a,L,m)) for a in range(m)]
                    second=[set(range(b,L,n)) for b in range(n)]
                    capacity+=max(sum(weights[x] for x in X|Y) for X in first for Y in second)
            if (demand,capacity)!=(payload['demand'],payload['capacity']) or demand<=capacity:
                raise ValueError(f'False integer cut at node {i}')
            checked[status]+=1
            events.append([i,status,demand,capacity])
        elif status!='pending': checked['unchecked_cuts']+=1
        if monotonic()-start>10 and count%100==0:
            print(json.dumps({'audit_seconds':round(monotonic()-start,2),'nodes_visited':count+1,
                              'checked':dict(checked)}),flush=True)
    counts=Counter(v[2] for v in records.values())
    complete=(not structure_only and max_nodes is None and not counts['pending']
              and not counts['covered'] and not checked['unchecked_cuts'])
    result={'all_checked_nodes_valid':True,'complete_exclusion':complete,'L':L,'root':meta['root'],
            'root_node':root_node,'root_anchors':records[root_node][1],
            'node_counts':dict(counts),'checked':dict(checked),'literal_branch_phases':literal_phases,
            'explicit_transported_phases':transported_phases,
            'coordinate_transport_witnesses':coordinate_transport.cache_info().currsize,
            'events_sha256':sha256(json.dumps(events,separators=(',',':')).encode('ascii')).hexdigest(),
            'seconds':monotonic()-start}
    print(json.dumps(result),flush=True)
    return result




def verify(document):
    need(document.get('format')=='dcs-literal-tree-1', 'Unknown certificate format')
    need(type(document.get('period')) is int and document['period']==10080, 'Wrong period')
    need(type(document.get('minimum')) is int and document['minimum']==8, 'Wrong minimum')
    trees=document['trees']; need(isinstance(trees,list) and len(trees)==1, 'Wrong case count')
    need(sorted(t['phase'] for t in trees)==[1], 'Missing or repeated case')
    reports=[audit_tree(t) for t in sorted(trees,key=lambda t:t['phase'])]
    need(all(r['complete_exclusion'] for r in reports), 'Incomplete exclusion')
    return {'period':10080,'minimum':8,'prescribed_mod16_phases':[1],
            'complete_conditional_exclusions':1,'global10080_exclusion':False,
            'records':sum(sum(r['node_counts'].values()) for r in reports),
            'literal_branch_phases':sum(r['literal_branch_phases'] for r in reports),
            'positive_transported_phases':sum(r['explicit_transported_phases'] for r in reports),
            'cases':reports}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--certificate',type=Path,default=Path(__file__).with_name('certificate.json'))
    a=p.parse_args();result=verify(json.loads(a.certificate.read_text()))
    print(json.dumps(result,sort_keys=True))
