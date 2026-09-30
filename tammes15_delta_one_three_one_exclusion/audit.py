"""Separate raw-label, unoriented-cell, bitset-link and signed-dual audit.

Imports no production schema, predicate or enumerator. Fixed raw role tables
and reversed actual face words are specified here separately. All saved
block-boundary and final partitions are compared entrywise.
Same author; independent peer review remains pending.
"""
from itertools import combinations, product
from pathlib import Path
import json

ANCHORS=('F','U','X','R','S','V','W','B','C')
RAW_CORE=(('F','R','X'),('F','S','R'),('F','W','V'),
          ('F','V','B','S'),('F','X','C','W'),
          ('R','S','Q','L'),('R','L','P','X'))
# Explicit labelled role cover. The order of deficient originals is fixed
# independently, to label each of its four three-element contact choices.
ROLE_TABLE={
 'A_X':((),('X','B','C'),('Z0',),('X','B','C','Z0')),
 'A_S':((),('S','B','C'),('Z0',),('S','B','C','Z0')),
 'A_V':((),('V','B','C'),('Z0',),('V','B','C','Z0')),
 'A_W':((),('W','B','C'),('Z0',),('W','B','C','Z0')),
 'A_outside':(('E',),('B','C','E'),('Z0',),('B','C','E','Z0')),
 'Bzero_X':((),('X','S','C'),('B',),('X','S','B','C')),
 'Bzero_V':((),('S','V','C'),('B',),('S','V','B','C')),
 'Bzero_W':((),('S','W','C'),('B',),('S','W','B','C')),
 'Bzero_outside':(('E',),('S','C','E'),('B',),('S','B','C','E')),
 'Czero_S':((),('X','S','B'),('C',),('X','S','B','C')),
 'Czero_V':((),('X','V','B'),('C',),('X','V','B','C')),
 'Czero_W':((),('X','W','B'),('C',),('X','W','B','C')),
 'Czero_outside':(('E',),('X','B','E'),('C',),('X','B','C','E')),
}


def specification(role,contacts,stage):
    extra,ones,zeros,deficient=ROLE_TABLE[role]
    originals=ANCHORS+extra+tuple(n for n in zeros if n not in ANCHORS)
    exact={'F':3,'U':0,**{n:1 for n in ones},**{n:0 for n in zeros}}
    names=originals+('L','P','Q')
    words=RAW_CORE
    if 'X' in ones:
        names+=('AX',);words+=(('X','P','AX','C'),)
    else:words+=(('X','P','C'),)
    if 'S' in ones:
        names+=('AS',);words+=(('S','B','AS','Q'),)
    else:words+=(('S','B','Q'),)
    if stage=='unpaired':
        if 'V' not in ones:
            names+=('JV',);words+=(('V','JV','B'),)
        if 'W' not in ones:
            names+=('JW',);words+=(('W','C','JW'),)
    else:
        names+=('H','M','N')
        words+=(('W','H','V'),('V','H','M','B'),('W','C','N','H'))
        if 'B' in ones and 'S' in ones:words+=(('B','M','AS'),)
        else:
            names+=('JB',);words+=(('B','M','JB','AS' if 'S' in ones else 'Q'),)
        if 'C' in ones and 'X' in ones:words+=(('C','AX','N'),)
        else:
            names+=('KC',);words+=(('C','AX' if 'X' in ones else 'P','KC','N'),)
        if stage=='H_Q':
            names+=('JH',);words+=(('H','N','JH','M'),)
    number={name:i for i,name in enumerate(names)}
    return {'names':names,'faces':tuple(tuple(number[n] for n in w) for w in words),
            'mode':'full','maxima':{},'exact':{number[n]:value for n,value in exact.items()},
            'distinct':(),'initial':tuple(range(len(originals))),
            'contact_edges':tuple((number['U'],number[n]) for n in contacts)}

def normalize(labels):
    rename, answer = {}, []
    for value in labels:
        if value not in rename:
            rename[value] = len(rename)
        answer.append(rename[value])
    return tuple(answer)


def face_key(face):
    rotated = [face[i:] + face[:i] for i in range(len(face))]
    reverse = face[::-1]
    rotated.extend(reverse[i:] + reverse[:i] for i in range(len(face)))
    return min(rotated)


