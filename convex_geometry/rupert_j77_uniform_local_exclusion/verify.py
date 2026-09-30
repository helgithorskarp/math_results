#!/usr/bin/env python3
"""Exact finite hypotheses for J77's uniform near-identity strict exclusion."""
from fractions import Fraction
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
PRIOR=ROOT.parent/'rupert_j77_critical_axes'

def require(condition,message):
    if not condition:raise ValueError(message)

def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

manifest=json.loads((ROOT/'dependencies.json').read_text())
require(manifest['source_commit']=='00ba486565df55ee9373f6e5da4668aefb7b71c8','Unexpected dependency provenance')
require(set(manifest['sha256'])=={'.gitignore','README.md','PROOF.md','verify.py','certificates.json','dependencies.json','expected.json'},
        'Incomplete dependency manifest')
for name,digest in manifest['sha256'].items():
    require(hashlib.sha256((PRIOR/name).read_bytes()).hexdigest()==digest,'Changed dependency: '+name)
critical=module('j77_critical_dependency',PRIOR/'verify.py');fixed=critical.fixed
from q5 import Q,dot,cross,sub,scale
from model import VERTICES
from chamber import partition,chamber
P=module('j77_uniform_polynomials',ROOT/'polynomial.py')

def mirror_geometry(parents,audit):
    u=(Q(1)/4-Q(0,3)/20,Q(1)/4-Q(0,1)/20,-Q(0,1)/10);N=dot(u,u)
    H,triangle=chamber();coords=P.solve(list(map(list,zip(*triangle))),u)
    require(coords==[Q(),Q(1)/2,Q(1)/2] and dot(H,u)==1,'Invalid equatorial chamber midpoint')
    index={v:i for i,v in enumerate(VERTICES)};permutation=[]
    for v in VERTICES:
        reflected=sub(v,scale(2*dot(u,v)/N,u));require(reflected in index,'Remaining normal is not a body mirror')
        permutation.append(index[reflected])
    require(all(permutation[permutation[i]]==i for i in range(55)),'Mirror is not an involution')
    require([i for i,j in enumerate(permutation) if i==j]==[9,14,54],'Wrong fixed mirror vertices')
    for i in (9,14,54):
        v=VERTICES[i];require(dot(u,v)==0,'Fixed vertex is outside the mirror plane')
        for j,w in enumerate(VERTICES):
            if i!=j:
                gap=dot(v,sub(v,w));require(gap>0,'Radial vertex is not uniquely exposed');audit.values.append(gap)
    required=set()
    for i,t in enumerate(parents):
        barycentric=P.solve(list(map(list,zip(*t))),u)
        if all(x>=0 for x in barycentric):
            require(u in t,'Critical ray is not a parent corner');required.add(i)
    require(required=={21,23,28,30,31,32,33},'Changed incident partition')
    return u,required,permutation

def coverage(data,required):
    ids=[r['parent'] for r in data['cases']]
    require(len(ids)==len(set(ids)) and set(ids)==required,'Missing, duplicate or extraneous mirror incidence')

def cover_shape(covers):
    require(len(covers)==4 and {(d['coordinate'],d['sign']) for d in covers}=={(k,s) for k in range(2) for s in (1,-1)},
            'Missing coordinate or sign')
    for d in covers:
        end=Fraction()
        require(d['pieces'],'Empty parameter cover')
        for piece in d['pieces']:
            lo,hi=map(Fraction,piece['interval'])
            require(lo==end and 0<=lo<hi<=1,'Gap, overlap or invalid parameter interval');end=hi
        require(end==1,'Closed parameter endpoint missing')

def bernstein_replay(p,lo,hi):
    beta=P.bernstein(p,lo,hi);n=len(beta)-1
    # Independent coefficient replay: substitute t=lo+(hi-lo)x, then
    # reconstruct sum beta[k] binomial(n,k)x^k(1-x)^(n-k).
    transformed=P.ZERO
    for c in reversed(p):transformed=P.padd(P.pmul(transformed,(lo,hi-lo)),P.poly(c))
    recovered=P.ZERO
    for k,b in enumerate(beta):
        basis=(Q(),)*k+(Q(1),)
        for _ in range(n-k):basis=P.pmul(basis,(Q(1),Q(-1)))
        recovered=P.padd(recovered,P.pscale(b*P.comb(n,k),basis))
    require(recovered==P.trim(transformed),'Bernstein conversion identity fails')
    return beta

