"""Exact original-face alias covers; see PROOF.md for the written bridges.

Standard library only. No solver, floating arithmetic or private input.
All four deficient originals are assigned before any alias pruning.
The separate U contact edges encode the global three-neighbor constraint.
F has FOUR triangles throughout this ordinary-five computation.
"""
from collections import Counter
from itertools import combinations
import json


def cyclic(face):
    return min(face[i:] + face[:i] for i in range(len(face)))


def necessary(partition, spec):
    assigned = len(partition)
    for a, b in spec['distinct']:
        if a < assigned and b < assigned and partition[a] == partition[b]:
            return 'forbidden_anchor_alias'
    faces = set()
    for word in spec['faces']:
        if max(word) >= assigned:
            continue
        face = tuple(partition[index] for index in word)
        if len(set(face)) != len(face):
            return 'nonsimple_face'
        if cyclic(face[::-1]) in faces:
            return 'reversed_face'
        # Repeated descriptions of the same actual face coalesce.
        faces.add(cyclic(face))
    count = max(partition) + 1
    degrees = [4] * count
    degrees[partition[0]], degrees[partition[1]] = 5, 3
    maxima = [2] * count
    maxima[partition[0]], maxima[partition[1]] = 4, 0
    exact = [None] * count
    if spec['mode'] == 'full':
        exact = maxima[:]
    for name, value in spec['maxima'].items():
        index = spec['number'][name]
        if index < assigned:
            maxima[partition[index]] = min(maxima[partition[index]], value)
    fixed = {}
    for name, value in spec['exact'].items():
        index = spec['number'][name]
        if index < assigned:
            actual = partition[index]
            if actual in fixed and fixed[actual] != value:
                return 'conflicting_exact_roles'
            fixed[actual] = value
            exact[actual] = value
            maxima[actual] = min(maxima[actual], value)
    if any(t is not None and t > maxima[v] for v, t in enumerate(exact)):
        return 'inconsistent_role_bounds'
    neighbors = [set() for _ in range(count)]
    outgoing = [dict() for _ in range(count)]
    incoming = [dict() for _ in range(count)]
    triangles, corners = [0] * count, [0] * count
    edges, nonedges, darts = set(), set(), set()
    for face in faces:
        size = len(face)
        if size == 4:
            nonedges.add(tuple(sorted((face[0], face[2]))))
            nonedges.add(tuple(sorted((face[1], face[3]))))
        for i, v in enumerate(face):
            before, after = face[i - 1], face[(i + 1) % size]
            if (v, after) in darts:
                return 'repeated_oriented_edge'
            darts.add((v, after))
            edges.add(tuple(sorted((v, after))))
            neighbors[v].update((before, after))
            triangles[v] += size == 3
            corners[v] += 1
            if (before in outgoing[v] and outgoing[v][before] != after
                    or after in incoming[v] and incoming[v][after] != before):
                return 'incompatible_star'
            outgoing[v][before], incoming[v][after] = after, before
    for a, b in spec.get('contact_edges', ()):
        if a < assigned and b < assigned:
            x, y = partition[a], partition[b]
            if x == y:
                return 'contact_loop'
            edges.add(tuple(sorted((x,y))))
            neighbors[x].add(y)
            neighbors[y].add(x)
    if edges & nonedges:
        return 'contact_Q_diagonal'
    for v in range(count):
        if len(neighbors[v]) > degrees[v] or corners[v] > degrees[v]:
            return 'excess_degree'
        if triangles[v] > maxima[v]:
            return 'excess_triangles'
        if exact[v] is not None and corners[v] - triangles[v] > degrees[v] - exact[v]:
            return 'excess_quadrilateral_corners'
        for start in outgoing[v]:
            visited, cursor = set(), start
            while cursor in outgoing[v] and cursor not in visited:
                visited.add(cursor)
                cursor = outgoing[v][cursor]
            if cursor in visited:
                if len(visited) != degrees[v] or len(neighbors[v]) != degrees[v]:
                    return 'proper_closed_link'
                if exact[v] is not None and triangles[v] != exact[v]:
                    return 'closed_star_wrong_triangle_role'
    for a, b in combinations(range(count), 2):
        if len(neighbors[a] & neighbors[b]) > 2:
            return 'three_common_contacts'
    for a, b, c in combinations(range(count), 3):
        if b in neighbors[a] and c in neighbors[a] and c in neighbors[b]:
            if neighbors[a] & neighbors[b] & neighbors[c]:
                return 'contact_K4'
    return None

