"""Separate exhaustive raw-label/cell-parity/bitset-link/signed-dual audit.

Imports no production predicate, schema or enumerator. Exact roles,
reversed actual face words and strip additions are specified separately.
Every base boundary and every suffix boundary is compared entrywise.
Same author; independent mathematical review and formalization pending.
"""
from itertools import combinations, product
from pathlib import Path
import json

ANCHORS=('F','U','X','R','S','T','Z','D')
BASE=(('F','R','X'),('F','S','R'),('F','T','S'),('F','Z','T'),
      ('F','X','D','Z'),('R','S','K','L'),('R','L','P','X'),
      ('S','T','M','K'),('T','Z','Q','M'))
ROLE_TABLE={
 'D_zero':(('A0',),('X','Z'),('D','A0'),('X','Z','D','A0')),
 'D_one_X_one':(('A0','B0'),('D','X'),('A0','B0'),('X','D','A0','B0')),
 'D_one_Z_one':(('A0','B0'),('D','Z'),('A0','B0'),('Z','D','A0','B0')),
}


def specification(role,contacts):
    extra,ones,zeros,deficient=ROLE_TABLE[role]
    originals=ANCHORS+extra
    names=originals+('L','K','M','P','Q');words=BASE
    if 'X' in ones:
        names+=('AX',);words+=(('X','P','AX','D'),)
    else:words+=(('X','P','D'),)
    if 'Z' in ones:
        names+=('AZ',);words+=(('Z','D','AZ','Q'),)
    else:words+=(('Z','D','Q'),)
    number={name:i for i,name in enumerate(names)}
    roles={'F':4,'U':0,**{name:1 for name in ones},**{name:0 for name in zeros}}
    return {'names':names,'words':words,
        'faces':tuple(tuple(number[n] for n in w) for w in words),
        'mode':'full','maxima':{},'exact':{number[n]:value for n,value in roles.items()},
        'distinct':(),'initial':tuple(range(len(originals))),
        'contact_edges':tuple((1,number[n]) for n in contacts)}


def extend(prefix,spec):
    positions={n:i for i,n in enumerate(spec['names'])}
    roles={n:spec['exact'].get(prefix[positions[n]],2) for n in ('L','K','M')}
    if roles['L']==roles['K']==2:
        kind='both_ordinary';words=(('L','K','H'),('L','H','P'),('K','M','H'))
    elif {roles['L'],roles['K']}=={0,2}:
        kind='ordinary_zero';words=(('L','K','H'),)
    else:raise RuntimeError('No valid left-strip classifier')
    names=spec['names']+('H',);number={n:i for i,n in enumerate(names)}
    result=dict(spec);result['names']=names
    result['faces']=spec['faces']+tuple(tuple(number[n] for n in w) for w in words)
    return kind,roles,result

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
    maximum[0], maximum[1] = 4, 0
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




def audit_base(spec,expected):
    start=len(spec['initial']);states={spec['initial']} if check(spec['initial'],spec) else set()
    if [list(p) for p in sorted(states)]!=expected['passing_partitions_by_depth'].get(str(start),[]):
        raise RuntimeError('Initial base partitions differ')
    previous=start;blocks=[]
    for end in list(range(start+2,len(spec['names']),2))+[len(spec['names'])]:
        final=set();raw=accepted=0
        for prefix in sorted(states):
            for tail in product(range(end),repeat=end-previous):
                raw+=1
                if raw>200000:raise RuntimeError('INCOMPLETE: fixed200000rawblockbudget')
                labels=prefix+tail
                if check(labels,spec):accepted+=1;final.add(normalize(labels))
        wanted=expected['passing_partitions_by_depth'].get(str(end),[])
        if [list(p) for p in sorted(final)]!=wanted:
            surplus=sorted(final-set(map(tuple,wanted)))[:3];missing=sorted(set(map(tuple,wanted))-final)[:3]
            raise RuntimeError('Base boundary '+str(end)+' differs surplus '+str(surplus)+' missing '+str(missing))
        blocks.append({'start_depth':previous,'end_depth':end,'raw_tuples':raw,
                       'accepted_raw_tuples':accepted,'normalized_partitions':sorted(final)})
        previous,states=end,final
    if [list(p) for p in sorted(states)]!=expected['survivors']:
        raise RuntimeError('Full base partition list differs')
    return {'initial_checked':True,'blocks':blocks,'final_normalized_partitions':sorted(states),
            'total_raw_tuples':sum(b['raw_tuples'] for b in blocks)}


def audit_suffix(prefix,spec,expected):
    kind,roles,full=extend(prefix,spec)
    if kind!=expected['kind'] or roles!=expected['triangle_roles']:
        raise RuntimeError('Exact strip roles differ')
    if not check(prefix,full):raise RuntimeError('Suffix initial prefix rejected')
    if expected['cover']['passing_partitions_by_depth'].get(str(len(prefix)))!=[list(prefix)]:
        raise RuntimeError('Suffix initial partition differs')
    final=set();raw=accepted=0
    for value in range(len(full['names'])):
        raw+=1;labels=prefix+(value,)
        if check(labels,full):accepted+=1;final.add(normalize(labels))
    wanted=expected['cover']['passing_partitions_by_depth'].get(str(len(full['names'])),[])
    if [list(p) for p in sorted(final)]!=wanted or final:
        raise RuntimeError('Strip extension boundary differs')
    return {'prefix':prefix,'kind':kind,'triangle_roles':roles,'raw_tuples':raw,
            'accepted_raw_tuples':accepted,'final_normalized_partitions':sorted(final)}


