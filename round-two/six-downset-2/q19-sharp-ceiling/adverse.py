"""New-ceiling mathematical damages AFTER complete source binding.

Countermodel controls use explicitly exposed in-memory inputs; hash/source
faults, crashes, timeout and resource failures are never semantic rejects.
Same-author prior damage-test scaffolding is credited in SOURCE.json.
"""
from binding import check_current
check_current()
from encoding import F,comparison,scalar_rows,classify,schur_forms,model,physical
import check_boundary as boundary
import check_structure as structure
from pathlib import Path
from copy import deepcopy
from collections import Counter
import hashlib,json,resource,tempfile,time


def run():
    began=time.monotonic();root=Path(__file__).resolve().parent
    path=root/'BOUNDARY-CANDIDATE.json';table,base,tau=boundary.read_candidate(path)
    parts,budgets=classify(base);checks=[];q=F(1,65536)
    def reject(name,reason,fn):
        try:fn()
        except ValueError as error:
            model.require(reason in str(error),'damage reached its intended mathematical guard: '+name+' '+str(error))
            checks.append(dict(name=name,exception='ValueError',reason=str(error)))
            return
        raise ValueError('mathematical damage was accepted: '+name)
    def json_control(name,reason,predicate,change):
        saved=structure.json.loads
        def damaged(raw,*args,**kwargs):
            obj=saved(raw,*args,**kwargs)
            if isinstance(obj,dict) and predicate(obj):change(obj)
            return obj
        structure.json.loads=damaged
        try:reject(name,reason,structure.run)
        finally:structure.json.loads=saved
    isdual=lambda d:'inequality_multipliers' in d
    json_control('negative sharp-ceiling dual inequality multiplier',
                 'all nonnegative new dual inequality weights',isdual,
                 lambda d:d['inequality_multipliers'].__setitem__(3,'-1/65536'))
    json_control('nonnegative dual with wrong original144-coordinate identity',
                 'entire144 exact objective identity',isdual,
                 lambda d:d['inequality_multipliers'].__setitem__(3,str(F(d['inequality_multipliers'][3])+q)))
    kg=next(k for k in parts['KG'] if structure.XY not in k)
    key_index=sorted(base).index(kg)
    json_control('entry-only vertex with a nonzero required KG coordinate',
                 'whole220 inequalities and30 equalities of entry-only LP vertex',
                 lambda d:'deltas' in d and 'active_row_guess_count' in d,
                 lambda d:d['deltas'].__setitem__(key_index,'1/1073741824'))
    with tempfile.TemporaryDirectory(prefix='q19-ceiling-semantic-',dir=root) as temp:
        target=Path(temp)/'candidate.json';data=json.loads(path.read_text())
        missing=deepcopy(data);missing['free_pair_values'].pop();target.write_text(json.dumps(missing))
        reject('missing original143rd coefficient','entire143 original real-coordinate witness',
               lambda:boundary.read_candidate(target))
        wrong=deepcopy(data);wrong['free_pair_values'][0]['delta']=str(F(wrong['free_pair_values'][0]['delta'])+q)
        target.write_text(json.dumps(wrong))
        reject('wrong exact original comparison-to-delta decoding','exact defining coordinate decoding',
               lambda:boundary.read_candidate(target))
    def original_control(name,bad):
        point=physical.original(bad,9,10)
        reject(name,'every actual original allowed floor',
               lambda:boundary.audit_entries(point['L'],point['den'],point['masks'],tau))
    yy=(structure.Y,structure.Y)
    bad=table.copy();bad[yy]-=q
    model.require(all(scalar_rows(bad)[r]==tau for r in [('empty',t) for t in budgets['bad_nn']]),
                  'loop damage holds all bad empty floors')
    original_control('actual empty loop below the new sharp ceiling',bad)
    bad=table.copy();bad[tuple(sorted((structure.Y,structure.XY)))]-=q;bad[yy]+=18*q
    model.require(scalar_rows(bad)[('loop',)]==tau,'selected proper-floor damage preserves actual loop')
    original_control('selected original Y/XY proper floor below ceiling with loop held',bad)
    def table_control(name,bad):
        saved=boundary.read_candidate;boundary.read_candidate=lambda unused:(bad,base,tau)
        try:reject(name,'all boundary sharp-pattern signs',lambda:boundary.run(path))
        finally:boundary.read_candidate=saved
    eqkeys=[('empty',t) for t in budgets['bad_nn']]+[('loop',)]
    pivots=[(structure.Y,structure.Y),((0,0,2),(0,0,2)),
            ((0,0,2),(2,0,1)),((0,0,2),(4,0,1)),((0,0,2),(6,0,1))]
    rows0=scalar_rows(base);minor=[]
    for r in eqkeys:
        minor.append([])
        for key in pivots:
            unit=base.copy();unit[key]+=1
            minor[-1].append(scalar_rows(unit)[r]-rows0[r])
    inv,det=structure.inverse_and_det(minor)
    step=F(1,2**35);unit=base.copy();unit[kg]+=1
    response=[(scalar_rows(unit)[r]-rows0[r])*step for r in eqkeys]
    bad=table.copy();bad[kg]+=step
    for i,key in enumerate(pivots):bad[key]-=sum(inv[i][j]*response[j] for j in range(5))
    rb=scalar_rows(bad);forced=set(eqkeys)|{('empty',structure.XY),
        ('proper',structure.Y,structure.XY),('proper',structure.X,structure.XY)}
    model.require(all(v>=tau for v in rb.values()) and all(rb[r]==tau for r in forced),
                  'KG countermodel holds EVERY180 floor and all eight ceiling equations')
    table_control('nonzero KG despite every original floor and all eight ceiling equations',bad)
    bad=table.copy();bad[tuple(sorted((structure.XY,(2,0,0))))]-=q;bad[yy]+=2*q
    rb=scalar_rows(bad)
    model.require(all(v>=tau for v in rb.values()) and all(rb[r]==tau for r in eqkeys),
                  'negative forced GG countermodel holds EVERY180 floor and five sharp equations')
    table_control('negative one of the7470 forced GG repairs despite original floors',bad)
    saved=structure.decode
    def wrong_line(path,pin,base,tau):
        out=saved(path,pin,base,tau)
        if Path(path).name=='POSTLINE-CANDIDATE.json':out[tuple(sorted((structure.XY,(2,0,0))))]+=q
        return out
    structure.decode=wrong_line
    try:reject('wrong supposedly constant coordinate on the eight-coordinate post-ceiling line',
               'every143 original coordinate obeys the specified eight-coordinate affine line',structure.run)
    finally:structure.decode=saved
    saved=model.members
    def duplicate_X(k,m):
        out=saved(k,m);out[out.index((3,))]=(4,);return out
    model.members=duplicate_X
    try:reject('same-count duplicate original X singleton invalidates new9000-coordinate census',
               'all35865 original coordinates checked',structure.run)
    finally:model.members=saved
    wrong=deepcopy(inv);wrong[0][0]+=q
    reject('damaged surviving boundary rank inverse at an actual position',
           'both whole NEW-domain inverse products',lambda:structure.audit_inverse(minor,wrong))
    singular=deepcopy(minor)
    for row in singular:row[0]=row[1]
    reject('singular surviving minor cannot pay the104-dimensional invariant face',
           'new-boundary surviving exact rank minor',lambda:structure.inverse_and_det(singular))
    point=physical.original(table,9,10);basis,gram=physical.complete_basis(point);reduced=schur_forms(table)
    full=model.sector_forms(table,9,10)['trivial_lower'];at=[i for i,t in enumerate(full['types']) if not t[0]&1]
    wrong=deepcopy(reduced);wrong['trivial_lower']['matrix']=[[full['matrix'][i][j] for j in at] for i in at]
    reject('omit original star coupling energy at the new ceiling matrix',
           'EVERY full-original Schur row/basis action',lambda:boundary.full_schur(point,table,basis,wrong))
    wrong=deepcopy(point);wrong['cap'][0][0]+=1
    reject('wrong original upper inverse-Gram row image at the new ceiling',
           'EVERY original upper row/basis image',lambda:physical.literal_actions(wrong,table,basis))
    wrong=basis.copy();wrong[-1]=wrong[0]
    reject('count-preserving duplicate of a new original physical direction',
           'all distinct physical directions',lambda:physical.literal_actions(point,table,wrong))
    form=model.sector_forms(table,9,10)['trivial_lower'];wrong=deepcopy(form['matrix']);wrong[0][0]=F(-1)
    negative=model.exact_ldl(wrong,form['metric'],F(1,1024))
    model.require(not negative['positive_definite'] and F(negative['witness_quadratic'])<0,
                  'entire exact negative shifted physical direction for the actual ceiling form')
    reject('explicit negative shifted original physical form cannot certify the endpoint',
           'negative shifted original physical direction',
           lambda:model.require(negative['positive_definite'],'negative shifted original physical direction'))
    model.require(len(checks)==17 and len({r['name'] for r in checks})==17,
                  'all17 distinct new mathematical controls actually rejected')
    return dict(agent='six-downset-2',role='researcher',semantic_rejection_count=len(checks),
        actual_semantic_rejections=checks,KG_countermodel_all180_floors_and_all8_equations_verified=True,
        negative_forced_GG_countermodel_all180_floors_and_five_sharp_equations_verified=True,
        complete_negative_shifted_physical_witness=negative,
        source_hash_crash_timeout_and_resource_status_not_counted_as_math_rejection=True,
        ordinary_real_bridges_unformalized=True,independently_reviewed=False,
        observed_seconds=time.monotonic()-began,peak_RSS_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)


if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
