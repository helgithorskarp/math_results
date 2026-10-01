"""Producer-free literal rebuild, complete set search and point bijections."""
from collections import Counter
from itertools import combinations, permutations, product
from pathlib import Path
import argparse
import json
import resource
import time

from common import Guard, Incomplete, HERE, WORK, digest, encoded, require


def literal_model(name):
    if name == 'isolated':
        n=4
        missing={(i,i) for i in range(4)}
    else:
        n=5
        # Complement generated from alternating-cycle edge lists.
        cycles=[(tuple(range(5)),tuple(range(5)))] if name=='cycle10' else [((0,1),(0,1)),((2,3,4),(2,3,4))]
        require(name in ('cycle10','cycle6_cycle4'),'unknown model')
        missing=set()
        for rows,cols in cycles:
            for k,row in enumerate(rows):
                missing.add((row,cols[k]))
                missing.add((row,cols[(k+1)%len(cols)]))
    occupied=sorted(set(product(range(n),repeat=2))-missing)
    rows=[tuple(x for x,c in enumerate(occupied) if c[0]==i) for i in range(n)]
    cols=[tuple(x for x,c in enumerate(occupied) if c[1]==j) for j in range(n)]
    anchors=([tuple(sorted(q+(15,))) for q in rows]+[tuple(sorted(q+(16,))) for q in cols])
    if n==4:
        anchors.insert(0,(12,13,15,16))
    require(all(len(q)==4 for q in anchors),'anchor size')
    used=Counter(e for q in anchors for e in combinations(q,2))
    require(set(used.values())=={1},'anchor repeated pair')
    eligible=tuple(e for e in combinations(range(15),2) if not used[e])
    candidates=tuple(q for q in combinations(range(15),4) if not any(used[e] for e in combinations(q,2)))
    lookup={c:x for x,c in enumerate(occupied)}
    row_neighbors=[{j for i,j in occupied if i==k} for k in range(n)]
    col_neighbors=[{i for i,j in occupied if j==k} for k in range(n)]
    actual_maps=set()
    for row_image in permutations(range(n)):
        for transpose in (False,True):
            source_neighbors=row_neighbors if transpose else col_neighbors
            choices=[[j for j in range(n) if col_neighbors[j]=={row_image[i] for i in source_neighbors[k]}]
                     for k in range(n)]
            for col_image in product(*choices):
                if len(set(col_image))!=n:
                    continue
                mapping=tuple(lookup[(row_image[j],col_image[i]) if transpose else (row_image[i],col_image[j])]
                              for i,j in occupied)
                for extra in (((12,13,14),(13,12,14)) if n==4 else ((),)):
                    p=mapping+extra+((16,15) if transpose else (15,16))
                    require(len(p)==17 and set(p)==set(range(17)) and
                            {tuple(sorted(p[x] for x in q)) for q in anchors}==set(anchors),'bad literal map')
                    actual_maps.add(p)
    maps=tuple(sorted(actual_maps))
    require(all(tuple(a[b[x]] for x in range(17)) in actual_maps for a in maps for b in maps),'literal group closure')
    return {'name':name,'cells':tuple(occupied),'anchors':tuple(anchors),'eligible':eligible,
            'pool':candidates,'maps':maps}


def matrix_coverage(models):
    choices=tuple(combinations(range(5),2))
    raw=set()
    guard=Guard()
    for rows in product(choices,repeat=5):
        guard.tick()
        if all(sum(j in row for row in rows)==2 for j in range(5)):
            raw.add(tuple((i,j) for i,row in enumerate(rows) for j in row))
    require(len(raw)==2040,'binary matrix census')
    seen=set()
    sizes={}
    for name in ('cycle10','cycle6_cycle4'):
        cells=models[name]['cells']
        missing=set(product(range(5),repeat=2))-set(cells)
        orbit={tuple(sorted((a[i],b[j]) for i,j in missing)) for a in permutations(range(5)) for b in permutations(range(5))}
        require(orbit<=raw and not orbit&seen,'matrix orbit escape or overlap')
        seen|=orbit;sizes[name]=len(orbit)
    require(seen==raw and sizes=={'cycle10':1440,'cycle6_cycle4':600},'incomplete matrix coverage')
    return {'labeled_matrices':2040,'orbits':sizes,'state_visits':guard.nodes}