def check(labels, spec, use_orientability=True):
    assigned = len(labels)
    for a, b in spec['distinct']:
        if a < assigned and b < assigned and labels[a] == labels[b]:
            return False
    faces = set()
    description_parity = {}
    for word in spec['faces']:
        if max(word) < assigned:
            actual = tuple(labels[i] for i in word)
            if len(set(actual)) != len(actual):
                return False
            key=face_key(actual)
            # Every source word follows the same orientation of the sphere.
            # A convex hemispherical cell cannot be described on both sides
            # of a boundary edge. Preserve this fact when cells coalesce.
            least=actual.index(min(actual))
            parity=1 if actual[(least+1)%len(actual)]==key[1] else -1
            if key in description_parity and description_parity[key]!=parity:
                return False
            description_parity[key]=parity
            faces.add(key)
    # Raw labels need not all occur. Original exceptional classes are fixed early.
    limit=max(2,max(labels)+1,len(spec.get('names',())))
    degree = [4] * limit
    degree[0], degree[1] = 5, 3
    maximum = [2] * limit
    maximum[0], maximum[1] = 3, 0
    exact = maximum[:] if spec['mode'] == 'full' else [None] * limit
    for index, value in spec['maxima'].items():
        if index < assigned:
            maximum[labels[index]] = min(maximum[labels[index]], value)
    fixed = {}
    for index, value in spec['exact'].items():
        if index < assigned:
            actual = labels[index]
            if actual in fixed and fixed[actual] != value:
                return False
            fixed[actual] = value
            exact[actual] = value
            maximum[actual] = min(maximum[actual], value)
    if any(t is not None and t > maximum[v] for v,t in enumerate(exact)):
        return False
    neighbors, banned = [0]*limit, [0]*limit
    link = [{} for _ in range(limit)]
    corners, triangles = [0]*limit, [0]*limit
    for face in faces:
        size = len(face)
        if size == 4:
            for offset in (0,1):
                a, b = face[offset], face[offset+2]
                banned[a] |= 1 << b
                banned[b] |= 1 << a
        for i, v in enumerate(face):
            a, b = face[i-1], face[(i+1) % size]
            neighbors[v] |= (1 << a) | (1 << b)
            corners[v] += 1
            triangles[v] += size == 3
            if b in link[v].get(a, set()):
                return False
            link[v].setdefault(a, set()).add(b)
            link[v].setdefault(b, set()).add(a)
    for a,b in spec.get('contact_edges',()):
        if a<assigned and b<assigned:
            x,y=labels[a],labels[b]
            if x==y:return False
            neighbors[x] |= 1<<y
            neighbors[y] |= 1<<x
    for v in range(limit):
        if (neighbors[v] & banned[v] or neighbors[v].bit_count() > degree[v]
                or corners[v] > degree[v] or triangles[v] > maximum[v]):
            return False
        if exact[v] is not None and corners[v]-triangles[v] > degree[v]-exact[v]:
            return False
        if any(len(row) > 2 for row in link[v].values()):
            return False
        unseen = set(link[v])
        while unseen:
            stack = [unseen.pop()]
            component = set(stack)
            while stack:
                item = stack.pop()
                for other in link[v][item]:
                    if other not in component:
                        component.add(other)
                        unseen.remove(other)
                        stack.append(other)
            if all(len(link[v][item]) == 2 for item in component):
                if len(component) != degree[v] or neighbors[v].bit_count() != degree[v]:
                    return False
                if exact[v] is not None and triangles[v] != exact[v]:
                    return False
    for a, b in combinations(range(limit), 2):
        if (neighbors[a] & neighbors[b]).bit_count() > 2:
            return False
    if use_orientability:
        # An orientable cell embedding admits one sign per actual face so
        # all shared boundary edges are traversed in opposite directions.
        boundary, actual_faces = {}, sorted(faces)
        for index, face in enumerate(actual_faces):
            for i, a in enumerate(face):
                b = face[(i+1) % len(face)]
                boundary.setdefault(tuple(sorted((a,b))), []).append(
                    (index, 1 if a < b else -1))
        dual = [[] for _ in actual_faces]
        for occupants in boundary.values():
            if len(occupants) > 2:
                return False
            if len(occupants) == 2:
                (a,sa), (b,sb) = occupants
                multiplier = -sa*sb
                dual[a].append((b,multiplier))
                dual[b].append((a,multiplier))
        signs = {}
        for root in range(len(actual_faces)):
            if root in signs:
                continue
            signs[root], stack = 1, [root]
            while stack:
                a = stack.pop()
                for b, multiplier in dual[a]:
                    desired = signs[a]*multiplier
                    if b in signs:
                        if signs[b] != desired:
                            return False
                    else:
                        signs[b] = desired
                        stack.append(b)
    # No production orientation, K4 test or global face-count shortcut.
    return True



def audit_case(spec,expected):
    start=len(spec['initial'])
    states={spec['initial']} if check(spec['initial'],spec) else set()
    initial_expected=expected['passing_partitions_by_depth'].get(str(start),[])
    if [list(p) for p in sorted(states)]!=initial_expected:
        raise RuntimeError('Initial boundary differs')
    previous=start;blocks=[]
    boundaries=list(range(start+2,len(spec['names']),2))+[len(spec['names'])]
    for end in boundaries:
        final=set();raw=accepted=0
        for prefix in sorted(states):
            for tail in product(range(end),repeat=end-previous):
                raw+=1
                if raw>200000:raise RuntimeError('INCOMPLETE: fixed raw-block budget')
                labels=prefix+tail
                if check(labels,spec):
                    accepted+=1;final.add(normalize(labels))
        wanted=expected['passing_partitions_by_depth'].get(str(end),[])
        if [list(p) for p in sorted(final)]!=wanted:
            surplus=sorted(final-set(map(tuple,wanted)))[:3]
            missing=sorted(set(map(tuple,wanted))-final)[:3]
            raise RuntimeError('Boundary differs '+str(end)+' surplus '+str(surplus)+' missing '+str(missing))
        blocks.append({'start_depth':previous,'end_depth':end,'raw_tuples':raw,
                       'accepted_raw_tuples':accepted,'normalized_partitions':sorted(final)})
        previous,states=end,final
    if [list(p) for p in sorted(states)]!=expected['survivors']:
        raise RuntimeError('Final partition list differs')
    return {'initial_checked':True,'names':spec['names'],'blocks':blocks,
            'total_raw_tuples':sum(b['raw_tuples'] for b in blocks),
            'final_normalized_partitions':sorted(states)}


