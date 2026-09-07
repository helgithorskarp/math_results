"""Exact positive maps, semantic clause controls, and bad-proof rejections."""
import copy
import json
import random
import tempfile
from itertools import combinations
from pathlib import Path
from check_rup import check
from verify import eq, geometric

# Coordinates are coefficient vectors in Q(sqrt(3),sqrt(11)), divided by 12.
# The basis order is 1, sqrt(3), sqrt(11), sqrt(33).
POINTS = [((0,0,0,0),(0,0,0,0)),
          ((0,6,0,0),(6,0,0,0)),
          ((0,6,0,0),(-6,0,0,0)),
          ((0,12,0,0),(0,0,0,0)),
          ((0,5,-1,0),(5,0,0,1)),
          ((0,5,1,0),(-5,0,0,1)),
          ((0,10,0,0),(0,0,0,2))]
MAP9 = [0,1,2,1,0,5,5,6,1,2,1,4,5,5,1,2,2,0,0,3,0,1,0,0,3,0,
        0,0,3,0,5,5,5,4,4,6]


def product(a, b):
    out = [0]*4
    for i in range(4):
        for j in range(4):
            common = i & j
            out[i ^ j] += a[i]*b[j]*(3 if common & 1 else 1)*(11 if common & 2 else 1)
    return out


def unit(i, j):
    dx = [a-b for a, b in zip(POINTS[i][0], POINTS[j][0])]
    dy = [a-b for a, b in zip(POINTS[i][1], POINTS[j][1])]
    return [a+b for a, b in zip(product(dx, dx), product(dy, dy))] == [144,0,0,0]


def source(n):
    vertices = list(combinations(range(1, n+1), 2))
    edges = [(a, b) for a, b in combinations(range(len(vertices)), 2)
             if vertices[a][1] == vertices[b][0] or vertices[b][1] == vertices[a][0]]
    return vertices, edges


def must_reject(callback):
    try:
        callback()
    except (ValueError, KeyError, TypeError):
        return
    raise ValueError('invalid control was accepted')


