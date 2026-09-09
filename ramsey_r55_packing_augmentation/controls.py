"""Physical transport, literal clause and adversarial certificate controls."""
from copy import deepcopy
from itertools import combinations, product
from pathlib import Path
import json
import transport
import verify_transport

HERE = Path(__file__).resolve().parent

def need(x, why):
    if not x:
        raise ValueError(why)

def fixture(q, r, inject=True, chosen=0):
    g6 = json.loads((HERE/'FIXTURE.json').read_text())['graph6']
    bits = ''.join(format(ord(c)-63,'06b') for c in g6[1:])
    core_edges = {p for k,p in enumerate(( (i,j) for j in range(1,11) for i in range(j))) if bits[k]=='1'}
    ncore = 43-4*q
    red = {p for b in range(r) for p in combinations(range(4*b,4*b+4),2)}
    red |= {(4*q+i,4*q+j) for i,j in core_edges if j<ncore}
    obj = {'n':43,'blocks':[list(range(4*i,4*i+4)) for i in range(q)],'core':list(range(4*q,43)),'r':r}
    def encode():
        return format(sum(int(p in red)<<k for k,p in enumerate(combinations(range(43),2))),'0226x')
    obj['red_hex']=encode()
    a=transport.validate(obj)
    m=transport.matching(a,obj['core'],{8:4,9:2}[q])
    if inject:
        for part,edge in ((obj['blocks'][chosen][:2],m[0]),(obj['blocks'][chosen][2:],m[1])):
            red |= {tuple(sorted((x,y))) for x in part for y in edge}
    obj['red_hex']=encode()
    return obj

def run(out):
    out=Path(out); out.mkdir()
    checked=edges=corruptions=0
    for q in (8,9):
        for r in range(5,q+1):
            for chosen in (0,r-1):
                src=fixture(q,r,chosen=chosen)
                cert=transport.step(src)
                receipt=verify_transport.check(src,cert)
                edges+=receipt['edges']; checked+=1
                stem=f'q{q}-r{r}-b{chosen}'
                for suffix,obj in (('input',src),('certificate',cert),('receipt',receipt)):
                    (out/f'{stem}-{suffix}.json').write_text(json.dumps(obj,sort_keys=True)+'\n')
                for kind in ('edge','permutation','binding','r','replacement'):
                    bad=deepcopy(cert)
                    if kind=='edge': bad['output']['red_hex']=format(int(bad['output']['red_hex'],16)^1,'0226x')
                    if kind=='permutation':bad['new_to_old'][0]=bad['new_to_old'][1]
                    if kind=='binding':bad['source_sha256']='0'*64
                    if kind=='r':bad['output']['r']-=1
                    if kind=='replacement':bad['new_blocks_old_labels'][0][0]=bad['new_blocks_old_labels'][0][1]
                    try:verify_transport.check(src,bad)
                    except (ValueError,KeyError,TypeError):corruptions+=1
                    else:raise ValueError('accepted corrupted transport '+kind)
                cs=transport.clauses(src)
                need(len(cs)==(36*r if q==8 else 6*r),'clause count')
                need(all(len(c)==8 and len(set(c))==8 and all(-903<=v<0 for v in c) for c in cs),'clause shape')
                w=int(src['red_hex'],16)
                need(any(all(w>>(-v-1)&1 for v in c) for c in cs),'injected false clause')
            clean=fixture(q,r,inject=False)
            need(transport.step(clean)['status']=='NO_SELECTED_AUGMENTATION_NO_RAMSEY_VERDICT','negative transport control')
    # Exhaust all four endpoint stars against literal physical clause variables.
    src=fixture(9,5,inject=False)
    a=transport.validate(src)
    m=transport.matching(a,src['core'],2)
    vertices=m[0]+m[1]
    ps=list(combinations(range(43),2)); index={p:k for k,p in enumerate(ps)}
    cs=transport.clauses(src)[:6]
    count=0
    for stars in product(range(15),repeat=4):
        added=0
        for vertex,star in zip(vertices,stars):
            for i in range(4):
                if star>>i&1:added |= 1<<index[i,vertex]
        accepted=all(any(not (added>>(-v-1)&1) for v in clause) for clause in cs)
        direct=not any(all((stars[j]>>i)&1 for i in s for j in (0,1)) and
                       all((stars[j]>>i)&1 for i in range(4) if i not in s for j in (2,3))
                       for s in combinations(range(4),2))
        need(accepted==direct,'physical clause equivalence')
        count+=accepted
    need(count==50151,'literal physical allowed count')
    # A small actual good graph exercises preservation, independently of the
    # deliberately non-Ramsey 43-vertex transport fixtures.
    pairs=list(combinations(range(8),2))
    red=set(combinations(range(4),2))|{(4,5),(6,7)}|{(i,j) for i in (0,1) for j in (4,5)}|{(i,j) for i in (2,3) for j in (6,7)}
    small={'n':8,'red_hex':format(sum(int(p in red)<<k for k,p in enumerate(pairs)),'07x'),'blocks':[[0,1,2,3]],'core':[4,5,6,7],'r':1}
    certificate=transport.step(small); verify_transport.check(small,certificate)
    for obj in (small,certificate['output']):
        a=transport.decode(obj)
        need(all(not transport.mono(a,s,c) for s in combinations(range(8),5) for c in (False,True)),'small good graph')
    return {'status':'PHYSICAL_CONTROLS_PASS','transport43':checked,'physical_edges_checked':edges,
            'rejected_transport_corruptions':corruptions,'literal_star_assignments':15**4,
            'actual_small_good_graph_transport':True,'good43_found':False}

if __name__=='__main__':
    import sys
    print(json.dumps(run(sys.argv[1]),sort_keys=True))
