"""Positive graph, component-predicate and damaged-input controls."""
import argparse
import copy
import itertools
import json
from pathlib import Path
import random

import blocks
import complete
import independent
import verify


def require(condition,message):
    if not condition:
        raise RuntimeError(message)


def fixture_specs():
    rng = random.Random(10520261001)
    for k in range(24):
        yield dict(internal=[rng.randrange(2) for _ in range(7)],
                   cross=[rng.randrange(8) for _ in range(21)],
                   joins=None if k%2==0 else [1,1,1,0,0,0,0])
    kg,_,_ = blocks.kg_control()
    for bit in range(70):
        spec = copy.deepcopy(kg)
        spec['joins'] = [1,1,1,0,0,0,0]
        if bit<7:
            spec['internal'][bit] ^= 1
        else:
            pair,offset = divmod(bit-7,3)
            spec['cross'][pair] ^= 1<<offset
        yield spec


def components(rows):
    local = [rows[a]&511 for a in range(9)]
    columns = tuple(rows[b]&511 for b in range(9,21))
    bgraph = tuple(rows[b]>>9&4095 for b in range(9,21))
    return local,columns,bgraph


def literal_component_pages(prepared,bgraph):
    local,columns,stars,_,_ = prepared
    counts = {}
    for a in range(9):
        counts[a,21] = local[a].bit_count()
    for b in range(12):
        counts[b+9,21] = 11-bgraph[b].bit_count()
    for u,v in independent.PAIRS_A:
        if local[u]>>v&1:
            count = (local[u]&local[v]).bit_count()+(stars[u]&stars[v]).bit_count()+1
        else:
            count = (511^(local[u]|local[v]|(1<<u)|(1<<v))).bit_count()
            count += (4095^(stars[u]|stars[v])).bit_count()
        counts[u,v] = count
    for u,v in independent.POINT_PAIRS_B:
        if bgraph[u]>>v&1:
            count = (bgraph[u]&bgraph[v]).bit_count()+(columns[u]&columns[v]).bit_count()
        else:
            count = (4095^(bgraph[u]|bgraph[v]|(1<<u)|(1<<v))).bit_count()
            count += (511^(columns[u]|columns[v])).bit_count()+1
        counts[u+9,v+9] = count
    for a in range(9):
        for b in range(12):
            if columns[b]>>a&1:
                count = (local[a]&columns[b]).bit_count()+(stars[a]&bgraph[b]).bit_count()
            else:
                count = (511^(local[a]|columns[b]|(1<<a))).bit_count()
                count += (4095^(stars[a]|bgraph[b]|(1<<b))).bit_count()
            counts[a,b+9] = count
    return counts


def expect_rejected(callback,message):
    try:
        callback()
    except (ValueError,RuntimeError,TypeError,KeyError):
        return
    raise RuntimeError('damaged input accepted: '+message)


