"""Physical complete-family controls, transport and hostile certificate checks."""
import copy
from itertools import combinations
import json
import random
from extract import canonical,extract,read_input
from verify import parse,verify,check


PAIRS=list(combinations(range(43),2))
INDEX={p:i for i,p in enumerate(PAIRS)}


def cut_input(a,rank,seed):
    rng=random.Random(seed)
    word=rng.getrandbits(903)
    left=[1<<i for i in range(rank)]+[rng.randrange(1<<rank) for _ in range(a-rank)]
    right=[1<<i for i in range(rank)]+[rng.randrange(1<<rank) for _ in range(43-a-rank)]
    for u,x in enumerate(left):
        for j,y in enumerate(right):
            e=INDEX[u,a+j]
            bit=(x & y).bit_count()%2
            word=(word & ~(1<<e)) | (bit<<e)
    return {'n':43,'red_hex':format(word,'0226x'),'kind':'cut','cut':list(range(a)),
            'rank_color':'red'}


def decomposition_input(seed):
    rng=random.Random(seed)
    # Each component has at most seven vertices, so any internal split of
    # that component has cross rank at most three. Components have no edges
    # between them. The displayed tree keeps each component together.
    sizes=([7]*6+[1]) if seed%2==0 else ([6]*7+[1])
    groups=[];start=0;word=0
    for size in sizes:
        g=list(range(start,start+size));start+=size;groups.append(g)
        for pair in combinations(g,2):
            if rng.randrange(2):word|=1<<INDEX[pair]
    edges=[];next_id=43
    def merge(roots):
        nonlocal next_id
        if len(roots)==1:return roots[0]
        split=len(roots)//2
        u=merge(roots[:split]);v=merge(roots[split:])
        p=next_id;next_id+=1
        edges.extend([(u,p),(v,p)])
        return p
    component_roots=[merge(g) for g in groups]
    root=merge(component_roots)
    check(root==84 and next_id==85,'rooted tree dimensions')
    incident=[u if v==root else v for u,v in edges if root in (u,v)]
    check(len(incident)==2,'suppress degree-two root')
    edges=[e for e in edges if root not in e]+[tuple(incident)]
    return {'n':43,'red_hex':format(word,'0226x'),'kind':'decomposition',
            'tree_edges':sorted([sorted(e) for e in edges]),'rank_color':'red'}


def transport(obj,flip=False,permute=False):
    result=copy.deepcopy(obj)
    permutation=list(range(43))
    if permute:random.Random(97043).shuffle(permutation)
    old=int(obj['red_hex'],16);new=0
    for e,(u,v) in enumerate(PAIRS):
        color=((old>>e)&1)^flip
        if color:new|=1<<INDEX[tuple(sorted((permutation[u],permutation[v])))]
    result['red_hex']=format(new,'0226x')
    if flip:result['rank_color']='blue' if obj['rank_color']=='red' else 'red'
    if obj['kind']=='cut':result['cut']=sorted(permutation[v] for v in obj['cut'])
    else:
        internals=list(range(43,84))
        if permute:random.Random(9784).shuffle(internals)
        result['tree_edges']=sorted([sorted(permutation[v] if v<43 else internals[v-43] for v in e)
                                     for e in obj['tree_edges']])
    # Check every physical pair of the transport, separately from extraction.
    g,_,_=parse(obj);h,_,_=parse(result)
    check(all(h[permutation[u]][permutation[v]]==g[u][v]^flip for u,v in PAIRS),'pair transport')
    return result


