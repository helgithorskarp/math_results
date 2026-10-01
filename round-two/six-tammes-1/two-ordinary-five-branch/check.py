"""Exact necessary contact/face checks for PROOF.md. six-tammes-1, researcher.
CPython >=3.11 standard library. No expected file or private input is read.
"""
from collections import Counter
from itertools import combinations, permutations, product
import hashlib
import json

from core import C, U, CLASSES, dot, paired_fan_cover, complete_core, sign_open
from fans import need, edges_of
from polynomial import bernstein


def digest(x):
    return hashlib.sha256(json.dumps(x, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def edge(a, b):
    return tuple(sorted((a, b)))


def neighbors(edges, v):
    return sorted(b if a == v else a for a, b in edges if v in (a, b))


def corners(v, triangles, qs):
    pairs = []
    for t in triangles:
        if v in t:
            pairs.append(tuple(sorted(w for w in t if w != v)))
    for q in qs:
        if v in q:
            k = q.index(v)
            pairs.append(edge(q[k-1], q[(k+1) % 4]))
    need(len(pairs) == len(set(pairs)), 'distinct actual face corners')
    return set(pairs)


def link_cycles(nb, required):
    # Enumerate cyclic words with their least neighbor first, modulo reversal.
    result = []
    for tail in permutations(nb[1:]):
        word = (nb[0],) + tail
        if word[1] > word[-1]:
            continue
        pairs = {edge(word[k], word[(k+1) % len(word)]) for k in range(len(word))}
        if required <= pairs:
            result.append(pairs)
    return result


def relabeled_patch_sets(triangles):
    result = set()
    for swap_f, swap_s, swap_l, swap_r in product((0, 1), repeat=4):
        m = {0:1 if swap_f else 0, 1:0 if swap_f else 1,
             2:3 if swap_s else 2, 3:2 if swap_s else 3}
        for src, dst, swap in (((4,5), (6,7) if swap_f else (4,5), swap_l),
                              ((6,7), (4,5) if swap_f else (6,7), swap_r)):
            m.update(zip(src, dst[::-1] if swap else dst))
        result.add(tuple(sorted(tuple(sorted(m[v] for v in t)) for t in triangles)))
    need(len(result) == 8, 'eight role-labeled T patches')
    return sorted(result)


def core_certificate(co, contacts):
    sign_witnesses = []
    for v in sorted(co):
        need(not (dot(co[v],co[v])-U).n, 'unit identity')
        for k,r in enumerate(co[v]):
            need(sign_open(type(r)(r.d)) != 0, 'coordinate pole')
            sign_witnesses.append(['pole',v,k,r.d])
    for a,b in combinations(range(14),2):
        g = C-dot(co[a],co[b])
        if (a,b) in contacts:
            need(not g.n, 'contact identity')
        elif (a,b) in {e for cls in CLASSES for e in cls}:
            r = U-dot(co[a],co[b]); need(sign_open(r)==1, 'exceptional injectivity')
            sign_witnesses.append(['different',a,b,r.n,r.d])
        else:
            need(sign_open(g)==1, 'strict packing gap')
            sign_witnesses.append(['gap',a,b,g.n,g.d])
    # Compact digest of every exact reduced sign input and its Bernstein data.
    bern = [[list(map(str,bernstein(row[-2]))), list(map(str,bernstein(row[-1])))]
            if row[0] != 'pole' else [list(map(str,bernstein(row[-1])))]
            for row in sign_witnesses]
    return {'positions':14,'pair_count':91,'fixed_contacts':25,'strict_gaps':62,
            'exceptional_pairs':4,'reduced_sign_inputs_sha256':digest(sign_witnesses),
            'bernstein_witnesses_sha256':digest(bern)}


def adjacent_cover(contacts, triangles, qs):
    records=[]; raw=0
    for mask in range(4):
        core=set(contacts)
        for k,cls in enumerate(CLASSES):
            if mask & (1<<k): core.update(cls)
        for d in (3,4):
            for nb in combinations(range(14),d):
                raw+=1
                es=core|{edge(14,v) for v in nb}
                deg=Counter(v for e in es for v in e)
                if len(es)!=30 or deg[0]!=5 or deg[1]!=5:
                    continue
                if any(deg[v] not in (3,4) for v in range(2,15)):
                    continue
                if sum(deg[v]==3 for v in range(15))!=2:
                    continue
                need(d==3 and mask in (1,2), 'degree parity')
                cls='A' if mask==1 else 'B'
                omitted=next(v for v in range(14) if deg[v]==3)
                r={'class':cls,'outside_neighbors':list(nb),'omitted':omitted}
                if cls=='A' and omitted in (10,11):
                    o=6 if omitted==10 else 4
                    need(edge(o,omitted) in es, 'three/ordinary-four fixed contact')
                    need(sum(o in t for t in triangles)==2,'ordinary four witness')
                    r.update(reason='THREE_ORDINARY_CONTACT',witness=[omitted,o])
                elif cls=='A':
                    p=5 if omitted==12 else 7
                    other=8 if omitted==12 else 9
                    cycles=link_cycles(neighbors(es,p),corners(p,triangles,qs))
                    need(cycles and all(edge(other,omitted) in cy for cy in cycles),'forced T link sector')
                    need(edge(other,omitted) in es,'sector neighbors contact')
                    r.update(reason='TRIANGLE_AT_THREE',witness=sorted([p,other,omitted]))
                elif omitted in (8,9):
                    q=qs[0 if omitted==8 else 1]
                    need(q[2]==omitted,'ordinary-five Q opposite')
                    r.update(reason='FIVE_OPPOSITE_THREE',witness=list(q))
                else:
                    zeros=[]
                    for v in (8,9,10,11):
                        need(deg[v]==4,'claimed zero-T four degree')
                        cycles=link_cycles(neighbors(es,v),corners(v,triangles,qs))
                        need(cycles and all(not (cy & es) for cy in cycles),'all possible sectors Q')
                        zeros.append(v)
                    need(len(zeros)>3,'census zero-four bound')
                    r.update(reason='FOUR_ZERO_FOURS_EXCEED3',witness=zeros)
                records.append(r)
    records.sort(key=lambda r:(r['class'],r['outside_neighbors']))
    need(raw==5460 and len(records)==8,'complete adjacent degree cover')
    return {'raw_degree_candidates':raw,'admitted_entries':records,
            'admitted_entries_sha256':digest(records),
            'released_geometric_terminal_tests_admitted':len(records)}


def shared_q_cover():
    rows=[]
    for ordinary in range(5,9):
        choices=list(combinations(range(ordinary-2),3))
        records=[[list(a),list(b),2+len(set(a)&set(b))] for a,b in product(choices,repeat=2)]
        allowed=[r for r in records if r[2]<=2]
        if ordinary<=7: need(not allowed,'third common contact when at most seven ordinary')
        else: need(len(allowed)==20,'released eighth ordinary control')
        rows.append({'ordinary_fours':ordinary,'raw_subset_pairs':len(records),
                     'common_contact_records_sha256':digest(records),'admitted':len(allowed)})
    return rows


def noncontact_b1():
    # All fifteen actual originals retained. F,G,U,V,A,D,C,E,B,I0..I2,J0..J2.
    F,G,U0,V,A,D,C0,E,B=range(9)
    allowed_h={B,C0,E};allowed_k={B,A,D};rows=[];raw=[]
    for h,k in product(range(15),repeat=2):
        admissible=h in allowed_h and k in allowed_k
        raw.append([h,k,admissible])
        if not admissible: continue
        forced={edge(A,h),edge(D,h),edge(C0,k),edge(E,k)}
        need(all(set(e)<={A,D,C0,E,B} for e in forced),'deficient-four ends only')
        ends=Counter(v for e in forced for v in e)
        extra=0 if B in (h,k) else 2
        required=sum(ends.values())+extra
        need(required==8 and required>2*4+4*1-6,'deficient QQ-end budget')
        rows.append({'H':h,'K':k,'forced_edges':[list(e) for e in sorted(forced)],
                     'forced_deficient_ends':sum(ends.values()),'additional_B_ends':extra,
                     'required_ends':required,'available_ends':6})
    need(len(raw)==225 and len(rows)==9,'all b1 original opposite aliases')
    return {'raw_original_opposite_pairs':225,'admitted_aliases_sha256':digest(raw),
            'terminal_entries':rows,'terminal_entries_sha256':digest(rows)}


def noncontact_b2():
    # F,G,U,V,A,D,I0,I1,I2,J0,J1,J2,P,zero1,zero2.
    F,G,U0,V,A,D,I0,I1,I2,J0,J1,J2,P,Z1,Z2=range(15)
    full_p={F,G,I2,J2};g_neighbors={D,J0,J1,J2,P};rows=[]
    for h in range(15):
        if h not in full_p: reason='OUTSIDE_COMPLETE_P_CONTACTS'
        elif h==F: reason='REPEATED_Q_VERTEX'
        elif h==I2: reason='CONTACT_Q_DIAGONAL'
        elif h==G:
            need(A not in g_neighbors,'GA exceeds complete G contacts')
            reason='OUTSIDE_COMPLETE_G_CONTACTS'
        else:
            need(h==J2,'ordinary-four opposite witness')
            reason='ORDINARY_FOUR_OPPOSITE_FIVE'
        rows.append([h,reason])
    # Cover endpoint slots before normal form: two one-T roles, one remaining O.
    endpoint_rows=[]
    for fp,gp in product(permutations((A,D,P),2),repeat=2):
        use=Counter(fp+gp)
        if use[A]<=1 and use[D]<=1:
            need(use[A]==use[D]==1 and use[P]==2,'forced shared ordinary endpoint')
            endpoint_rows.append([list(fp),list(gp)])
    need(len(endpoint_rows)==8,'all ordered endpoint assignments')
    return {'credited_existing_case':True,'original_Q_opposite_aliases':rows,
            'opposite_aliases_sha256':digest(rows),
            'ordered_endpoint_normal_forms':endpoint_rows,
            'endpoint_forms_sha256':digest(endpoint_rows)}


def catalogue_corollaries():
    # Literal imported rows from lemma8975 EXPECTED.json; derivation not regenerated.
    committed=[(2,2,1,0,2,0,8),(2,2,1,1,0,1,8),(2,2,2,2,0,0,7),
               (2,3,0,0,1,1,8),(2,3,1,1,1,0,7),(2,4,0,0,2,0,7),
               (2,4,0,1,0,1,7),(2,4,1,2,0,0,6),(2,5,0,1,1,0,6),(2,6,0,2,0,0,5)]
    source=[r for r in committed if r not in committed[:3]]
    rows=[]
    for name,prior,wanted in [('committed_basis',committed,7),('source_only_basis',source,5)]:
        remain=[list(r) for r in prior if r[3]!=2]
        removed=[list(r) for r in prior if r[3]==2]
        need(len(remain)==wanted and all(r[0]==2 for r in remain),'catalogue deletion')
        rows.append({'name':name,'imported_count':len(prior),'remaining_count':wanted,
                     'remaining_profiles':remain,'removed_profiles':removed,
                     'derivation_imported_not_regenerated':True})
    return rows


def run():
    fan_rows,rep=paired_fan_cover()
    co,contacts,qs,degrees=complete_core(rep)
    patch_sets=relabeled_patch_sets(rep['faces'])
    census=[[6-2*b,b,5+b] for b in range(4)]
    need(15-30+8+9==2 and 3*8+4*9==2*30,'Euler and face degrees')
    need(2*3+11*4+2*5==2*30,'two-threes/two-fives census')
    need(6>census[0][2],'six distinct noncontact internals exceed five ordinary fours')
    # b3: both actual threes must have precisely the same three zero-T neighbors.
    need(census[-1]==[0,3,8] and len({0,1,2})>2,'b3 common-contact obstruction')
    return {'actual_agent':'six-tammes-1','role':'researcher',
            'scope':'complete connected convex hemispherical T/Q15 graph,9Q,n5=2,both four-T,1/2<c<3/5',
            'status':'author-checked conditional proof; unformalized geometric bridges',
            'census_a_b_ordinary':census,'paired_fan_rotations':len(fan_rows),
            'permitted_rotations':[[r['i'],r['j']] for r in fan_rows if max(r['triangle_counts'][v] for v in (2,3))<=2],
            'role_labeled_T_patch_sets_sha256':digest(patch_sets),
            'core_certificate':core_certificate(co,contacts),
            'adjacent':adjacent_cover(contacts,rep['faces'],qs),
            'shared_Q':shared_q_cover(),'noncontact_b1':noncontact_b1(),
            'noncontact_b2':noncontact_b2(),'catalogue_corollaries':catalogue_corollaries(),
            'global_numerical_bound_unchanged':True}


if __name__=='__main__':
    print(json.dumps(run(),sort_keys=True,indent=2))
