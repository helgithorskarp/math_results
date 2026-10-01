"""Complete exact original-face cover for profile(0,4,1); see PROOF.md.
Standard library only; no floating sign, solver or private input.
F always has FOUR Ts. All five deficient originals are fixed before aliases.
--export-partitions regenerates the transient comparison trace for audit.py.
"""
from pathlib import Path
from collections import Counter,defaultdict
from itertools import combinations
import argparse,hashlib,json

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

ANCHORS=('F','U','X','R','S','T','Z','D')
CORE=(('F','X','R'),('F','R','S'),('F','S','T'),('F','T','Z'),
      ('F','Z','D','X'),('R','L','K','S'),('R','X','P','L'),
      ('S','K','M','T'),('T','M','Q','Z'))
TABLE={
 'D_zero':(('E','G'),('X','Z','E','G'),('D',)),
 'D_one_X_one':(('E','G','A0'),('D','X','E','G'),('A0',)),
 'D_one_Z_one':(('E','G','A0'),('D','Z','E','G'),('A0',)),
 'D_one_both_one':(('E','A0'),('D','X','Z','E'),('A0',)),
}

def schema(role,choice):
    extra,ones,zeros=TABLE[role];originals=ANCHORS+extra
    deficient=tuple(n for n in originals if n in ones+zeros)
    contacts=tuple(deficient[i] for i in choice)
    names=originals+('L','K','M','P','Q');words=CORE
    if 'X' in ones:names+=('AX',);words+=(('X','D','AX','P'),)
    else:words+=(('X','D','P'),)
    if 'Z' in ones:names+=('AZ',);words+=(('Z','Q','AZ','D'),)
    else:words+=(('Z','Q','D'),)
    number={n:i for i,n in enumerate(names)}
    if len(deficient)!=5 or len(names)!=17:raise RuntimeError('Wrong exact role cover')
    return {'case':role+'_U'+''.join(contacts),'names':names,'words':words,'number':number,
        'faces':tuple(tuple(number[n] for n in w) for w in words),
        'mode':'full','maxima':{},'exact':{'F':4,'U':0,**{n:1 for n in ones},**{n:0 for n in zeros}},
        'distinct':(),'initial':tuple(range(len(originals))),
        'contact_edges':tuple((1,number[n]) for n in contacts)}

def complete_ordinary_stars(prefix,spec):
    roles={n:triangle_role(prefix,spec,n) for n in ('L','K','M')}
    words=();names=spec['names']
    for n in ('L','K','M'):
        if roles[n] not in (0,1,2):raise RuntimeError('Unclassified strip vertex')
        if roles[n]!=2:continue
        h='H'+n;names+=(h,)
        if n=='L':words+=(('L',h,'K'),('L','P',h))
        if n=='K':words+=(('K',h,'M'),('K','L',h))
        if n=='M':words+=(('M','K',h),('M',h,'Q'))
    full=dict(spec);full['names']=names;full['words']=spec['words']+words
    full['number']={n:i for i,n in enumerate(names)}
    full['faces']=tuple(tuple(full['number'][n] for n in w) for w in full['words'])
    return roles,full

def actual_state(prefix,spec):
    if len(prefix)!=len(spec['names']):raise RuntimeError('Incomplete original partition for star forcing')
    faces={cyclic(tuple(prefix[i] for i in w)) for w in spec['faces']}
    corners=defaultdict(list);neighbors=defaultdict(set);outgoing=defaultdict(dict)
    for face in faces:
        for i,v in enumerate(face):
            a,b=face[i-1],face[(i+1)%len(face)]
            corners[v].append(face);neighbors[v].update((a,b));outgoing[v][a]=b
    actual_neighbors={v:set(row) for v,row in neighbors.items()}
    for a,b in spec['contact_edges']:
        x,y=prefix[a],prefix[b];actual_neighbors.setdefault(x,set()).add(y);actual_neighbors.setdefault(y,set()).add(x)
    return faces,corners,neighbors,actual_neighbors,outgoing

def one_T_U_obstruction(prefix,spec):
    faces,corners,neighbors,actual_neighbors,outgoing=actual_state(prefix,spec)
    for name,t in spec['exact'].items():
        v=prefix[spec['number'][name]]
        if t!=1 or len(corners[v])!=2 or any(len(f)!=4 for f in corners[v]) or len(neighbors[v])!=3:continue
        if 1 in actual_neighbors[v] and 1 not in neighbors[v]:return name
    return None

