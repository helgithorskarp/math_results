"""Exact original-face alias covers; see PROOF.md for the written bridges.

Standard library only. No solver, floating arithmetic or private input.
All four deficient originals are assigned before any alias pruning.
The separate U contact edges encode the global three-neighbor constraint.
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
    maxima[partition[0]], maxima[partition[1]] = 3, 0
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

ANCHORS=('F','U','X','R','S','V','W','B','C')
CORE=(('F','X','R'),('F','R','S'),('F','V','W'),
      ('F','S','B','V'),('F','W','C','X'),
      ('R','L','Q','S'),('R','X','P','L'))
ROLES=tuple([('A',e) for e in ('X','S','V','W','outside')]
           +[('Bzero',e) for e in ('X','V','W','outside')]
           +[('Czero',e) for e in ('S','V','W','outside')])


def schema(family, e, choice, stage='unpaired'):
    roles={'F':3,'U':0,'B':1,'C':1}
    if family=='Bzero': roles.update(B=0,S=1)
    if family=='Czero': roles.update(C=0,X=1)
    originals=list(ANCHORS)
    if e=='outside': originals.append('E'); roles['E']=1
    else: roles[e]=1
    if family=='A': originals.append('Z0');roles['Z0']=0
    deficient=tuple(n for n in originals if n not in ('F','U') and roles.get(n,2)<2)
    if len(deficient)!=4: raise RuntimeError('role cover wrong')
    contacts=tuple(deficient[i] for i in choice)
    words=list(CORE)
    names=originals+['L','P','Q']
    if roles.get('X',2)==2: words.append(('X','C','P'))
    else: names.append('AX');words.append(('X','C','AX','P'))
    if roles.get('S',2)==2: words.append(('S','Q','B'))
    else: names.append('AS');words.append(('S','Q','AS','B'))
    if stage=='unpaired':
        if roles.get('V',2)==2: names.append('JV');words.append(('V','B','JV'))
        if roles.get('W',2)==2: names.append('JW');words.append(('W','JW','C'))
    else:
        if roles.get('V',2)!=2 or roles.get('W',2)!=2: raise ValueError('paired one-T isolated endpoint')
        names+=['H','M','N'];words+=[('W','V','H'),('V','B','M','H'),('W','H','N','C')]
        if roles['B']==1 and roles.get('S',2)==1:
            words.append(('B','AS','M'))
        else:
            names.append('JB')
            words.append(('B','Q' if roles.get('S',2)==2 else 'AS','JB','M'))
        if roles['C']==1 and roles.get('X',2)==1:
            words.append(('C','N','AX'))
        else:
            names.append('KC')
            words.append(('C','N','KC','P' if roles.get('X',2)==2 else 'AX'))
        if stage=='H_Q':
            if e!='outside': raise ValueError('H_Q only after outside-E classifier')
            names.append('JH');words.append(('H','M','JH','N'))
    number={n:i for i,n in enumerate(names)}
    return {'case':f'{family}_{e}_U'+''.join(contacts)+'_'+stage,
            'family':family,'extra_one':e,'contacts':contacts,'stage':stage,
            'names':tuple(names),'number':number,'words':tuple(words),
            'faces':tuple(tuple(number[n] for n in w) for w in words),
            'distinct':(),'mode':'full','maxima':{},'exact':roles,
            'initial':tuple(range(len(originals))),
            'contact_edges':tuple((number['U'],number[n]) for n in contacts)}


def cover(spec):
    nodes,rejects,passing,final=0,Counter(),{},[]
    def visit(partition):
        nonlocal nodes
        nodes+=1
        if nodes>200000:raise RuntimeError('INCOMPLETE: fixed200000nodebudget '+spec['case'])
        reason=necessary(partition,spec)
        if reason: rejects[reason]+=1;return
        passing.setdefault(len(partition),[]).append(partition)
        if len(partition)==len(spec['names']): final.append(partition);return
        for value in range(max(partition)+2):visit(partition+(value,))
    visit(spec['initial'])
    return {'names':spec['names'],'faces':spec['words'],'exact_triangle_roles':spec['exact'],
            'U_neighbors':spec['contacts'],'initial':spec['initial'],
            'max_points':len(spec['names']),'nodes':nodes,'passing_counts':{k:len(v) for k,v in passing.items()},
            'passing_partitions_by_depth':passing,'rejects':dict(sorted(rejects.items())),'survivors':final}


def classifications(spec, result):
    answer={}
    for name in ('H','M','N','JH'):
        if name not in spec['number']:continue
        i=spec['number'][name];counts=Counter()
        for p in result['survivors']:
            hit=[n for n in spec['exact'] if p[spec['number'][n]]==p[i]]
            counts['+'.join(hit) if hit else 'ordinary']+=1
        answer[name]=dict(counts)
    return answer



def controls():
    spec=schema('A','outside',(0,2,3),'basic')
    quotient=(0,1,2,3,4,5,6,7,8,9,10,11,12,13,9,1,14,10,10)
    if necessary(quotient,spec) is not None:
        raise RuntimeError('Fifteen-class proper partial patch rejected')
    alternative=quotient[:-1]+(15,)
    if necessary(alternative,spec) is not None:
        raise RuntimeError('Sixteen-class partial patch rejected')
    last=schema('A','outside',(0,2,3),'H_Q')
    failed_extensions={}
    for value in range(16):
        reason=necessary(quotient+(value,),last)
        if reason is None:raise RuntimeError('Negative closing-Q control accepted')
        failed_extensions[value]=reason
    l_aliases={}
    for value in (5,6):
        partial=spec['initial']+(value,)
        if necessary(partial,spec) is not None:
            raise RuntimeError('Early L=V/W alias wrongly forbidden')
        l_aliases['V' if value==5 else 'W']=partial
    toy=dict(spec)
    toy['faces']=((1,7,2,8),)
    toy['contact_edges']=((1,7),(1,8),(1,9))
    identity=tuple(range(11))
    if necessary(identity,toy) is not None:
        raise RuntimeError('Positive separate-contact-edge control rejected')
    diagonal=dict(toy);diagonal['contact_edges']=((1,7),(1,8),(1,2))
    if necessary(identity,diagonal)!='contact_Q_diagonal':
        raise RuntimeError('Separate contact on Q diagonal accepted')
    overdegree=dict(toy);overdegree['contact_edges']=toy['contact_edges']+((1,10),)
    if necessary(identity,overdegree)!='excess_degree':
        raise RuntimeError('Fourth separate U contact accepted')
    return {'positive_fifteen_class_partial_patch':quotient,
            'positive_sixteen_class_partial_patch':alternative,
            'all_closing_Q_extensions_rejected':failed_extensions,
            'early_L_may_equal_V_or_W':l_aliases,
            'positive_separate_contact_edges':True,
            'separate_contact_Q_diagonal_rejected':True,
            'fourth_separate_U_contact_rejected':True}


def run():
    covers={}
    for family,e in ROLES:
        for choice in combinations(range(4),3):
            spec=schema(family,e,choice,'unpaired');result=cover(spec)
            if result['survivors']:raise RuntimeError('Unpaired case survives: '+spec['case'])
            covers[spec['case']]=result
            if e in ('V','W'):continue
            spec=schema(family,e,choice,'basic');result=cover(spec)
            covers[spec['case']]=result
            if result['survivors']:
                classification=classifications(spec,result)
                if family!='A' or e!='outside' or classification['H']!={'E':len(result['survivors'])}:
                    raise RuntimeError('Uncovered surviving role or H classifier: '+spec['case'])
                result['survivor_classification']=classification
                # Exhaustive previous cover establishes H=E, t(H)=1.
                # Its three known corners consequently force this Q.
                spec=schema(family,e,choice,'H_Q');result=cover(spec)
                if result['survivors']:raise RuntimeError('Closing-Q case survives: '+spec['case'])
                covers[spec['case']]=result
    if len(covers)!=82:raise RuntimeError('Role/contact-set coverage changed')
    return {'agent':'six-tammes-1','role':'researcher',
            'status':'AUTHOR_CHECKED_CONDITIONAL_NONCONTACT_PROFILE_EXCLUSION',
            'excluded_noncontact_case':{'profile':[1,3,1],'F_contacts_U':False},
            'labelled_role_cases':13,'U_contact_sets_per_role':4,
            'unpaired_covers':52,'paired_basic_covers':28,'paired_closing_Q_covers':2,
            'total_nodes':sum(r['nodes'] for r in covers.values()),
            'covers':covers,'controls':controls(),
            'remaining_r1_profiles_using_previous_contact_exclusion':[[0,6,0],[0,4,1],[0,2,2],[1,5,0]],
            'trust_boundary':'Written geometry, roles, original-face forcing and topology; previous h8054 contact exclusion and h7912 angle lemmas. Separate same-author audit; independent review and formalization pending. No unrestricted optimizer coverage or global numerical bound.'}


if __name__=='__main__':
    from pathlib import Path
    result=run()
    expected=json.loads((Path(__file__).resolve().parent/'EXPECTED.json').read_text())
    if json.loads(json.dumps(result))!=expected:
        raise RuntimeError('Recomputed result differs from EXPECTED.json')
    print(json.dumps(result,sort_keys=True,separators=(',',':')))
