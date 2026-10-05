"""Actual mathematical damages AFTER complete source binding.

Countermodels and damaged identities reach the actual endpoint, original
matrix, physical-action, Schur or affine-rank checks. Source corruption,
timeouts and resource statuses are separate, never mathematical rejects.
"""
from binding import check_current
check_current()
from encoding import F,affines,model,physical,schur_forms,scalar_rows
from pathlib import Path
from copy import deepcopy
from collections import Counter
import json
import resource
import tempfile
import time
import check
import chart


def run():
    start=time.monotonic();root=Path(__file__).resolve().parent
    path=root/'CANDIDATE.json';table,base,tau=check.read_candidate(path)
    parts,b=check.classify(base);q=F(1,65536);checks=[]
    def reject(name,reason,fn):
        try:fn()
        except ValueError as error:
            model.require(reason in str(error),'damage reached the intended mathematical guard: '+name+' '+str(error))
            checks.append(dict(name=name,exception='ValueError',reason=str(error)))
            return
        raise ValueError('mathematical damage was accepted: '+name)
    def table_control(name,reason,bad):
        saved=check.read_candidate;check.read_candidate=lambda unused:(bad,base,tau)
        try:reject(name,reason,lambda:check.run(path))
        finally:check.read_candidate=saved
    def original_control(name,bad):
        point=physical.original(bad,9,10)
        reject(name,'every actual original allowed floor',
               lambda:check.audit_entries(point['L'],point['den'],point['masks'],tau))
    point=physical.original(table,9,10);basis,gram=physical.complete_basis(point)
    reduced=schur_forms(table)
    multiplicity=Counter()
    for at,i in enumerate(range(2,303)):
        for j in range(i+1,303):
            if not point['masks'][i]&point['masks'][j]:
                key=tuple(sorted((point['types'][i-2],point['types'][j-2])))
                multiplicity[key]+=1
    kk,gg=parts['KK'][0],parts['GG'][0]
    bad=table.copy();bad[gg]-=q
    original_control('actual empty loop below claimed floor',bad)
    bad=table.copy();bad[kk]+=q;bad[gg]-=q*F(multiplicity[kk],multiplicity[gg])
    model.require(scalar_rows(bad)[('loop',)]==tau,'loop retained in bad-degree countermodel')
    original_control('bad empty degree below floor while actual loop is held',bad)
    bad=table.copy();bad[gg]+=q
    table_control('increase individual GG cost without paying sharp loop equality',
                  'all180 scalar rows, five sharp equations',bad)
    # A small KG perturbation with exact compensation at all five sharp
    # equalities reaches the SIGN guard, not a preceding degree failure.
    a=affines()
    pivots=[((0,0,1),(0,0,1)),((0,0,2),(0,0,2)),
            ((0,0,2),(2,0,1)),((0,0,2),(4,0,1)),((0,0,2),(6,0,1))]
    minor=[[a['rowdir'][r][a['keys'].index(k)] for k in pivots] for r in a['eqkeys']]
    inv,det=chart.inverse_and_det(minor);kg=parts['KG'][0];step=F(1,2**35)
    response=[a['rowdir'][r][a['keys'].index(kg)]*step for r in a['eqkeys']]
    bad=table.copy();bad[kg]+=step
    for i,key in enumerate(pivots):bad[key]-=sum(inv[i][j]*response[j] for j in range(5))
    rows=scalar_rows(bad)
    model.require(all(v>=tau for v in rows.values()) and all(rows[r]==tau for r in a['eqkeys']),
                  'KG countermodel retains EVERY original scalar floor and sharp equality')
    table_control('nonzero individual KG repair despite all five exact sharp degrees',
                  'all unrestricted sharp-pattern signs',bad)
    with tempfile.TemporaryDirectory(prefix='q19-semantic-input-',dir=root) as temp:
        temp=Path(temp);raw=json.loads(path.read_text())
        for name,reason,mutate in (
            ('missing actual143 coefficient','entire143 original real-coordinate witness',lambda d:d['free_pair_values'].pop()),
            ('wrong exact comparison-to-delta decoding','exact defining coordinate decoding',
             lambda d:d['free_pair_values'][0].update(delta=str(F(d['free_pair_values'][0]['delta'])+q))),
            ('endpoint outside stated certificate coverage','selected NEW exact dense endpoints only',lambda d:d.update(tau='1/4'))):
            data=deepcopy(raw);mutate(data);target=temp/'damaged.json';target.write_text(json.dumps(data))
            reject(name,reason,lambda:check.read_candidate(target))
    def loc(member):return point['members'].index(member)
    def add_symmetric(L,i,j,v):L[i][j]+=v;L[j][i]+=v
    # A balanced star four-cycle preserves every row and centered-star
    # equation, but violates original intersecting support.
    indices=list(map(loc,((0,),(0,1),(0,2),(0,1,2))))
    L=deepcopy(point['L']);i,j,k,l=indices
    for x,y,v in ((i,j,1),(k,l,1),(i,k,-1),(j,l,-1)):add_symmetric(L,x,y,v)
    reject('balanced intersecting star-support violation','all original support and symmetry',
           lambda:check.audit_entries(L,point['den'],point['masks'],tau))
    # Antisymmetric NN circulation keeps row/column sums and star kernel.
    L=deepcopy(point['L']);i,j,k=map(loc,((1,),(2,),(3,)))
    for x,y in ((i,j),(j,k),(k,i)):L[x][y]+=1;L[y][x]-=1
    reject('row-preserving asymmetric original NN circulation','all original support and symmetry',
           lambda:check.audit_entries(L,point['den'],point['masks'],tau))
    badpoint=deepcopy(point);anchor=loc((0,));nn=loc((1,))
    add_symmetric(badpoint['L'],anchor,nn,1)
    reject('wrong forced anchor breaks full star-column range','ENTIRE star-column range condition',
           lambda:check.full_schur(badpoint,table,basis,reduced))
    badpoint=deepcopy(point);badpoint['L'][anchor][anchor]+=1
    reject('wrong fixed singular star diagonal','ENTIRE fixed singular star block',
           lambda:check.full_schur(badpoint,table,basis,reduced))
    badreduced=deepcopy(reduced);full=model.sector_forms(table,9,10)['trivial_lower']
    at=[i for i,t in enumerate(full['types']) if not t[0]&1]
    badreduced['trivial_lower']['matrix']=[[full['matrix'][i][j] for j in at] for i in at]
    reject('omit full star-to-NN Schur coupling energy','EVERY full-original Schur row/basis action',
           lambda:check.full_schur(point,table,basis,badreduced))
    badreduced=deepcopy(reduced);badreduced['trivial_lower']['metric']=[F(1)]*13
    reject('unweighted original Schur action','EVERY full-original Schur row/basis action',
           lambda:check.full_schur(point,table,basis,badreduced))
    saved=model.sector_forms
    def wrong_star_form(t,k,m):
        forms=saved(t,k,m);f=forms['trivial_lower'];i=next(i for i,u in enumerate(f['types']) if u[0]&1)
        f['matrix'][i][i]+=q
        return forms
    model.sector_forms=wrong_star_form
    try:reject('false fixed-star inverse despite valid-shaped PD form',
               'both full fixed-star physical inverse products',lambda:schur_forms(table))
    finally:model.sector_forms=saved
    badpoint=deepcopy(point);badpoint['cap'][0][0]+=1
    reject('wrong full original upper inverse-Gram action','EVERY original upper row/basis image',
           lambda:physical.literal_actions(badpoint,table,basis))
    badbasis=basis.copy();badbasis[-1]=badbasis[0]
    reject('count-preserving duplicated physical direction','all distinct physical directions',
           lambda:physical.literal_actions(point,table,badbasis))
    badbasis=[v for v in basis if not(v['tag']=='XY_mixed' and v['sub'][1:]==(1,1))]
    reject('lost original nonstar mixed Schur direction','complete distinct nonstar physical basis',
           lambda:check.full_schur(point,table,badbasis,reduced))
    form=reduced['trivial_lower'];metric=form['metric'].copy();metric[0]=0
    reject('nonpositive physical orbit metric','positive physical metric domain',
           lambda:model.exact_ldl(form['matrix'],metric,F(0)))
    wrongform=deepcopy(form['matrix']);wrongform[0][0]=F(-1)
    negative=model.exact_ldl(wrongform,form['metric'],F(0))
    model.require(not negative['positive_definite'] and F(negative['witness_quadratic'])<0,
                  'entire rational negative-direction evidence for damaged Schur form')
    reject('explicit negative physical Schur direction cannot certify PSD','negative physical Schur direction',
           lambda:model.require(negative['positive_definite'],'negative physical Schur direction'))
    badinverse=deepcopy(inv);badinverse[0][0]+=q
    reject('wrong affine-rank inverse at an actual matrix position','both entire rational minor inverse products',
           lambda:chart.audit_inverse(minor,badinverse))
    singular=deepcopy(minor)
    for row in singular:row[0]=row[1]
    reject('singular five-equation minor cannot prove affine rank','entire stated five-equation rank minor nonsingular',
           lambda:chart.inverse_and_det(singular))
    saved=chart.comparison
    def missing_orbit():
        out=base.copy();out.pop(next(iter(out)));return out
    chart.comparison=missing_orbit
    try:reject('missing disjoint orbit invalidates full original budget closure','each parametric NN disjoint pair',chart.run)
    finally:chart.comparison=saved
    model.require(len(checks)==22,'all22 distinct new mathematical damages actually rejected')
    return dict(agent='six-downset-2',role='researcher',semantic_rejection_count=len(checks),
                actual_semantic_rejections=checks,complete_negative_Schur_witness=negative,
                KG_countermodel_all180_floors_and_five_equalities_verified=True,
                no_source_hash_or_timeout_or_resource_status_counted_as_math_rejection=True,
                actual_ValueError_guards_not_optimized_away=True,
                observed_seconds=time.monotonic()-start,
                peak_RSS_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)


if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
