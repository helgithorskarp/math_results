"""Independent arithmetic, certificate faults, and finite dual controls."""
import copy,json,itertools,random
from pathlib import Path
from fractions import Fraction as F
import exact as ex
import native
import cover as v
import verify as final
import transport
B=Path(__file__).resolve().parent

def main(path):
    g=v.geometry(path);cert=json.loads((B/'certificate.json').read_text())
    v.decode(cert,g)
    rejected=[]
    def bad(name,mutate):
        c=copy.deepcopy(cert);mutate(c)
        try:v.decode(c,g)
        except (ValueError,TypeError,KeyError):rejected.append(name)
        else:raise ValueError('accepted '+name)
    bad('version',lambda c:c.update(version='incorrect'))
    bad('target',lambda c:c.update(target=509))
    bad('boolean target',lambda c:c.update(target=True))
    bad('boolean terminal',lambda c:c['terminals'].__setitem__(0,False))
    bad('short baseline',lambda c:c.update(baseline=c['baseline'][:-1]))
    bad('baseline omission',lambda c:c.update(baseline='-'+c['baseline'][1:]))
    bad('nonlist steps',lambda c:c.update(steps={}))
    bad('deleted range',lambda c:c['steps'][0].update(deleted=721))
    bad('terminal deletion',lambda c:c['steps'][0].update(deleted=0))
    bad('boolean deleted',lambda c:c['steps'][0].update(deleted=False))
    bad('short seed',lambda c:c['steps'][0].update(word=c['steps'][0]['word'][:-1]))
    bad('duplicate row',lambda c:c['steps'].insert(1,copy.deepcopy(c['steps'][0])))
    def equal(c):
        w=list(c['steps'][0]['word']);w[1]=w[0];c['steps'][0]['word']=''.join(w)
    bad('equal terminals',equal)
    def mono(c):
        w=list(c['steps'][0]['word']);h=c['steps'][0]['deleted']
        a,b=next(e for e in g['half_edges']if h not in e and not set(e)&{0,1});w[b]=w[a];c['steps'][0]['word']=''.join(w)
    bad('monochromatic edge',mono)
    r=next(i for i,t in enumerate(cert['steps'])if t['kind']=='rotation')
    p=next(i for i,t in enumerate(cert['steps'])if t['kind']=='patch')
    bad('rotation zero',lambda c:c['steps'][r].update(power=0))
    bad('rotation six',lambda c:c['steps'][r].update(power=6))
    bad('boolean rotation',lambda c:c['steps'][r].update(power=True))
    bad('rotation parent',lambda c:c['steps'][r].update(parent=1))
    bad('rotation label',lambda c:c['steps'][r].update(deleted=c['steps'][0]['deleted']))
    bad('unknown kind',lambda c:c['steps'][p].update(kind='unknown'))
    bad('missing parent',lambda c:c['steps'][p].update(parent=1))
    bad('empty patch',lambda c:c['steps'][p].update(changes=[]))
    bad('duplicate patch label',lambda c:c['steps'][p]['changes'].append(c['steps'][p]['changes'][0][:]))
    bad('patch colour',lambda c:c['steps'][p]['changes'][0].__setitem__(1,'4'))
    bad('boolean patch label',lambda c:c['steps'][p]['changes'][0].__setitem__(0,False))
    # Reproduce the compact DAG solely from the small number of explicit seeds.
    seeds=[r for r in cert['steps']if r['kind']=='seed'];c=None;pos=0
    for size in cert['seed_batches']:
        source={'baseline':cert['baseline'],'steps':seeds[pos:pos+size]};pos+=size
        c=transport.generate(source,g,g['rotations'],existing=c)
    v.need(pos==len(seeds)and c==cert,'DAG reproduction')
    # Independent parsers agree on a deterministic rational-expression family.
    exprs=['0','-1','Sqrt[2/3]','1/(Sqrt[2]+Sqrt[3])','1/(2-Sqrt[3])','Sqrt[0]']
    for a in range(-3,4):
        for z in (1,2,3,6):
            for q in (2,5,7):exprs.append(f'({a}+Sqrt[{z}])/({q}+Sqrt[2])')
    for s in exprs:
        parsed=ex.Parser('{'+s+',0}').point()[0]
        v.need(native.parse(s)==tuple(parsed.get(r,F(0))for r in native.D),'expression mismatch')
    invalid=['{1/0,0}','{Sqrt[-1],0}','{Sqrt[11],0}','{x,0}','{1,0}junk','{1,0,2}','{(1+2,0}','{1/0*0,0}']
    for s in invalid:
        try:ex.Parser(s).point()
        except (ValueError,TypeError,KeyError):rejected.append('parse '+s)
        else:raise ValueError('accepted expression '+s)
    # Test the dual inequality on all small labelled graphs and all subsets.
    cases=graphs=0
    for n in range(1,6):
        pairs=list(itertools.combinations(range(n),2))
        for bits in range(1<<len(pairs)):
            edges=[e for i,e in enumerate(pairs)if bits>>i&1];A=[set()for _ in range(n)]
            for u,w in edges:A[u].add(w);A[w].add(u)
            weights=[F((3*u+bits)%7,3)for u in range(n)]
            M={u for u in range(n)if(bits+u)%3==0}
            for k in (1,2,3,4):
                co=[1+k*weights[u]-sum((weights[z]for z in A[u]),F(0))for u in range(n)]
                lower=sum((co[u]if u in M else min(0,co[u])for u in range(n)),F(0))
                for mask in range(1<<n):
                    X={u for u in range(n)if mask>>u&1}
                    if not M<=X or any(len(A[u]&X)<k for u in X):continue
                    v.need(F(len(X))>=lower,'dual inequality small control');cases+=1
            graphs+=1
    cover=v.full_cover(cert,g,require_target=False);proof=json.loads((B/'weights.json').read_text());M=cover['mandatory_global_vertices'];final.weighted_bound(proof,g,M)
    def weight_bad(name,mutate):
        p=copy.deepcopy(proof);mutate(p)
        try:final.weighted_bound(p,g,M)
        except (ValueError,TypeError,KeyError):rejected.append(name)
        else:raise ValueError('accepted '+name)
    weight_bad('weight sign',lambda p:p['weights'][0].__setitem__(1,-1))
    weight_bad('weight duplicate',lambda p:p['weights'].append(p['weights'][0][:]))
    weight_bad('weight outside mandatory',lambda p:p['weights'][0].__setitem__(0,next(u for u in range(1441)if u not in M)))
    weight_bad('weight boolean',lambda p:p['weights'][0].__setitem__(1,True))
    weight_bad('degree boolean',lambda p:p.update(minimum_degree=True))
    weight_bad('capacity',lambda p:p.update(outside_capacity=3))
    weight_bad('missing exception',lambda p:p.update(exceptional_outside=[]))
    weight_bad('boolean exception',lambda p:p.update(exceptional_outside=[True]))
    ng=native.build(path)
    v.need(all(ng[k]==g[k]for k in ['points','edges','left','right','half_edges','rotations']),'independent geometry disagreement')
    original=v.ex.edges
    try:
        v.ex.edges=lambda points:([e for e in g['edges']if e!=tuple(g['bridge'])],0)
        try:v.geometry(path)
        except ValueError:rejected.append('missing bridge')
        else:raise ValueError('accepted missing bridge')
        L,R=set(g['left']),set(g['right']);extra=tuple(sorted((min(L-R),min(R-L))))
        v.need(extra not in set(g['edges']),'extra edge fixture')
        v.ex.edges=lambda points:(sorted(g['edges']+[extra]),0)
        try:v.geometry(path)
        except ValueError:rejected.append('additional bridge')
        else:raise ValueError('accepted additional bridge')
    finally:v.ex.edges=original
    result={'verified':True,'malformed_inputs_rejected':len(rejected),'rejections':rejected,'parser_expression_cases':len(exprs),'DAG_regenerated':True,'seed_words':len(seeds),'independent_geometries_equal':True,'producer_filter_survivors':ng['filter_survivors'],'small_dual_graphs':graphs,'feasible_dual_subset_cases':cases}
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--input',required=True,type=Path);a=ap.parse_args();main(a.input)