def force_last_face(prefix,spec):
    faces,corners,neighbors,actual_neighbors,outgoing=actual_state(prefix,spec)
    # Keep the most primitive representative for readable exact face words.
    representatives={v:next(n for n,x in zip(spec['names'],prefix) if x==v) for v in set(prefix)}
    for v in sorted(corners):
        if v in (0,1) or len(corners[v])!=3:continue
        number=next(i for i,x in enumerate(prefix) if x==v);name=spec['names'][number]
        role=triangle_role(prefix,spec,name)
        t=sum(len(f)==3 for f in corners[v])
        if role-t not in (0,1):raise RuntimeError('Unexpected exact remaining face role')
        row=outgoing[v];first=set(row)-set(row.values());last=set(row.values())-set(row)
        if len(first)!=1 or len(last)!=1:raise RuntimeError('Known three-corner link is not a path')
        a,b=next(iter(first)),next(iter(last));start,end=representatives[a],representatives[b]
        # Existing directed link runs a to b; the last face must run b to a.
        if role-t==1:
            words=((name,start,end),);new_names=()
        else:
            j='J'+str(len(spec['names']));words=((name,start,j,end),);new_names=(j,)
        full=dict(spec);full['names']=spec['names']+new_names;full['words']=spec['words']+words
        full['number']={n:i for i,n in enumerate(full['names'])}
        full['faces']=tuple(tuple(full['number'][n] for n in w) for w in full['words'])
        if words[0] in spec['words']:raise RuntimeError('Repeated forcing without new information')
        return name,role,words,full
    return None

def controls():
    spec=schema('D_one_X_one',(0,2,4))
    prefix=(0,1,2,3,4,5,6,7,8,9,10,8,9,11,1,12,10)
    roles,full=complete_ordinary_stars(prefix,spec);p=prefix+(13,)
    if necessary(p,full) is not None or one_T_U_obstruction(p,full):
        raise RuntimeError('Fourteen-class positive ordinary-star patch rejected')
    steps=[]
    for expected_vertex,alias in (('D',13),('G',10)):
        forced=force_last_face(p,full)
        if forced is None or forced[0]!=expected_vertex or len(forced[2][0])!=4:
            raise RuntimeError('Positive forced-Q classifier differs')
        full=forced[3];p+=(alias,)
        if necessary(p,full) is not None:raise RuntimeError('Positive forced-Q extension rejected')
        steps+=list(forced[2])
    forced=force_last_face(p,full)
    if forced is None or forced[0]!='E' or len(forced[2][0])!=3 or necessary(p,forced[3]) is None:
        raise RuntimeError('Negative mandatory final-T control differs')
    before=schema('D_zero',(0,2,4));identity=before['initial']
    if necessary(identity,before) is not None:raise RuntimeError('Four-T F star rejected')
    wrong=dict(before);wrong['exact']=dict(before['exact'],F=3)
    if necessary(identity,wrong)!='excess_triangles':raise RuntimeError('Wrong F3 role accepted')
    toy={'names':('F','U','E','R','K','P','O1','O2'),'faces':((2,3,6,4),(2,5,7,3)),
         'number':{'F':0,'U':1,'E':2,'R':3,'K':4,'P':5,'O1':6,'O2':7},
         'mode':'full','maxima':{},'exact':{'F':4,'U':0,'E':1},'distinct':(),
         'contact_edges':((1,2),)}
    if necessary(tuple(range(8)),toy) is not None or one_T_U_obstruction(tuple(range(8)),toy)!='E':
        raise RuntimeError('One-T new-U-neighbor control differs')
    actual=dict(toy);actual['faces']=((2,3,6,4),(2,1,7,3))
    if necessary(tuple(range(8)),actual) is not None or one_T_U_obstruction(tuple(range(8)),actual):
        raise RuntimeError('Known-Q U neighbor wrongly excluded')
    return {'fourteen_class_positive_ordinary_star_prefix':prefix+(13,),
            'two_forced_Qs_positive_final_T_negative':True,'forced_Q_words':steps,
            'F_four_T_positive_three_T_negative':True,
            'one_T_four_new_U_neighbor_negative_known_Q_U_neighbor_positive':True}