from pathlib import Path
ANCHORS=('F','U','X','R','S','T','Z','D')
CORE=(('F','X','R'),('F','R','S'),('F','S','T'),('F','T','Z'),
      ('F','Z','D','X'),('R','L','K','S'),('R','X','P','L'),
      ('S','K','M','T'),('T','M','Q','Z'))
ROLES=('D_zero','D_one_X_one','D_one_Z_one')


def schema(role,choice):
    exact={'F':4,'U':0}
    originals=list(ANCHORS)
    if role=='D_zero':
        exact.update(D=0,X=1,Z=1,A0=0);originals+=['A0']
    elif role=='D_one_X_one':
        exact.update(D=1,X=1,A0=0,B0=0);originals+=['A0','B0']
    elif role=='D_one_Z_one':
        exact.update(D=1,Z=1,A0=0,B0=0);originals+=['A0','B0']
    else:raise ValueError(role)
    deficient=tuple(n for n in originals if n not in ('F','U') and exact.get(n,2)<2)
    contacts=tuple(deficient[i] for i in choice)
    names=originals+['L','K','M','P','Q'];words=list(CORE)
    if exact.get('X',2)==1:names+=['AX'];words.append(('X','D','AX','P'))
    else:words.append(('X','D','P'))
    if exact.get('Z',2)==1:names+=['AZ'];words.append(('Z','Q','AZ','D'))
    else:words.append(('Z','Q','D'))
    number={name:i for i,name in enumerate(names)}
    return {'case':role+'_U'+''.join(contacts),'role':role,'contacts':contacts,
            'names':tuple(names),'words':tuple(words),'number':number,
            'faces':tuple(tuple(number[n] for n in w) for w in words),
            'mode':'full','maxima':{},'exact':exact,'distinct':(),
            'initial':tuple(range(len(originals))),
            'contact_edges':tuple((number['U'],number[n]) for n in contacts)}


def triangle_role(partition,spec,name):
    actual=partition[spec['number'][name]]
    matches=[value for n,value in spec['exact'].items() if partition[spec['number'][n]]==actual]
    if len(set(matches))>1:raise RuntimeError('Conflicting exact role in a passing partition')
    return matches[0] if matches else 2


def cover(spec,initial=None):
    nodes,rejects,passing,final=0,Counter(),{},[]
    def visit(partition):
        nonlocal nodes
        nodes+=1
        if nodes>200000:raise RuntimeError('INCOMPLETE: fixed200000nodebudget')
        reason=necessary(partition,spec)
        if reason:rejects[reason]+=1;return
        passing.setdefault(len(partition),[]).append(partition)
        if len(partition)==len(spec['names']):final.append(partition);return
        for value in range(max(partition)+2):visit(partition+(value,))
    visit(spec['initial'] if initial is None else initial)
    return {'nodes':nodes,'passing_counts':{k:len(v) for k,v in passing.items()},
            'passing_partitions_by_depth':passing,'rejects':dict(sorted(rejects.items())),
            'survivors':final}


def obstruction(partition,spec):
    roles={n:triangle_role(partition,spec,n) for n in ('L','K','M')}
    pair=(roles['L'],roles['K'])
    if pair==(2,2):
        kind='both_ordinary'
        words=(('L','H','K'),('L','P','H'),('K','H','M'))
    elif pair in ((2,0),(0,2)):
        kind='ordinary_zero';words=(('L','H','K'),)
    else:
        raise RuntimeError('No validated left-strip obstruction '+str(roles)+' '+str(partition))
    out=dict(spec);out['names']=spec['names']+('H',);out['words']=spec['words']+words
    out['number']={n:i for i,n in enumerate(out['names'])}
    out['faces']=tuple(tuple(out['number'][n] for n in w) for w in out['words'])
    return 'LK',kind,roles,out



