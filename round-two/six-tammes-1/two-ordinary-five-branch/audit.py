"""Same-author finite incidence audit. Imports no production modules.
Continuous input: the proved 25/62/4 core classification in PROOF.md.
Representation: vertex/edge bits and Hamiltonian link edge subsets.
six-tammes-1, researcher; CPython >=3.11 standard library only.
"""
from itertools import combinations, permutations, product
from collections import Counter
import hashlib
import json


def require(p, message):
    if not p: raise ValueError(message)


def sha(x):
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()


PAIRS=list(combinations(range(15),2))
INDEX={p:i for i,p in enumerate(PAIRS)}


def bit(a,b):
    return 1<<INDEX[min(a,b),max(a,b)]


def edges(x):
    return [p for i,p in enumerate(PAIRS) if x>>i&1]


def adjacency(x):
    result=[0]*15
    for a,b in edges(x): result[a]|=1<<b;result[b]|=1<<a
    return result


def labels(mask):
    return [v for v in range(15) if mask>>v&1]


TRIANGLES=[(0,1,2),(0,1,3),(0,3,4),(0,4,5),(1,2,6),(1,6,7)]
QUADS=[(0,2,8,5),(1,3,9,7),(2,6,10,8),(3,4,11,9),(4,5,12,11),(6,7,13,10)]
BASE=0
for t in TRIANGLES:
    for a,b in combinations(t,2): BASE|=bit(a,b)
for q in QUADS:
    for k in range(4): BASE|=bit(q[k],q[(k+1)%4])
require(BASE.bit_count()==25,'25 edges regenerated from actual faces')
CLASS_BITS=[bit(8,12)|bit(9,13),bit(10,12)|bit(11,13)]


def required_corner_bits(v):
    result=0;occurrences=0
    for t in TRIANGLES:
        if v in t:
            a,b=[w for w in t if w!=v];result|=bit(a,b);occurrences+=1
    for q in QUADS:
        if v in q:
            k=q.index(v);result|=bit(q[k-1],q[(k+1)%4]);occurrences+=1
    require(result.bit_count()==occurrences,'do not deduplicate repeated face corner')
    return result


def Hamiltonian_cycles(nb_bits,known):
    nb=labels(nb_bits);n=len(nb);possible=[bit(a,b) for a,b in combinations(nb,2)]
    cycles=[]
    for chosen in combinations(possible,n):
        mask=sum(chosen)
        if mask&known!=known: continue
        adj=adjacency(mask)
        if any(adj[v].bit_count()!=2 for v in nb): continue
        reached=1<<nb[0];old=-1
        while reached!=old:
            old=reached
            for v in labels(old): reached|=adj[v]
        if reached==nb_bits: cycles.append(mask)
    return cycles


def fan_word_cover():
    def faces(center,word):
        return {tuple(sorted((center,word[k],word[k+1]))) for k in range(4)}
    words=[]
    for center,other,private in ((0,1,(4,5)),(1,0,(6,7))):
        good=[]
        for w in permutations((other,2,3)+private):
            k=w.index(other)
            if 0<k<4 and {w[k-1],w[k+1]}=={2,3}: good.append(w)
        require(len(good)==12,'all oriented adjacent-five words')
        words.append(good)
    good_rows=[];sets=set()
    for f,g in product(*words):
        ts=faces(0,f)|faces(1,g)
        if all(sum(v in t for t in ts)<=2 for v in (2,3)):
            sets.add(tuple(sorted(ts)));good_rows.append([list(f),list(g)])
    require(len(good_rows)==32 and len(sets)==8,'full word cover')
    representative=set(TRIANGLES)
    # Explicit role-preserving maps; no simultaneous metric symmetry premise.
    images=set()
    for sf,ss,sl,sr in product((False,True),repeat=4):
        m={0:int(sf),1:int(not sf),2:3 if ss else 2,3:2 if ss else 3}
        for orig,new,swap in (((4,5),(6,7) if sf else (4,5),sl),
                              ((6,7),(4,5) if sf else (6,7),sr)):
            for v,w in zip(orig,tuple(reversed(new)) if swap else new):m[v]=w
        images.add(tuple(sorted(tuple(sorted(m[v] for v in t)) for t in representative)))
    require(images==sets,'each admitted word patch maps to actual representative')
    return {'all_fan_words_each':120,'permitted_words_each':12,'raw_word_pairs':144,
            'admitted_word_pairs':32,'distinct_T_sets':8,
            'role_labeled_T_patch_sets_sha256':sha(sorted(sets)),
            'admitted_word_pairs_sha256':sha(good_rows)}


