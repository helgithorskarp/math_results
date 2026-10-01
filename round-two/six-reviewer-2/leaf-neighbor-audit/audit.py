"""Independent exact leaf-interface and low-type-count audit; standard library."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

J = ((1,8,9),(0,),(6,7),(4,5),(3,7,9),(3,6,8),
     (2,5,9),(2,4,8),(0,5,7),(0,4,6))
F = tuple(frozenset(y-2 for y in J[x] if y >= 2) for x in range(2,10))

def require(condition, message):
    if not condition:
        raise ValueError(message)

def compact(value):
    return json.dumps(value, separators=(',',':'), sort_keys=True).encode()

def patterns():
    """Choose four singleton columns and two missing colors: 3**6 states.

    The two degree-two ordinary columns must avoid BOTH neighboring singleton
    columns. If those singletons differ, no two-subset of three can do so.
    This is a complete necessary-domain generator, separate from both author
    algorithms (3**8 columns and ordered 70**2 row pairs).
    """
    found = []
    states = 0
    for colors in itertools.product(range(3),repeat=6):
        states += 1
        c4,c5,c6,c7,miss8,miss9 = colors
        if c6!=c7 or c4!=c5:
            continue
        columns = [set(range(3))-{c6},set(range(3))-{c4},
                   {c4},{c5},{c6},{c7},
                   set(range(3))-{miss8},set(range(3))-{miss9}]
        # Six-cycle ordinary red edges each force disjoint T neighborhoods.
        if any(columns[i]&columns[j] for i in range(6) for j in F[i]
               if j<6 and i<j):
            continue
        rows = tuple(sum(1<<i for i in range(8) if t in columns[i]) for t in range(3))
        if any(row.bit_count()!=4 for row in rows):
            continue
        require(all(len(columns[i])==4-len(F[i]) for i in range(8)), 'column margin')
        found.append(rows)
    require(states==729 and len(found)==len(set(found))==12,'complete interface size')
    return sorted(found), states

def distinguished(rows):
    hits = [t for t in range(3) if rows[t]&192==192]
    require(len(hits)==1, 'unique two-special row')
    return hits[0]

def frame(left,right):
    # T=0,1,2; mark=3; roots=4,5; X=6..13, Y=14..21.
    matrix = [[False]*22 for _ in range(22)]
    def red(a,b): matrix[a][b]=matrix[b][a]=True
    red(4,5);red(4,3);red(5,3)
    for offset,root,rows in ((6,4,left),(14,5,right)):
        for i in range(8):
            red(root,offset+i)
            if i>=6:red(3,offset+i)
            for j in F[i]:
                if i<j:red(offset+i,offset+j)
            for t in range(3):
                if rows[t]>>i&1:red(t,offset+i)
    for t in range(3):red(3,t)
    return matrix

def pages(matrix,a,b):
    color=matrix[a][b]
    return tuple(x for x in range(22) if x!=a and x!=b
                 and matrix[a][x]==color and matrix[b][x]==color)

def interfaces(rows):
    counts={'red_four':0,'blue_seven':0}
    toggles=0
    free=[(a,b) for a in range(6,14) for b in range(14,22)]
    require(len(free)==64, 'unknown cross set')
    for left,right in itertools.product(rows,repeat=2):
        matrix=frame(left,right)
        require([sum(matrix[t]) for t in range(6)]==[9,9,9,9,10,10],'fixed degrees')
        gx,gy=distinguished(left),distinguished(right)
        spine=(3,gx) if gx==gy else (gx,gy)
        wanted=4 if gx==gy else 7
        require(matrix[spine[0]][spine[1]]==(gx==gy),'spine color')
        original=pages(matrix,*spine)
        require(len(original)==wanted,'literal forbidden pages')
        counts['red_four' if gx==gy else 'blue_seven']+=1
        # Proof of all-assignment invariance: no free edge meets the spine.
        require(all(spine[0] not in edge and spine[1] not in edge for edge in free),
                'free edge touches endpoint')
        for a,b in free:
            matrix[a][b]=matrix[b][a]=True
            require(pages(matrix,*spine)==original,'single-edge sensitivity')
            matrix[a][b]=matrix[b][a]=False
            toggles+=1
        for a,b in free:matrix[a][b]=matrix[b][a]=True
        require(pages(matrix,*spine)==original,'all-red sensitivity')
    require(counts=={'red_four':48,'blue_seven':96},'pair count')
    return {'pattern_pairs':144,**counts,'free_edges':64,'single_toggles':toggles,
            'all_red_controls':144,'endpoint_disjointness_checks':144}

def compositions(total,parts):
    if parts==1:
        yield (total,)
    else:
        for first in range(total+1):
            for tail in compositions(total-first,parts-1):
                yield (first,)+tail

def low_types():
    # Seven nonempty neighbor types on three low points z,a,b; no empty type.
    types=[frozenset(i for i in range(3) if mask>>i&1) for mask in range(1,8)]
    cases=[];tested=0
    for e in (0,1):
        for counts in compositions(19,7):
            tested+=1
            margins=[sum(c for c,s in zip(counts,types) if i in s) for i in range(3)]
            if margins != [6,8-e,8-e]:continue
            by_type={s:c for s,c in zip(types,counts)}
            y=by_type[frozenset((1,2))];t=by_type[frozenset((0,1,2))]
            r=by_type[frozenset((1,))]+by_type[frozenset((2,))]
            require(r==13-y,'rootless occurrence identity')
            require(y+2*t<=3-2*e,'extra incidence constraint')
            require(r>=10+2*e+2*t,'stronger occurrence')
            capacity=16-2*e
            require(2*r-capacity>=4+6*e+4*t,'stronger nonleaf count')
            # Direct low-spine caps; these are relaxed counts, not full hosts.
            require(by_type[frozenset((0,1))]+t+e<=3,'za red cap')
            require(by_type[frozenset((0,2))]+t+e<=3,'zb red cap')
            require(y+t+1<=3 if e else y+t+1<=4,'ab red/blue cap')
            cases.append({'e_ab':e,'counts':counts,'t':t,'y':y,'R':r,
                          'incidence_capacity':capacity,'nonleaf_lower':2*r-capacity})
    minima=[]
    for e,t in ((0,0),(0,1),(1,0)):
        subset=[x for x in cases if x['e_ab']==e and x['t']==t]
        require(subset,'nonvacuous relaxed stratum')
        minima.append({'e_ab':e,'t':t,'profiles':len(subset),
                       'minimum_nonleaf':min(x['nonleaf_lower'] for x in subset)})
    require(len(cases)==16 and [x['minimum_nonleaf'] for x in minima]==[4,8,10],
            'complete low-count strata')
    return {'weak_compositions_tested':tested,'necessary_profiles':cases,'stratum_minima':minima}

def audit():
    require(all(i in J[j] for i in range(10) for j in J[i]),'J symmetry')
    key=sum(1<<k for k,(i,j) in enumerate(itertools.combinations(range(10),2)) if j in J[i])
    require(key==6790396772737 and sum(map(len,J))==26,'literal leaf key')
    rows,states=patterns()
    result={'agent':'six-reviewer-2','role':'independent mathematical reviewer',
            'leaf_key':key,'six_choice_states':states,'patterns':rows,
            'patterns_sha256':hashlib.sha256(compact(rows)).hexdigest(),
            'interfaces':interfaces(rows),'low_type_counts':low_types()}
    return result

def validate(record, expected):
    require(record==expected,'complete mathematical record mismatch')

def self_test(expected):
    import copy
    mutations=[]
    for damage in range(6):
        bad=copy.deepcopy(expected)
        if damage==0:bad['patterns'].pop()
        if damage==1:bad['patterns'][0][0]^=1
        if damage==2:bad['interfaces']['red_four']=47
        if damage==3:bad['interfaces']['blue_seven']=95
        if damage==4:bad['low_type_counts']['stratum_minima'][1]['minimum_nonleaf']=6
        if damage==5:bad['low_type_counts']['necessary_profiles'].pop()
        try:validate(bad,expected)
        except ValueError:mutations.append(damage)
        else:raise ValueError('damaged evidence accepted')
    return {'semantic_damages_rejected':mutations}

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--check-file',type=Path)
    parser.add_argument('--self-test',action='store_true')
    args=parser.parse_args()
    result=audit()
    if args.check_file:validate(json.loads(args.check_file.read_text()),json.loads(compact(result)))
    print(compact(self_test(json.loads(compact(result))) if args.self_test else result).decode())
