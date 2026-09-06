"""Direct geometry, disjoint-pair proof, full positive witness and CNF audit.

The principal lower bound uses only proper colourings and nine disjoint pairs.
Native SAT/DRAT is an additional check, not a premise of that counting proof.
"""
import argparse
import copy
import hashlib
from itertools import combinations, product
import json
from math import comb
from pathlib import Path
import resource
import subprocess
import sys

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
sys.path.insert(0,str(REPO/'hadwiger_nelson_heule632_pair_pilot'))
import independent as I


def need(ok,why):
    if not ok:raise ValueError(why)


def sha(raw):return hashlib.sha256(raw).hexdigest()


def proper(cs,support,edges):
    need(set(cs)==support and set(cs.values())<=set('0123'),'proper colouring domain')
    count=0
    for a,b in edges:
        if a in support and b in support:
            need(cs[a]!=cs[b],'unit inequality');count+=1
    return count


def prepare():
    plan=json.loads((HERE/'plan.json').read_text())
    for path,digest in plan['input_files'].items():need(sha((REPO/path).read_bytes())==digest,('input identity',path))
    points,host_edges,_=I.geometry()
    b=json.loads((REPO/'hadwiger_nelson_heule632_minimize/boundary.json').read_text())
    m0,u0=set(b['mandatory_vertices']),set(b['optional_vertices']);erased={510,512,513,520,521,523,524,535}
    v0=(m0|u0)-erased;u60=sorted(u0-erased);added={310,393,578};m=m0|added;u=sorted(v0-m)
    need(len(m0)==492 and len(m)==495 and len(u)==57,'family dimensions')
    edges=[(a,b) for a,b in host_edges if a in v0 and b in v0];need(len(edges)==2726,'reduced graph')
    adjacency={v:set() for v in v0}
    for a,b in edges:adjacency[a].add(b);adjacency[b].add(a)
    parent=json.loads((REPO/'hadwiger_nelson_heule560_global_decision/certificate.json').read_text())
    left=json.loads((REPO/'hadwiger_nelson_heule560_separator/certificate.json').read_text())
    old=json.loads((REPO/'hadwiger_nelson_heule560_kempe/certificate.json').read_text())
    need(parent['optional_order']==u60,'parent selector order')
    positive_sets=[];provenance=[];checks=0
    for i,row in enumerate(parent['positive_covers']):
        chosen={v for j,v in enumerate(u60) if row['mask']//2**j%2};support=m0|chosen
        rp=parent['right_vertices'];need(len(row['colouring'])==len(rp),'right colour length')
        cs={v:c for v,c in zip(rp,row['colouring']) if c!='.'}
        block=left['blocks']['full' if 310 in chosen else 'mandatory']
        lr=next(r for r in block['states'] if r['state']==row['state'])
        lc={v:c for v,c in zip(block['vertices'],lr['colouring']) if v in support}
        need(all(cs[v]==lc[v] for v in parent['separator']),'pasted boundary')
        lc.update(cs);checks+=proper(lc,support,host_edges)
        positive_sets.append(support);provenance.append({'source':'global_decision','row':i})
    for i,row in enumerate(old['maximal_extending_cover_colourings']):
        support=m0|(u0-set(row['omitted_optional']));text=row['colouring'];need(len(text)==632,'old colour length')
        cs={v:c for v,c in enumerate(text) if c!='.'};checks+=proper(cs,support,host_edges)
        positive_sets.append(support&v0);provenance.append({'source':'kempe','row':i})
    need(len(positive_sets)==45,'all known positive covers')
    need(all(v0-{v} in positive_sets for v in added),'three singleton complements')
    raw=[tuple(sorted(v0-p)) for p in positive_sets if not (v0-p)&m]
    clauses=sorted(set(raw),key=lambda cl:(len(cl),cl))
    clauses=[list(cl) for cl in clauses if not any(set(other)<set(cl) for other in clauses)]
    need(all(cl and set(cl)<=set(u) for cl in clauses),'selector cut domains')
    return {'m0':m0,'m':m,'u':u,'v0':v0,'edges':edges,'host_edges':host_edges,'adj':adjacency,'covers':clauses,
            'positive_sets':positive_sets,'provenance':provenance,'cover_edge_checks':checks}


def lower_cnf(g,budget):
    u=g['u'];m=g['m'];adj=g['adj'];var={v:i+1 for i,v in enumerate(u)}
    clauses=[[var[v] for v in cl] for cl in g['covers']];top=len(u)
    for v in sorted(g['v0']):
        ns=sorted(adj[v]&set(u));fixed=len(adj[v]&m);required=4-fixed
        if required>0:
            guard=[-var[v]] if v in var else []
            if len(ns)<required:clauses.append(guard)
            else:
                # Forbid each largest possible collection of absent neighbours.
                for zeros in combinations(ns,len(ns)-required+1):clauses.append(guard+[var[w] for w in zeros])
        if fixed>4:continue
        high,low=top+1,top+2;top+=2;k=5-fixed
        if k>len(ns):clauses.append([-high])
        else:
            for zeros in combinations(ns,len(ns)-k+1):clauses.append([-high]+[var[w] for w in zeros])
            for ones in combinations(ns,k):clauses.append([high]+[-var[w] for w in ones])
        if v in var:clauses.extend([[-low,var[v]],[-low,-high],[-var[v],high,low]])
        else:clauses.extend([[low,high],[-low,-high]])
    counter=[]
    for i in range(len(u)+1):
        row=[]
        for j in range(budget+2):top+=1;row.append(top)
        counter.append(row)
    clauses.extend([[row[0]] for row in counter])
    clauses.extend([[-counter[0][j]] for j in range(1,budget+2)])
    for i,v in enumerate(u,1):
        for j in range(1,budget+2):
            prev=counter[i-1][j];smaller=counter[i-1][j-1];out=counter[i][j];x=var[v]
            clauses.extend([[-prev,out],[-smaller,-x,out],[-out,prev,smaller],[-out,prev,x]])
    clauses.append([-counter[-1][budget+1]])
    raw=(f'p cnf {top} {len(clauses)}\n'+''.join(' '.join(map(str,cl))+' 0\n' for cl in clauses)).encode('ascii')
    return raw,top,len(clauses)


def inspect(cert,candidate,g,manifest):
    need(cert['gallai_cuts']==[],'this certificate uses no learned Gallai cuts')
    need(cert['mandatory_added']==[310,393,578] and cert['lower_bound_budget']==8,'fixed bound scope')
    pairs=cert['disjoint_cover_pairs'];need(len(pairs)==9,'nine pairs')
    need(all(len(p)==2 and p==sorted(set(p)) and p in g['covers'] for p in pairs),'pair clauses')
    need(len({v for p in pairs for v in p})==18,'pairwise disjointness')
    sources=[]
    for pair in pairs:
        at=next(i for i,support in enumerate(g['positive_sets']) if g['v0']-support==set(pair))
        sources.append(g['provenance'][at])
    w=cert['witness'];selected=w['selected_optional']
    need(selected==sorted(set(selected)) and set(selected)<=set(g['u']) and len(selected)==9,'attaining selector set')
    need(all(set(selected)&set(cl) for cl in g['covers']),'attaining cover intersections')
    support=g['m']|set(selected);ds={v:len(g['adj'][v]&support) for v in support}
    need(min(ds.values())>=4,'attaining minimum degree')
    low=sorted(v for v in support if ds[v]==4)
    low_edges=[[a,b] for a,b in g['edges'] if a in low and b in low]
    need(low==w['low_vertices'] and low_edges==w['low_edges']==[],'independent low vertices')
    need(w['low_blocks']==[[v] for v in low] and w['bad_blocks']==[],'full Gallai upper witness')
    need(w['vertices']==len(support)==504,'504 attaining support')
    need(candidate['status']=='FOUR_COLOURABLE' and candidate['record_improvement'] is False,'candidate scope')
    text=candidate['colouring'];need(len(text)==632,'candidate colour length')
    cs={v:c for v,c in enumerate(text) if c!='.'};edge_checks=proper(cs,support,g['host_edges'])
    need(edge_checks==candidate['unit_edges'] and candidate['vertices']==504,'candidate graph dimensions')
    need(set(candidate['selected_optional'])==set(selected)|{310,393,578},'candidate selectors')
    # Count actual subsets, rather than choices of representatives from doubled pairs.
    terms=[comb(9,d)*2**(9-d)*comb(39,4-d) for d in range(5)]
    need(sum(terms)==cert['outer_exact508_support_count'] and cert['outer_family_only'] is True,'outer-family count')
    raw,nv,nc=lower_cnf(g,8)
    need(sha(raw)==manifest['cnf_sha256'] and len(raw)==manifest['cnf_bytes'],'independent lower CNF bytes')
    need((nv,nc)==(manifest['variables'],manifest['clauses']),'independent lower CNF dimensions')
    return {'mandatory_vertices':495,'remaining_optional_vertices':57,'input_positive_covers':45,
            'positive_cover_edge_checks':g['cover_edge_checks'],'irredundant_cover_clauses':len(g['covers']),
            'disjoint_pair_clauses':pairs,'pair_certificate_sources':sources,'minimum_screen_optional_count':9,
            'screen_optimum_verified_without_solver':True,'every_H560_subgraph_at_most_503_four_colourable':True,
            'attaining_support_vertices':504,'attaining_support_unit_edges':edge_checks,'attaining_support_four_colourable':True,
            'attaining_minimum_degree':min(ds.values()),'attaining_low_vertices':low,'attaining_low_edges':0,
            'outer_exact508_supports':sum(terms),'outer_count_terms_by_double_pairs':terms,
            'previous_M495_exact508_domain':comb(57,13),'outer_family_is_unclassified_count':False,
            'lower_cnf_sha256':sha(raw),'lower_cnf_variables':nv,'lower_cnf_clauses':nc,
            'host_pairs_reconstructed':199396,'whole_at_most508_family_closed':False,'record_improvement':False},raw


def controls(cert,candidate,g,manifest):
    changes=[]
    x=copy.deepcopy(cert);x['disjoint_cover_pairs'][1]=x['disjoint_cover_pairs'][0];changes.append((x,candidate))
    x=copy.deepcopy(cert);x['disjoint_cover_pairs'][0]=[358,379];changes.append((x,candidate))
    x=copy.deepcopy(cert);x['witness']['selected_optional'].pop();changes.append((x,candidate))
    x=copy.deepcopy(cert);x['witness']['low_vertices'].pop();changes.append((x,candidate))
    x=copy.deepcopy(cert);x['outer_exact508_support_count']+=1;changes.append((x,candidate))
    y=copy.deepcopy(candidate);y['colouring']='0'*632;changes.append((cert,y))
    y=copy.deepcopy(candidate);y['record_improvement']=True;changes.append((cert,y))
    for x,y in changes:
        try:inspect(x,y,g,manifest)
        except (ValueError,StopIteration):continue
        raise ValueError('mutated certificate accepted')
    # The recurrence is exact in all four input/output bits.
    local=0
    for a,b,x,z in product([False,True],repeat=4):
        need(all([not a or z,not b or not x or z,not z or a or b,not z or a or x])==(z==(a or(b and x))),'counter local truth');local+=1
    # Check the combinatorial count independently on smaller disjoint-pair families.
    count_cases=0
    for pairs in range(1,5):
        for outside in range(5):
            for extra in range(4):
                target=pairs+extra;n=2*pairs+outside
                observed=sum(all(2*i in chosen or 2*i+1 in chosen for i in range(pairs)) for chosen in map(set,combinations(range(n),target)))
                expected=sum(comb(pairs,d)*2**(pairs-d)*comb(outside,extra-d) for d in range(min(pairs,extra)+1) if extra-d<=outside)
                need(observed==expected,'disjoint pair count');count_cases+=1
    return {'mutations_rejected':len(changes),'counter_truth_cases':local,'small_pair_family_counts':count_cases}


def limits():
    resource.setrlimit(resource.RLIMIT_AS,(4*1024**3,4*1024**3));resource.setrlimit(resource.RLIMIT_FSIZE,(512*1024**2,512*1024**2))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True)
    modes=ap.add_mutually_exclusive_group();modes.add_argument('--archive',type=Path);modes.add_argument('--prove',action='store_true')
    ap.add_argument('--kissat',default='/scratch/researcher3-kissat/build/kissat');ap.add_argument('--drat-trim',default='/scratch/drat-trim-package/usr/bin/drat-trim')
    args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=False)
    cert=json.loads((HERE/'certificate.json').read_text());candidate=json.loads((HERE/'candidate.json').read_text());manifest=json.loads((HERE/'proof_manifest.json').read_text())
    g=prepare();report,raw=inspect(cert,candidate,g,manifest);report.update(controls(cert,candidate,g,manifest))
    cnf=args.out/'lower.cnf';cnf.write_bytes(raw);report['additional_drat_check']=False
    if args.archive or args.prove:
        if args.prove:
            proof=args.out/'lower.drat'
            with (args.out/'kissat.log').open('wb') as log:
                r=subprocess.run([args.kissat,'--seed=0','--conflicts=4000000','--time=180',str(cnf),str(proof)],stdout=log,stderr=subprocess.STDOUT,timeout=200,preexec_fn=limits)
            need(r.returncode==20,'fresh lower proof')
        else:
            proof=args.archive/'lower.drat';need(sha(proof.read_bytes())==manifest['proof_sha256'],'archived proof identity')
        with (args.out/'drat.log').open('wb') as log:
            r=subprocess.run([args.drat_trim,str(cnf),str(proof)],stdout=log,stderr=subprocess.STDOUT,timeout=200,preexec_fn=limits)
        need(r.returncode==0 and b's VERIFIED' in (args.out/'drat.log').read_bytes().splitlines(),'independent DRAT')
        report['additional_drat_check']=True;report['proof_sha256']=sha(proof.read_bytes())
    (args.out/'result.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print(json.dumps(report,sort_keys=True))


if __name__=='__main__':main()
