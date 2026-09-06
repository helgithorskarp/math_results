"""Definition-level positive certificate check and independent paired DFS."""
import argparse
from collections import Counter
import copy
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import sys
import time

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
sys.path.insert(0,str(REPO/'hadwiger_nelson_heule632_pair_pilot'))
import independent as I


def need(ok,why):
    if not ok:raise ValueError(why)


def sha(raw):return hashlib.sha256(raw).hexdigest()


def proper(word,active,edges):
    need(len(word)==632 and set(word)<=set('.0123'),'colour word alphabet')
    need({v for v,c in enumerate(word) if c!='.'}==active,'exact colour domain')
    checks=0
    for u,v in edges:
        if u in active and v in active:
            need(word[u]!=word[v],'unit edge inequality');checks+=1
    return checks


def prepare():
    plan=json.loads((HERE/'plan.json').read_text())
    for path,digest in plan['input_files'].items():need(sha((REPO/path).read_bytes())==digest,('input identity',path))
    points,edges,_=I.geometry()
    boundary=json.loads((REPO/'hadwiger_nelson_heule632_minimize/boundary.json').read_text())
    seed=json.loads((REPO/'hadwiger_nelson_heule632_minimize/certificate.json').read_text())
    m492=set(boundary['mandatory_vertices']);v560=set(seed['retained'])
    need(len(m492)==492 and len(v560)==560 and v560==m492|set(boundary['optional_vertices']),'old exact support')
    earlier=json.loads((REPO/'hadwiger_nelson_heule560_cylinder508/expected.json').read_text())
    packing=earlier['global_corollary']['disjoint_omission_sets']
    additions=sorted(cut[0] for cut in packing if len(cut)==1);pairs=[tuple(cut) for cut in packing if len(cut)==2]
    need(additions==[310,393,454,539,578,615] and additions==plan['mandatory_additions'],'six mandatory additions')
    need(list(map(list,pairs))==plan['disjoint_pairs'] and len(pairs)==9,'nine prior pairs')
    base=m492|set(additions);optional=sorted(v560-base);erase={510,512,513,520,521,523,524,535};free=sorted(set(optional)-erase)
    need(len(base)==498 and len(optional)==62 and len(free)==54,'selector domains')
    need(len(set.union(*map(set,pairs)))==18 and set.union(*map(set,pairs))<=set(optional),'disjoint optional pairs')
    parent=json.loads((REPO/'hadwiger_nelson_heule560_global_decision/certificate.json').read_text())
    sep=json.loads((REPO/'hadwiger_nelson_heule560_separator/certificate.json').read_text())
    rel=json.loads((REPO/'hadwiger_nelson_heule560_left_relation/certificate.json').read_text())
    table={row['state']:row['colouring'] for row in sep['blocks']['full']['states']};without310=dict(table)
    for row in rel['rows']:
        if not row['inherited_full']:without310[row['state']]=next(p['colouring'] for p in row['positive_covers'] if p['mask']==510)
    q=sep['separator'];right=parent['right_vertices'];left=sep['blocks']['full']['vertices']
    need(q==parent['separator'] and set(q)<=m492,'separator identity')
    need(set(right)-base==set(free) and len(right)==196 and len(table)==20,'right formula domain')
    return locals()


def lift_right(word,active,g):
    cs={v:c for v,c in zip(g['right'],word) if c!='.'};state=''.join(cs[v] for v in g['q'])
    table=g['table'] if 310 in active else g['without310'];need(state in table,'explicit left word exists')
    colors={v:c for v,c in zip(g['left'],table[state]) if v in active}
    need(all(colors[v]==cs[v] for v in g['q']),'left/right agreement');colors.update(cs)
    full=''.join(colors.get(v,'.') for v in range(632));count=proper(full,active,g['edges']);return full,count


