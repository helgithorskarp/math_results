"""Complete exact alias covers of six forced original-face patches.

See PROOF.md for the complete geometric case split and written bridges.
No imported data, floating arithmetic, solver or coordinate search.
"""
from collections import Counter
from itertools import combinations
import json

def cyclic(face):
    return min(face[i:] + face[:i] for i in range(len(face)))


def necessary(partition, schema):
    """Only necessary complete-contact/star constraints; no invented faces."""
    faces_spec = schema['faces']
    required_distinct = schema['distinct']
    use_triangle_roles = schema.get('use_triangle_roles', True)
    assigned = len(partition)
    for a, b in required_distinct:
        if a < assigned and b < assigned and partition[a] == partition[b]:
            return 'identified_triangle_thirds'
    faces = set()
    for word in faces_spec:
        if any(index >= assigned for index in word):
            continue
        face = tuple(partition[index] for index in word)
        if len(set(face)) != len(face):
            return 'nonsimple_face'
        canon = cyclic(face)
        if cyclic(tuple(reversed(face))) in faces:
            return 'reversed_face'
        # Identical actual oriented faces are allowed to coalesce.
        faces.add(canon)
    count = max(partition) + 1
    degrees = [4] * count
    degrees[partition[0]], degrees[partition[1]] = 5, 3
    triangle_roles = [2] * count
    triangle_roles[partition[0]], triangle_roles[partition[1]] = 2, 0
    for name in ('B', 'C', 'D', schema['extra']):
        if name is None:
            continue
        index = schema['number'][name]
        if index < assigned:
            triangle_roles[partition[index]] = 1
    neighbors = [set() for _ in range(count)]
    outgoing = [dict() for _ in range(count)]
    incoming = [dict() for _ in range(count)]
    triangles = [0] * count
    corner_count = [0] * count
    edges, nonedges, darts = set(), set(), set()
    for face in faces:
        length = len(face)
        if length == 4:
            nonedges.add(tuple(sorted((face[0], face[2]))))
            nonedges.add(tuple(sorted((face[1], face[3]))))
        for i, v in enumerate(face):
            before, after = face[i - 1], face[(i + 1) % length]
            if (v, after) in darts:
                return 'repeated_oriented_edge'
            darts.add((v, after))
            edges.add(tuple(sorted((v, after))))
            neighbors[v].update((before, after))
            triangles[v] += length == 3
            corner_count[v] += 1
            if (before in outgoing[v] and outgoing[v][before] != after
                    or after in incoming[v] and incoming[v][after] != before):
                return 'incompatible_star'
            outgoing[v][before], incoming[v][after] = after, before
    if edges & nonedges:
        return 'contact_Q_diagonal'
    for v in range(count):
        if len(neighbors[v]) > degrees[v] or corner_count[v] > degrees[v]:
            return 'excess_degree'
        if use_triangle_roles and triangles[v] > triangle_roles[v]:
            return 'excess_triangles'
        if (use_triangle_roles and corner_count[v] - triangles[v]
                > degrees[v] - triangle_roles[v]):
            return 'excess_quadrilateral_corners'
        # A closed subcycle of a spherical vertex link must be its whole star.
        for start in outgoing[v]:
            walked = set()
            cursor = start
            while cursor in outgoing[v] and cursor not in walked:
                walked.add(cursor)
                cursor = outgoing[v][cursor]
            if cursor in walked:
                if len(walked) != degrees[v] or len(neighbors[v]) != degrees[v]:
                    return 'proper_closed_link'
                if use_triangle_roles and triangles[v] != triangle_roles[v]:
                    return 'closed_star_wrong_triangle_role'
    for a, b in combinations(range(count), 2):
        if len(neighbors[a] & neighbors[b]) > 2:
            return 'three_common_contacts'
    # Four distinct pairwise c-contact vectors have a positive-definite Gram
    # matrix for 0<c<1, contradicting rank at most three.
    for a, b, c in combinations(range(count), 3):
        if b in neighbors[a] and c in neighbors[a] and c in neighbors[b]:
            if neighbors[a] & neighbors[b] & neighbors[c]:
                return 'contact_K4'
    return None


ANCHORS = ('F','U','X','R','S','Z','B','C','D')
PREFIX = (('F','X','R'),('F','S','Z'),('R','X','J'),('S','D','K'),('C','Z','L'),
          ('F','U','B','X'),('F','R','D','S'),('F','Z','C','U'),('U','C','Y','B'),
          ('X','B','M','J'),('R','J','N','D'),('S','K','L','Z'),('C','L','P','Y'))

