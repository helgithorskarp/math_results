"""Broad physical fixtures and adversarial certificates, all explicitly bad43."""
from collections import Counter
from copy import deepcopy
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json
import random
import time
import bridge
import verify_bridge
from compile_family import selected_matching
from lookup import Lookup, catalog
from support import HERE, graph, matrix, need, parents

@lru_cache(None)
def cores(cache,n): return catalog(cache,n)

def fixture(cache,q,r,c,exchange_choice=None):
    n=43-4*q; word=cores(str(cache),n)[c]; pairs=list(combinations(range(n),2))
    a=[[0]*43 for _ in range(43)]; rows=[0]*n
    for k,(u,v) in enumerate(pairs):
        if word>>k&1:
            a[4*q+u][4*q+v]=a[4*q+v][4*q+u]=1
            rows[u]|=1<<v;rows[v]|=1<<u
    selected=selected_matching(rows,4 if q==8 else 2) if q in (8,9) else []
    triangles=[s for s in combinations(range(n),3) if all(rows[u]>>v&1 for u,v in combinations(s,2))]
    # This finite fixture choice is not used as an imported mathematical theorem.
    coloring=next((z for z in range(1<<n)
                   if all(len({(z>>v)&1 for v in s})==2 for s in triangles)
                   and all(((z>>u)^(z>>v))&1 for u,v in selected)),None)
    need(coloring is not None,'fixture vertex coloring')
    for b in range(q):
        for u,v in combinations(range(4*b,4*b+4),2):a[u][v]=a[v][u]=int(b<r)
        for d in range(b+1,q):
            for u in range(4*b,4*b+4):
                for v in range(4*d,4*d+4):a[u][v]=a[v][u]=(u^v)&1
        for v in range(n):
            for u in range(4*b,4*b+4):a[u][4*q+v]=a[4*q+v][u]=((coloring>>v)^u)&1
    if exchange_choice is not None:
        e,f=list(combinations(selected,2))[exchange_choice]
        for edge,part in ((e,(0,1)),(f,(2,3))):
            for v in edge:
                for u in range(4):a[u][4*q+v]=a[4*q+v][u]=int(u in part)
    # All child root signatures are 10,5,10,5 before column ordering.
    order=list(range(4))+[4*b+j for b in range(1,q) for j in (0,2,1,3)]+list(range(4*q,43))
    g=graph(a,order)
    # A fixed blue K5 proves these are interface controls, never candidate claims.
    aa=matrix(g)
    need(all(aa[u][v]==0 for u,v in combinations((0,4,8,12,16),2)), 'explicitly non-Ramsey fixture')
    return dict(g,task=f'bo1-q{q}-r{r}-c{c:06d}')

def scramble(src,seed):
    q,r,_=verify_bridge.parameters(src['task']); a=matrix(src)
    p=list(range(43));random.Random(seed).shuffle(p);inv={old:new for new,old in enumerate(p)}
    return dict(graph(a,p),blocks=[[inv[v] for v in range(4*b,4*b+4)] for b in range(q)],
                core=[inv[v] for v in range(4*q,43)],r=r)

