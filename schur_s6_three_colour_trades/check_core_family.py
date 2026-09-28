"""Check the fixed-core splitting theorem and a Cartesian family of inputs."""
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

from check import colourable, require, violations
from check_splitting import blocked_colours


def verify_product(certificate,fixtures,partial):
    old=fixtures['baseline']['colours']
    require(len(old)==536 and set(old)==set('123456'),'wrong product base')
    require(sha256((old+'\n').encode()).hexdigest()==fixtures['baseline']['sha256'],'product base hash')
    base=[0]+list(map(int,old))
    require(not violations(base[1:]),'product base is invalid')
    require(all(not partial[v] or base[v]==partial[v] for v in range(1,537)),'product base misses a core')
    domains=[set()]+[{d} for d in base[1:]]
    changed=set()
    for row in certificate['product_switches']:
        v=row['vertex'];a=row['old'];b=row['alternative']
        require(type(v) is int and 1<=v<=536 and v not in changed,'invalid switch vertex')
        require(partial[v]==0,'switch changes a core')
        require(a==base[v] and type(b) is int and 1<=b<=6 and b!=a,'invalid switch colours')
        domains[v].add(b);changed.add(v)
    triples=0
    for z in range(2,537):
        for x in range(1,z//2+1):
            require(not (domains[x]&domains[z-x]&domains[z]),'product family admits a monochromatic triple')
            triples+=1
    return len(changed),triples


def verify(certificate,kernel_certificate,fixtures):
    require(certificate.get('format')==1,'unsupported core certificate')
    cores=certificate['cores']
    require(set(cores)==set('123456'),'core labels')
    partial=[0]*538
    for d in range(1,7):
        B=cores[str(d)]
        require(B and B==sorted(set(B)),'empty or repeated core vertices')
        require(all(type(v) is int and 1<=v<=536 for v in B),'invalid core vertex')
        for v in B:
            require(partial[v]==0,'overlapping cores')
            partial[v]=d
        S=set(B)
        require(not any(x+y in S for x in S for y in S),'core is not sum-free')
    pairs=set()
    for row in certificate['nonmerge']:
        pair=tuple(row['palette']);triple=row['triple']
        require(pair in set(combinations(range(1,7),2)) and pair not in pairs,'nonmerge pair coverage')
        require(len(triple)==3 and all(type(v) is int and 1<=v<=536 for v in triple),'invalid pair triple')
        x,y,z=triple
        require(x<=y and x+y==z,'pair triple is not additive')
        require({partial[x],partial[y],partial[z]}==set(pair),'pair triple is not supported by cores')
        pairs.add(pair)
    require(pairs==set(combinations(range(1,7),2)),'missing pair witness')
    dimension,triples=verify_product(certificate,fixtures,partial)
    rows=[r for r in kernel_certificate['cases'] if r['input']=='baseline']
    palettes=[tuple(r['palette']) for r in rows]
    require(len(palettes)==20 and set(palettes)==set(combinations(range(1,7),3)),'kernel coverage')
    blocked=blocked_colours(partial)
    results=[]
    for row in rows:
        frozen=set(range(1,7))-set(row['palette'])
        W=row['vertices']
        require(all(type(v) is int and 1<=v<=537 for v in W),'invalid kernel vertex')
        require(all(frozen<=blocked[v] for v in W),'core does not block a frozen colour')
        # No old colour or membership requirement is imposed on W.
        answer,nodes,edges=colourable(W,3,row['root'])
        require(answer is None,'kernel is three-colourable')
        results.append({'free_labels':row['palette'],'vertices':len(W),'edges':edges,'nodes':nodes})
    core_size=sum(len(B) for B in cores.values())
    return {'status':'VERIFIED_CORE_FAMILY_SPLITTING','core_sizes':[len(cores[str(d)]) for d in range(1,7)],
            'core_vertices':core_size,'unprescribed_positions':536-core_size,'nonmerge_pairs':len(pairs),
            'kernels':len(rows),'blocked_incidences':3*sum(r['vertices'] for r in results),
            'nodes':sum(r['nodes'] for r in results),'maximum_kernel':max(r['vertices'] for r in results),
            'product_dimension':dimension,'product_colourings':str(1<<dimension),
            'product_triples':triples,'cases':results}


def main():
    p=Path(__file__).resolve().parent
    cert=json.loads((p/'core_family.json').read_text())
    kernels=(p/'class_splitting.json').read_bytes();fixtures=(p/'fixtures.json').read_bytes()
    require(sha256(kernels).hexdigest()==cert['kernel_certificate_sha256'],'wrong kernel certificate')
    require(sha256(fixtures).hexdigest()==cert['fixtures_sha256'],'wrong fixture file')
    result=verify(cert,json.loads(kernels),json.loads(fixtures))
    require(result==json.loads((p/'core_family_expected.json').read_text()),'core family expected result differs')
    print('PASS core_family cores={} free_positions={} kernels={} nodes={} product=2^{}'.format(
        result['core_vertices'],result['unprescribed_positions'],result['kernels'],result['nodes'],result['product_dimension']))
    print('core_family_sha256='+sha256((p/'core_family.json').read_bytes()).hexdigest())


if __name__=='__main__':main()