def inherited(g):
    words=[];checks=0;opt=g['parent']['optional_order']
    for row in g['parent']['positive_covers']:
        cut={v for i,v in enumerate(opt) if row['mask']//2**i%2==0}
        word,n=lift_right(row['colouring'],g['v560']-cut,g);words.append(word);checks+=n
    previous=json.loads((REPO/'hadwiger_nelson_heule560_cylinder508/certificate.json').read_text())
    for row in previous['covers']:
        active={v for v,c in enumerate(row['colouring']) if c!='.'}|g['erase']
        word,n=lift_right(''.join(row['colouring'][v] for v in g['right']),active,g);words.append(word);checks+=n
    need(len(words)==40,'forty inherited witnesses')
    cuts=[g['v560']-{v for v,c in enumerate(word) if c!='.'} for word in words]
    provenance=[]
    for cut in [set([v]) for v in g['additions']]+list(map(set,g['pairs'])):
        need(cut in cuts,'checked complement for each necessity')
        provenance.append({'omitted':sorted(cut),'inherited_cover_index':cuts.index(cut)})
    need(all(not set(r['omitted'])&g['m492'] for r in provenance),'packing outside M492')
    return words,checks,provenance


def inspect(cert,g):
    need(cert['mandatory_additions']==g['additions'] and cert['disjoint_pairs']==list(map(list,g['pairs'])),'fixed packing labels')
    need(cert['necessary_exact508_supports']==24832,'complete family scope')
    need(cert['entire_H560_through508_four_colourable'] is True and cert['record_improvement'] is False,'claim flags')
    words=cert['new_H560_colourings'];need(len(words)==2 and len(set(words))==2,'two distinct new witnesses')
    checks=0;supports=[]
    for word in words:
        active={v for v,c in enumerate(word) if c!='.'}
        need(g['base']|g['erase']<=active<=g['v560'],'new H560 cover domain')
        checks+=proper(word,active,g['edges']);supports.append(active)
    need(not supports[0]<=supports[1] and not supports[1]<=supports[0],'distinct cover supports')
    return words,checks,supports


def paired_dfs(universe,pairs,k):
    """Include/exclude every optional label, pruning only impossible prefixes.

    Each unhit pair requires a further distinct selected vertex. A pair whose
    last endpoint has passed can never be hit. These and cardinality bounds
    are the only prunings; the producer's two-case decomposition is not used.
    """
    universe=tuple(universe);n=len(universe);index={v:i for i,v in enumerate(universe)}
    pair_of={v:j for j,pair in enumerate(pairs) for v in pair}
    last=[max(index[v] for v in pair) for pair in pairs];complete=(1<<len(pairs))-1;rows=[]
    def visit(pos,chosen,hit):
        if len(chosen)==k:
            if hit==complete:rows.append(tuple(chosen))
            return
        if pos==n or len(chosen)+n-pos<k:return
        missing=complete^hit
        if len(chosen)+missing.bit_count()>k:return
        if any(missing>>j&1 and end<pos for j,end in enumerate(last)):return
        v=universe[pos];bit=0 if v not in pair_of else 1<<pair_of[v]
        visit(pos+1,chosen+[v],hit|bit);visit(pos+1,chosen,hit)
    visit(0,[],0);return rows


def classify(g,words):
    rows=paired_dfs(g['optional'],g['pairs'],10)
    need(len(rows)==24832 and rows==sorted(set(rows)),'entire labelled DFS family')
    supports=[{v for v,c in enumerate(word) if c!='.'} for word in words]
    hits=Counter();classes=Counter();outside=[];assignment=bytearray()
    for i,row in enumerate(rows):
        chosen=set(row);active=g['base']|chosen
        need(len(active)==508 and all(chosen&set(pair) for pair in g['pairs']),'literal family member')
        double=sum(set(pair)<=chosen for pair in g['pairs']);classes[double]+=1
        hit=next((j for j,support in enumerate(supports) if active<=support),None)
        need(hit is not None,'every necessary target has a checked colouring')
        if hit>=40:outside.append(i)
        hits[hit]+=1;assignment.extend(hit.to_bytes(2,'little'))
    need(classes=={0:22528,1:2304},'independent two-case multiplicities')
    raw=''.join(','.join(map(str,row))+'\n' for row in rows).encode()
    return rows,bytes(assignment),raw,dict(hits),outside,dict(classes)


def oracle(g):
    right=g['right'];ix={v:i for i,v in enumerate(right)};cv=lambda v,c:4*ix[v]+c+1
    selector={v:4*len(right)+j+1 for j,v in enumerate(g['free'])};nv=4*len(right)+len(selector);clauses=[]
    for v in right:
        names=[cv(v,c) for c in range(4)];clauses.append(names)
        for a,b in combinations(names,2):clauses.append([-a,-b])
    for u,v in g['edges']:
        if u not in ix or v not in ix:continue
        for c in range(4):clauses.append([-selector[w] for w in (u,v) if w in selector]+[-cv(u,c),-cv(v,c)])
    gates=[]
    for state in g['table']:
        nv+=1;gates.append(nv)
        for v,c in zip(g['q'],state):clauses.append([-nv,cv(v,int(c))])
    clauses.append(gates)
    raw=(f'p cnf {nv} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)).encode()
    return raw,nv,len(clauses)


def controls(cert,g):
    bad=[]
    c=copy.deepcopy(cert);c['new_H560_colourings'].pop();bad.append(c)
    c=copy.deepcopy(cert);word=list(c['new_H560_colourings'][0]);u,v=next((u,v) for u,v in g['edges'] if word[u]!='.' and word[v]!='.');word[v]=word[u];c['new_H560_colourings'][0]=''.join(word);bad.append(c)
    c=copy.deepcopy(cert);word=list(c['new_H560_colourings'][0]);word[min(g['base'])]='.';c['new_H560_colourings'][0]=''.join(word);bad.append(c)
    c=copy.deepcopy(cert);c['new_H560_colourings'][1]=c['new_H560_colourings'][0];bad.append(c)
    c=copy.deepcopy(cert);c['disjoint_pairs'][0]=c['disjoint_pairs'][1];bad.append(c)
    c=copy.deepcopy(cert);c['mandatory_additions'].pop();bad.append(c)
    c=copy.deepcopy(cert);c['entire_H560_through508_four_colourable']=False;bad.append(c)
    c=copy.deepcopy(cert);c['record_improvement']=True;bad.append(c)
    for c in bad:
        try:inspect(c,g)
        except ValueError:continue
        raise ValueError('invalid certificate accepted')
    cases=0;members=0
    for p in range(5):
        for b in range(5):
            n=2*p+b
            if n>10:continue
            pairs=[(2*j,2*j+1) for j in range(p)]
            for k in range(n+1):
                actual=paired_dfs(range(n),pairs,k)
                expected=[s for s in combinations(range(n),k) if all(set(s)&set(pair) for pair in pairs)]
                need(actual==expected,'DFS versus unpruned exhaustive combinations');cases+=1;members+=len(actual)
    guards=0
    for a,b in product([False,True],repeat=2):
        for s,t,x,y in product([False,True],repeat=4):
            clause=(a and not s) or (b and not t) or not x or not y
            need(clause==(not((s or not a) and (t or not b) and x and y)),'guard truth');guards+=1
    return {'invalid_certificates_rejected':len(bad),'exhaustive_small_paired_cases':cases,'exhaustive_small_paired_members':members,'guard_truth_cases':guards}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=False)
    start=time.monotonic();g=prepare();old,old_checks,provenance=inherited(g)
    cert=json.loads((HERE/'certificate.json').read_text());new,new_checks,supports=inspect(cert,g)
    rows,assignment,familyraw,hits,residual,classes=classify(g,old+new);raw,nv,nc=oracle(g)
    run=json.loads((HERE/'run_summary.json').read_text())
    need(sha(raw)==run['oracle_sha256'] and len(raw)==run['oracle_bytes'] and (nv,nc)==(run['oracle_variables'],run['oracle_clauses']),'executed oracle bytes')
    need(sha(familyraw)==run['family_sha256'] and sha(assignment)==run['coverage_sha256'],'entrywise family and cover witness agreement')
    need({str(k):v for k,v in hits.items()}==run['first_cover_counts'] and len(residual)==run['outside_40_inherited_covers'],'all producer classifications')
    report={'necessary_exact508_supports':len(rows),'case_one_from_each_plus_outside':classes[0],'case_one_doubled_pair':classes[1],
            'outside_40_inherited_covers':len(residual),'new_cover_first_assignments':[hits.get(40,0),hits.get(41,0)],
            'remaining_targets':0,'inherited_positive_colourings':40,'new_positive_colourings':2,
            'new_omission_sets':[sorted(g['v560']-s) for s in supports],'new_H560_cover_orders':list(map(len,supports)),
            'inherited_positive_unit_edge_checks':old_checks,'new_positive_unit_edge_checks':new_checks,
            'mandatory_vertices':len(g['base']),'optional_vertices_original':len(g['optional']),
            'necessity_witness_provenance':provenance,'family_sha256':sha(familyraw),'coverage_sha256':sha(assignment),'first_cover_counts':hits,
            'oracle_variables':nv,'oracle_clauses':nc,'oracle_sha256':sha(raw),'exact_host_pairs':199396,'exact_host_unit_edges':len(g['edges']),
            'entire_H560_through508_four_colourable':True,'non_four_colourable_H560_order_at_least':509,'record_improvement':False,
            'imported_theorem':'Accepted M492 singleton-deletion mandatory theorem. The six added singleton and nine pair necessities are directly rechecked from proper full-H560 colourings.',
            'solver_or_separator_completeness_needed_for_positive_proof':False,**controls(cert,g)}
    for name,data in [('result.json',report),('timing.json',{'seconds':time.monotonic()-start})]:(args.out/name).write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
    (args.out/'family.txt').write_bytes(familyraw);(args.out/'coverage.bin').write_bytes(assignment);(args.out/'oracle.cnf').write_bytes(raw)
    print(json.dumps(report,sort_keys=True))


if __name__=='__main__':main()
