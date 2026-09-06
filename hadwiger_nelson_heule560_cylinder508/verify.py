"""Direct positive-cover proof for the cylinder and the order-506 corollary."""
import argparse
from collections import Counter
import copy
import hashlib
from itertools import combinations, product
import json
from math import comb
from pathlib import Path
import sys
import time

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
sys.path.insert(0,str(REPO/'hadwiger_nelson_heule632_pair_pilot'))
import independent as I

OLD_PAIRS=[[358,362],[361,379],[406,455],[407,440],[409,542],
           [431,505],[434,530],[500,571],[604,613]]
OLD_SINGLETONS=[310,393,578]


def need(ok,why):
    if not ok:raise ValueError(why)


def sha(raw):return hashlib.sha256(raw).hexdigest()


def proper(text,support,edges):
    need(len(text)==632 and set(text)<=set('.0123'),'colour string')
    need({v for v,c in enumerate(text) if c!='.'}==support,'exact colouring domain')
    count=0
    for u,v in edges:
        if u in support and v in support:
            need(text[u]!=text[v],'unit edge inequality');count+=1
    return count


def prepare():
    plan=json.loads((HERE/'plan.json').read_text())
    for name,digest in plan['input_files'].items():need(sha((REPO/name).read_bytes())==digest,('input identity',name))
    _,edges,_=I.geometry()
    boundary=json.loads((REPO/'hadwiger_nelson_heule632_minimize/boundary.json').read_text())
    m=set(boundary['mandatory_vertices']);v560=m|set(boundary['optional_vertices'])
    seed=json.loads((REPO/'hadwiger_nelson_heule632_minimize/certificate.json').read_text())
    need(v560==set(seed['retained']) and len(v560)==560,'original H560 domain')
    erase={510,512,513,520,521,523,524,535};v552=v560-erase
    parent=json.loads((REPO/'hadwiger_nelson_heule560_global_decision/certificate.json').read_text())
    expected=json.loads((REPO/'hadwiger_nelson_heule560_global_decision/expected.json').read_text())
    fixed=plan['base_optional'];need(fixed==expected['residual_required_vertices'],'published base')
    need(set(parent['optional_order'])==v552-m,'canonical selector domain')
    base=m|set(fixed);free=sorted(v552-base);all_free=sorted(v560-base)
    need(len(m)==492 and len(base)==504 and len(free)==48 and len(all_free)==56,'family sizes')
    sep=json.loads((REPO/'hadwiger_nelson_heule560_separator/certificate.json').read_text())
    rel=json.loads((REPO/'hadwiger_nelson_heule560_left_relation/certificate.json').read_text())
    full={r['state']:r['colouring'] for r in sep['blocks']['full']['states']}
    # Only explicit positive words are used. No old negative/completeness proof
    # is a premise of pasting and then checking a whole-graph colouring.
    no310={s:w for s,w in full.items()}
    for row in rel['rows']:
        if not row['inherited_full']:
            pos=next(p for p in row['positive_covers'] if p['mask']==510)
            no310[row['state']]=pos['colouring']
    right=parent['right_vertices'];q=parent['separator']
    need(q==sep['separator'] and set(q)<=m,'fixed separator')
    return {'plan':plan,'m':m,'v560':v560,'v552':v552,'base':base,'fixed':fixed,'free':free,'all_free':all_free,
            'erase':erase,'edges':edges,'parent':parent,'q':q,'right':right,'left':sep['blocks']['full']['vertices'],
            'full':full,'no310':no310}


def lift(cs,active,g):
    state=''.join(cs[v] for v in g['q'])
    table=g['full'] if 310 in active else g['no310']
    need(state in table,'explicit matching left witness')
    left={v:c for v,c in zip(g['left'],table[state]) if v in active}
    need(all(left[v]==cs[v] for v in g['q']),'pasted boundary')
    left.update(cs)
    text=''.join(left.get(v,'.') for v in range(632))
    count=proper(text,active,g['edges'])
    return text,count