def dual_piece(rows,rhs,mirror,tight,d,piece,audit):
    ids=piece['row_indices'];coordinates=piece['coordinate_indices'];n=len(ids)
    require(0<n<=5 and len(set(ids))==n and set(ids)<=set(tight),'Invalid or non-mirror-tight dual rows')
    require(len(coordinates)==len(set(coordinates))==n and set(coordinates)<=set(range(5)),'Invalid determinant coordinates')
    target=[d['sign']*int(k==d['coordinate']) for k in range(5)]
    matrix=[[rows[i][k] for i in ids] for k in coordinates];raw=P.determinant(matrix)
    require(raw and len(raw)<=3,'Unexpected raw determinant degree')
    for t in (Q(),Q(1)/2,Q(1)):
        sample=[[P.peval(p,t) for p in row] for row in matrix]
        require(P.peval(raw,t)==critical.gaussian_determinant(sample),'Independent determinant replay fails')
    den,nums=P.cramer(rows,ids,coordinates,target)
    lo,hi=(Q(Fraction(x)) for x in piece['interval']);middle=(lo+hi)/2
    require(P.peval(den,middle)!=0,'Singular reduced denominator')
    if P.peval(den,middle)<0:den=P.pscale(-1,den);nums=[P.pscale(-1,p) for p in nums]
    db=bernstein_replay(den,lo,hi);nb=[bernstein_replay(p,lo,hi) for p in nums]
    require(all(x>0 for x in db) and all(x>=0 for row in nb for x in row),'Invalid denominator or negative dual weight')
    require(P.pdot(nums,[rhs[i] for i in ids])==P.pscale(d['sign'],P.pmul(den,mirror[d['coordinate']])),
            'Coordinate right-side identity fails')
    audit.values.extend(db+[x for row in nb for x in row])
    return {'basis_size':n,'numerator_coefficients':sum(len(p) for p in nums),'denominator_degree':len(den)-1,
            'common_factor_cancelled':len(raw)>len(den),'Bernstein_coefficients':len(db)+sum(map(len,nb))}

def case_check(c,parent,u,audit):
    require(fixed.decode(c['direction'])==u and u in parent,'Wrong critical corner')
    rays=[fixed.decode(v) for v in c['extreme_motions']]
    require(len(rays)==2 and all(len(v)==5 and v[3:]==(Q(),Q()) and dot(u,v[:3])==0 for v in rays),
            'Invalid tangent cone generators')
    require(cross(rays[0][:3],rays[1][:3])!=(Q(),Q(),Q()),'Dependent motion generators')
    contacts=c['contacts'];require(len(contacts)==len({tuple(v) for v in contacts}),'Duplicate contact')
    columns=[];derivatives=[];ds=[sub(v,u) for v in parent if v!=u]
    for ids in contacts:
        audit.contact(ids,parent,'full');x,y,j=ids;e=sub(VERTICES[y],VERTICES[x]);h=dot(cross(e,u),VERTICES[j])
        require(h>0,'Collapsed critical support');m=scale(1/h,cross(e,u))
        columns.append(cross(VERTICES[j],m)+m)
        derivatives.append([cross(VERTICES[j],scale(1/h,cross(e,d))) for d in ds])
    G=[v[:3]+(v[3],v[5]) for v in columns];common=c['common_indices'];weights=fixed.decode(c['common_weights'])
    require(common==[i for i,v in enumerate(columns) if cross(v[:3],u)==(Q(),Q(),Q())],
            'Incomplete common active rows')
    require(len(common)==6 and len(weights)==6 and all(w>0 for w in weights) and sum(weights,Q())==1,
            'Nonpositive or incomplete common equilibrium')
    require(all(sum((w*columns[i][k] for w,i in zip(weights,common)),Q())==0 for k in range(6)),
            'Full six-coordinate equilibrium fails')
    rr=c['rank_rows'];cc=c['rank_coordinates']
    require(len(rr)==len(set(rr))==3 and set(rr)<=set(common) and len(cc)==len(set(cc))==3 and set(cc)<=set(range(5)),
            'Invalid rank-three minor')
    minor=[[G[i][j] for j in cc] for i in rr];det=critical.determinant(minor)
    require(det!=0 and det==critical.gaussian_determinant(minor),'Rank-three independent replay fails')
    require(all(dot(G[i],r)==0 for i in common for r in rays),'Common kernel fails')
    values=[[dot(v,r) for r in rays] for v in G]
    require(all(x<=0 for row in values for x in row),'Invalid necessary cone generator')
    require(len(c['facet_rows'])==2,'Missing cone facet')
    for k,i in enumerate(c['facet_rows']):
        require(type(i) is int and 0<=i<len(G) and values[i][k]<0 and values[i][1-k]==0,'Wrong oriented cone facet')
    rates=[[sum((w*dot(r[:3],derivatives[i][k]) for w,i in zip(weights,common)),Q()) for k in range(2)] for r in rays]
    require(all(x>0 for row in rates for x in row),'Receiver rate stress is not positive on a cone corner')
    audit.values.extend(list(weights)+[det,-det]+[x for row in rates for x in row]+[x for row in values for x in row])
    rows,rhs,labels,mirror,tight=P.family(c,parent);cover_shape(c['dual_covers']);duals=[]
    for d in c['dual_covers']:
        for piece in d['pieces']:duals.append(dual_piece(rows,rhs,mirror,tight,d,piece,audit))
    return {'parent':c['parent'],'persistent_contacts':len(contacts),'common_active_contacts':len(common),
            'normal_balanced_weights':len(weights),'common_rank':3,'necessary_motion_cone_rays':2,
            'strict_drift_corners':4,'necessary_polynomial_rows':len(rows),'universal_mirror_tight_rows':len(tight),
            'coordinate_dual_pieces':len(duals),'Cramer_basis_sizes':[d['basis_size'] for d in duals],
            'cancelled_common_factors':sum(d['common_factor_cancelled'] for d in duals),
            'Bernstein_sign_coefficients':sum(d['Bernstein_coefficients'] for d in duals)}