def serialized(value):
    return (json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode()

def run():
    trace={'cases':{},'controls':controls()};stats=Counter();roles_summary={};terminal=0
    for role in TABLE:
        role_stats=Counter()
        for choice in combinations(range(5),3):
            spec=schema(role,choice);base=cover(spec);entries=[]
            stats['base_covers']+=1;stats['base_nodes']+=base['nodes'];stats['base_partial_survivors']+=len(base['survivors'])
            role_stats['base_nodes']+=base['nodes'];role_stats['base_partial_survivors']+=len(base['survivors'])
            for prefix in base['survivors']:
                roles,full=complete_ordinary_stars(prefix,spec);first=cover(full,prefix);closures=[]
                stats['ordinary_star_covers']+=1;stats['ordinary_star_nodes']+=first['nodes'];stats['ordinary_star_partial_survivors']+=len(first['survivors'])
                role_stats['ordinary_star_partial_survivors']+=len(first['survivors'])
                for p in first['survivors']:
                    stats['closure_roots']+=1;root={'prefix':p,'names':full['names'],'steps':[]};queue=[(p,full,[])]
                    while queue:
                        current,chart,path=queue.pop();bad=one_T_U_obstruction(current,chart)
                        if bad:
                            stats['one_T_U_new_neighbor_rejections']+=1
                            root['steps'].append({'path':path,'prefix':current,'reason':'one_T_U_new_neighbor','vertex':bad});continue
                        forced=force_last_face(current,chart)
                        if forced is None:
                            terminal+=1;root['steps'].append({'path':path,'prefix':current,'reason':'no_forced_fourth_face'});continue
                        name,t,words,next_spec=forced;result=cover(next_spec,current)
                        stats['closing_face_covers']+=1;stats['closing_face_nodes']+=result['nodes']
                        stats['maximum_closing_positions']=max(stats['maximum_closing_positions'],len(next_spec['names']))
                        root['steps'].append({'path':path,'prefix':current,'vertex':name,'triangle_role':t,
                            'forced_words':words,'new_names':next_spec['names'],'cover':result})
                        if len(path)>=12:raise RuntimeError('INCOMPLETE: fixed12faceforcingdepth')
                        for survivor in result['survivors']:queue.append((survivor,next_spec,path+list(words)))
                    closures.append(root)
                entries.append({'prefix':prefix,'triangle_roles':roles,'names':full['names'],
                    'forced_words':full['words'][len(spec['words']):],'cover':first,'closures':closures})
            trace['cases'][spec['case']]={'names':spec['names'],'words':spec['words'],'exact_roles':spec['exact'],
                'contacts':spec['contact_edges'],'initial':spec['initial'],'base':base,'ordinary_stars':entries}
        roles_summary[role]=dict(role_stats)
    if len(trace['cases'])!=40 or terminal:raise RuntimeError('Incomplete cover or terminal patch survives')
    stats['terminal_survivors']=terminal;stats['total_covers']=stats['base_covers']+stats['ordinary_star_covers']+stats['closing_face_covers']
    stats['total_nodes']=stats['base_nodes']+stats['ordinary_star_nodes']+stats['closing_face_nodes']
    encoded=serialized(trace)
    summary={'agent':'six-tammes-1','role':'researcher','status':'AUTHOR_CHECKED_CONDITIONAL_FULL_PROFILE_EXCLUSION',
        'excluded_profile':[0,4,1],'stats':dict(stats),'role_summary':roles_summary,'trace_sha256':hashlib.sha256(encoded).hexdigest(),
        'trace_bytes':len(encoded),'controls':trace['controls'],
        'remaining_r1_profiles_using_previous_three_profile_theorem':[[0,6,0],[1,5,0]],
        'trust_boundary':'Written full-interval geometry, original-star forcing, role coverage and pruning. Same-author separate audit; independent mathematical review/formalization pending. No global bound or optimizer coverage.'}
    return summary,trace

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--export-partitions',type=Path);args=parser.parse_args()
    summary,trace=run();expected=json.loads((Path(__file__).resolve().parent/'EXPECTED.json').read_text())
    if json.loads(serialized(summary))!=expected:raise RuntimeError('Recomputed summary differs from EXPECTED.json')
    if args.export_partitions:args.export_partitions.write_bytes(serialized(trace))
    print(serialized(summary).decode(),end='')