def controls():
    ordinary=schema('D_one_Z_one',(0,2,3))
    ordinary_prefix=(0,1,2,3,4,5,6,7,8,9,10,11,8,12,1,9)
    if necessary(ordinary_prefix,ordinary) is not None:
        raise RuntimeError('Thirteen-class positive ordinary-pair prefix rejected')
    pair,kind,roles,last=obstruction(ordinary_prefix,ordinary)
    if kind!='both_ordinary':raise RuntimeError('Ordinary-pair control misclassified')
    trimmed=dict(last);trimmed['faces']=last['faces'][:-1]
    if necessary(ordinary_prefix+(13,),trimmed) is not None:
        raise RuntimeError('Two-triangle positive strip control rejected')
    if necessary(ordinary_prefix+(13,),last) is None:
        raise RuntimeError('Full negative strip control accepted')
    mixed=schema('D_one_X_one',(0,2,3))
    mixed_prefix=(0,1,2,3,4,5,6,7,8,9,8,10,11,1,12,9)
    if necessary(mixed_prefix,mixed) is not None:
        raise RuntimeError('Mixed positive partial patch rejected')
    _,kind,_,last_mixed=obstruction(mixed_prefix,mixed)
    if kind!='ordinary_zero' or necessary(mixed_prefix+(13,),last_mixed) is None:
        raise RuntimeError('Mixed negative control differs')
    star=schema('D_zero',(0,2,3));star_prefix=star['initial']
    if necessary(star_prefix,star) is not None:
        raise RuntimeError('Four-triangle F star rejected')
    wrong=dict(star);wrong['exact']=dict(star['exact'],F=3)
    if necessary(star_prefix,wrong)!='excess_triangles':
        raise RuntimeError('Three-triangle F role wrongly accepted')
    for name,value in (('L',5),('M',3)):
        partial=star_prefix+((value,) if name=='L' else (9,10,value))
        # Keep the initial L=T/M=R alternatives before all strip faces
        # activate. With no late role pruning they must remain eligible.
        untouched=dict(star);untouched['faces']=star['faces'][:5]
        if necessary(partial,untouched) is not None:
            raise RuntimeError('Early F-fan alias wrongly banned')
    toy=dict(ordinary);toy['faces']=((1,7,2,6),)
    toy['contact_edges']=((1,7),(1,6),(1,8));identity=tuple(range(10))
    if necessary(identity,toy) is not None:
        raise RuntimeError('Separate actual-edge positive control rejected')
    diagonal=dict(toy);diagonal['contact_edges']=((1,7),(1,6),(1,2))
    extra=dict(toy);extra['contact_edges']=toy['contact_edges']+((1,9),)
    if necessary(identity,diagonal)!='contact_Q_diagonal' or necessary(identity,extra)!='excess_degree':
        raise RuntimeError('Separate actual-edge negative control differs')
    return {'ordinary_pair_positive_prefix':ordinary_prefix,'mixed_pair_positive_prefix':mixed_prefix,
            'two_forced_triangles_positive_full_third_negative':True,
            'mixed_forced_triangle_rejects_zero':True,
            'F_four_T_positive_three_T_role_negative':True,
            'early_L_equals_T_M_equals_R_not_banned':True,
            'separate_actual_contact_edge_controls':True}


def run():
    covers={};base_nodes=strip_nodes=0;extensions=0;types=Counter()
    for role in ROLES:
        for choice in combinations(range(4),3):
            spec=schema(role,choice);base=cover(spec);subs=[];base_nodes+=base['nodes']
            for prefix in base['survivors']:
                pair,kind,roles,full=obstruction(prefix,spec)
                result=cover(full,prefix)
                if result['survivors']:raise RuntimeError('Final strip alias survives')
                subs.append({'prefix':prefix,'pair':pair,'kind':kind,'triangle_roles':roles,
                             'forced_faces':full['words'][len(spec['words']):],
                             'full_names':full['names'],'cover':result})
                extensions+=1;strip_nodes+=result['nodes'];types[kind]+=1
            covers[spec['case']]={'names':spec['names'],'faces':spec['words'],
                'exact_triangle_roles':spec['exact'],'U_contacts':spec['contacts'],
                'initial':spec['initial'],'base':base,'strip_extensions':subs}
    if len(covers)!=12 or extensions!=20:raise RuntimeError('Finite coverage changed')
    return {'agent':'six-tammes-1','role':'researcher',
        'status':'AUTHOR_CHECKED_CONDITIONAL_ORDINARY_FIVE_ROW_EXCLUSION',
        'excluded_profile':[0,2,2],'labelled_role_cases':3,'U_contact_sets_per_role':4,
        'base_covers':12,'base_nodes':base_nodes,'base_partial_survivors':20,
        'strip_covers':extensions,'strip_nodes':strip_nodes,'strip_kinds':dict(types),
        'total_nodes':base_nodes+strip_nodes,'covers':covers,'controls':controls(),
        'remaining_r1_profiles_using_previous_four_profile_theorem':[[0,6,0],[0,4,1],[1,5,0]],
        'trust_boundary':'Written angular input, actual-star forcing, role coverage and pruning; separate same-author raw-label audit. Independent review/formalization pending. Necessary counts only; no global bound or optimizer coverage.'}


if __name__=='__main__':
    result=run()
    expected=json.loads((Path(__file__).resolve().parent/'EXPECTED.json').read_text())
    if json.loads(json.dumps(result))!=expected:
        raise RuntimeError('Recomputed result differs from EXPECTED.json')
    print(json.dumps(result,sort_keys=True,separators=(',',':')))