def malformed(data,parents,u,required):
    def copy():return json.loads(json.dumps(data))
    a=copy();a['cases'].pop()
    b=copy()['cases'][0];b['extreme_motions'][0]=[['0','0']]*5
    w=copy()['cases'][0];w['common_weights'][0]=['-1','0']
    f=copy()['cases'][0];f['facet_rows'].pop()
    r=copy()['cases'][0];r['rank_coordinates'][1]=r['rank_coordinates'][0]
    d=copy()['cases'][0]['dual_covers'];d.pop()
    e=copy()['cases'][0]['dual_covers'];e[0]['pieces'][0]['interval'][1]='1/2'
    bad=copy()['cases'][0];rows,rhs,labels,mirror,tight=P.family(bad,parents[bad['parent']])
    piece=bad['dual_covers'][0]['pieces'][0];piece['row_indices'][0]=len(rows)
    failures=[lambda:coverage(a,required),lambda:case_check(b,parents[b['parent']],u,fixed.Audit()),
              lambda:case_check(w,parents[w['parent']],u,fixed.Audit()),lambda:case_check(f,parents[f['parent']],u,fixed.Audit()),
              lambda:case_check(r,parents[r['parent']],u,fixed.Audit()),lambda:cover_shape(d),lambda:cover_shape(e),
              lambda:dual_piece(rows,rhs,mirror,tight,bad['dual_covers'][0],piece,fixed.Audit())]
    for invalid in failures:
        try:invalid()
        except ValueError:pass
        else:raise ValueError('Malformed uniform certificate accepted')

def check(data,self_test=False):
    inherited=critical.check(json.loads((PRIOR/'certificates.json').read_text()),self_test)
    part=partition();parents=[tuple(fixed.decode(u) for u in t) for t in part['triangles']]
    audit=fixed.Audit();u,required,permutation=mirror_geometry(parents,audit);coverage(data,required)
    results=[case_check(c,parents[c['parent']],u,audit) for c in data['cases']]
    signs=fixed.independent_sign_audit(audit.values)
    if self_test:malformed(data,parents,u,required)
    return {'agent':'six-rupert-2','role':'researcher','claim_status':'J77_uniform_positive_small_full_relative_angle_gap_for_strict_passages',
            'both_projections_may_vary':True,'arbitrary_planar_translations':True,'scales_covered':'lambda >= 1',
            'uniform_angle_gap_exists':True,'explicit_angle_gap_printed':False,'global_Rupert_resolved':False,
            'closed_equality_families_exist':True,'mirror_orbit_axes':5,'incident_regions':len(results),
            'common_active_equilibria':len(results),'positive_common_weights':sum(r['normal_balanced_weights'] for r in results),
            'strict_receiver_drift_corner_checks':sum(r['strict_drift_corners'] for r in results),
            'closed_parameter_coordinate_dual_covers':sum(r['coordinate_dual_pieces'] for r in results),
            'Bernstein_sign_coefficients':sum(r['Bernstein_sign_coefficients'] for r in results),
            'common_polynomial_factors_cancelled':sum(r['cancelled_common_factors'] for r in results),
            'independent_point_determinant_replays':3*sum(r['coordinate_dual_pieces'] for r in results)+len(results),
            'new_whole_parent_support_comparisons':audit.comparisons,'radial_exposure_comparisons':162,
            'new_independent_rational_sign_audits':signs,'case_summary':results,
            'prior_certificate_sha256':inherited['canonical_certificate_sha256'],
            'canonical_certificate_sha256':hashlib.sha256(json.dumps(data,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
            'mirror_permutation_sha256':hashlib.sha256(json.dumps(permutation,separators=(',',':')).encode()).hexdigest()}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--self-test',action='store_true');args=parser.parse_args()
    print(json.dumps(check(json.loads((ROOT/'certificates.json').read_text()),args.self_test),indent=2,sort_keys=True))