def inputs(model):
    used=set(e for q in model['anchors'] for e in combinations(q,2))
    maps=model['maps']
    if model['name']=='isolated':
        raw=list(combinations(range(14),4))
        def image(value,p):
            return tuple(sorted(p[x] for x in value))
    else:
        raw=[(pattern,high,special) for pattern in ('311','221')
             for high in combinations(range(15),3) for special in high]
        def image(value,p):
            return value[0],tuple(sorted(p[x] for x in value[1])),p[value[2]]
    buckets={}
    for value in raw:
        representative=min(image(value,p) for p in maps)
        buckets.setdefault(representative,[]).append(value)
    result=[]
    for value,orbit in sorted(buckets.items()):
        if model['name']=='isolated':
            others=set(value);highs=others|{14}
            target=[4 if x in highs else 5 for x in range(17)]
            R=sum(e in used for e in combinations(value,2))
            direct=R>2
            columns=tuple(q for q in model['pool'] if sum(set(e)<=others for e in combinations(q,2))<=2-R)
            mandatory=tuple(e for e in model['eligible'] if all(x not in highs for x in e) or
                            (14 in e and set(e)<=highs))
        else:
            pattern,high,special=value
            deficits={x:(3 if x==special else 1) if pattern=='311' else
                      (1 if x==special else 2) for x in high}
            target=[5-deficits.get(x,0) for x in range(17)]
            R=sum(e in used for e in combinations(high,2));direct=R>0
            columns=tuple(q for q in model['pool'] if all(not set(e)<=set(high) for e in combinations(q,2)))
            mandatory=tuple(e for e in model['eligible'] if all(x not in high for x in e))
        rep=Counter(x for q in model['anchors'] for x in q)
        quota=tuple(target[x]-rep[x] for x in range(15))
        require(min(quota)>=0 and sum(quota)==(44 if model['name']=='isolated' else 40),'literal quota')
        result.append({'key':value,'orbit':sorted(orbit),'quota':quota,'mandatory':mandatory,
                       'columns':columns,'direct':direct,'anchor_high_pairs':R})
    require(sum(len(r['orbit']) for r in result)==len(raw),'literal quota carrier mass')
    return result


def literal_covers(eligible,columns,quota,mandatory,nodes=200000,seconds=10):
    require(len(quota)==15 and all(type(n) is int and n>=0 for n in quota),'bad literal quota')
    require(len(set(columns))==len(columns),'duplicated literal columns')
    universe=set(eligible);required=frozenset(mandatory)
    require(required<=universe,'bad mandatory pair')
    pairs=[]
    for q in columns:
        require(len(q)==4 and tuple(sorted(set(q)))==q and all(0<=x<15 for x in q),'bad literal quadruple')
        es=frozenset(combinations(q,2))
        require(es<=universe and bool(es&required),'bad or irrelevant literal column')
        pairs.append(es)
    answers=[];guard=Guard(nodes,seconds)

    def visit(left,need,free,selected):
        guard.tick()
        possible=[i for i,ps in enumerate(pairs) if ps<=free and all(left[x]>0 for x in columns[i])]
        if not need:
            if not any(left):
                answers.append(tuple(sorted(selected)))
            return
        for x,n in enumerate(left):
            if sum(x in columns[i] for i in possible)<n:
                return
        # Opposite tie/order conventions from the bitset producer.
        choices,e=min((([i for i in possible if e in pairs[i]],e) for e in need),
                      key=lambda item:(len(item[0]),tuple(-x for x in item[1])))
        for i in reversed(choices):
            remaining=list(left)
            for x in columns[i]:remaining[x]-=1
            visit(tuple(remaining),need-pairs[i],free-pairs[i],selected+(i,))

    visit(tuple(quota),required,frozenset(eligible),())
    require(len(set(answers))==len(answers),'literal duplicated cover')
    return sorted(answers),guard.nodes


def inspect_fixture(blocks,marked):
    require(len(blocks)==20 and len(set(blocks))==20,'fixture size')
    require(all(len(q)==4 and tuple(sorted(set(q)))==q and all(0<=x<17 for x in q) for q in blocks),'fixture block')
    rep=Counter(x for q in blocks for x in q)
    pair=Counter(e for q in blocks for e in combinations(q,2))
    require(sorted(rep.values())==[4]*5+[5]*12 and set(pair.values())=={1},'fixture profile or pair repetition')
    highs={x for x in range(17) if rep[x]==4}
    leave=set(combinations(range(17),2))-set(pair)
    core={e for e in leave if set(e)<=highs}
    require(marked in highs and len(core)==4 and all(marked not in e for e in core),'not an isolated high core')
    require(all(sum(x in e for e in core)==(0 if x==marked else 2) for x in highs),'covered complement not C4')
    return rep,pair


