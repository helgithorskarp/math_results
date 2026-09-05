#!/usr/bin/env python3
"""Bounded shared-colouring pilot on a fixed eleven-point cohort."""
from pathlib import Path
from hashlib import sha256
from itertools import combinations
import importlib.util
import argparse,json,resource,sys,time
import pysat
from pysat.solvers import Solver

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
BASE=REPO/'hadwiger_nelson_parts509_degree7_extension610'
WORK=None


def save(name,data):
    path=WORK/name;tmp=path.with_suffix(path.suffix+'.tmp')
    tmp.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n');tmp.replace(path)


def four_disjoint(groups):
    ordered=sorted(groups,key=lambda x:(len(x[1]),x[1],x[0]))
    def search(start,used,chosen):
        if len(chosen)==4:return chosen
        for k in range(start,len(ordered)):
            i,group=ordered[k]
            if not used.intersection(group):
                answer=search(k+1,used.union(group),chosen+[i])
                if answer is not None:return answer
        return None
    return search(0,set(),[])


def main():
    global WORK
    ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True);args=ap.parse_args()
    WORK=args.work.resolve();WORK.mkdir(parents=True,exist_ok=True)
    assert pysat.__version__=='1.8.dev24'
    assert not (WORK/'pilot.json').exists()
    resource.setrlimit(resource.RLIMIT_AS,(4<<30,4<<30))
    start=time.monotonic();plan=json.loads((HERE/'plan.json').read_text())
    sys.path.insert(0,str(BASE))
    spec=importlib.util.spec_from_file_location('lifting',BASE/'verify.py')
    lifting=importlib.util.module_from_spec(spec);spec.loader.exec_module(lifting)
    old=json.loads((REPO/'hadwiger_nelson_parts509_degree_pool_minimum/certificate_D7.json').read_text())
    _,ee,den,points,raw=lifting.geometry(old)
    vertices=old['vertices'];edges=[(a,b) for a,b in ee if b!=610]
    fieldpath=REPO/'hadwiger_nelson_parts509_pool_shape6_review1/independent_check.py'
    spec=importlib.util.spec_from_file_location('field',fieldpath)
    field=importlib.util.module_from_spec(spec);spec.loader.exec_module(field)
    Dsets=[set(r['D']) for r in old['family']]
    minimal=[i for i,D in enumerate(Dsets) if not any(E<D for E in Dsets)]
    assert len(minimal)==337
    adjacency={v:set() for v in vertices}
    for a,b in edges:adjacency[a].add(b);adjacency[b].add(a)
    triangles=sorted((a,b,c) for a,b in edges for c in adjacency[a]&adjacency[b] if c>b)
    library={}
    def add(kind,key,D,witness):
        lifting.proper(vertices,edges,D,witness)
        bucket=library.setdefault((kind,key),[])
        if witness not in bucket:bucket.append(witness)
        return bucket.index(witness)
    for v in old['forced']:add('forced',v,[v],old['forced_witness'][str(v)])
    for i in minimal:add('kill',i,old['family'][i]['D'],old['family'][i]['witness'])
    prior=json.loads((BASE/'certificate.json').read_text())
    for row in prior['replacement_witnesses']:
        kind,key=row['kind'],int(row['key'])
        if kind=='forced':D=[key]
        else:
            if key not in minimal:continue
            D=old['family'][key]['D']
        add(kind,key,D,row['witness'][:-1])
    initial_sizes={str(k):len(v) for k,v in library.items()}
    result={'status':'running','selected':plan['selection'],'minimal_killing_rows':minimal,'supports':[],
            'queries':[],'native_seconds':0.0,'native_negative_answers_are_graph_certificates':False}
    neighbors={q:[v for v in vertices if field.squared_distance(points[v],points[q])==(den*den,)+(0,)*7]
               for q in plan['selection']}
    masks={}
    def extension(kind,key,D,q):
        labels=[v for v in vertices if v not in D]
        for index,witness in enumerate(library[kind,key]):
            cachekey=(kind,key,index)
            if cachekey not in masks:masks[cachekey]=dict(zip(labels,witness,strict=True))
            colours=masks[cachekey]
            available=set('0123')-{colours[v] for v in neighbors[q] if v in colours}
            if available:return [index,min(available)]
        return None
    def solve(kind,key,D,q):
        labels=[v for v in vertices if v not in D]+[q];pos={v:i for i,v in enumerate(labels)}
        ee=[(a,b) for a,b in edges if a in pos and b in pos]+[(v,q) for v in neighbors[q] if v in pos]
        clauses=[[4*i+c+1 for c in range(4)] for i in range(len(labels))]
        clauses += [[-(4*pos[a]+c+1),-(4*pos[b]+c+1)] for a,b in ee for c in range(4)]
        triangle=next(t for t in triangles if all(v in pos for v in t))
        clauses += [[4*pos[v]+c+1] for c,v in enumerate(triangle)]
        cnf=(f'p cnf {4*len(labels)} {len(clauses)}\n'+''.join(' '.join(map(str,row))+' 0\n' for row in clauses)).encode()
        with Solver(name='cadical195',bootstrap_with=clauses,use_timer=True) as solver:
            solver.conf_budget(100000);answer=solver.solve_limited();elapsed=solver.time()
            query={'q':q,'kind':kind,'key':key,'status':{True:'SAT',False:'UNSAT_UNCERTIFIED',None:'UNKNOWN'}[answer],
                   'native_seconds':elapsed,'cnf_sha256':sha256(cnf).hexdigest(),'triangle':triangle,
                   'variables':4*len(labels),'clauses':len(clauses),'statistics':solver.accum_stats()}
            if answer is True:
                positive={x for x in solver.get_model() if x>0}
                witness=''.join(str(next(c for c in range(4) if 4*pos[v]+c+1 in positive)) for v in labels)
                lifting.proper(vertices+[q],edges+[(v,q) for v in neighbors[q]],D,witness)
                add(kind,key,D,witness[:-1])
            result['queries'].append(query);result['native_seconds']+=elapsed
            print(json.dumps(query),flush=True)
        return extension(kind,key,D,q)
    def checkpoint():
        result['wall_seconds']=time.monotonic()-start
        result['maximum_rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        result['library']=[{'kind':kind,'key':key,'witnesses':witnesses} for (kind,key),witnesses in sorted(library.items())]
        save('pilot.json',result)
    for q in plan['selection']:
        assert len(raw['points'][q-509]['neighbors'])==6
        support={'q':q,'neighbors':neighbors[q],'forced':{},'killing':{},'missing_forced':[],'missing_killing':[]}
        for v in old['forced']:
            witness=extension('forced',v,[v],q)
            if witness is None:witness=solve('forced',v,[v],q)
            if witness is None:
                support['missing_forced'].append(v)
                break  # This sufficient certificate mechanism cannot close the support.
            support['forced'][str(v)]=witness
        if support['missing_forced']:
            support['status']='UNCLASSIFIED_FORCED_LIFT';result['supports'].append(support);checkpoint();continue
        for i in minimal:
            D=old['family'][i]['D'];witness=extension('kill',i,D,q)
            if witness is None:witness=solve('kill',i,D,q)
            if witness is None:support['missing_killing'].append(i)
            else:support['killing'][str(i)]=witness
        missing=support['missing_killing']
        if not missing:
            support['status']='CLOSED_COMPLETE_LIFT'
        else:
            common=set.intersection(*(Dsets[i] for i in missing))
            support['common_repair_vertices']=sorted(common);support['branches']={}
            if common:
                for i in missing:
                    groups=[(int(j),sorted(Dsets[int(j)]-Dsets[i])) for j in support['killing']
                            if Dsets[int(j)]-Dsets[i] and Dsets[int(j)]-Dsets[i]<=set(old['pool'])]
                    support['branches'][str(i)]=four_disjoint(groups)
            if common & set(old['pool']):support['status']='CLOSED_POOL_REPAIR'
            else:support['status']='CLOSED_COMMON_REPAIR' if common and all(support['branches'][str(i)] is not None for i in missing) else 'UNCLASSIFIED_KILLING_LIFT'
        result['supports'].append(support);checkpoint()
        print(json.dumps({'q':q,'status':support['status'],'missing':missing}),flush=True)
    result['status']='completed';checkpoint()
    print(json.dumps({'status':'completed','native_seconds':result['native_seconds'],'queries':len(result['queries']),
                      'supports':[(r['q'],r['status']) for r in result['supports']]}),flush=True)


if __name__=='__main__':main()