def main():
    result={'cut_controls':0,'decomposition_controls':0,'tree_cuts_checked':0,
            'physical_five_pairs_checked':0,'transport_pairs_checked':0,'outside_controls':0,
            'malformed_inputs_rejected_by_each_parser':0,'corrupt_certificates_rejected':0}
    bases=[cut_input(a,r,100*a+r) for a in range(15,22) for r in range(4)]
    bases += [cut_input(a,3,seed) for a in (20,21) for seed in range(8)]
    for a in (20,21):
        for r in range(4):
            obj=cut_input(a,r,200*a+r)
            obj['cut']=list(range(a,43))
            bases.append(obj)
    bases += [decomposition_input(seed) for seed in range(6)]
    widths=[]
    for obj in bases:
        for flip,permute in [(False,False),(True,False),(False,True),(True,True)]:
            physical=transport(obj,flip,permute)
            cert=extract(physical);checked=verify(physical,cert)
            check(checked['status']=='VERIFIED_PHYSICAL_EXCLUSION','inside family')
            result['cut_controls' if obj['kind']=='cut' else 'decomposition_controls']+=1
            result['tree_cuts_checked']+=checked['tree_cuts_checked']
            result['physical_five_pairs_checked']+=10
            result['transport_pairs_checked']+=903
            if obj['kind']=='decomposition':widths.append(cert['measured_width'])
    result['decomposition_widths']=dict((str(w),widths.count(w)) for w in sorted(set(widths)))
    outside=[cut_input(20,4,71),cut_input(21,4,72),cut_input(14,3,73)]
    random_tree=decomposition_input(0)
    random_tree['red_hex']=format(random.Random(917).getrandbits(903),'0226x')
    outside.append(random_tree)
    for obj in outside:
        cert=extract(obj);checked=verify(obj,cert)
        check(checked['status']=='VERIFIED_OUTSIDE_DECLARED_FAMILY','outside semantics')
        result['outside_controls']+=1
    base=cut_input(20,3,7)
    invalid=[]
    p=copy.deepcopy(base);p['n']=42;invalid.append(p)
    p=copy.deepcopy(base);p['red_hex']='0';invalid.append(p)
    p=copy.deepcopy(base);p['red_hex']='f'*226;invalid.append(p)
    p=copy.deepcopy(base);p['red_hex']='g'+p['red_hex'][1:];invalid.append(p)
    p=copy.deepcopy(base);p['rank_color']='green';invalid.append(p)
    p=copy.deepcopy(base);p['cut']=[];invalid.append(p)
    p=copy.deepcopy(base);p['cut']=[1,0];invalid.append(p)
    p=copy.deepcopy(base);p['cut']=[0,0];invalid.append(p)
    p=copy.deepcopy(base);p['cut']=[43];invalid.append(p)
    p=copy.deepcopy(base);p['extra']=0;invalid.append(p)
    p=decomposition_input(0);p['tree_edges'].pop();invalid.append(p)
    p=decomposition_input(0);p['tree_edges'][1]=p['tree_edges'][0];invalid.append(p)
    p=decomposition_input(0);p['tree_edges'][0][0]=84;invalid.append(p)
    p=decomposition_input(0);p['tree_edges'][0][0]=1;p['tree_edges'].sort();invalid.append(p)
    for obj in invalid:
        for parser in (lambda x:extract(x),parse):
            try:parser(obj)
            except ValueError:pass
            else:raise RuntimeError('malformed input accepted')
        result['malformed_inputs_rejected_by_each_parser']+=1
    cert=extract(base);bad=[]
    p=copy.deepcopy(cert);p['input_sha256']='0'*64;bad.append(p)
    p=copy.deepcopy(cert);p['five_color']='blue' if p['five_color']=='red' else 'red';bad.append(p)
    p=copy.deepcopy(cert);p['five'].pop();bad.append(p)
    p=copy.deepcopy(cert);p['five'][0]=43;bad.append(p)
    p=copy.deepcopy(cert);p['cut_rank']+=1;bad.append(p)
    p=copy.deepcopy(cert);p['cut']=list(range(14));bad.append(p)
    p=copy.deepcopy(cert);p['row_basis'][0]=0;bad.append(p)
    p=copy.deepcopy(cert);p['row_basis'][1]=p['row_basis'][0];bad.append(p)
    p=copy.deepcopy(cert);p['status']='OUTSIDE_DECLARED_FAMILY';bad.append(p)
    p=copy.deepcopy(cert);p['measured_width']+=1;bad.append(p)
    for corrupt in bad:
        try:verify(base,corrupt)
        except ValueError:result['corrupt_certificates_rejected']+=1
        else:raise RuntimeError('corrupted certificate accepted')
    bad_out=extract(outside[0]);bad_out['status']='EXCLUDED_WITH_PHYSICAL_FIVE_SET'
    try:verify(outside[0],bad_out)
    except ValueError:result['corrupt_certificates_rejected']+=1
    else:raise RuntimeError('false outside exclusion accepted')
    return dict(result,status='PHYSICAL_GLOBAL_FAMILY_CONTROLS_PASS')


if __name__=='__main__':print(canonical(main()).decode(),end='')