def point_bijections(first,second,marked_first=14,marked_second=14):
    """Backtracking on literal incidence; no leave-cohort/group import."""
    rep1=Counter(x for q in first for x in q);rep2=Counter(x for q in second for x in q)
    pairs=[{e for q in f for e in combinations(q,2)} for f in (first,second)]
    triples=[{e for q in f for e in combinations(q,3)} for f in (first,second)]
    mapping={marked_first:marked_second};used={marked_second};output=[];guard=Guard()
    highs={x for x in range(17) if rep1[x]==4}

    def choices(x):
        out=[]
        for y in range(17):
            if y in used or rep1[x]!=rep2[y]:continue
            if any((tuple(sorted((x,z))) in pairs[0]) != (tuple(sorted((y,t))) in pairs[1]) for z,t in mapping.items()):continue
            if any((tuple(sorted((x,a,b))) in triples[0]) != (tuple(sorted((y,mapping[a],mapping[b]))) in triples[1])
                   for a,b in combinations(mapping,2)):continue
            out.append(y)
        return out

    def visit():
        guard.tick()
        if len(mapping)==17:
            p=tuple(mapping[x] for x in range(17))
            require({tuple(sorted(p[x] for x in q)) for q in first}==set(second),'full incidence map failure')
            output.append(p);return
        domain=[x for x in highs if x not in mapping] or [x for x in range(17) if x not in mapping]
        lists=[(choices(x),x) for x in domain]
        candidates,x=min(lists,key=lambda item:(len(item[0]),item[1]))
        for y in candidates:
            mapping[x]=y;used.add(y)
            visit()
            used.remove(y);del mapping[x]

    visit()
    return sorted(output),guard.nodes