def run(cases,roots):
    kg,labels,positive = blocks.kg_control()
    require(positive==verify.summary(verify.block_rows(kg)) and positive['caps_valid'],'KG positive control')
    checked_spines = 210
    graph_count = 1
    component_spines = 0
    for spec in fixture_specs():
        rows = verify.block_rows(spec)
        literal = verify.summary(rows)
        direct = blocks.literal_summary(blocks.graph(spec))
        require(literal==direct,'edge-orbit versus pair-predicate graph construction')
        checked_spines += len(rows)*(len(rows)-1)//2
        graph_count += 1
        if len(rows)!=22:
            continue
        local,columns,bgraph = components(rows)
        prepared = independent.prepare_components(local,columns)
        require(independent.accepts_completion(prepared,bgraph)==literal['caps_valid'],'independent component acceptance')
        require((complete.bad_spine(rows) is None)==literal['caps_valid'],'primary full spine predicate')
        counts = literal_component_pages(prepared,bgraph)
        require(len(counts)==231,'component spine coverage')
        for u,v in itertools.combinations(range(22),2):
            red = bool(rows[u]>>v&1)
            truth = ((rows[u]&rows[v]) if red else ((1<<22)-1)^(rows[u]|rows[v]|(1<<u)|(1<<v))).bit_count()
            require(counts[u,v]==truth,'component page count differs at physical spine')
            component_spines += 1
        b_bad = any(9<=bad['spine'][0]<bad['spine'][1]<21 for bad in literal['violations'])
        signature = []
        for u,v in complete.SPINES_B:
            red = bool(bgraph[u]>>v&1)
            count = ((bgraph[u]&bgraph[v]) if red else 4095^(bgraph[u]|bgraph[v]|(1<<u)|(1<<v))).bit_count()
            signature.append((red,count))
        base = [row & ~(4095<<9) if 9<=i<21 else row for i,row in enumerate(rows)]
        require(complete.outside_spine_bad(dict(page_signature=signature),complete.known_outside_pages(base))==b_bad,
                'primary orbit screen differs from all physical B spines')
        profile = tuple(bgraph[3*i].bit_count() for i in range(4))
        full_b = [rows[9+3*i].bit_count() for i in range(4)]
        forcing = complete.forced_outside(base,profile,full_b)
        internal = sum(int(bgraph[3*i]>>(3*i+1)&1)<<i for i in range(4))
        masks = [sum(int(bgraph[3*i]>>(3*j+k)&1)<<k for k in range(3)) for i,j in complete.PAIRS]
        code = internal+sum(mask<<(4+3*p) for p,mask in enumerate(masks))
        force_reject = forcing is None or code&forcing[0]!=forcing[0] or bool(code&forcing[1])
        require(not force_reject or b_bad,'degree forcing falsely rejects a graph with valid B spines')
    primary = verify.summary(verify.read_rows(Path(__file__).with_name('primary21.rows')))
    require(primary['edges']==93 and primary['caps_valid'],'primary-literature positive control')
    require(primary['degrees_histogram']=={'8':4,'9':16,'10':1},'primary degree histogram')
    require(primary['red_histogram']=={'1':3,'2':33,'3':57} and primary['blue_histogram']=={'4':5,'5':44,'6':68},
            'primary spine histograms')
    dp = independent.incidence_minima()
    for size,table in dp.items():
        for total,minimum in table.items():
            q,r = divmod(total,12)
            require(minimum==12*q*(q-1)//2+r*q,'finite incidence DP versus convex minimum')
    damaged = []
    damaged.append(('missing degree placement',cases,copy.deepcopy(roots[:-1])))
    altered = copy.deepcopy(cases); altered[-1]=copy.deepcopy(altered[0])
    damaged.append(('duplicate incidence root',altered,roots))
    altered = copy.deepcopy(cases); altered[0]['code'] ^= 1
    damaged.append(('altered local root identifier',altered,roots))
    altered = copy.deepcopy(cases); altered[0]['degree_cycles'][0] += 1
    damaged.append(('forged degree cycle',altered,roots))
    altered = copy.deepcopy(cases); altered[0]['incidence_representatives'].pop()
    damaged.append(('omitted incidence without updated coverage declaration',altered,roots))
    altered = copy.deepcopy(cases); altered[0]['incidence_representatives'][0][0][0] = 8
    damaged.append(('invalid incidence mask',altered,roots))
    altered = copy.deepcopy(cases); altered[0]['incidence_representatives'][1] = copy.deepcopy(altered[0]['incidence_representatives'][0])
    damaged.append(('duplicate incidence template',altered,roots))
    for name,bad_cases,bad_roots in damaged:
        expect_rejected(lambda:independent.preflight(bad_cases,bad_roots),name)
    altered = copy.deepcopy(cases); altered[0]['incidence_representatives'][0][0][0] ^= 1
    independent.preflight(altered,roots)
    expect_rejected(lambda:independent.check_incidence_input(altered,roots),'validly shaped altered incidence')
    altered_roots = copy.deepcopy(roots)
    next(iter(altered_roots[0]['all_subsets_groups'].values())).pop()
    independent.preflight(cases,altered_roots)
    expect_rejected(lambda:independent.check_incidence_input(cases,altered_roots),'omitted labeled local word')
    return dict(status='CONTROLS_PASS',graph_controls=graph_count,literal_spines=checked_spines,
                component_spines=component_spines,primary21_spines=210,
                damaged_tables_rejected=len(damaged)+2,
                kg_pages=positive['red_histogram'],primary21_pages=[primary['red_histogram'],primary['blue_histogram']],
                all_incidence_minimum_DP_entries_match=True)


if __name__=='__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--roots',type=Path,required=True)
    parser.add_argument('--incidences',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args = parser.parse_args()
    result = run(json.loads(args.incidences.read_text()),json.loads(args.roots.read_text()))
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
