"""Independent fixed-size reconstruction and literal child-graph replay."""
import argparse
import base64
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCES = {
    'input': ('ramsey_r55_opposite22_realization/INPUT.json', 'ad40224bfefc36dbe387da389ca2c52c7ba95f823506ea4ba985bc8ed4d4902a'),
    'family': ('ramsey_r55_opposite22_realization/result.json', '0a2df58a3df138c6aec26cd73fb5b0bd104eb2fedb229827793c789c4c7e888e'),
    'H': ('ramsey_r55_root20_anchor_realization/GRAPH.json', '8d404855787227dc182d7bdc0e98751474ce6c9f1cf872abc52888477c096ccf'),
    'old_cases': ('ramsey_r55_marked_pair_decomposition/cases.json', 'c5dfb2f121e8b85fb4078f622257d4a6d924a3f81e055ded9f214d5ed9c89ef9'),
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def encoded(doc):
    return (json.dumps(doc, indent=2) + '\n').encode()


def parse_graph(doc):
    require(type(doc) is dict and set(doc) == {'n','red_edges'}, 'graph fields')
    n = doc['n']
    require(type(n) is int and 0 <= n <= 22 and type(doc['red_edges']) is list, 'graph order/edges')
    edges = []
    for pair in doc['red_edges']:
        require(type(pair) is list and len(pair) == 2 and all(type(v) is int for v in pair), 'edge type')
        u,v = pair
        require(0 <= u < v < n, 'edge range')
        edges.append((u,v))
    require(edges == sorted(set(edges)), 'edge order/duplicate')
    return n,set(edges)


def decode_source(doc):
    require(type(doc['n']) is int and doc['n'] == 22, 'source order')
    raw = base64.b64decode(doc['red_parent_graph6_base64'], validate=True)
    require(len(raw) == 40 and raw[0] == 85 and all(63 <= b <= 126 for b in raw), 'graph6 encoding')
    require((raw[-1]-63)&7 == 0, 'padding')
    adj = [0]*22
    offset = 0
    for v in range(1,22):
        for u in range(v):
            value = raw[1+offset//6]-63
            if value >> (5-offset%6) & 1:
                adj[u] |= 1<<v
                adj[v] |= 1<<u
            offset += 1
    require(sum(r.bit_count() for r in adj) == 228, 'parent edges')
    require(type(doc['red_deletions']) is list and len(doc['red_deletions']) == 6, 'source deletions')
    for pair in doc['red_deletions']:
        require(type(pair) is list and len(pair) == 2 and all(type(v) is int for v in pair), 'deletion types')
        u,v = pair
        require(0 <= u < v < 22 and adj[u] >> v & 1, 'deletion validity')
        adj[u] ^= 1<<v
        adj[v] ^= 1<<u
    require(sum(r.bit_count() for r in adj) == 216, 'source edges')
    return {(u,v) for u,v in itertools.combinations(range(22),2) if adj[u] >> v & 1}


def is_clique(vertices, edges):
    return all(p in edges for p in itertools.combinations(sorted(vertices),2))


def clique_masks(n, edges, k):
    return [sum(1<<v for v in q) for q in itertools.combinations(range(n),k) if is_clique(q,edges)]


def has_clique(n, edges, k):
    neighbors = [set() for _ in range(n)]
    for u,v in edges:
        neighbors[u].add(v)
        neighbors[v].add(u)
    def visit(available, needed):
        if not needed:
            return True
        while len(available) >= needed:
            v = min(available)
            available.remove(v)
            if visit(available & neighbors[v], needed-1):
                return True
        return False
    return visit(set(range(n)), k)


def exact_triangle_capacity(vertices, edges):
    triangles = [set(q) for q in itertools.combinations(sorted(vertices),3) if is_clique(q,edges)]
    maxima = []
    for q in itertools.combinations(sorted(vertices),8):
        if not any(t <= set(q) for t in triangles):
            maxima.append(sum(1<<v for v in q))
    require(maxima, 'no eight-set capacity witness')
    rejected = 0
    for q in itertools.combinations(sorted(vertices),9):
        require(any(t <= set(q) for t in triangles), 'triangle-free nine-set')
        rejected += 1
    return sorted(maxima),rejected


def reconstruct():
    docs = {}
    for key,(path,digest) in SOURCES.items():
        data = (HERE.parent/path).read_bytes()
        require(hashlib.sha256(data).hexdigest() == digest, 'input identity '+key)
        docs[key] = json.loads(data)
    source_red = decode_source(docs['input'])
    pairs = list(itertools.combinations(range(22),2))
    base = set(pairs)-source_red
    graph = {'n':22,'red_edges':[list(e) for e in sorted(base)]}
    require(len(base) == 123 and not has_clique(22,base,5) and not has_clique(22,source_red,4), 'valid base')
    _,h = parse_graph(docs['H'])
    neighbors = {v for v in range(20) if tuple(sorted((1,v))) in h}
    require(neighbors == {0,16,17,18,19}, 'H neighbors')
    constant = len(neighbors)+sum(p in h for p in itertools.combinations(sorted(neighbors),2))
    require(constant == 9, 'H density constant')
    k4 = clique_masks(22,base,4)
    domain = []
    examined = 0
    for q in itertools.combinations(range(22),14):
        m = sum(1<<v for v in q)
        examined += 1
        if not any(m&t == t for t in k4):
            domain.append(m)
    domain.sort()
    require(len(domain) == 6, 'six complete fourteen-sets')
    entries,cases = [],[]
    all_vertices = set(range(22))
    maximizers_count = nine_sets = 0
    for s1 in domain:
        vs = {v for v in range(22) if s1>>v&1}
        maxima,rejected = exact_triangle_capacity(vs,base)
        maximizers_count += len(maxima)
        nine_sets += rejected
        s0s=[]
        for zeros in itertools.combinations(sorted(vs),10):
            us = all_vertices-set(zeros)
            s0 = sum(1<<v for v in us)
            if any(s0&t == t for t in k4):
                continue
            if any(is_clique(t,base) for t in itertools.combinations(sorted(us&vs),3)):
                continue
            s0s.append(s0)
        for s0 in sorted(s0s):
            # Count every fixed edge of the literal twenty-vertex red neighborhood.
            vertices = [0]+[1+v for v in sorted(neighbors)]+[21+v for v in sorted(vs)]
            known=free=0
            for u,v in itertools.combinations(vertices,2):
                if u==0:
                    known += int(v<=20)
                elif v<=20:
                    known += int((u-1,v-1) in h)
                elif u>=21:
                    known += int((u-21,v-21) in base)
                elif u==1:
                    known += (s0>>(v-21))&1
                else:
                    free += 1
            require(free==56 and known+32<=90, 'base case cap')
            cases.append({'id':len(cases),'S0':f'{s0:06x}','S1':f'{s1:06x}','base_density_ceiling':known+32})
        e=sum(p in base for p in itertools.combinations(sorted(vs),2))
        entries.append({'S1':f'{s1:06x}','red_edges':e,'triangle_free_maximum':8,
                        'all_triangle_free_maximizers':[f'{m:06x}' for m in maxima],
                        'base_cover_markings':len(s0s)})
    # Independently reconstruct all 108 children; no inherited survivor completeness assumed.
    survivors=[]
    for pair in sorted(source_red):
        child=base|{pair}
        if not has_clique(22,child,5) and not has_clique(22,set(pairs)-child,4):
            survivors.append(list(pair))
    require(survivors==docs['family']['surviving_deletions'] and len(survivors)==16, 'exact valid child family')
    family=[]
    for pair in survivors:
        child=base|{tuple(pair)}
        child4=clique_masks(22,child,4)
        child3=clique_masks(22,child,3)
        accepted=[]
        for case in cases:
            s0,s1=int(case['S0'],16),int(case['S1'],16)
            if any(s0&q==q or s1&q==q for q in child4):
                continue
            if any(s0&s1&q==q for q in child3):
                continue
            accepted.append(case)
        upper=[]
        for case in accepted:
            vertices=[v for v in range(22) if int(case['S1'],16)>>v&1]
            # The bound uses the BASE tau=8; no child-capacity sharpness asserted.
            upper.append(13+sum(p in child for p in itertools.combinations(vertices,2))+32)
        require(upper and max(upper)<92, 'child obstruction')
        if pair==[0,10]:
            rebuilt=[{'id':i,'S0':c['S0'],'S1':c['S1']} for i,c in enumerate(accepted)]
            require(rebuilt==docs['old_cases'], 'old100 regression')
        bits=sum(1<<c['id'] for c in accepted)
        child_graph={'n':22,'red_edges':[list(e) for e in sorted(child)]}
        family.append({'added_red_edge':pair,'graph_sha256':hashlib.sha256(encoded(child_graph)).hexdigest(),
                       'size14_domain':[f'{m:06x}' for m in domain if not any(m&q==q for q in child4)],
                       'valid_base_case_bits_hex':f'{bits:035x}', 'valid_markings':len(accepted),'density_ceiling':max(upper)})
    ids=[-i for i,p in enumerate(pairs,1) if p in base]
    cnf='p cnf 231 1\n'+' '.join(map(str,ids))+' 0\n'
    total=sum(row['valid_markings'] for row in family)
    require(len(cases)==140 and total==1684 and len(ids)==123, 'finite totals')
    expected={
        'scope':'fixed H20, root red H blue O, marked outside degrees12/14 and union O, no red K5, density92 at b',
        'input_sha256':{key:pin[1] for key,pin in SOURCES.items()},
        'base_graph_sha256':hashlib.sha256(encoded(graph)).hexdigest(),
        'base_red_edges':len(base),'H_density_base':constant,'S1_entries':entries,'base_cases':cases,
        'base_uniform_density_ceiling':90,'supergraph_density_ceiling':'90 + number of added red edges',
        'family':family,'total_family_markings':total,'all_16_families_excluded_at_density92':True,
        'old_already_closed_markings':100,'newly_closed_labeled_markings':total-100,
        'target_O_red_edges':124,'required_density_at_b':92,
        'edge_toggle_lower_bound_from_base_at_124_red_edges':3,
        'conditional_cut_variables':231,'conditional_cut_width':123,
        'conditional_cut_sha256':hashlib.sha256(cnf.encode()).hexdigest(),
        'whole_degree_profile_excluded':False,'target_graph_found':False,
    }
    report={'accepted':True,'base_red_K4s':len(k4),'fourteen_subsets_examined':examined,
            'fourteen_sets_entry_matched':len(domain),'maximizing_eight_sets_entry_matched':maximizers_count,
            'nine_sets_obstructed':nine_sets,'base_markings_entry_matched':len(cases),
            'explicit_child_graphs_tested':len(source_red),'valid_child_graphs':len(survivors),
            'family_membership_bits_entry_matched':len(cases)*len(family),
            'accepted_family_markings':total,'conditional_cut_literals_checked':len(ids),
            'independent_peer_review':False}
    return graph,expected,cnf,report


def check_data(graph, certificate, cnf, expected):
    parse_graph(graph)
    require(encoded(graph)==encoded(expected[0]), 'base graph mismatch')
    require(encoded(certificate)==encoded(expected[1]), 'certificate mismatch')
    require(cnf==expected[2], 'conditional cut mismatch')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--work',type=Path,required=True)
    parser.add_argument('--report',type=Path,required=True)
    args=parser.parse_args()
    expected=reconstruct()
    check_data(json.loads((args.work/'BASE_GRAPH.json').read_text()),
               json.loads((args.work/'certificate.json').read_text()),
               (args.work/'conditional_cut.cnf').read_text(),expected)
    with args.report.open('x') as out:
        out.write(json.dumps(expected[3],indent=2)+'\n')
    print(json.dumps(expected[3]),flush=True)


if __name__=='__main__':
    main()