def controls():
    spec=specification('D_one_Z_one',('Z','A0','B0'))
    prefix=(0,1,2,3,4,5,6,7,8,9,10,11,8,12,1,9)
    if not check(prefix,spec):raise RuntimeError('Ordinary positive partial rejected')
    kind,roles,last=extend(prefix,spec);trimmed=dict(last);trimmed['faces']=last['faces'][:-1]
    if kind!='both_ordinary' or not check(prefix+(13,),trimmed) or check(prefix+(13,),last):
        raise RuntimeError('Two-T positive/three-T negative strip control differs')
    mixed=specification('D_one_X_one',('X','A0','B0'))
    mp=(0,1,2,3,4,5,6,7,8,9,8,10,11,1,12,9)
    if not check(mp,mixed):raise RuntimeError('Mixed positive partial rejected')
    kind,roles,mlast=extend(mp,mixed)
    if kind!='ordinary_zero' or check(mp+(13,),mlast):
        raise RuntimeError('Mixed forced-T negative control differs')
    star=specification('D_zero',('X','D','A0'))
    if not check(star['initial'],star):raise RuntimeError('Four-T fan rejected')
    wrong=dict(star);wrong['exact']=dict(star['exact']);wrong['exact'][0]=3
    if check(star['initial'],wrong):raise RuntimeError('Wrong three-T F role accepted')
    for tail in ((5,),(9,10,3)):
        bare=dict(star);bare['faces']=star['faces'][:5]
        if not check(star['initial']+tail,bare):raise RuntimeError('Early fan alias wrongly banned')
    toy=dict(spec);toy['faces']=((1,7,2,6),);toy['contact_edges']=((1,7),(1,6),(1,8))
    identity=tuple(range(10))
    if not check(identity,toy):raise RuntimeError('Separate edge positive control rejected')
    diagonal=dict(toy);diagonal['contact_edges']=((1,7),(1,6),(1,2))
    extra=dict(toy);extra['contact_edges']=toy['contact_edges']+((1,9),)
    if check(identity,diagonal) or check(identity,extra):
        raise RuntimeError('Separate edge negative control accepted')
    quotient=(0,1,2,3,4,5,6,7,8,9,10,8,10,7,6,9)
    cells=((0,2,3),(0,4,5),(2,3,9),(4,5,10),
           (0,1,6,2),(0,3,8,4),(0,5,7,1),(1,7,11,6),
           (2,6,12,9),(3,9,13,8),(4,8,14,10),(5,10,15,7))
    twisted={'faces':cells,'distinct':(),'mode':'maxima','maxima':{},'exact':{}}
    if not check(quotient,twisted,False) or check(quotient,twisted,True):
        raise RuntimeError('Signed-dual quotient control differs')
    return {'ordinary_and_mixed_positive_partial_patches':True,
            'two_T_strip_positive_full_third_T_negative':True,
            'mixed_zero_T_negative':True,'F_four_T_positive_F_three_T_negative':True,
            'early_L_equals_T_M_equals_R_allowed_before_strip_activation':True,
            'separate_actual_contact_controls':True,'local_pass_signed_dual_fail_quotient':True}


def run():
    expected=json.loads((Path(__file__).resolve().parent/'EXPECTED.json').read_text())['covers']
    results={};total=0;extension_count=0
    for role,(extra,ones,zeros,deficient) in ROLE_TABLE.items():
        for omitted in range(4):
            contacts=tuple(n for i,n in enumerate(deficient) if i!=omitted)
            key=role+'_U'+''.join(contacts);saved=expected[key];spec=specification(role,contacts)
            base=audit_base(spec,saved['base']);total+=base['total_raw_tuples'];ext=[]
            if len(base['final_normalized_partitions'])!=len(saved['strip_extensions']):
                raise RuntimeError('Number of suffix prefixes differs')
            for prefix,entry in zip(base['final_normalized_partitions'],saved['strip_extensions']):
                if list(prefix)!=entry['prefix']:raise RuntimeError('Suffix prefix order differs')
                result=audit_suffix(prefix,spec,entry);ext.append(result);total+=result['raw_tuples'];extension_count+=1
            results[key]={'names':spec['names'],'base':base,'strip_extensions':ext}
    if set(results)!=set(expected) or extension_count!=20:
        raise RuntimeError('Role/contact/suffix coverage differs')
    return {'agent':'six-tammes-1','role':'researcher',
        'status':'SEPARATE_SAME_AUTHOR_RAW_LABEL_CELL_PARITY_BITSET_SIGNED_DUAL_AUDIT',
        'base_covers':12,'strip_covers':extension_count,'total_raw_tuples':total,
        'covers':results,'controls':controls(),
        'entrywise_comparison':'Every initial/base block-boundary/final and all suffix boundaries equal EXPECTED.json. No production schema/predicate/enumerator import; no K4 or global face-count shortcut.',
        'scope':'Written geometry, original-star forcing and role coverage remain unformalized; independent review pending.'}


if __name__=='__main__':
    result=run();saved=Path(__file__).resolve().parent/'AUDIT_EXPECTED.json'
    if saved.exists() and json.loads(json.dumps(result))!=json.loads(saved.read_text()):
        raise RuntimeError('Audit differs from AUDIT_EXPECTED.json')
    print(json.dumps(result,sort_keys=True,separators=(',',':')))