def run():
    if len(set(POINTS)) != 7 or sum(unit(a,b) for a,b in combinations(range(7),2)) != 11:
        raise ValueError('exact Moser fixture failed')
    v, edges = source(9)
    if len(MAP9) != len(v) or any(not unit(MAP9[a], MAP9[b]) for a,b in edges):
        raise ValueError('S9 unit-edge map failed')
    maps = {2: {}, 3: {}}
    for k in maps:
        intervals = [(2**l, 2**k-2**(k-l)+2) for l in range(k+1)]
        selected = {i for i,(x,y) in enumerate(v) if y <= 2**k+1 and any(a<=x<y<=b for a,b in intervals)}
        selected_edges = [(a,b) for a,b in edges if a in selected and b in selected]
        if any(not unit(MAP9[a], MAP9[b]) for a,b in selected_edges):
            raise ValueError('critical positive map failed')
        maps[k] = {'vertices':len(selected),'edges':len(selected_edges)}

    # The complete three-label equality truth table: precisely the five
    # equivalence relations satisfy all transitivity clauses.
    three_valid = 0
    for bits in range(8):
        x,y,z = [bool(bits & (1<<i)) for i in range(3)]
        accepted = (not x or not y or z) and (not x or not z or y) and (not y or not z or x)
        if accepted != ((x+y+z) != 2):
            raise ValueError('transitivity truth table failed')
        three_valid += accepted
    # Independent arithmetic formula for the lexical variable numbering.
    numbering = 0
    for n in range(2, 18):
        for expected,(a,b) in enumerate(combinations(range(n),2),1):
            if eq(a,b,n) != expected or eq(b,a,n) != expected:
                raise ValueError('equality numbering mismatch')
            numbering += 1

    rng = random.Random(17087)
    semantic = 0
    sample_record = None
    for trial in range(100):
        images = list(range(7))*2
        rng.shuffle(images)
        n = len(images)
        edge = lambda a,b,images=tuple(images): unit(images[a],images[b])
        original = [(a,b) for a,b in combinations(range(n),2) if edge(a,b)]
        true = {eq(a,b,n) for a,b in combinations(range(n),2) if images[a] == images[b]}
        for kind in ('k23','wheel3','wheel5','wheel7'):
            labels = rng.sample(range(n),5 if kind=='k23' else int(kind[-1])+1)
            if kind=='k23':
                record = {'kind':'k23','left':labels[:2],'right':labels[2:]}
                qedges = {tuple(sorted((a,b))) for a in labels[:2] for b in labels[2:]}
            else:
                record = {'kind':'wheel','center':labels[0],'cycle':labels[1:]}
                rim=labels[1:]
                qedges={tuple(sorted((labels[0],a))) for a in rim}
                qedges|={tuple(sorted((rim[i],rim[(i+1)%len(rim)]))) for i in range(len(rim))}
            record['witnesses'] = [[c,d,*rng.choice(original)] for c,d in sorted(qedges)]
            clause = geometric(record,n,edge)
            if not any((literal in true) if literal>0 else (-literal not in true) for literal in clause):
                raise ValueError('geometric clause rejected an exact planar assignment')
            semantic += 1
            if kind=='k23':
                sample_record=(record,n,edge)

    # Both collision alternatives occur in exact plane maps. The first case
    # has three distinct right points; the next three isolate each right pair.
    collapsed = {'kind':'k23','left':[0,1],'right':[2,3,4],
                 'witnesses':[[a,b,a,b] for a in (0,1) for b in (2,3,4)]}
    collision_images = [[0,0,1,2,4], [1,2,0,0,3], [1,2,0,3,0],
                        [1,2,3,0,0], [0,0,1,1,1]]
    for images in collision_images:
        cl = geometric(collapsed,5,lambda a,b:unit(images[a],images[b]))
        true = {eq(a,b,5) for a,b in combinations(range(5),2) if images[a]==images[b]}
        if not any(x in true for x in cl):
            raise ValueError('collapsed K23 was excluded')
    rejected = 0
    record,n,edge = sample_record
    bad = copy.deepcopy(record);bad['witnesses'].pop()
    must_reject(lambda: geometric(bad,n,edge));rejected+=1
    bad = copy.deepcopy(record);bad['witnesses'][0][2:]=[0,0]
    must_reject(lambda: geometric(bad,n,edge));rejected+=1
    bad = copy.deepcopy(record);bad['left'][0]=bad['right'][0]
    must_reject(lambda: geometric(bad,n,edge));rejected+=1
    bad = {'kind':'wheel','center':0,'cycle':[1,2,3,4],'witnesses':[]}
    must_reject(lambda: geometric(bad,5,lambda a,b:True));rejected+=1
    bad = {'kind':'wheel','center':0,'cycle':[1,2,1],'witnesses':[]}
    must_reject(lambda: geometric(bad,5,lambda a,b:True));rejected+=1
    bad = {'kind':'unknown'}
    must_reject(lambda: geometric(bad));rejected+=1

    with tempfile.TemporaryDirectory() as tmp:
        d=Path(tmp);cnf=d/'test.cnf';proof=d/'test.lrat'
        cnf.write_text('p cnf 2 4\n1 2 0\n-1 2 0\n1 -2 0\n-1 -2 0\n')
        valid='5 2 0 1 2 0\n5 d 1 2 0\n6 0 5 3 4 0\n'
        proof.write_text(valid)
        if check(cnf,proof)['rup_additions'] != 2:
            raise ValueError('positive RUP fixture failed')
        for text in ['5 0 1 2 0\n','5 2 0 -1 2 0\n','5 2 0 1 99 0\n',
                     '4 2 0 1 2 0\n','5 3 0 1 2 0\n','5 2 0 1 0\n',
                     '5 2 0 1 2 1 0\n','5 2 0 1 2 0\n',
                     '5 2 2 0 1 2 0\n','5 2 -2 0 1 2 0\n']:
            proof.write_text(text);must_reject(lambda:check(cnf,proof));rejected+=1
        # A satisfiable formula cannot support the copied contradiction.
        cnf.write_text('p cnf 2 4\n1 2 0\n-1 2 0\n1 -2 0\n1 -2 0\n')
        proof.write_text(valid);must_reject(lambda:check(cnf,proof));rejected+=1
    return {'exact_moser_points':7,'exact_unit_edges':11,'s9_source_edges_checked':len(edges),
            'critical_positive_maps':maps,'valid_three_label_equivalences':three_valid,
            'variable_numbering_checks':numbering,'exact_semantic_clause_controls':semantic,
            'collapsed_k23_allowed':True,'exact_k23_collision_controls':len(collision_images),'malformed_input_or_proof_rejections':rejected}


if __name__ == '__main__':
    print(json.dumps(run(),sort_keys=True))
