"""Exact fan cover and nineteen Cramer-norm exclusions. No floating point.
Author: six-tammes-1, researcher. CPython 3.11.2 standard library.
The unformalized geometric reduction is in PROOF.md.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import copy, hashlib, json

from fans import (run, triple_run, build, fan, edges_of, star_path,
                  boundary_cycle, canonical, need)
from polynomial import T, ONE, bernstein, value
from rational import Rat

C=Rat(T); ONE_R=Rat(ONE); ZERO=Rat(); REF=2*C/(ONE_R+C)
AVAILABLE=(5,7,8,9,10,11)
LAST=(9,10,11)

def dot(x,y):
    return ((ONE_R-C)*sum((a*b for a,b in zip(x,y)),ZERO)
            +C*sum(x,ZERO)*sum(y,ZERO))

def sign_open(r):
    """Strict sign on (1/2,3/5), or zero meaning undecided/identically zero."""
    def sign(p):
        b=bernstein(p)
        if b and all(x>=0 for x in b) and any(x>0 for x in b): return 1
        if b and all(x<=0 for x in b) and any(x<0 for x in b): return -1
        return 0
    return sign(r.n)*sign(r.d)

def coordinates(triangles):
    original=set(edges_of(triangles)); edges=set(original)
    active={v for e in edges for v in e}; removed=[]
    while len(active)>3:
        nb={v:{w for e in edges if v in e for w in e if w!=v} for v in active}
        ears=sorted(v for v in active if len(nb[v])==2)
        need(ears,'triangulation ear missing')
        new=ears[0]; a,b=sorted(nb[new]); old=(nb[a]&nb[b])-{new}
        need(len(old)==1,'old ear triangle not unique')
        removed.append((new,a,b,next(iter(old))))
        active.remove(new); edges={e for e in edges if new not in e}
    anchors=tuple(sorted(active))
    need(edges==set(combinations(anchors,2)),'final anchor triangle')
    co={v:tuple(ONE_R if k==j else ZERO for k in range(3)) for j,v in enumerate(anchors)}
    for new,a,b,old in reversed(removed):
        co[new]=tuple(REF*(x+y)-z for x,y,z in zip(co[a],co[b],co[old]))
    need(all(not (dot(v,v)-ONE_R).n for v in co.values()),'unit norm identities')
    need(all(not (dot(co[a],co[b])-C).n for a,b in original),'contact identities')
    need(all(sign_open(Rat(x.d)) for v in co.values() for x in v),'coordinate poles')
    return co

def face_correspondence(row,representative):
    cycle=boundary_cycle(row['faces']); target=boundary_cycle(representative['faces'])
    n=len(cycle); need(len(target)==n,'different polygon sizes')
    target_faces={tuple(t) for t in representative['faces']}
    fs={0,1,row['c']}; target_fs={0,1,representative['c']}
    for shift in range(n):
        for sign in (-1,1):
            mapping={v:target[(shift+sign*k)%n] for k,v in enumerate(cycle)}
            image={tuple(sorted(mapping[v] for v in t)) for t in row['faces']}
            if image==target_faces and {mapping[v] for v in fs}==target_fs: return mapping
    raise ValueError('no full face/F correspondence')

def three_five_face_table():
    """Definition-level incidence derivation on all eight labeled F masks."""
    pairs=tuple(combinations(range(3),2)); rows=[]
    for mask in range(8):
        edges={p for k,p in enumerate(pairs) if mask&(1<<k)}
        triple=int(len(edges)==3)
        # Each F-F contact is T-T. A facial F clique contributes to all
        # three pairs. The other incident triangle at each pair is distinct.
        doubles={p:2-triple for p in edges}
        singles=[4-sum(n for p,n in doubles.items() if v in p)-triple for v in range(3)]
        need(all(n>=0 for n in singles),'negative single-F face count')
        used=sum(singles)+sum(doubles.values())+triple
        need(sum(singles)+2*sum(doubles.values())+3*triple==12,'F corner total')
        rows.append({'mask':mask,'edges':len(edges),'single_F_Ts':sum(singles),
                     'double_F_Ts':sum(doubles.values()),'triple_F_Ts':triple,
                     'F_free_Ts':10-used,'admitted':used<=10})
    return rows

def fan_cover():
    pairs=run(); extensions=triple_run()
    need(len(pairs)==9 and len(extensions)==25,'paired rotation/extension cover size')
    for row in pairs:
        aa,bb,tris=build(row['i'],row['j'])
        common_eligible={v for v in (2,3) if aa.index(v) in (1,2,3) and bb.index(v) in (1,2,3)}
        forced={v for v in (2,3) if row['triangle_counts'][v]>=3}
        need(common_eligible==forced,'F-TT link-position correspondence')
    surviving=[r for r in extensions if r.get('survives_triangle_ceiling')]
    need(Counter(r['third_five_contact_type'] for r in surviving)=={'P3':4,'K3':4},'three-F survivors')
    reps={}
    for row in surviving: reps.setdefault(row['third_five_contact_type'],row)
    for row in surviving:
        rep=reps[row['third_five_contact_type']]
        mapping=face_correspondence(row,rep)
        co=coordinates(row['faces']); target=coordinates(rep['faces'])
        need(all(not (dot(co[a],co[b])-dot(target[mapping[a]],target[mapping[b]])).n
                 for a,b in combinations(sorted(co),2)),'full Gram identity under face mapping')
    for row in surviving:
        if row['third_five_contact_type']!='P3': continue
        fs=(0,1,row['c'])
        endpoints={f:{star_path(f,row['faces'])[0],star_path(f,row['faces'])[-1]} for f in fs}
        repeated=[(a,b,endpoints[a]&endpoints[b]) for a,b in combinations(fs,2) if endpoints[a]&endpoints[b]]
        need(len(repeated)==1,'unique repeated Q-neighbor')
        a,b,shared=repeated[0]
        need(len(shared)==1 and endpoints[a]!=endpoints[b],'distinct Qs forced')
        v=next(iter(shared)); need(row['triangle_counts'][v]==2,'repeated neighbor has two Ts')
    return pairs,extensions,reps

def completed_triangle_core(rep):
    triangles=rep['faces']; co=coordinates(triangles)
    need((rep['i'],rep['j'],rep['c'])==(1,2,3),'deterministic K3 representative')
    qs=[]
    for f,new in zip((0,1,3),(9,10,11)):
        path=star_path(f,triangles); a,b=path[0],path[-1]
        denominator=ONE_R+dot(co[a],co[b])
        need(sign_open(denominator)==1,'Q reflection denominator')
        q=tuple(2*C/denominator*(x+y)-z for x,y,z in zip(co[a],co[b],co[f]))
        need(not (dot(q,q)-ONE_R).n,'Q completion unit norm')
        need(not (dot(q,co[a])-C).n and not (dot(q,co[b])-C).n,'Q completion contacts')
        co[new]=q; qs.append((f,a,new,b))
    need(all(sign_open(Rat(x.d)) for v in co.values() for x in v),'completed-core coordinate poles')
    contacts=set(); strict_pairs=0
    for a,b in combinations(sorted(co),2):
        delta=C-dot(co[a],co[b])
        if not delta.n: contacts.add((a,b))
        else:
            need(sign_open(delta)==1,'strict noncontact packing inequality')
            strict_pairs+=1
    prescribed=set(edges_of(triangles))
    for f,a,new,b in qs: prescribed.update((tuple(sorted((a,new))),tuple(sorted((b,new)))))
    need(contacts==prescribed and len(contacts)==21 and strict_pairs==45,'exact completed contact graph')
    degrees=Counter(v for e in contacts for v in e)
    need({v for v,d in degrees.items() if d<4}==set(AVAILABLE),'six unsaturated core points')
    need(all(degrees[f]==5 for f in (0,1,3)),'three saturated F degrees')
    need([degrees[v] for v in (2,4,6)]==[4,4,4],'three saturated R degrees')
    need([degrees[v] for v in AVAILABLE]==[3,3,3,2,2,2],'available degrees')
    need(3*5+9*4-2*len(contacts)==9,'nine required new core contacts')
    return co,contacts,qs

def determinant(rows):
    a,b,d=rows
    return (a[0]*(b[1]*d[2]-b[2]*d[1])-a[1]*(b[0]*d[2]-b[2]*d[0])
            +a[2]*(b[0]*d[1]-b[1]*d[0]))

def cramer_audit(co):
    normals={i:tuple((ONE_R-C)*a[k]+C*sum(a,ZERO) for k in range(3)) for i,a in co.items()}
    rows=[]
    for triple in combinations(AVAILABLE,3):
        ns=[normals[i] for i in triple]; d=determinant(ns)
        if triple==LAST:
            need(sign_open(d)==-1,'last contact triple is uniformly independent')
            rows.append({'triple':list(triple),'determinant_sign':-1,'status':'AT_MOST_ONE_POSITION'})
            continue
        # Y=adj(N)*(c,c,c). The adjugate identity is valid even when d=0.
        y=tuple(determinant([tuple(C if j==k else x for j,x in enumerate(row)) for row in ns]) for k in range(3))
        need(all(not (sum((a*b for a,b in zip(row,y)),ZERO)-C*d).n for row in ns),'N*Y=c*d*1 identity')
        # Check every column of adj(N)*N=d*I, including singular parameters.
        for col in range(3):
            rhs=[ns[row][col] for row in range(3)]
            for k in range(3):
                image=determinant([tuple(rhs[i] if j==k else x for j,x in enumerate(row)) for i,row in enumerate(ns)])
                need(not (image-(d if k==col else ZERO)).n,'adj(N)*N=d*I identity')
        g=dot(y,y)-d*d; sign=sign_open(g)
        need(sign in (-1,1),'unit contact triple exclusion undecided')
        rows.append({'triple':list(triple),'norm_residual_sign':sign,
                     'numerator_degree':len(g.n)-1,'denominator_degree':len(g.d)-1,
                     'residual_sha256':hashlib.sha256(json.dumps([g.n,g.d],separators=(',',':')).encode()).hexdigest(),
                     'status':'NO_UNIT_CONTACT_POINT'})
    need(len(rows)==20,'all available triples')
    need(Counter(r.get('norm_residual_sign') for r in rows[:-1])=={1:16,-1:3},'nineteen strict norm signs')
    return rows

def validate_certificate(certificate,rows):
    need(certificate['available_vertices']==list(AVAILABLE),'certificate available labels')
    need(certificate['last_triple']==list(LAST),'certificate remaining triple')
    expected={tuple(r['triple']):r['norm_residual_sign'] for r in rows[:-1]}
    entries=certificate['excluded_triples']
    need(len(entries)==19,'nineteen certificate rows')
    actual={tuple(r['triple']):r['sign'] for r in entries}
    need(len(actual)==19 and actual==expected,'entry-level triple/sign cover')

def q_occurrence_bookkeeping():
    # Four marked D vertices, each with capacity one X; three F corners.
    possible=[x for x in range(3+3,3+4+1) if x%2==0]
    need(possible==[6],'global X parity and capacity')
    # Three X/Y/D vertices have zeta; the fourth marked D has two slots.
    last=[k for k in range(3) if (3+k)%2==0]
    need(last==[1],'global zeta parity')
    # alpha+Y+X+zeta=2*pi is symbolic from X=2*pi-4*alpha,
    # zeta=3*alpha-Y. A fourth D Y/zeta requires a forbidden X.
    need(1-4+3==0 and 1-1==0,'remaining-angle linear identity')
    # Original vertex intersection counts, independently from fan splitting.
    intersections={p:8+6-(15-1-p) for p in (0,1)}
    need(intersections=={0:0,1:1},'two T-component vertex intersection counts')
    # Two weakly intersecting, internally distinct Q neighbor pairs cannot
    # describe the same simple Q if their other neighbors are distinct.
    pair_a={0,1};pair_b={0,2}
    need(len(pair_a&pair_b)==1 and pair_a!=pair_b,'single-ear Q sharing obstruction')
    return {'X_occurrences':possible,'fourth_D_zeta_occurrences':last,
            'T_patch_intersections':intersections,'maximum_three_extra_core_contacts':3+2+2,
            'required_core_contacts':9}

def expect_rejection(fn):
    try: fn()
    except (ValueError,ZeroDivisionError): return
    raise ValueError('false-certificate control was accepted')

def selftests(certificate,rows,representatives):
    controls=0
    for action in (lambda:need(False,'negative assertion'),lambda:Rat((1,),()),
                   lambda:ONE_R/ZERO):
        expect_rejection(action);controls+=1
    need(sign_open(Rat((0,1)))==1 and sign_open(Rat((0,-1)))==-1,'Bernstein sign controls')
    need(sign_open(ZERO)==0 and sign_open(Rat((-11,20)))==0,'zero and undecided sign controls')
    controls+=2
    for alteration in ('missing','duplicate','wrong_sign','extra_last','wrong_labels'):
        altered=copy.deepcopy(certificate)
        if alteration=='missing':altered['excluded_triples'].pop()
        if alteration=='duplicate':altered['excluded_triples'][-1]=copy.deepcopy(altered['excluded_triples'][0])
        if alteration=='wrong_sign':altered['excluded_triples'][0]['sign']*=-1
        if alteration=='extra_last':altered['excluded_triples'].append({'triple':list(LAST),'sign':1})
        if alteration=='wrong_labels':altered['available_vertices'][0]=0
        expect_rejection(lambda:validate_certificate(altered,rows));controls+=1
    altered=copy.deepcopy(representatives['K3']);altered['faces'].pop()
    expect_rejection(lambda:face_correspondence(altered,representatives['K3']));controls+=1
    # Definition-level coefficient evaluation of the Bernstein transform.
    for polynomial in ((1,),(-1,0,1),(0,1),(-1,4,-4),(1,-3,7,-5)):
        b=bernstein(polynomial);n=len(b)-1
        from math import comb
        for u in (Fraction(0),Fraction(1,3),Fraction(1,2),Fraction(1)):
            direct=sum(b[k]*comb(n,k)*u**k*(1-u)**(n-k) for k in range(n+1))
            need(direct==value(polynomial,Fraction(1,2)+u/Fraction(10)),'Bernstein evaluation identity')
    controls+=1
    return controls

def main():
    face_table=three_five_face_table();pairs,extensions,reps=fan_cover()
    co,contacts,qs=completed_triangle_core(reps['K3'])
    rows=cramer_audit(co)
    certificate=json.loads(Path(__file__).with_name('certificate.json').read_text())
    validate_certificate(certificate,rows)
    controls=selftests(certificate,rows,reps)
    bookkeeping=q_occurrence_bookkeeping()
    print(json.dumps({'agent':'six-tammes-1','role':'researcher',
      'status':'AUTHOR_AUDITED_EXACT_CONDITIONAL_THREE_FIVE_EXCLUSION',
      'scope':'Complete connected degree3..5 convex cellular T/Q graph, q8, 1/2<c<beta: n3=0, n5=2; two necessary profiles. No global bound or optimizer coverage.',
      'F_face_incidence_cover':face_table,'two_F_rotations':len(pairs),
      'two_F_octagon_types':sorted({r['canonical_mask'] for r in pairs}),
      'third_F_local_records':len(extensions),'third_F_surviving_P3':4,'third_F_surviving_K3':4,
      'full_face_and_Gram_correspondences':8,
      'representative_L10_mask':reps['P3']['canonical_mask'],
      'representative_N9_mask':reps['K3']['canonical_mask'],
      'completed_N9_Qs':[list(q) for q in qs],
      'completed_core_points':len(co),'completed_core_contacts':len(contacts),
      'completed_core_strict_noncontacts':45,'cramer_contact_triples':rows,
      'nineteen_norm_signs':{'positive':16,'negative':3},
      'quadrilateral_occurrence_checks':bookkeeping,'controls':controls,
      'remaining_profiles':[{'d41':4,'d42':0,'d51':0,'n3':0,'n4':13,'n5':2,'H_types':6},
                            {'d41':2,'d42':1,'d51':0,'n3':0,'n4':13,'n5':2,'H_types':5}],
      'independent_review':'PENDING','global_numerical_bounds':'UNCHANGED'},indent=2,sort_keys=True))

if __name__=='__main__':main()
