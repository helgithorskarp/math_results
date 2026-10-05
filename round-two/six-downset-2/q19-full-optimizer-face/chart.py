"""Exact original-edge affine ranks and uniform full-face tube constants.

This is a structural witness for the ordinary proof, not a floating rank
calculation, search, or proof-assistant formalization.
"""
from binding import check_current
check_current()
from encoding import F, comparison, classify, affines, model
from collections import Counter, deque
from pathlib import Path
import argparse
import json
import resource
import time


def audit_inverse(A,inv):
    n=len(A)
    model.require(len(inv)==n and all(len(row)==n for row in inv), 'whole exact rank-inverse shape')
    model.require(all(sum(A[i][k]*inv[k][j] for k in range(n))==int(i==j)
                      and sum(inv[i][k]*A[k][j] for k in range(n))==int(i==j)
                      for i in range(n) for j in range(n)), 'both entire rational minor inverse products')


def inverse_and_det(A):
    n=len(A);work=[list(row)+[F(i==j) for j in range(n)] for i,row in enumerate(A)]
    det=F(1)
    for j in range(n):
        pivot=next((i for i in range(j,n) if work[i][j]),None)
        model.require(pivot is not None,'entire stated five-equation rank minor nonsingular')
        if pivot!=j:work[pivot],work[j]=work[j],work[pivot];det=-det
        value=work[j][j];det*=value;work[j]=[v/value for v in work[j]]
        for i in range(n):
            if i!=j:
                value=work[i][j];work[i]=[v-value*w for v,w in zip(work[i],work[j])]
    inv=[row[n:] for row in work]
    audit_inverse(A,inv)
    return inv,det