def degree_and_link_cover():
    rows=[];tested=0;raw=0
    for classes in range(4):
        core=BASE
        for k,x in enumerate(CLASS_BITS):
            if classes>>k&1:core|=x
        for outside in range(1<<14):
            tested+=1
            if outside.bit_count() not in (3,4):continue
            raw+=1
            mask=core
            for v in labels(outside):mask|=bit(14,v)
            adj=adjacency(mask);ds=[x.bit_count() for x in adj]
            if mask.bit_count()!=30 or ds[:2]!=[5,5]:continue
            if any(d not in (3,4) for d in ds[2:]) or ds.count(3)!=2:continue
            require(classes in (1,2) and ds[14]==3,'exactly one class and outside three')
            other=next(v for v in range(14) if ds[v]==3)
            r={'class':'A' if classes==1 else 'B','outside_neighbors':labels(outside),'omitted':other}
            if classes==1:
                ordinary=[v for v in (2,3,4,6) if adj[other]>>v&1]
                if ordinary:
                    require(len(ordinary)==1 and other in (10,11),'three ordinary-neighbor cases')
                    r.update(reason='THREE_ORDINARY_CONTACT',witness=[other,ordinary[0]])
                else:
                    witnesses=[]
                    for v in (5,7):
                        cy=Hamiltonian_cycles(adj[v],required_corner_bits(v))
                        require(cy,'actual full link cycle remains possible')
                        for a,b in combinations(labels(adj[v]),2):
                            if other in (a,b) and bit(a,b)&mask and all(bit(a,b)&c for c in cy):
                                witnesses.append(sorted((v,a,b)))
                    require(len(witnesses)==1,'forced triangle at omitted three')
                    r.update(reason='TRIANGLE_AT_THREE',witness=witnesses[0])
            elif other in (8,9):
                opposite=[list(q) for q in QUADS if q[0] in (0,1) and q[2]==other]
                require(len(opposite)==1,'three opposite ordinary five')
                r.update(reason='FIVE_OPPOSITE_THREE',witness=opposite[0])
            else:
                zeros=[]
                for v in (8,9,10,11):
                    require(ds[v]==4,'four full neighbors')
                    cy=Hamiltonian_cycles(adj[v],required_corner_bits(v))
                    require(cy and all((c&mask)==0 for c in cy),'zero triangles in every necessary cyclic link')
                    zeros.append(v)
                require(len(zeros)>3,'triangle-deficit census')
                r.update(reason='FOUR_ZERO_FOURS_EXCEED3',witness=zeros)
            rows.append(r)
    rows.sort(key=lambda r:(r['class'],r['outside_neighbors']))
    require(tested==65536 and raw==5460 and len(rows)==8,'exhaustive bit domain')
    return {'all_outside_bitmasks':tested,'raw_degree_candidates':raw,
            'admitted_entries':rows,'admitted_entries_sha256':sha(rows),
            'released_geometric_terminal_tests_admitted':len(rows)}


