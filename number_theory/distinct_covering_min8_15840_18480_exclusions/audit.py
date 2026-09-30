"""Alternate compact-tree audit by six-covering-2, researcher.

Independent of the LP, Cartesian orbit constructor and first-appearance
branch checker. Same-author audit; no external review is claimed.

Every positive-gain phase is transported to an actual child by an explicitly
checked permutation of prime-power coordinates. No gcd-signature theorem is
trusted: signatures only propose a target, and the transport is verified.
Zero-gain phases are dominated by replacing that class by a positive-gain
one. A nonempty pending frontier, partial audit, or covering leaf is never
reported as nonexistence.
"""
import argparse
from collections import Counter, defaultdict
from functools import lru_cache
from hashlib import sha256
import json
from math import gcd, prod
from pathlib import Path
from time import monotonic

ROOTS = {
    'hard9': [(8,0),(9,0),(10,5),(12,10),(14,7),(15,1),(16,4),(18,12),(20,17)],
    'global8': [(8,0)],
    'joint13': [(8,0),(9,0),(10,5),(12,10),(14,7),(15,1),(16,4),(18,12),(20,17),
                (21,7),(24,2),(28,1),(30,23)],
}


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


def audit(database,structure_only=False,max_nodes=None,root_node=0,target=15840):
    start=monotonic()
    certificate=json.loads(database.read_text())
    if certificate.get('schema')!=2 or certificate.get('minimum')!=8 or certificate.get('L')!=target or certificate.get('root_anchors')!=[[8,0]]:
        raise ValueError('Wrong complete global-period theorem')
    meta={'schema':1,'minimum':8,'L':target,'root':'global8'}
    records={};vectors=certificate['vectors'];nodes=certificate['nodes'];used_vectors=set()
    def unfold(i,parent,A):
        if type(i) is not int or not 0<=i<len(nodes) or i in records:
            raise ValueError('Missing/cyclic/shared node')
        node=nodes[i]
        if not node or type(node[0]) is not int or node[0] not in (0,1,2):raise ValueError('Open node')
        if node[0]==0:
            if len(node)!=3:raise ValueError('Bad uniform node')
            records[i]=(parent,A,'uniform',{'demand':node[1],'capacity':node[2]})
        elif node[0]==1:
            if len(node)!=5 or type(node[1]) is not int or not 0<=node[1]<len(vectors):raise ValueError('Bad weighted node')
            used_vectors.add(node[1])
            records[i]=(parent,A,'weighted',{'boxes':vectors[node[1]],'demand':node[2],'capacity':node[3],'pairs':node[4]})
        else:
            if len(node)!=3 or not node[2]:raise ValueError('Bad expanded node')
            phases=[a for a,j in node[2]]
            records[i]=(parent,A,'expanded',{'modulus':node[1],'phases':phases})
            for a,j in node[2]:unfold(j,i,A+[(node[1],a)])
    unfold(0,None,[(8,0)])
    if set(records)!=set(range(len(nodes))) or used_vectors!=set(range(len(vectors))):raise ValueError('Unused material')
    if meta['schema']!=1 or meta['minimum']!=8: raise ValueError('Unknown schema or minimum')
    L=meta['L']; factors=factor(L); periods=tuple(p**e for p,e in factors)
    permitted=[m for m in range(8,L+1) if L%m==0]
    if 0 not in records or records[0][0] is not None or records[0][1]!=ROOTS[meta['root']]:
        raise ValueError('Wrong declared root')
    if root_node not in records: raise ValueError('Missing requested subtree root')
    if root_node:
        selected={root_node}
        for i in sorted(records):
            if records[i][0] in selected: selected.add(i)
        records={i:v for i,v in records.items() if i in selected}
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
    events=[]; pair_events=[]; pair_phase_count=0; checked=Counter(); literal_phases=0; transported_phases=0
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
                    # Sum actual second progression outside the first, with
                    # ordinary remainder predicates and no CRT intersection.
                    left=[sum(weights[x] for x in range(a,L,m)) for a in range(m)]
                    second=[tuple((x,weights[x]) for x in range(b,L,n) if weights[x]) for b in range(n)]
                    largest=0;pair_digest=sha256()
                    for a in range(m):
                        for b in range(n):
                            value=left[a]+sum(w for x,w in second[b] if x%m!=a)
                            largest=max(largest,value)
                            pair_digest.update((str(value)+',').encode('ascii'))
                    capacity+=largest;pair_phase_count+=m*n
                    pair_events.append([i,m,n,pair_digest.hexdigest()])
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
            'events_sha256':sha256(json.dumps(sorted(events),separators=(',',':')).encode('ascii')).hexdigest(),
            'pair_events_sha256':sha256(json.dumps(sorted(pair_events),separators=(',',':')).encode('ascii')).hexdigest(),
            'pair_phase_tuples_checked':pair_phase_count,
            'seconds':monotonic()-start}
    print(json.dumps(result),flush=True)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificate',type=Path,nargs='?')
    parser.add_argument('--target',type=int,choices=(15840,18480),default=15840)
    parser.add_argument('--expected',type=Path)
    args=parser.parse_args()
    args.certificate=args.certificate or Path(__file__).with_name(f'certificate-{args.target}.json')
    args.expected=args.expected or Path(__file__).with_name(f'expected-{args.target}.json')
    actual=audit(args.certificate,target=args.target)
    expected=json.loads(args.expected.read_text())
    if not actual['all_checked_nodes_valid'] or not actual['complete_exclusion']:
        raise ValueError('A full exclusion replay is required')
    if actual['node_counts']!={k:v for k,v in expected['node_counts'].items() if k!='grouped_weighted'}:
        raise ValueError('Node-count mismatch')
    for field in ('events_sha256','pair_events_sha256','pair_phase_tuples_checked'):
        if actual[field]!=expected[field]:raise ValueError('Full event/table mismatch')
    if actual['literal_branch_phases']!=expected['literal_branch_phases_checked']:
        raise ValueError('Branch coverage mismatch')
