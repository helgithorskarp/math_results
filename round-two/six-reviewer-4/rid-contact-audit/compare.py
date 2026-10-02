"""Compare original DATA with freshly derived independent physical records.
Original executable is not imported. Requires its hash-pinned expected.json.
"""
import argparse,json,hashlib,itertools
from fractions import Fraction as F
from pathlib import Path
from check import load,decode,need,encode,absolute
HERE=Path(__file__).resolve().parent

def old(b,x):
    A,B=map(F,x);a=A+B/2;c=B/2;return b.q(a.numerator,a.denominator)+b.q(c.numerator,c.denominator)*b.S(0,1)

def verify(original):
    raw=original.read_bytes();need(hashlib.sha256(raw).hexdigest()=='bfddc098ec79f8ddd003d7dd59c3929f3bf31f755fecca6284ff2913c072c658','original whole expected bytes')
    x=json.loads(raw);o=json.loads((HERE/'expected.json').read_text());b=load();V=[tuple(decode(b,t) for t in v) for v in o['originals']]
    # Distinct polynomial coefficient-key order derived from the exact coordinate values.
    order=sorted(V,key=lambda v:tuple((F(t.a-t.b,t.d),F(2*t.b,t.d)) for t in v));idx={v:i for i,v in enumerate(V)}
    cyc=[idx[order[i]] for i in x['center_certificate']['complete_receiving_cycle']];own=o['cycle_original_indices'];need({(a,c) for a,c in zip(cyc,cyc[1:]+cyc[:1])}=={(a,c) for a,c in zip(own,own[1:]+own[:1])},'literal whole shadow cycle')
    r=tuple(decode(b,t) for t in o['center_raw']);rows=[];contacts=[]
    for i,j in zip(cyc,cyc[1:]+cyc[:1]):
        m=b.fcross(b.sub(V[j],V[i]),r);h=b.fdot(m,V[i]);m=b.scale(1/h,m)
        for k in (i,j):
            f=b.fcross(V[k],m);contacts.append((k,m,f))
            if f not in rows:rows.append(f)
    cc=x['center_certificate'];need(cc['endpoint_constraints']==32 and cc['unique_torque_rows']==16 and len(rows)==16,'complete row inventory')
    need(old(b,cc['maximum_polytope_coordinate_M'])==decode(b,o['exact_M']),'exact constant')
    supplied=set();activechecks=0
    for z in cc['polytope_vertices']:
        v=tuple(old(b,t) for t in z['x']);need(v not in supplied,'duplicate original vertex');supplied.add(v);need(all(b.fdot(f,v)<=1 for f in rows),'all inequalities on original vertex')
        actual=[]
        for ids in itertools.combinations([i for i,f in enumerate(rows) if b.fdot(f,v)==1],3):
            if b.fdot(rows[ids[0]],b.fcross(rows[ids[1]],rows[ids[2]]))!=0:actual.append(list(ids))
        need(actual==z['active_triples'],'every original active triple');activechecks+=len(actual)
    ownverts={tuple(decode(b,t) for t in v) for v in o['complete_polytope_vertices']};need(supplied==ownverts,'entire vertex set equals independent clipping')
    selected=cc['positive_spanning_original_contact_indices'];w=[old(b,t) for t in cc['positive_spanning_weights']];f=[contacts[i][2] for i in selected]
    need(len(w)==5 and min(w)>0 and sum(w,b.Z)==1,'all positive stress weights')
    need(tuple(sum((ww*ff[j] for ww,ff in zip(w,f)),b.Z) for j in range(3))==(b.Z,)*3,'literal positive stress equilibrium')
    determinant=b.fdot(f[0],b.fcross(f[1],f[3]));need(determinant!=0 and determinant==old(b,cc['positive_spanning_rank_determinant']),'actual stress rank determinant')
    singular=sum(b.fdot(a,b.fcross(c,d))==0 for a,c,d in itertools.combinations(rows,3));need(cc['singular_constraint_triples']==singular==26 and cc['attempted_constraint_triples']==560,'full original triple counters')
    centermax=max(b.fdot(m,m) for k,m,f in contacts);need(centermax==old(b,cc['maximum_normalized_support_normal_squared']),'whole center normal maximum')
    wb=x['whole_receiving_box'];need(old(b,wb['maximum_normalized_torque_row_l1_perturbation'])==decode(b,o['maximum_l1_error']),'entire real-box row bound')
    need(old(b,wb['all_source_width_margin'])==decode(b,o['continuum_gates']['width_margin']),'whole width margin')
    for a,c in zip(wb['corner_records'],o['continuum_gates']['corners']):
        cr=tuple(decode(b,t) for t in c['raw']);need(cr==tuple(old(b,t) for t in a['raw_corner']),'corner coordinates')
        need(old(b,a['raw_Cauchy_area'])==decode(b,c['area']) and old(b,a['weighted_diagonal_ratio'])==decode(b,c['ratio']),'complete corner area/ratio')
        margins=[]
        for i,j in zip(cyc,cyc[1:]+cyc[:1]):
            m=b.fcross(b.sub(V[j],V[i]),cr);h=b.fdot(m,V[i]);margins.extend(h-b.fdot(m,v) for k,v in enumerate(V) if k not in (i,j))
        need(min(margins)==old(b,a['minimum_nonendpoint_edge_support_margin']),'all corner support minima')
    need(wb['all_original_edge_support_corner_comparisons']==3840 and wb['incident_endpoint_equalities_at_corners']==128 and wb['strict_original_edge_support_corner_comparisons']==3712,'whole support coverage')
    q=tuple(b.q(z,200000) for z in (12,14,11));k,m,f=contacts[0];poly=b.fdot(f,q)+b.fdot(m,q)*b.fdot(V[k],q)-b.fdot(q,q)
    need(poly==old(b,x['controls']['explicit_prior_gap_endpoint_polynomial_excess']) and poly>0,'literal prior gap contact')
    return {'actual_agent':'six-reviewer-4','role':'independent mathematical reviewer','original_whole_expected_sha256':hashlib.sha256(raw).hexdigest(),'original_bytes':len(raw),'independent_whole_expected_sha256':hashlib.sha256((HERE/'expected.json').read_bytes()).hexdigest(),'entire_original_and_clipped_vertex_sets_equal':True,'original_primal_vertices':len(supplied),'all_original_active_triples_checked':activechecks,'all_original_stress_weights_rank_and_equilibrium_verified':True,'literal_contacts':32,'complete_corner_original_support_comparisons':3840,'all_corner_area_ratio_and_support_minima_equal':True,'all_original_560_basis_counters_equal':True,'whole_real_box_l1_error_equal':True,'whole_width_margin_equal':True,'prior_gap_contact_equal':True,'comparison_is_data_only_no_author_executable_import':True}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('original_expected',type=Path);a=p.parse_args();print(json.dumps(verify(a.original_expected),indent=2,sort_keys=True))