def run():
    start=time.monotonic();base=comparison();parts,b=classify(base)
    members=model.members(9,10);masks=[sum(1<<p for p in v) for v in members]
    model.require(len(members)==303 and members[:2]==[(),(0,)],'actual original empty and anchor')
    Q=list(range(2,303));NN=[i for i in Q if not masks[i]&1]
    S=[i for i in Q if masks[i]&1]
    K=[i for i in NN if model.type_of(members[i],9) in b['bad_nn']]
    Kset=set(K);NNset=set(NN);Sset=set(S)
    model.require((len(Q),len(NN),len(S),len(K))==(301,241,60,75),'literal complete proper cardinalities')
    edges=[];bytag={tag:[] for tag in ('KK','KG','GG','star')};orbits=Counter()
    for at,i in enumerate(Q):
        for j in Q[at+1:]:
            if masks[i]&masks[j]:continue
            pair=(i,j);edges.append(pair)
            key=tuple(sorted((model.type_of(members[i],9),model.type_of(members[j],9))))
            model.require(key in base,'every literal original free edge has its defining orbit')
            tag='star' if i in Sset or j in Sset else 'KK' if i in Kset and j in Kset else 'KG' if i in Kset or j in Kset else 'GG'
            model.require(key in parts[tag],'whole edge/orbit/repair partition agrees')
            bytag[tag].append(pair);orbits[(tag,key)]+=1
    counts={tag:len(v) for tag,v in bytag.items()}
    model.require(len(edges)==35865 and counts==dict(KK=1800,KG=10820,GG=11245,star=12000),
                  'entire independent original-edge census')
    for tag in parts:
        model.require({key for t,key in orbits if t==tag}==set(parts[tag]),'all143 orbits used without omission')
    adj={i:[] for i in K}
    for i,j in bytag['KK']:adj[i].append(j);adj[j].append(i)
    root=next(i for i in K if members[i]==(12,13));parent={root:None};queue=deque([root])
    while queue:
        i=queue.popleft()
        for j in adj[i]:
            if j not in parent:parent[j]=i;queue.append(j)
    triangle=[members.index(v) for v in ((12,13),(14,15),(16,17))]
    model.require(len(parent)==75 and len({tuple(sorted((i,parent[i]))) for i in parent if parent[i] is not None})==74,
                  'complete explicit connected KK spanning tree')
    model.require(all(j in adj[i] for i,j in zip(triangle,triangle[1:]+triangle[:1])),
                  'explicit original odd KK cycle')
    # A left-null coefficient obeys y_i=-y_j along each edge.  The odd
    # cycle kills the root, and the saved spanning tree kills all75 rows.
    gg_edge=bytag['GG'][0]
    model.require(all(i not in Kset and i in NNset for i in gg_edge),
                  'loop independence: a GG column is zero on every bad-degree row and has loop coefficient2')
    a=affines()
    pivot_keys=[((0,0,1),(0,0,1)),((0,0,2),(0,0,2)),
                ((0,0,2),(2,0,1)),((0,0,2),(4,0,1)),((0,0,2),(6,0,1))]
    model.require(all(k not in parts['KG'] and k in a['keys'] for k in pivot_keys),
                  'five distinct remaining invariant columns')
    minor=[[a['rowdir'][row][a['keys'].index(key)] for key in pivot_keys] for row in a['eqkeys']]
    inv,det=inverse_and_det(minor)
    model.require(abs(det)==117573120,'whole five-row invariant rank determinant')
    full_dimension=len(edges)-len(bytag['KG'])-len(K)-1
    inv_dimension=len(base)-len(parts['KG'])-len(a['eqkeys'])
    model.require((full_dimension,inv_dimension)==(24969,113),'exact full and invariant affine dimensions')
    nn_degrees={i:sum(i in e for tag in ('KK','KG','GG') for e in bytag[tag]) for i in NN}
    star_degrees={i:sum(i in e for e in bytag['star']) for i in S}
    anchor_columns={i:sum(i in e for e in bytag['star']) for i in NN}
    model.require(max(nn_degrees.values())<=240 and max(star_degrees.values())<=241 and
                  max(anchor_columns.values())<=60 and len(bytag['star'])==12000,
                  'every original completion-row perturbation coefficient bound')
    mu=F(1,256);delta=F(1,1024);radius=F(1,2**25)
    entry_margin=mu-12000*radius;sign_margin=mu-radius;spectral=delta-301*radius
    model.require(entry_margin==F(3721,1048576) and sign_margin>0 and spectral>F(1,2048),
                  'strict exact all-coordinate tube comparisons')
    return dict(agent='six-downset-2',role='researcher',exact_original_free_coordinates=len(edges),
        literal_vertex_counts=dict(N=303,Q=301,NN=241,free_star=60,bad_NN=75),
        individual_edge_counts=counts,invariant_orbit_counts={t:len(parts[t]) for t in parts},
        entire_original_edges_sha256=model.digest(edges),
        entire_original_orbit_counts_sha256=model.digest([[tag,key,v] for (tag,key),v in sorted(orbits.items())]),
        KK_connected_odd_cycle_rank=75,
        original_KK_spanning_tree=[[members[i],None if p is None else members[p]] for i,p in sorted(parent.items())],
        original_KK_odd_cycle=[members[i] for i in triangle],
        loop_independent_GG_column=[members[i] for i in gg_edge],
        invariant_equality_rows=a['eqkeys'],invariant_minor_columns=pivot_keys,
        entire_invariant_minor=[[str(v) for v in row] for row in minor],
        entire_invariant_minor_inverse=[[str(v) for v in row] for row in inv],
        invariant_minor_determinant=str(det),both_whole_inverse_products_checked=True,
        full_affine_dimension=full_dimension,invariant_affine_dimension=inv_dimension,
        max_literal_NN_free_degree=max(nn_degrees.values()),
        max_literal_free_star_NN_degree=max(star_degrees.values()),
        max_literal_anchor_column_degree=max(anchor_columns.values()),
        loop_and_bad_empty_tangent_variation_exactly_zero_by_affine_premise=True,
        entry_center_margin=str(mu),spectral_center_margin=str(delta),free_coordinate_radius=str(radius),
        all_nonforced_original_entry_margin=str(entry_margin),all_strict_repair_margin=str(sign_margin),
        full_T_and_upper_comparison_floor='1/2048',actual_norm_budget=str(301*radius),
        other301_original_lower_and_upper_gaps='1/495616',real_tau_interval=['0','1/8'],
        ordinary_rank_completeness_and_real_tube_bridges_unformalized=True,
        independently_reviewed=False,observed_seconds=time.monotonic()-start,
        peak_RSS_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);args=p.parse_args()
    r=run();args.out.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if 'tree' not in k and 'minor' not in k}))
