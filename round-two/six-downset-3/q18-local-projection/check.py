"""Exact new residual-map verifier. Never imports the producer or parent code.

Carrier and stochastic-lift ideas openly adapt D3's own published10326
reader. This is a same-author separate certificate verifier, not an
independent mathematical review. No old PSD or center is rechecked.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json

BASE=Path(__file__).resolve().parent


def require(ok,msg):
    if not ok: raise ValueError(msg)


def pair(u,v):
    return (min(u,v),max(u,v))


def clean(d):
    return {e:v for e,v in d.items() if v}


def carrier():
    X=[]
    for core in range(8):
        for n in range(3):
            k=core.bit_count()
            if not (1<=k+n<=2 or k+n==3 and k>=2): continue
            for out in combinations(range(3,21),n):
                if core==6 and n==1 and out[0]<12: continue
                X.append(core+sum(1 << i for i in out))
    X.sort();present=set(X)|{0}
    require(len(X)==len(set(X))==277,'complete original carrier')
    require(all(x^(1 << i) in present for x in X for i in range(21) if x&(1 << i)),
            'all original downward relations')
    require([sum(bool(x&(1 << i)) for x in X) for i in range(21)]==
            [58,49,49]+[23]*9+[24]*9,'all21 actual star counts')
    S={x for x in X if x&1};T=set(X)-S
    B={x for x in T if x.bit_count()==2 and
       (x&7)==0 and (x>>3<512 or x&((1 << 12)-1)==0)}
    B|={x for x in T if x&7==6 and x>>12}
    require(len(S)==58 and len(T)==219 and len(B)==81,'complete bad/nonstar/star sets')
    all_edges=[(u,v) for i,u in enumerate(X) for v in X[i+1:] if not u&v]
    bb=[e for e in all_edges if all(v in B for v in e)]
    G=T-B
    gg=[e for e in all_edges if all(v in G for v in e)]
    mixed=[e for e in all_edges if all(v in T for v in e) and sum(v in B for v in e)==1]
    ns=[e for e in all_edges if sum(v in S for v in e)==1]
    require((len(all_edges),len(bb),len(gg),len(mixed),len(ns))==
            (30021,2628,7885,9009,10499),'complete original support partition')
    return X,S,T,B,bb,gg,mixed,ns


def inverse(data,B):
    order=data['bad_vertex_order'];edges=data['pivot_edge_order']
    require(order==sorted(B),'all original bad row labels')
    require(type(data['inverse_denominator']) is int and data['inverse_denominator']==2,
            'exact inverse denominator')
    require(type(edges) is list and len(edges)==81 and len({tuple(e) for e in edges})==81
            and all(type(e) is list and len(e)==2 and all(type(v) is int for v in e)
                    and 0<e[0]<e[1] and all(v in B for v in e) and not e[0]&e[1]
                    for e in edges),'all81 original pivot columns')
    # Cut growth pays the complete tree and literal odd chord.
    seen={order[0]}
    for e in edges[:80]:
        require(sum(v in seen for v in e)==1,'complete original spanning-tree growth')
        seen.update(e)
    require(seen==B and edges[-1]==[12288,49152] and
            [24,12288] in edges and [24,49152] in edges,'full original tree and odd triangle')
    # Exact deterministic choice is checked independently of elimination.
    visited={order[0]};todo=[order[0]];canonical=[]
    for v in todo:
        neighbors=sorted(u for u in B-visited if not v&u)
        for u in neighbors:
            visited.add(u);todo.append(u);canonical.append(list(pair(u,v)))
    require(edges==canonical+[[12288,49152]],'canonical original BFS pivot order')
    textrows=data['twice_inverse_rows']
    require(type(textrows) is list and len(textrows)==81 and all(type(r) is str for r in textrows),
            'complete textual inverse rows')
    Q=[[int(v) for v in r.split()] for r in textrows]
    require(all(len(r)==81 and all(abs(v)<=2 for v in r) for r in Q),'all inverse entries bounded over2')
    idx={v:i for i,v in enumerate(order)}
    incident=[[j for j,e in enumerate(edges) if v in e] for v in order]
    for i in range(81):
        for j in range(81):
            require(sum(Q[k][j] for k in incident[i])==2*int(i==j),'all entries of A Q=2I')
            require(Q[i][idx[edges[j][0]]]+Q[i][idx[edges[j][1]]]==2*int(i==j),
                    'all entries of Q A=2I')
    norms=[F(sum(abs(Q[i][j]) for i in range(81)),2) for j in range(81)]
    require(max(norms)==F(7,2),'complete inverse COLUMN l1 norm7/2')
    return order,list(map(tuple,edges)),Q,norms


def lift(proper,data,S,present):
    rows=Counter();Hh=Counter();actual=Counter()
    for (u,v),value in proper.items():
        require(type(value) is int and value and u in present and v in present and
                0<u<v and not u&v,'all nonzero proper entries and support')
        rows[u]+=value;rows[v]+=value;actual[(u,v)]+=value
        if v in S:Hh[u]+=value
        if u in S:Hh[v]+=value
    require(all(v==0 for v in Hh.values()),'all original star-kernel rows')
    for u,v in rows.items():
        if v: actual[(0,u)]+=data['empty_row_multiplier']*v
    if sum(rows.values()):
        actual[(0,0)]+=data['empty_loop_multiplier']*sum(rows.values())
    actual=clean(actual);actual_rows=Counter()
    for (u,v),value in actual.items():
        require(not u&v and (u!=v or u==0),'every actual support including empty loop')
        actual_rows[u]+=value
        if u!=v:actual_rows[v]+=value
    require(all(actual_rows[v]==0 for v in present),'ALL278 actual stochastic responses')
    return actual


def verify(data):
    require((data['actual_agent'],data['role'],data['q'],data['k'],data['actual_N'],data['s'])==
            ('six-downset-3','researcher',18,9,278,58),'fixed carrier and actual author')
    require(data['chart_graph']=='bafkreihejcf55p7eu47ms5u4cxblknpmsf2hr7kdy5bwoj4lybbe54z6zm' and
            data['chart_source']=='54ef84d14c0fb6133cbfb8ce6840bfe722226d61',
            'attributed original pivot mechanism')
    require(data['center_graph']=='bafkreiarggds2lrbkbbbv5amnjomopfsm32gm4btoez2mzia6cezceknzq' and
            data['center_source']=='df5a588c88f57babcb489c8690399fa5be50a0f7' and
            data['parent_center_and_PSD_not_rechecked'] is True and
            data['real_tau_interval']==['0','1/64'] and F(data['eta'])==F(1,2**20) and
            F(data['center_proper_floor'])==F(39,4096) and
            F(data['center_actual_C_unit_surplus'])==F(9,2**20),
            'explicit SAME-carrier ordinary stronger-center premises')
    intkeys=['residual_denominator','sigma_pivot_multiplier','sigma_gauge_numerator',
             'mixed_edge_numerator','mixed_pivot_multiplier','mixed_gauge_numerator',
             'loop_gauge_numerator','empty_row_multiplier','empty_loop_multiplier',
             'trace_support_edge_count','trace_coefficient','local_radius_eta_denominator_power',
             'lift_operator_square','global_blend_coefficient']
    require(all(type(data[k]) is int for k in intkeys),'exact integer residual/lift parameters')
    require(data['residual_denominator']==2,'literal column denominator2')
    X,S,T,B,bb,gg,mixed,ns=carrier();present=set(X)|{0}
    order,pivots,Q,norms=inverse(data,B);index={v:i for i,v in enumerate(order)}
    gauge=tuple(data['good_gauge_masks'])
    require(gauge==gg[0]==(2,4),'original good gauge')
    selected=(set(bb)-set(pivots))|set(gg[1:])|{e for e in ns if 1 not in e}
    require(len(selected)==20711,'complete selected canonical coordinates')
    mixed_set=set(mixed);pivot_set=set(pivots)
    allowed_column_support=pivot_set|mixed_set|{gauge}
    require(data['trace_support_edge_count']==len(gg)+len(mixed),
            'ALL good and potentially positive mixed trace entries')
    K=data['trace_coefficient'];eta=F(data['eta'])
    require(K>0 and 2*K*K>=len(T)*data['trace_support_edge_count'],
            'full Frobenius trace cost bound')
    require(data['lift_operator_square']==1+len(X)==278,'actual E transpose E norm factor278')
    power=data['local_radius_eta_denominator_power']
    require(0<=power<=32,'finite local dyadic radius')
    radius=eta/2**power
    require(radius<eta,'strict input NN signs on the entire closed operator ball')
    column_hash=hashlib.sha256();counts=Counter();proper_max=Counter();actual_max=Counter()
    maxterms=Counter();positions=Counter();proper_mass=Counter();all_empty=Counter()

    def accept(kind,label,H):
        H=clean(H)
        require(set(H)<=allowed_column_support and not (set(H)&selected),
                'all selected20711 original coordinates preserved')
        require(all(u in T and v in T for u,v in H),'ALL10499 proper NS entries unchanged')
        bad_degrees=Counter();good_total=0;cross={}
        for e,value in H.items():
            u,v=e
            if u in B and v in B:bad_degrees[u]+=value;bad_degrees[v]+=value
            elif u not in B and v not in B:good_total+=value
            else:cross[e]=value
        bad_vertex=label if kind=='sigma' else next((v for v in label if v in B),None) if kind=='mixed' else None
        expected_degree={bad_vertex:2} if kind in ['sigma','mixed'] else {}
        require(all(bad_degrees[v]==expected_degree.get(v,0) for v in order),
                'ALL81 original bad-degree responses per residual')
        require(cross==({tuple(label):-2} if kind=='mixed' else {}),
                'complete mixed-edge residual response including zeros')
        expected_good=1 if kind=='mixed' else -1
        require(good_total==expected_good,'complete good-total residual response')
        actual=lift(H,data,S,present)
        expected_empty=Counter()
        if kind=='sigma':
            expected_empty[(0,label)]=-2;expected_empty[(0,2)]+=1;expected_empty[(0,4)]+=1
        elif kind=='mixed':
            good=next(v for v in label if v not in B)
            expected_empty[(0,good)]+=2;expected_empty[(0,2)]-=1;expected_empty[(0,4)]-=1
        else:
            expected_empty[(0,0)]=-2;expected_empty[(0,2)]=1;expected_empty[(0,4)]=1
        empty={e:v for e,v in actual.items() if e[0]==0}
        require(empty==clean(expected_empty),'complete signed original empty response')
        require(all(actual.get((0,v),0)==(-2 if kind=='sigma' and v==label else 0) for v in order)
                and actual.get((0,0),0)==(-2 if kind=='loop' else 0),
                'ALL163 ordered forced-floor responses')
        mass=sum(abs(v) for v in H.values());entry=max(map(abs,actual.values()),default=0)
        counts[kind]+=1;proper_max[kind]=max(proper_max[kind],mass)
        actual_max[kind]=max(actual_max[kind],entry);maxterms[kind]=max(maxterms[kind],len(H))
        proper_mass[kind]+=mass;positions['proper_unordered']+=len(H);positions['actual_unordered']+=len(actual)
        positions['actual_stochastic_rows']+=len(present);positions['bad_degree_rows']+=len(B)
        for e,v in empty.items():all_empty[e]+=abs(v)
        rec={'kind':kind,'residual':label,
             'proper':[[u,v,a] for (u,v),a in sorted(H.items())],
             'actual':[[u,v,a] for (u,v),a in sorted(actual.items())]}
        column_hash.update((json.dumps(rec,sort_keys=True,separators=(',',':'))+'\n').encode())

    for A in order:
        H={e:data['sigma_pivot_multiplier']*Q[j][index[A]] for j,e in enumerate(pivots)}
        H[gauge]=data['sigma_gauge_numerator'];accept('sigma',A,H)
    for edge in mixed:
        A=next(v for v in edge if v in B)
        H={e:data['mixed_pivot_multiplier']*Q[j][index[A]] for j,e in enumerate(pivots)}
        H[edge]=data['mixed_edge_numerator'];H[gauge]=data['mixed_gauge_numerator']
        accept('mixed',list(edge),H)
    accept('loop',0,{gauge:data['loop_gauge_numerator']})
    require(dict(counts)=={'sigma':81,'mixed':9009,'loop':1},'ALL9091 complete residual columns')
    l1={k:F(v,2) for k,v in proper_max.items()}
    entrymax={k:F(v,2) for k,v in actual_max.items()}
    require(l1=={'sigma':F(4),'mixed':F(5),'loop':F(1,2)},'full exact proper column norm maxima')
    require(entrymax=={'sigma':F(1),'mixed':F(1),'loop':F(1)},'full exact ACTUAL column entry maxima')
    op_cost=2*max(l1.values());actual_cost=2*max(entrymax.values())
    require(F(data['proper_operator_cost_coefficient'])>=op_cost,
            'proper operator cost bound from all residual columns')
    require(F(data['actual_entry_cost_coefficient'])>=actual_cost,
            'actual entry cost bound including empty loop')
    require(F(data['M_entry_cost_coefficient'])>=actual_cost/220,
            'M units actual entry distance coefficient')
    require(F(data['M_operator_cost_coefficient'])>=278*op_cost/220,
            'M units actual OPERATOR distance coefficient')
    # The ordinary identity2Delta=S+2W pays W<=Delta and S<=2Delta.
    # Per-edge proper correction<=S, hence corrected wrong sign<=W+S<=2Delta.
    wrong_sign_cost=max(F(1),actual_cost)
    blend=data['global_blend_coefficient']
    global_sign_numerator=(blend-wrong_sign_cost)*eta
    global_actual_numerator=blend*F(data['center_actual_C_unit_surplus'])-actual_cost*eta
    global_proper_numerator=blend*F(data['center_proper_floor'])-op_cost*eta
    require(blend==3 and global_sign_numerator>0,'global blend pays STRICT NN signs for every positive gap')
    require(global_actual_numerator>0,'global blend pays ALL unforced original entry floors')
    require(global_proper_numerator>0,'global blend pays BOTH proper PSD cones')
    global_entry_cost=F(blend)/eta+actual_cost/220
    global_operator_cost=F(blend)*F(139,110)/eta+278*op_cost/220
    require(F(data['global_M_entry_cost_coefficient'])>=global_entry_cost,
            'global FULL feasible optimizer entry distance coefficient')
    require(F(data['global_M_operator_cost_coefficient'])>=global_operator_cost,
            'global FULL feasible optimizer operator distance coefficient')
    sign_surplus=eta-(1+actual_cost*K)*radius
    actual_surplus=F(data['center_actual_C_unit_surplus'])-(278+actual_cost*K)*radius
    proper_floor=F(data['center_proper_floor'])-(1+op_cost*K)*radius
    require(sign_surplus>=F(data['projected_NN_sign_margin'])>0,
            'entire closed local ball strict NN sign margin')
    require(actual_surplus>=F(data['projected_actual_C_unit_surplus'])>0,
            'entire closed local ball ALL unforced actual floors')
    require(proper_floor>=F(data['projected_proper_floor'])>0,
            'entire closed local ball BOTH proper spectral floors')
    require(F(data['other276_gap'])<=F(data['projected_proper_floor'])/220,
            'actual normalized nonextreme spectral gap')
    # Exact claimed constants and simple sufficient inequalities from PROOF.
    require(K==1361 and power==12 and op_cost==10 and actual_cost==2,
            'stated sufficient theorem constants')
    require(2723<3*4096//4 and 3000<4096 and 13611<4*4096 and
            F(39,4096)-4*eta==F(2495,262144)>F(1,128),
            'displayed all-real sign floor and spectral arithmetic')
    emptybytes=json.dumps([[u,v,a] for (u,v),a in sorted(all_empty.items())],separators=(',',':')).encode()
    return {
        'actual_agent':'six-downset-3','role':'researcher',
        'coverage':'ALL9091 original residual columns; ordinary all-real local domain in PROOF',
        'q':18,'actual_N':278,'s':58,'nonstar_dimension':219,
        'real_tau_interval':data['real_tau_interval'],'eta':str(eta),'local_proper_operator_radius':str(radius),
        'source_dependencies':{'chart':data['chart_source'],'stronger_center':data['center_source']},
        'graph_dependencies':{'chart':data['chart_graph'],'stronger_center':data['center_graph']},
        'parent_center_and_PSD_not_rechecked':True,'inverse_product_positions_checked':13122,
        'inverse_COLUMN_l1_norms':[str(v) for v in norms],
        'inverse_COLUMN_l1_max':'7/2','inverse_COLUMN_maximizer_bad_masks':[v for v,n in zip(order,norms) if n==F(7,2)],
        'residual_column_counts':dict(counts),'complete_residual_column_sha256':column_hash.hexdigest(),
        'all_original_sparse_and_row_checks':dict(positions),'maximum_proper_column_terms':dict(maxterms),
        'proper_column_l1_maxima':{k:str(v) for k,v in l1.items()},
        'proper_column_l1_totals':{k:str(F(v,2)) for k,v in proper_mass.items()},
        'actual_column_entry_maxima':{k:str(v) for k,v in entrymax.items()},
        'complete_empty_response_envelope_sha256':hashlib.sha256(emptybytes).hexdigest(),
        'selected_original_coordinates_preserved':20711,'ALL_proper_NS_entries_preserved':10499,
        'forced_ordered_floor_positions':163,'good_gauge_masks':list(gauge),
        'trace_support_edges':16894,'trace_Frobenius_square':'8447','trace_square_product':1849893,
        'trace_coefficient':1361,'trace_coefficient_square':1852321,
        'proper_operator_cost_coefficient':str(op_cost),'actual_entry_cost_coefficient':str(actual_cost),
        'M_entry_cost_coefficient':str(actual_cost/220),'M_operator_cost_coefficient':str(278*op_cost/220),
        'global_blend_coefficient':blend,'global_projected_wrong_sign_cost_coefficient':str(wrong_sign_cost),
        'global_strict_sign_numerator':str(global_sign_numerator),
        'global_unforced_actual_C_unit_numerator':str(global_actual_numerator),
        'global_both_proper_floor_numerator':str(global_proper_numerator),
        'global_M_entry_cost_coefficient':str(global_entry_cost),
        'global_M_operator_cost_coefficient':str(global_operator_cost),
        'global_domain':'ALL real M in F_tau; no local hypothesis; same tau interval',
        'global_relative_interior_domain':'every input with Delta>0; fixes every optimizer at Delta=0',
        'computed_local_sign_surplus':str(sign_surplus),'computed_local_actual_C_unit_surplus':str(actual_surplus),
        'computed_local_proper_floor':str(proper_floor),
        'stated_NN_sign_margin':data['projected_NN_sign_margin'],
        'stated_actual_C_unit_surplus':data['projected_actual_C_unit_surplus'],
        'stated_both_proper_floors':data['projected_proper_floor'],'other276_gap':data['other276_gap'],
        'actual_endpoint_ranks':[277,277],'simple_extreme_eigenvalues':['-29/110','1'],
        'ordinary_unformalized_bridges':['all-real affine retraction','dual residual budget',
                'operator/Frobenius norms','local original feasibility','full feasible optimizer distance',
                'relative interior','proper-to-actual congruence/ranks',
                'coupled dual wrong-sign budget','global continuous blended retraction',
                'global FULL feasible optimizer distances'],
        'independent_review_claimed':False}


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--certificate',type=Path,default=BASE/'CERTIFICATE.json')
    ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    spec=importlib.util.spec_from_file_location('sourcecheck',BASE/'sourcecheck.py')
    gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
    gate.check_bundle(BASE)
    result=verify(json.loads(args.certificate.read_bytes()))
    args.out.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'complete_residual_columns':9091,'whole_record_written':str(args.out)},sort_keys=True))