def run(cache,tables,out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True);lookup=Lookup(cache,tables)
    start=time.monotonic();normalizations=transports=edges=bad=corruptions=0;steps=Counter();destinations=set()
    digest=hashlib.sha256();sample=None
    with (out/'physical.jsonl').open('xb') as stream:
        def record(kind,src,cert,receipt):
            raw=(json.dumps({'kind':kind,'source':src,'certificate':cert,'receipt':receipt},sort_keys=True,separators=(',',':'))+'\n').encode()
            stream.write(raw);digest.update(raw)
        for q,count in ((9,362),(10,4)):
            for c in range(count):
                for r in range(5,q+1):
                    src=fixture(cache,q,r,c);obj=scramble(src,10000*q+100*c+r)
                    cert=bridge.normalize_partition(obj,cache,lookup)
                    count_edges=verify_bridge.check_normalization(obj,cert,cache)
                    need(cert['task']==src['task'],'catalogue index recovery')
                    edges+=count_edges;normalizations+=1
                    record('normalization',obj,cert,{'edge_identities':count_edges})
                    if sample is None:sample=(obj,cert)
        # Every q9 source core and every q9 red-block count; these are complete
        # physical carriers, not arbitrary partitions or one labelled template.
        for c in range(362):
            for r in range(5,10):
                src=fixture(cache,9,r,c,0);cert=bridge.reduce(src,cache,lookup)
                receipt=verify_bridge.check_reduce(src,cert,cache)
                need(cert['status']=='REDUCED_FAMILY_CARRIER_NO_RAMSEY_VERDICT','q9 fixture transport')
                need(len(cert['steps'])==1,'q9 forced exchange')
                edges+=receipt['edge_identities'];transports+=1;steps[1]+=1
                destinations.add(cert['destination_task']);record('reduction',src,cert,receipt)
        # Four existing q8 representative cores, all six selected edge-pair choices.
        old=json.loads((HERE.parent/'ramsey_r55_maximal_block_order'/'FORMULAS.json').read_text())
        for row in old:
            if row['triangles'] or not row['task'].startswith('bo1-q8-'):continue
            q,r,c=verify_bridge.parameters(row['task'])
            for choice in range(6):
                src=fixture(cache,q,r,c,choice);cert=bridge.reduce(src,cache,lookup)
                receipt=verify_bridge.check_reduce(src,cert,cache);edges+=receipt['edge_identities']
                if cert['status']=='MONOCHROMATIC_FIVE':bad+=1
                else:
                    transports+=1;steps[len(cert['steps'])]+=1;destinations.add(cert['destination_task'])
                record('reduction',src,cert,receipt)
        # A fixed two-step fixture tests composition across both normalizations.
        src=fixture(cache,8,8,0,0);first=bridge.reduce(src,cache,lookup)
        need(len(first.get('steps',[]))==1,'two-step setup')
        _,_,c=verify_bridge.parameters(first['destination_task'])
        co=parents()[1].catalog.get(cache,7,c);e,f=selected_matching(co,2)
        p=first['new_to_old'];aa=matrix(src)
        for edge,part in ((e,(0,2)),(f,(1,3))):
            for v in edge:
                for u in range(4):aa[p[u]][p[36+v]]=aa[p[36+v]][p[u]]=int(u in part)
        src=dict(graph(aa),task=src['task']);two_src=src;two_cert=bridge.reduce(src,cache,lookup)
        receipt=verify_bridge.check_reduce(src,two_cert,cache)
        need(len(two_cert.get('steps',[]))==2,'two-step certificate')
        record('reduction',src,two_cert,receipt);edges+=receipt['edge_identities'];steps[2]+=1;transports+=1
        destinations.add(two_cert['destination_task'])
        # Zero-exchange receiver path and a deliberately detected bad-five path.
        src=fixture(cache,9,9,0);cert=bridge.reduce(src,cache,lookup)
        receipt=verify_bridge.check_reduce(src,cert,cache)
        need(cert['status']=='REDUCED_FAMILY_CARRIER_NO_RAMSEY_VERDICT' and not cert['steps'],'zero-step path')
        record('reduction',src,cert,receipt);edges+=receipt['edge_identities'];steps[0]+=1;transports+=1
        destinations.add(cert['destination_task'])
        # Different same-color endpoint stars into another red block force a new
        # pair-domain failure after the first exchange, hence a real source K5.
        src=fixture(cache,9,9,0,0);aa=matrix(src)
        core=parents()[1].catalog.get(cache,7,0);e=selected_matching(core,2)[0]
        for v in e:
            for u in range(4,8):aa[u][36+v]=aa[36+v][u]=int(u in (4,5))
        src=dict(graph(aa),task=src['task']);cert=bridge.reduce(src,cache,lookup)
        receipt=verify_bridge.check_reduce(src,cert,cache)
        need(cert['status']=='MONOCHROMATIC_FIVE','bad-five output path')
        record('reduction',src,cert,receipt);bad+=1;edges+=receipt['edge_identities']
        # Adversarial edits target independent bindings, physical labels, task IDs,
        # core membership, and terminal-family membership.
        norm_src,norm_cert=sample
        for kind in ('duplicate','edge','task','block','core'):
            altered=deepcopy(norm_cert)
            if kind=='duplicate':altered['new_to_old'][0]=altered['new_to_old'][1]
            if kind=='edge':altered['graph']['red_hex']=format(int(altered['graph']['red_hex'],16)^1,'0226x')
            if kind=='task':altered['task']=altered['task'][:-1]+'1'
            if kind=='block':altered['new_to_old'][0],altered['new_to_old'][4]=altered['new_to_old'][4],altered['new_to_old'][0]
            if kind=='core':altered['new_to_old'][-1],altered['new_to_old'][0]=altered['new_to_old'][0],altered['new_to_old'][-1]
            try:verify_bridge.check_normalization(norm_src,altered,cache)
            except (ValueError,KeyError,TypeError):corruptions+=1
            else:raise ValueError('accepted corrupt normalization '+kind)
        src=fixture(cache,9,9,1,0);cert=bridge.reduce(src,cache,lookup)
        for kind in ('binding','destination','permutation','exchange','normalization','steps','edge'):
            altered=deepcopy(cert)
            if kind=='binding':altered['source_sha256']='0'*64
            if kind=='destination':altered['destination_task']='bo1-q10-r9-c000000'
            if kind=='permutation':altered['new_to_old'][0]=altered['new_to_old'][1]
            if kind=='exchange':altered['steps'][0]['exchange']['replaced_block']=99
            if kind=='normalization':altered['steps'][0]['normalization']['new_to_old'].reverse()
            if kind=='steps':altered['steps']=[]
            if kind=='edge':altered['graph']['red_hex']=format(int(altered['graph']['red_hex'],16)^1,'0226x')
            try:verify_bridge.check_reduce(src,altered,cache)
            except (ValueError,KeyError,TypeError):corruptions+=1
            else:raise ValueError('accepted corrupt reduction '+kind)
        for kind in ('second-permutation','second-task','composite'):
            altered=deepcopy(two_cert)
            if kind=='second-permutation':altered['steps'][1]['exchange']['new_to_old'].reverse()
            if kind=='second-task':altered['steps'][1]['normalization']['task']='bo1-q10-r9-c000000'
            if kind=='composite':altered['new_to_old'][0],altered['new_to_old'][1]=altered['new_to_old'][1],altered['new_to_old'][0]
            try:verify_bridge.check_reduce(two_src,altered,cache)
            except (ValueError,KeyError,TypeError):corruptions+=1
            else:raise ValueError('accepted corrupt composition '+kind)
    observed=set()
    for line in (out/'physical.jsonl').open():
        certificate=json.loads(line)['certificate']
        if certificate['status']=='REDUCED_FAMILY_CARRIER_NO_RAMSEY_VERDICT':observed.add(certificate['destination_task'])
    need(observed==destinations,'distinct destination summary')
    result={'status':'BROAD_PHYSICAL_BRIDGE_CONTROLS_PASS','normalizations':normalizations,
            'successful_reductions':transports,'monochromatic_five_outputs':bad,
            'step_histogram':dict(sorted(steps.items())),'edge_identities':edges,
            'distinct_destination_tasks':len(destinations),'certificate_sha256':digest.hexdigest(),
            'rejected_corruptions':corruptions,'all_fixtures_explicitly_non_Ramsey':True,
            'target_found':False,'seconds':time.monotonic()-start}
    (out/'PHYSICAL.json').write_text(json.dumps(result,indent=2)+'\n')
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('cache');p.add_argument('tables');p.add_argument('out');args=p.parse_args()
    print(json.dumps(run(args.cache,args.tables,args.out),sort_keys=True))