def schema(case):
    if case=='both_paired':
        names=ANCHORS+('J','K','Y','L','M','N','O')
        words=(('F','X','R'),('F','S','Z'),('R','X','J'),('Z','S','K'),
               ('F','U','B','X'),('F','R','D','S'),('F','Z','C','U'),('U','C','Y','B'),
               ('X','B','L','J'),('R','J','M','D'),('S','D','N','K'),('Z','K','O','C'))
        extra=None;distinct_names=(('F','J'),('F','K'));anchors=9
    elif case=='extra_equals_J':
        names=ANCHORS+('J','K','L','Y','M','N','P','W')
        words=PREFIX+(('J','M','W','N'),)
        extra='J'
        distinct_names=tuple(('J',a) for a in ANCHORS)
        anchors=10
    elif case=='extra_outside_J_ordinary':
        names=ANCHORS+('E','J','K','L','Y','M','N','P')
        words=PREFIX+(('J','M','N'),)
        extra='E'
        distinct_names=(('J','F'),('J','E'))
        anchors=10
    elif case=='extra_endpoint_X':
        names=ANCHORS+('K','H','L','Y','A','M','N','O')
        words=(('F','X','R'),('F','S','Z'),('R','K','D'),('Z','S','L'),
               ('B','Y','A'),('C','N','Y'),('L','M','N'),('K','H','O'),
               ('F','U','B','X'),('F','R','D','S'),('F','Z','C','U'),('U','C','Y','B'),
               ('R','X','H','K'),('X','B','A','H'),('S','D','M','L'),('Z','L','N','C'),('D','K','O','M'))
        extra='X';distinct_names=(('L','F'),);anchors=9
    elif case=='extra_inner_R_SZ_paired':
        names=ANCHORS+('K','H','L','Y','A','M','N','O')
        words=(('F','X','R'),('F','S','Z'),('X','B','K'),('Z','S','L'),
               ('D','A','N'),('C','O','Y'),('L','N','O'),('K','M','H'),
               ('F','U','B','X'),('F','R','D','S'),('F','Z','C','U'),('U','C','Y','B'),
               ('R','X','K','H'),('R','H','A','D'),('B','Y','M','K'),('S','D','N','L'),('Z','L','O','C'))
        extra='R';distinct_names=(('L','F'),);anchors=9
    elif case=='extra_inner_R_SZ_separate':
        names=ANCHORS+('K','H','L','M','Y','A','N','P')
        words=(('F','X','R'),('F','S','Z'),('X','B','K'),('S','D','L'),('C','Z','M'),
               ('K','N','H'),('L','P','M'),
               ('F','U','B','X'),('F','R','D','S'),('F','Z','C','U'),('U','C','Y','B'),
               ('R','X','K','H'),('R','H','A','D'),('B','Y','N','K'),('S','L','M','Z'),
               ('D','A','P','L'),('C','M','P','Y'))
        extra='R';distinct_names=();anchors=9
    else:
        raise ValueError(case)
    number={n:i for i,n in enumerate(names)}
    return {'case':case,'names':names,'number':number,'words':words,
            'faces':tuple(tuple(number[n] for n in w) for w in words),
            'extra':extra,'distinct':tuple((number[a],number[b]) for a,b in distinct_names),
            'initial_distinct':anchors,'use_triangle_roles':case!='both_paired'}

def cover(s,max_points):
    rejects=Counter();passing={};nodes=0;survivors=[]
    def visit(p):
        nonlocal nodes
        nodes+=1
        if nodes>200000:
            raise RuntimeError('INCOMPLETE: fixed local work budget')
        why=necessary(p,s)
        if why:
            rejects[why]+=1;return
        passing.setdefault(len(p),[]).append(p)
        if len(p)==len(s['names']):
            survivors.append(p);return
        classes=max(p)+1
        for v in range(min(classes+1,max_points)):
            visit(p+(v,))
    visit(tuple(range(s['initial_distinct'])))
    return {'case':s['case'],'max_points':max_points,'nodes':nodes,
            'names':s['names'],'faces':s['words'],
            'passing_counts':{k:len(v) for k,v in passing.items()},
            'passing_partitions_by_depth':passing,'rejects':dict(sorted(rejects.items())),
            'survivors':survivors,'minimum_classes':min((max(p)+1 for p in survivors),default=None)}

CASES = ('both_paired','extra_equals_J','extra_outside_J_ordinary',
         'extra_endpoint_X','extra_inner_R_SZ_paired','extra_inner_R_SZ_separate')


def run():
    results={case:cover(schema(case),16 if case=='both_paired' else 17) for case in CASES}
    minima={'both_paired':16,'extra_equals_J':16,'extra_outside_J_ordinary':16,
            'extra_endpoint_X':17,'extra_inner_R_SZ_paired':17,'extra_inner_R_SZ_separate':None}
    for case,result in results.items():
        if result['minimum_classes']!=minima[case] or any(max(p)<15 for p in result['survivors']):
            raise RuntimeError('Unexpected complete cover outcome: '+case)
    positive={}
    for case in CASES[:-1]:
        s=schema(case);p=tuple(range(len(s['names'])))
        if necessary(p,s) is not None:
            raise RuntimeError('All-distinct positive partial patch rejected: '+case)
        positive[case]=p
    separate=schema(CASES[-1])
    trimmed=dict(separate)
    trimmed['faces']=separate['faces'][:-1]
    if necessary(tuple(range(17)),trimmed) is not None:
        raise RuntimeError('Separate prefix positive control rejected')
    positive['inner_separate_without_final_Q']=tuple(range(17))
    extra_J=schema('extra_equals_J')
    old_fifteen=tuple(range(15))+(14,12)
    negatives={
        'E_equals_J_fifteen_point_alias':necessary(old_fifteen,extra_J),
        'inner_separate_all_distinct':necessary(tuple(range(17)),separate),
        'paired_second_triangle_equals_first':necessary(tuple(range(9))+(0,)+tuple(range(10,16)),schema('both_paired'))}
    if any(value is None for value in negatives.values()):
        raise RuntimeError('Negative control incorrectly accepted')
    return {'agent':'six-tammes-1','role':'researcher',
            'status':'AUTHOR_CHECKED_EXACT_CONDITIONAL_ORIGINAL_FACE_ALIAS_EXCLUSION',
            'excluded_profile':[2,4,0],'covers':results,
            'controls':{'positive_partial_consistency':positive,'negative':negatives},
            'remaining_r1_profiles_full_interval':[[0,6,0],[0,4,1],[0,2,2],[1,5,0],[1,3,1]],
            'remaining_profiles_on_beta':{'r1':5,'r2':12,'r3':11,'total':28},
            'trust_boundary':'Written geometry, original face forcing, roles, links and pruning are unformalized. Separate same-author algorithm; independent review pending. No unrestricted optimizer cover or global numerical bound.'}


if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