def inspect(cert,g):
    need(cert['base_optional']==g['fixed'] and cert['free_optional']==g['free'],'fixed family labels and order')
    need(cert['choose_free']==4 and cert['family_size']==194580,'target family')
    need(cert['entire_defined_family_four_colourable'] is True and cert['record_improvement'] is False
         and cert['whole_h560_target_family_closed'] is False,'claim scope')
    need(len(cert['covers'])==5,'five covers')
    cuts=[];free_sets=[];new_checks=0;lifted_checks=0;sizes=[];lifted=[]
    for row in cert['covers']:
        mask=row['mask'];need(type(mask) is int and 0<=mask<2**48,'48-bit mask')
        chosen={v for i,v in enumerate(g['free']) if mask//2**i%2}
        support=g['base']|chosen;new_checks+=proper(row['colouring'],support,g['edges'])
        cut=set(g['free'])-chosen;need(cut,'proper positive cover')
        cs={v:row['colouring'][v] for v in g['right'] if v in support}
        text,count=lift(cs,g['v560']-cut,g);lifted_checks+=count;lifted.append(text)
        cuts.append(cut);free_sets.append(chosen);sizes.append(len(support))
    need(len(set.union(*cuts))==sum(map(len,cuts)),'five pairwise disjoint omission sets')
    need(all(not cut&g['base'] for cut in cuts),'omissions outside fixed base')
    return {'cuts':cuts,'free_sets':free_sets,'new_checks':new_checks,'lifted_checks':lifted_checks,'sizes':sizes,'lifted':lifted}


def enumerate_cover(universe,cuts):
    hits=Counter();stream=bytearray();count=0
    for vertices in combinations(universe,4):
        chosen=set(vertices)
        # Omission sets are read from the actual checked colouring domains.
        hit=next((i for i,cut in enumerate(cuts) if not chosen&cut),None)
        need(hit is not None,'every exact-508 extension has a proper witness')
        hits[hit]+=1;stream.append(hit);count+=1
    need(count==comb(len(universe),4),'complete labelled enumeration')
    return {'members':count,'first_cover_counts':[hits[i] for i in range(len(cuts))],'coverage_sha256':sha(stream)},bytes(stream)


def global_corollary(g,new):
    parent=g['parent'];opt=parent['optional_order'];old_sets=[{v} for v in OLD_SINGLETONS]+list(map(set,OLD_PAIRS))
    provenance=[];checks=0
    for cut in old_sets:
        i,row=next((i,r) for i,r in enumerate(parent['positive_covers'])
                   if {v for j,v in enumerate(opt) if not r['mask']//2**j%2}==cut)
        cs={v:c for v,c in zip(g['right'],row['colouring']) if c!='.'}
        need(''.join(cs[v] for v in g['q'])==row['state'],'old positive boundary')
        _,edges=lift(cs,g['v560']-cut,g);checks+=edges
        provenance.append({'omitted':sorted(cut),'global_positive_row':i})
    added=sorted(next(iter(cut)) for cut in new['cuts'] if len(cut)==1)
    need(added==[454,539,615],'new mandatory vertices')
    packing=old_sets+[{v} for v in added]
    need(len(packing)==15 and len(set.union(*packing))==sum(map(len,packing)),'fifteen disjoint omission sets')
    need(all(cut<=g['v560']-g['m'] for cut in packing),'all packing choices outside M492')
    # Accepted M492 mandatory theorem plus fifteen disjoint proper-colouring
    # complements gives at least 492+15=507 vertices in every obstruction.
    return {'old_positive_edges_checked_on_H560':checks,'old_cover_provenance':provenance,
            'new_mandatory_vertices':added,'mandatory_vertices_total':498,'disjoint_omission_sets':list(map(sorted,packing)),
            'non_four_colourable_H560_order_at_least':507,'every_H560_subgraph_at_most506_four_colourable':True,
            'imported_premise':'The accepted M492 singleton-deletion mandatory theorem; not recomputed here.',
            'separator_or_erasure_completeness_needed':False}


def oracle_cnf(g):
    right=g['right'];number={v:i for i,v in enumerate(right)};var=lambda v,c:4*number[v]+c+1
    sel={v:4*len(right)+i+1 for i,v in enumerate(g['free'])};top=4*len(right)+len(sel);clauses=[]
    for v in right:
        names=[var(v,c) for c in range(4)];clauses.append(names)
        for a,b in combinations(names,2):clauses.append([-a,-b])
    for u,v in g['edges']:
        if u not in number or v not in number:continue
        for c in range(4):clauses.append([-sel[w] for w in (u,v) if w in sel]+[-var(u,c),-var(v,c)])
    gates=[]
    for word in g['full']:
        top+=1;gates.append(top)
        for i,v in enumerate(g['q']):clauses.append([-top,var(v,int(word[i]))])
    clauses.append(gates)
    raw=(f'p cnf {top} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)).encode()
    return raw,top,len(clauses)


def controls(cert,g):
    altered=[]
    c=copy.deepcopy(cert);c['covers'].pop();altered.append(c)
    c=copy.deepcopy(cert);c['covers'][0]['mask']^=1;altered.append(c)
    c=copy.deepcopy(cert);word=list(c['covers'][0]['colouring'])
    u,v=next((u,v) for u,v in g['edges'] if word[u]!='.' and word[v]!='.');word[v]=word[u]
    c['covers'][0]['colouring']=''.join(word);altered.append(c)
    c=copy.deepcopy(cert);c['free_optional'].reverse();altered.append(c)
    c=copy.deepcopy(cert);c['base_optional'].pop();altered.append(c)
    c=copy.deepcopy(cert);c['entire_defined_family_four_colourable']=False;altered.append(c)
    c=copy.deepcopy(cert);c['record_improvement']=True;altered.append(c)
    c=copy.deepcopy(cert);c['covers'][-1]=copy.deepcopy(c['covers'][-2]);altered.append(c)
    for c in altered:
        try:inspect(c,g)
        except ValueError:continue
        raise ValueError('malformed certificate accepted')
    cover_cases=0
    for n in range(7):
        for k in range(n+1):
            for mask in range(2**n):
                kept={i for i in range(n) if mask>>i&1}
                for chosen in combinations(range(n),k):
                    bits=sum(1<<i for i in chosen)
                    need((bits&~mask==0)==(set(chosen)<=kept),'bit versus set cover control');cover_cases+=1
    gate_cases=0
    for optional_u,optional_v in product([False,True],repeat=2):
        for s,t,x,y in product([False,True],repeat=4):
            clause=(optional_u and not s) or (optional_v and not t) or not x or not y
            selected=(s or not optional_u) and (t or not optional_v)
            need(clause==(not(selected and x and y)),'guarded edge truth');gate_cases+=1
    return {'invalid_certificates_rejected':len(altered),'coverage_controls':cover_cases,'guard_truth_cases':gate_cases}


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);args=p.parse_args();args.out.mkdir(parents=True,exist_ok=False)
    start=time.monotonic();g=prepare();cert=json.loads((HERE/'certificate.json').read_text());new=inspect(cert,g)
    canonical,a=enumerate_cover(g['free'],new['cuts']);original,b=enumerate_cover(g['all_free'],new['cuts'])
    corollary=global_corollary(g,new);raw,nv,nc=oracle_cnf(g)
    run=json.loads((HERE/'run_summary.json').read_text())
    need(sha(raw)==run['oracle_sha256'] and len(raw)==run['oracle_bytes'] and (nv,nc)==(run['oracle_variables'],run['oracle_clauses']),'independent executed CNF bytes')
    report={'canonical_exact508_family':canonical,'original_H560_exact508_extensions':original,
            'base_vertices':504,'new_positive_covers':5,'omitted_sets':list(map(sorted,new['cuts'])),
            'new_cover_vertex_counts':new['sizes'],'new_G552_positive_edge_checks':new['new_checks'],
            'lifted_H560_positive_edge_checks':new['lifted_checks'],'exact_host_pairs':199396,
            'new_five_omission_sets_pairwise_disjoint':True,'global_corollary':corollary,
            'oracle_sha256':sha(raw),'oracle_variables':nv,'oracle_clauses':nc,
            'entire_defined_family_four_colourable':True,'whole_H560_at_most508_family_closed':False,'record_improvement':False,
            'positive_family_proof_needs_solver_or_imported_completeness':False,**controls(cert,g)}
    for name,data in [('result.json',report),('timing.json',{'seconds':time.monotonic()-start})]:
        (args.out/name).write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
    (args.out/'canonical_coverage.bin').write_bytes(a);(args.out/'original_coverage.bin').write_bytes(b);(args.out/'oracle.cnf').write_bytes(raw)
    print(json.dumps(report,sort_keys=True))


if __name__=='__main__':main()
