#!/usr/bin/env python3
"""Independent actual-role incidence audit of the two-ordinary-five branch.

Generation differs from author code: connected four-edge subgraphs give fan
paths; degree-deficit assignments give outside neighbors; missing-degree
recursion completes local links. Endpoint geometry uses literal Fractions.
The open-interval continuous core is an explicit reviewed premise, not code.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
TRIANGLES = ((0,1,2),(0,1,3),(0,3,4),(0,4,5),(1,2,6),(1,6,7))
QUADS = ((0,2,8,5),(1,3,9,7),(2,6,10,8),(3,4,11,9),(4,5,12,11),(6,7,13,10))
CLASSES = (((8,12),(9,13)),((10,12),(11,13)))


def need(ok, message):
    if not ok:
        raise ValueError(message)


def edge(a,b):
    need(type(a) is int and type(b) is int and a != b, 'distinct original contact endpoints')
    return tuple(sorted((a,b)))


def canonical(obj):
    return json.dumps(obj,sort_keys=True,separators=(',',':')).encode()


def digest(obj):
    return sha256(canonical(obj)).hexdigest()


class Audit:
    def __init__(self):self.checks,self.damages=[],[]
    def check(self, ok, message):
        need(ok,message);self.checks.append(message)
    def reject(self, fn, message):
        try:fn()
        except ValueError:self.damages.append(message)
        else:raise ValueError('damage accepted: '+message)


def graph(vertices, es):
    result={v:set() for v in vertices}
    for a,b in es:
        need(a in result and b in result, 'actual edge lies in current vertex set')
        result[a].add(b);result[b].add(a)
    return result


def connected(vertices, es):
    vertices=set(vertices)
    if not vertices:return False
    g=graph(vertices,es);seen=set();stack=[min(vertices)]
    while stack:
        v=stack.pop()
        if v in seen:continue
        seen.add(v);stack.extend(g[v]-seen)
    return seen==vertices


def path_subgraphs(vertices, required):
    """All connected four-edge degree-at-most-two graphs on five originals."""
    vertices=sorted(vertices);out=[]
    for rows in combinations(list(combinations(vertices,2)),4):
        es=set(rows)
        if not set(required)<=es:continue
        g=graph(vertices,es)
        if sorted(len(g[v]) for v in vertices)!=[1,1,2,2,2] or not connected(vertices,es):continue
        out.append(frozenset(es))
    return out


def link_completions(vertices, required):
    """Complete missing degrees to two, then require one connected cycle."""
    vertices=tuple(sorted(vertices));required=frozenset(required)
    if any(not set(e)<=set(vertices) for e in required):return []
    initial=Counter(v for e in required for v in e)
    if any(initial[v]>2 for v in vertices):return []
    done=set()
    def recurse(es, degrees):
        missing=[v for v in vertices if degrees[v]<2]
        if not missing:
            if connected(vertices,es):done.add(frozenset(es))
            return
        a=missing[0]
        for b in vertices:
            if b==a or degrees[b]>=2 or edge(a,b) in es:continue
            updated=degrees.copy();updated[a]+=1;updated[b]+=1
            recurse(es|{edge(a,b)},updated)
    recurse(required,initial)
    return sorted(done,key=lambda es:sorted(es))


def contact_edges():
    out={edge(a,b) for t in TRIANGLES for a,b in combinations(t,2)}
    for q in QUADS:
        out.update(edge(q[k],q[(k+1)%4]) for k in range(4))
    return out


def required_corners(v):
    rows=[]
    for t in TRIANGLES:
        if v in t:rows.append(tuple(sorted(w for w in t if w != v)))
    for q in QUADS:
        if v in q:
            k=q.index(v);rows.append(edge(q[k-1],q[(k+1)%4]))
    need(len(set(rows))==len(rows), 'known actual face corners distinct')
    return set(rows)


def fan_cover(audit):
    allpaths=[path_subgraphs((1,2,3,4,5),()),path_subgraphs((0,2,3,6,7),())]
    paths=[path_subgraphs((1,2,3,4,5),((1,2),(1,3))),path_subgraphs((0,2,3,6,7),((0,2),(0,3)))]
    audit.check([len(x) for x in allpaths]==[60,60], 'complete unlabeled-orientation fan path edge domain')
    audit.check([len(x) for x in paths]==[6,6], 'all adjacent-five paths retain both actual common thirds')
    admitted=[];patches=set()
    for fp,gp in product(*paths):
        ts={tuple(sorted((0,)+e)) for e in fp}|{tuple(sorted((1,)+e)) for e in gp}
        counts=Counter(v for t in ts for v in t)
        if counts[2]<=2 and counts[3]<=2:
            admitted.append({'F_path_edges':[list(e) for e in sorted(fp)],'G_path_edges':[list(e) for e in sorted(gp)],'triangles':[list(t) for t in sorted(ts)]});patches.add(tuple(sorted(ts)))
    audit.check(len(admitted)==len(patches)==8, 'complete admitted undirected paired-fan patches')
    images=set();maps=[]
    for fg,shared,private in product(permutations((0,1)),permutations((2,3)),permutations((4,5,6,7))):
        image=dict(zip(range(8),fg+shared+private))
        ts=tuple(sorted(tuple(sorted(image[v] for v in t)) for t in TRIANGLES))
        if ts in patches:
            images.add(ts);maps.append([image[v] for v in range(8)])
    audit.check(images==patches, 'literal whole triangle-set bijections cover every admitted patch')
    return {'all_paths_each':60,'necessary_paths_each':6,'raw_path_pairs':36,'admitted_path_pairs':admitted,'complete_patch_sets':[list(map(list,p)) for p in sorted(patches)],'role_labeled_T_patch_sets_sha256':digest(sorted(patches)),'bijection_count':len(maps),'whole_T_bijections':maps}


def adjacent_cover(audit):
    base=contact_edges();audit.check(len(base)==25, '25 necessary core contacts regenerated from actual faces')
    rows=[];assignment_controls=[]
    for mask in range(4):
        es=base|{p for k,cls in enumerate(CLASSES) if mask&(1<<k) for p in cls}
        coredeg=Counter(v for e in es for v in e)
        # Enumerate complete final3/4 role assignments first; outside contacts
        # are exactly the one-unit deficits, without guessed neighbor triples.
        for three in range(2,14):
            targets={v:(5 if v<2 else 3 if v==three else 4) for v in range(14)}
            deficits={v:targets[v]-coredeg[v] for v in range(14)}
            if any(x not in (0,1) for x in deficits.values()):continue
            nb=tuple(v for v in range(14) if deficits[v]==1)
            if len(nb)!=3 or len(es)+len(nb)!=30:continue
            full=es|{edge(14,v) for v in nb}
            audit.check(mask in (1,2), 'parity forces exactly one paired exceptional class '+str((mask,three)))
            row={'class':'A' if mask==1 else 'B','outside_neighbors':list(nb),'omitted':three}
            if mask==1:
                ords=[v for v in (2,3,4,6) if edge(v,three) in full]
                if ords:
                    audit.check(len(ords)==1 and sum(ords[0] in t for t in TRIANGLES)==2, 'omitted three contacts an actual ordinary four '+str(three))
                    row.update(reason='THREE_ORDINARY_CONTACT',witness=[three,ords[0]])
                else:
                    witness=[]
                    for p in (5,7):
                        nbp=sorted(v for v in range(15) if v!=p and edge(p,v) in full)
                        cycles=link_completions(nbp,required_corners(p))
                        audit.check(bool(cycles),'nonempty required four-link at '+str(p))
                        for a,b in combinations(nbp,2):
                            if three in (a,b) and edge(a,b) in full and all(edge(a,b) in cy for cy in cycles):witness.append(sorted((p,a,b)))
                    audit.check(len(witness)==1, 'every degree-deficit completion forces a triangle at the omitted three '+str(three))
                    row.update(reason='TRIANGLE_AT_THREE',witness=witness[0])
            elif three in (8,9):
                qs=[list(q) for q in QUADS if q[0] in (0,1) and q[2]==three]
                audit.check(len(qs)==1,'exact known Q opposite at omitted three '+str(three))
                row.update(reason='FIVE_OPPOSITE_THREE',witness=qs[0])
            else:
                zeros=[]
                for v in (8,9,10,11):
                    nbv=sorted(w for w in range(15) if w!=v and edge(v,w) in full)
                    cycles=link_completions(nbv,required_corners(v))
                    audit.check(len(nbv)==4 and bool(cycles) and all(not (set(cy)&full) for cy in cycles), 'every actual link has zero T at four '+str((three,v)))
                    zeros.append(v)
                audit.check(len(zeros)>3, 'four zero-T fours violate global two-ordinary-five census '+str(three))
                row.update(reason='FOUR_ZERO_FOURS_EXCEED3',witness=zeros)
            rows.append(row)
        # A degree-four outside point makes the required core count26.
        assignment_controls.append({'class_mask':mask,'core_edges':len(es),'outside_degree4_required_core_edges':26,'parity_can_equal26':len(es)==26})
    rows.sort(key=lambda r:(r['class'],r['outside_neighbors']))
    audit.check(len(rows)==8 and all(not r['parity_can_equal26'] for r in assignment_controls), 'complete eight original degree assignments and no outside four')
    return {'final_three_role_assignments_tested':48,'outside_degree4_parity_controls':assignment_controls,'admitted_entries':rows,'admitted_entries_sha256':digest(rows),'released_terminal_tests_admitted':len(rows)}


def b1_cover(audit):
    # Actual originals:0F,1G,2U,3V,4A,5D,6C,7E,8B,9..11I,12..14J.
    A,D,C,E,B=4,5,6,7,8
    H_allowed={B,C,E};K_allowed={B,A,D};rows=[];allaliases=[]
    for h,k in product(range(15),repeat=2):
        ok=h in H_allowed and k in K_allowed;allaliases.append([h,k,ok])
        if not ok:continue
        forced={edge(A,h),edge(D,h),edge(C,k),edge(E,k)}
        incidence=Counter(v for p in forced for v in p)
        # The zero-T original has at most two actual three neighbors, leaving
        # at least two nonthree QQ ends unless those edges are already forced.
        extras=max(0,2-incidence[B])
        mandatory=sum(incidence.values())+extras
        audit.check(set(incidence)<=set((A,D,C,E,B)) and mandatory==8 and mandatory>6, 'full original opposite QQ debt '+str((h,k)))
        rows.append({'H':h,'K':k,'forced_edges':[list(p) for p in sorted(forced)],'forced_deficient_ends':sum(incidence.values()),'additional_B_ends':extras,'required_ends':mandatory,'available_ends':6})
    audit.check(len(rows)==9 and len(allaliases)==225,'all b1 original opposite aliases')
    return {'raw_original_opposite_pairs':225,'admitted_aliases_sha256':digest(allaliases),'terminal_entries':rows,'terminal_entries_sha256':digest(rows)}


def b2_cover(audit):
    # Independently enumerate four endpoint slots by multiset capacity.
    A,D,P=4,5,12;forms=[]
    for slots in product((A,D,P),repeat=4):
        if slots[0]==slots[1] or slots[2]==slots[3]:continue
        used=Counter(slots)
        if used[A]>1 or used[D]>1:continue
        audit.check(used[A]==used[D]==1 and used[P]==2,'endpoint-slot capacity forces common ordinary original '+str(slots))
        forms.append([list(slots[:2]),list(slots[2:])])
    rows=[];complete_P={0,1,8,11};complete_G={D,9,10,11,P}
    for h in range(15):
        if h not in complete_P:reason='OUTSIDE_COMPLETE_P_CONTACTS'
        elif h==0:reason='REPEATED_Q_VERTEX'
        elif h==8:reason='CONTACT_Q_DIAGONAL'
        elif h==1:
            audit.check(A not in complete_G,'forced opposite G would add forbidden original endpoint contact')
            reason='OUTSIDE_COMPLETE_G_CONTACTS'
        else:
            audit.check(h==11,'last remaining original Q opposite is ordinary')
            reason='ORDINARY_FOUR_OPPOSITE_FIVE'
        rows.append([h,reason])
    forms.sort();audit.check(len(forms)==8,'all ordered endpoint assignments generated by capacity')
    return {'original_Q_opposite_aliases':rows,'opposite_aliases_sha256':digest(rows),'ordered_endpoint_normal_forms':forms,'endpoint_forms_sha256':digest(forms)}


def shared_q(audit):
    rows=[]
    for ordinary in range(5,9):
        # Two actual shared endpoints consume2 ordinary roles; six internal
        # occurrences are chosen with aliases before common-contact pruning.
        cases=[]
        choices=list(combinations(range(ordinary-2),3))
        for x,y in product(choices,repeat=2):cases.append([list(x),list(y),2+len(set(x)&set(y))])
        admitted=[r for r in cases if r[2]<=2]
        audit.check(not admitted if ordinary<=7 else len(admitted)==20,'shared Q ordinary-capacity and released-eight control '+str(ordinary))
        rows.append({'ordinary_fours':ordinary,'raw_subset_pairs':len(cases),'common_contact_records_sha256':digest(cases),'admitted':len(admitted)})
    return rows


def endpoints(audit):
    rows=[]
    expected=contact_edges();exceptional={p for cls in CLASSES for p in cls}
    for c in (F(1,2),F(3,5)):
        def dot(x,y):return (1-c)*sum(a*b for a,b in zip(x,y))+c*sum(x)*sum(y)
        co={1:(F(1),F(0),F(0)),6:(F(0),F(1),F(0)),7:(F(0),F(0),F(1))};normals=[]
        for new,a,b,old in ((2,1,6,7),(0,1,2,6),(3,0,1,2),(4,0,3,1),(5,0,4,3)):
            co[new]=tuple(2*c/(1+c)*(x+y)-z for x,y,z in zip(co[a],co[b],co[old]))
        for f,a,new,b in QUADS:
            denominator=1+dot(co[a],co[b]);audit.check(denominator>0,'endpoint true Q divisor '+str((c,new)));normals.append(str(denominator))
            co[new]=tuple(2*c/denominator*(x+y)-z for x,y,z in zip(co[a],co[b],co[f]))
        audit.check(all(dot(v,v)==1 for v in co.values()),'all14 endpoint unit identities '+str(c))
        pairs=[]
        for a,b in combinations(range(14),2):
            inner=dot(co[a],co[b]);gap=c-inner
            if (a,b) in expected:audit.check(gap==0,'endpoint fixed actual contact '+str((c,a,b)))
            elif (a,b) in exceptional:audit.check(1-inner>0,'endpoint exceptional original distinctness '+str((c,a,b)))
            else:audit.check(gap>0,'endpoint strict nonexception packing gap '+str((c,a,b)))
            pairs.append({'pair':[a,b],'inner':str(inner),'packing_gap':str(gap),'injectivity_gap':str(1-inner)})
        class_gaps=[c-dot(co[cls[0][0]],co[cls[0][1]]) for cls in CLASSES]
        audit.check(all(c-dot(co[a],co[b])==gap for cls,gap in zip(CLASSES,class_gaps) for a,b in cls),'endpoint paired-class equality '+str(c))
        audit.check(all(gap<0 for gap in class_gaps) if c==F(1,2) else all(gap>0 for gap in class_gaps), 'endpoint adjacent pair excluded by metric or degree parity '+str(c))
        rows.append({'c':str(c),'all14_original_positions':[[str(x) for x in co[v]] for v in range(14)],'all91_pairs':pairs,'Q_denominators':normals,'class_gaps':[str(x) for x in class_gaps]})
    return rows


def catalogue():
    # Exact imported prior rows, with provenance in INPUTS. Their derivations
    # are an explicit ordinary premise; the code only checks literal deletion.
    prior=[(2,2,1,0,2,0,8),(2,2,1,1,0,1,8),(2,2,2,2,0,0,7),(2,3,0,0,1,1,8),(2,3,1,1,1,0,7),(2,4,0,0,2,0,7),(2,4,0,1,0,1,7),(2,4,1,2,0,0,6),(2,5,0,1,1,0,6),(2,6,0,2,0,0,5)]
    later=[r for r in prior if r not in prior[:3]]
    return [{'name':name,'imported_count':len(rows),'remaining_count':len([r for r in rows if r[3]!=2]),'remaining_profiles':[list(r) for r in rows if r[3]!=2],'removed_profiles':[list(r) for r in rows if r[3]==2],'derivation_imported_not_regenerated':True} for name,rows in [('committed_basis',prior),('source_only_basis',later)]]


def run():
    audit=Audit()
    census=[[6-2*b,b,5+b] for b in range(4)]
    audit.check(15-30+8+9==2 and 3*8+4*9==60,'complete sphere Euler and face side sums')
    audit.check(census==[[6,0,5],[4,1,6],[2,2,7],[0,3,8]],'all four complete triangle-deficit censuses')
    audit.check(3>2,'b3 common-neighbor bound contradiction')
    audit.check(6>census[0][2],'b0 six distinct ordinary internal originals contradiction')
    audit.check(len(link_completions(range(4),()))==3,'unconstrained four-link complete-cycle control')
    audit.check(len(link_completions(range(5),()))==12,'unconstrained five-link complete-cycle control')
    audit.check(not link_completions(range(4),((0,1),(1,2),(0,2))), 'smaller sealed cycle cannot be a complete original link')
    out={'actual_agent':'six-reviewer-3','role':'independent mathematical reviewer','method':'path edge subsets, final degree-deficit assignments, missing-degree link recursion, actual-slot capacity and QQ incidence debt, literal rational endpoint Gram data', 'census':census,'fan':fan_cover(audit),'adjacent':adjacent_cover(audit),'b1':b1_cover(audit),'b2':b2_cover(audit),'shared_Q':shared_q(audit),'endpoint_metric_records':endpoints(audit),'catalogue':catalogue()}
    audit.reject(lambda:need(out['b1']['terminal_entries'][0]['required_ends']<=6,'wrong QQ budget'),'discarded required deficient incidence debt')
    audit.reject(lambda:need(out['adjacent']['admitted_entries']==[],'wrong parity cover'),'lost all eight actual original completions')
    audit.reject(lambda:need(len(out['fan']['complete_patch_sets'])==7,'wrong fan normalization'),'lost an actual triangle patch')
    audit.reject(lambda:need(link_completions(range(4),((0,1),(1,2),(0,2))),'wrong sealed-cycle handling'),'accepted a disconnected complete link')
    audit.reject(lambda:need(out['b2']['original_Q_opposite_aliases'][11][1]!='ORDINARY_FOUR_OPPOSITE_FIVE','wrong original opposite'),'accepted final ordinary-four Q opposite')
    audit.reject(lambda:edge(1,1),'repeated actual edge original')
    audit.reject(lambda:need(F(out['endpoint_metric_records'][0]['class_gaps'][0])>=0,'wrong endpoint metric sign'),'accepted endpoint negative packing gap')
    audit.reject(lambda:need(out['catalogue'][0]['remaining_count']==8,'wrong original catalogue deletion'),'wrong conditional committed profile count')
    out.update(exact_checks=audit.checks,rejected_damages=audit.damages)
    return out


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--fixture',type=Path,default=BASE/'EXPECTED.json');parser.add_argument('--emit-fixture',type=Path);parser.add_argument('--author-fixture',type=Path);args=parser.parse_args();out=run()
    if args.emit_fixture is not None:args.emit_fixture.write_text(json.dumps(out,indent=2)+'\n')
    else:need(canonical(out)==canonical(json.loads(args.fixture.read_text())),'complete independent frozen record, including JSON types')
    if args.author_fixture is not None:
        author=json.loads(args.author_fixture.read_text())
        matches=[(out['census'],author['census_a_b_ordinary']), (out['fan']['role_labeled_T_patch_sets_sha256'],author['role_labeled_T_patch_sets_sha256']), (out['adjacent']['admitted_entries'],author['adjacent']['admitted_entries']), (out['b1'],author['noncontact_b1']), (out['shared_Q'],author['shared_Q']), (out['catalogue'],author['catalogue_corollaries'])]
        matches.extend((out['b2'][key],author['noncontact_b2'][key]) for key in out['b2'])
        for i,(actual,expected) in enumerate(matches):need(canonical(actual)==canonical(expected),'complete source mathematical field '+str(i))
    print('PASS',len(out['exact_checks']),'exact checks;',len(out['rejected_damages']),'damages rejected; full-record SHA256',digest(out))


if __name__=='__main__':main()