def arithmetic_checks():
    triples=[]
    for mask in range(8):
        edges=[(0,1),(0,2),(1,2)]
        deg=[sum(bool(mask>>i&1) and x in e for i,e in enumerate(edges)) for x in range(3)]
        homogeneous=sum(d in (0,2) for d in deg)
        require(homogeneous==(3 if mask.bit_count() in (0,3) else 1),'triple incidence identity')
        triples.append(homogeneous)
    require([5-f for f in range(5) if f<=f*(f-1)//2]==[5,2,1],'deficit filter')
    patterns=sorted([a,b,c] for a in range(18) for b in range(18) for c in range(18)
                    if a+b+c==17 and a+2*b+5*c==25)
    require(patterns==[[9,8,0],[12,4,1],[15,0,2]],'one-unsaturated integer patterns')
    require(all(4*a+3*b==60 for a,b,c in patterns),'deficit graph edge count')
    require(816-710==106 and 136-6*15==46 and 106-46==60,'uncovered triple counts')
    return {'three_point_homogeneous_counts':triples,'near71_patterns':patterns}


def run(compare_primary=False):
    expected=json.loads((HERE/'expected.json').read_text())
    primary=json.loads((WORK/'producer.json').read_text()) if compare_primary else None
    models={name:literal_model(name) for name in ('cycle10','cycle6_cycle4','isolated')}
    coverage=matrix_coverage(models)
    all_positive=[];reports={};total_nodes=0;instance_records=[];solution_fibers=[]
    for name,model in models.items():
        records=inputs(model)
        if primary:
            for key in ('name','cells','anchors','eligible','pool','maps'):
                require(encoded(model[key])==encoded(primary['models'][name][key]),'actual model/map mismatch '+name+' '+key)
            require(len(records)==len(primary['models'][name]['cases']),'case count mismatch')
        solutions=0;positive_orbits=0;sol_records=[]
        for i,r in enumerate(records):
            if primary:
                pr=primary['models'][name]['cases'][i]
                for key in ('key','orbit','quota','mandatory','columns','direct','anchor_high_pairs'):
                    require(encoded(r[key])==encoded(pr[key]),'actual quota/column entry mismatch '+name+' '+str(i)+' '+key)
            covers,nodes=([],0) if r['direct'] else literal_covers(model['eligible'],r['columns'],r['quota'],r['mandatory'])
            total_nodes+=nodes;solutions+=len(covers)
            positive_orbits+=bool(covers);sol_records.append((r['key'],covers))
            if primary:
                require(encoded(covers)==encoded(pr['solutions']),'actual solution-fiber mismatch')
            if name!='isolated':require(not covers,'three-high missing-pair witness')
            for cover in covers:
                blocks=tuple(sorted(model['anchors']+tuple(r['columns'][i] for i in cover)))
                inspect_fixture(blocks,14)
                all_positive.append(blocks)
        summary=expected['models'][name]
        require(len(records)==summary['orbits'] and len(model['maps'])==summary['group_order'] and
                len(model['pool'])==summary['candidate_quadruples'] and
                sum(len(r['orbit']) for r in records)==summary['raw_inputs'] and
                sum(r['direct'] for r in records)==summary['direct_orbits'] and solutions==summary['solutions'] and
                sum(not r['direct'] for r in records)==summary['quota_cases'] and
                sum(len(r['orbit']) for r in records if not r['direct'])==summary['raw_quota_inputs'] and
                positive_orbits==summary['positive_orbits'],
                'compact carrier or solution count mismatch')
        instance_records.append(model|{'cases':records})
        solution_fibers.append({'name':name,'cases':sol_records})
        reports[name]={'orbits':len(records),'quota_cases':sum(not r['direct'] for r in records),'solutions':solutions}
    require(len(all_positive)==8,'complete isolated solution count')
    require(digest(instance_records)==expected['actual_instances_sha256'],'actual instance stream digest')
    require(digest(solution_fibers)==expected['actual_solution_fibers_sha256'],'actual solution fiber digest')
    canonical=tuple(tuple(q) for q in expected['isolated_canonical'])
    inspect_fixture(canonical,14)
    require(digest(canonical)==expected['canonical_sha256'],'canonical digest')
    bijection_nodes=0
    for packing in all_positive:
        maps,nodes=point_bijections(packing,canonical)
        require(len(maps)==8,'positive packing not in unique marked class')
        bijection_nodes+=nodes
    aut,nodes=point_bijections(canonical,canonical);bijection_nodes+=nodes
    require(len(aut)==expected['marked_automorphism_order']==8 and
            all(tuple(a[b[x]] for x in range(17)) in aut for a in aut for b in aut),'actual full aut group failure')
    historical_words='ABCD EFGH IJKL MNOP AEIM BFJN CGKO DHLP AHJO BGIP CFLM DEKN AGLN BHKM CEJP DFIO AFKP BELO CHIN DGJM'.split()
    historical=[]
    replacements={'ABCD':'BCD','EFGH':'FGH','AFKP':'AKP','BELO':'ELO'}
    for word in historical_words:
        chosen=replacements.get(word,word)
        b=tuple(ord(c)-65 for c in chosen)+((16,) if word in replacements else ())
        historical.append(tuple(sorted(b)))
    historical=tuple(sorted(historical))
    inspect_fixture(historical,16)
    require(digest(historical)==expected['historical_fixture_sha256'],'historical fixture digest')
    maps,nodes=point_bijections(historical,canonical,16,14);bijection_nodes+=nodes
    require(len(maps)==8,'historical construction outside marked class')
    if primary:
        require(encoded(aut)==encoded(primary['marked_automorphisms']),'actual marked automorphisms mismatch')
    checks=arithmetic_checks()
    require(checks['near71_patterns']==expected['near71_pair_deficit_counts_1_2_5'],'compact near71 count mismatch')
    require(expected['marked_isomorphism_classes']==1 and expected['near71_saturated_deficit_graph_edges']==30 and
            expected['near71_uncovered_triples_sat']==60 and
            expected['near71_uncovered_triples_through_unique_unsaturated']==46,'compact boundary summary mismatch')
    return {'agent':'six-code-3','role':'researcher','status':'COMPLETE','producer_imported':False,
            'entry_level_comparison':compare_primary,'models':reports,'literal_search_nodes':total_nodes,
            'bijection_nodes':bijection_nodes,'matrix_coverage':coverage,'arithmetic':checks,
            'marked_isomorphism_classes':1,'marked_automorphism_order':8,
            'independent_peer_review':False,'ordinary_bridges_formalized':False}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--compare-primary',action='store_true')
    args=parser.parse_args();started=time.monotonic()
    try:result=run(args.compare_primary)
    except Incomplete as error:
        print(json.dumps({'status':'INCOMPLETE','reason':str(error)}));raise SystemExit(3)
    result.update(seconds=time.monotonic()-started,maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    WORK.mkdir(parents=True,exist_ok=True);(WORK/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__':main()