def controls():
    spec=specification('A_outside',('B','E','Z0'),'basic')
    quotient=(0,1,2,3,4,5,6,7,8,9,10,11,12,13,9,1,14,10,10)
    alternative=quotient[:-1]+(15,)
    if not check(quotient,spec) or not check(alternative,spec):
        raise RuntimeError('Positive partial patches rejected')
    last=specification('A_outside',('B','E','Z0'),'H_Q')
    if any(check(quotient+(value,),last) for value in range(16)):
        raise RuntimeError('Negative closing-Q extension accepted')
    for value in (5,6):
        if not check(spec['initial']+(value,),spec):
            raise RuntimeError('Early L=V/W alias rejected')
    toy=dict(spec);toy['faces']=((1,7,2,8),);toy['contact_edges']=((1,7),(1,8),(1,9))
    identity=tuple(range(11))
    if not check(identity,toy):raise RuntimeError('Separate-edge positive control rejected')
    diagonal=dict(toy);diagonal['contact_edges']=((1,7),(1,8),(1,2))
    overdegree=dict(toy);overdegree['contact_edges']=toy['contact_edges']+((1,10),)
    if check(identity,diagonal) or check(identity,overdegree):
        raise RuntimeError('Separate-edge negative control accepted')
    # Published earlier proper local quotient: orientability is essential.
    twisted_labels=(0,1,2,3,4,5,6,7,8,9,10,8,10,7,6,9)
    cells=((0,2,3),(0,4,5),(2,3,9),(4,5,10),
           (0,1,6,2),(0,3,8,4),(0,5,7,1),(1,7,11,6),
           (2,6,12,9),(3,9,13,8),(4,8,14,10),(5,10,15,7))
    twisted={'faces':cells,'distinct':(),'mode':'maxima','maxima':{},'exact':{}}
    if not check(twisted_labels,twisted,False) or check(twisted_labels,twisted,True):
        raise RuntimeError('Signed-dual control differs')
    return {'positive_fifteen_and_sixteen_class_partial_patches':True,
            'all_sixteen_closing_Q_extensions_rejected':True,
            'early_L_may_equal_V_or_W':True,'separate_actual_edge_controls_passed':True,
            'nonorientable_local_quotient_rejected_by_signed_dual':True}


def run():
    expected=json.loads((Path(__file__).resolve().parent/'EXPECTED.json').read_text())['covers']
    results={}
    for role,(extra,ones,zeros,deficient) in ROLE_TABLE.items():
        # Generate each three-contact choice by omitting one of four originals.
        for omitted in range(4):
            contacts=tuple(n for i,n in enumerate(deficient) if i!=omitted)
            stages=('unpaired',) if 'V' in ones or 'W' in ones else ('unpaired','basic')
            for stage in stages:
                key=role+'_U'+''.join(contacts)+'_'+stage
                result=audit_case(specification(role,contacts,stage),expected[key]);results[key]=result
                if stage=='basic' and result['final_normalized_partitions']:
                    spec=specification(role,contacts,stage)
                    idx=spec['names'].index('H');eidx=spec['names'].index('E')
                    if any(p[idx]!=p[eidx] for p in result['final_normalized_partitions']):
                        raise RuntimeError('H=E classifier differs')
                    key=role+'_U'+''.join(contacts)+'_H_Q'
                    results[key]=audit_case(specification(role,contacts,'H_Q'),expected[key])
    if set(results)!=set(expected):raise RuntimeError('Cover identifier sets differ')
    return {'agent':'six-tammes-1','role':'researcher',
            'status':'SEPARATE_SAME_AUTHOR_RAW_LABEL_UNORIENTED_SIGNED_DUAL_AUDIT',
            'covers':results,'total_raw_tuples':sum(r['total_raw_tuples'] for r in results.values()),
            'controls':controls(),
            'entrywise_comparison':'Every initial, two-slot block-boundary and final partition equals EXPECTED.json. No production schema, predicate or enumerator import, no K4 or global face-count shortcut.',
            'scope':'Written geometric and actual-face bridges remain unformalized; independent review pending.'}


if __name__=='__main__':
    result=run()
    saved=Path(__file__).resolve().parent/'AUDIT_EXPECTED.json'
    if saved.exists() and json.loads(json.dumps(result))!=json.loads(saved.read_text()):
        raise RuntimeError('Audit differs from AUDIT_EXPECTED.json')
    print(json.dumps(result,sort_keys=True,separators=(',',':')))