def shared_opposite_cover():
    rows=[]
    for ordinary in range(5,9):
        masks=[x for x in range(1<<(ordinary-2)) if x.bit_count()==3]
        masks.sort(key=labels)
        entries=[[labels(a),labels(b),2+(a&b).bit_count()] for a,b in product(masks,repeat=2)]
        allowed=sum(r[2]<=2 for r in entries)
        require(allowed==(20 if ordinary==8 else 0),'shared Q requires eight ordinary fours')
        rows.append({'ordinary_fours':ordinary,'raw_subset_pairs':len(entries),
                     'common_contact_records_sha256':sha(entries),'admitted':allowed})
    return rows


def b1_qq_incidence_cover():
    # Use vertex-role masks; normals are identical actual labels to check.py.
    H_MASK=(1<<8)|(1<<6)|(1<<7);K_MASK=(1<<8)|(1<<4)|(1<<5)
    rows=[];aliases=[]
    for h in range(15):
        for k in range(15):
            admissible=bool(H_MASK>>h&1 and K_MASK>>k&1)
            aliases.append([h,k,admissible])
            if not admissible:continue
            mask=bit(4,h)|bit(5,h)|bit(6,k)|bit(7,k)
            adj=adjacency(mask)
            endpoint_ends=sum(adj[v].bit_count() for v in (4,5,6,7,8))
            # If B is absent, its four QQ incidences leave at least two beyond U,V.
            extra=2 if not adj[8] else 0
            require(endpoint_ends+extra==8 and 8>12-6,'deficient-four QQ incidences only')
            rows.append({'H':h,'K':k,'forced_edges':[list(e) for e in edges(mask)],
                         'forced_deficient_ends':endpoint_ends,'additional_B_ends':extra,
                         'required_ends':endpoint_ends+extra,'available_ends':6})
    require(len(rows)==9,'retained b1 opposite choices')
    return {'raw_original_opposite_pairs':225,'admitted_aliases_sha256':sha(aliases),
            'terminal_entries':rows,'terminal_entries_sha256':sha(rows)}


def b2_full_neighbor_cover():
    # The remaining ordinary P=12 has known contacts0,1,8,11.
    contact_mask=(1<<0)|(1<<1)|(1<<8)|(1<<11)
    rows=[]
    for h in range(15):
        if not (contact_mask>>h&1): why='OUTSIDE_COMPLETE_P_CONTACTS'
        elif h==0:why='REPEATED_Q_VERTEX'
        elif h==8:why='CONTACT_Q_DIAGONAL'
        elif h==1:
            g_mask=(1<<5)|(1<<9)|(1<<10)|(1<<11)|(1<<12)
            require(not g_mask>>4&1,'A cannot contact G')
            why='OUTSIDE_COMPLETE_G_CONTACTS'
        else:
            require(h==11,'last original is ordinary internal')
            why='ORDINARY_FOUR_OPPOSITE_FIVE'
        rows.append([h,why])
    words=[]
    for mask in range(1<<15):
        if mask.bit_count()==2 and not mask&~((1<<4)|(1<<5)|(1<<12)):
            a,b=labels(mask);words.extend([(a,b),(b,a)])
    words.sort();forms=[]
    for f,g in product(words,repeat=2):
        chosen=f+g
        if chosen.count(4)<=1 and chosen.count(5)<=1:
            require(chosen.count(4)==chosen.count(5)==1 and chosen.count(12)==2,'endpoint quota normal form')
            forms.append([list(f),list(g)])
    require(len(forms)==8,'all endpoint orientations')
    return {'credited_existing_case':True,'original_Q_opposite_aliases':rows,
            'opposite_aliases_sha256':sha(rows),'ordered_endpoint_normal_forms':forms,
            'endpoint_forms_sha256':sha(forms)}


def run():
    return {'actual_agent':'six-tammes-1','role':'researcher',
            'status':'same-author distinct finite representation; continuous core shared as explicit input',
            'fan_word_cover':fan_word_cover(),'adjacent':degree_and_link_cover(),
            'shared_Q':shared_opposite_cover(),'noncontact_b1':b1_qq_incidence_cover(),
            'noncontact_b2':b2_full_neighbor_cover(),
            'continuous_core_arithmetic_independently_audited':False}


if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
