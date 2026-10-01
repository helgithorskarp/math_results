"""Whole-entry agreement and concrete malformed-certificate controls."""
import bootstrap
from fractions import Fraction as F
from pathlib import Path
from tempfile import TemporaryDirectory
import copy,shutil,json
from weights import scalar,formula,cap_parameters,inverse,KAPPA
from matrices import literal_base,prepare,check_whole,trade
from entries import make_entries,entry
from poly import R,exact_divide
from exact import require,lift,schur_psd,polynomial_psd

def compare(expected,actual):
    require(json.loads(json.dumps(expected))==json.loads(json.dumps(actual)),'frozen exact certificate differs from regeneration')

def original_entries(q):
    info,X,core,star,L=prepare(q);N=len(X);_,scaled,normalized=make_entries(q)
    for i,A in enumerate(X):
        for j,B in enumerate(X):
            require(scaled(A,B)==L[i][j],'constant-size scaled entry differs from original lift')
            require(normalized(A,B)==(L[i][j]-info['s']*int(i==j))/(N-info['s']),'normalized entry differs from original lift')
    extra=0
    if q==7:
        t=info['tau']/2;Rmat,_,_=trade(X);small=lift([[core[i][j]+t*Rmat[i][j] for j in range(N-1)] for i in range(N-1)])
        _,half,_=make_entries(q,t)
        require(all(half(A,B)==small[i][j] for i,A in enumerate(X) for j,B in enumerate(X)),'closed-interval entry slope differs')
        check_whole(q,X,small);extra=N*N
    return {'q':q,'N':N,'whole_scaled_and_normalized_entry_comparisons':2*N*N,'half_interval_scaled_comparisons':extra}

def controls(base_record):
    rejected=[]
    def reject(name,call):
        try:call()
        except (ValueError,TypeError,ZeroDivisionError):rejected.append(name);return
        raise ValueError('Malformed control was accepted: '+name)
    reject('theorem_q6',lambda:scalar(6))
    reject('floating_q',lambda:scalar(7.0))
    reject('boolean_q',lambda:scalar(True))
    reject('huge_literal_allocation',lambda:prepare(10**6))
    reject('deleted_triple_entry',lambda:entry(7,14,0))
    reject('nonmember_triple_entry',lambda:entry(7,1|8|16,0))
    reject('out_of_ground_entry',lambda:entry(7,1<<10,0))
    reject('floating_index',lambda:entry(7,1.0,0))
    reject('zero_repair',lambda:make_entries(7,F(0)))
    reject('repair_above_endpoint',lambda:make_entries(7,2*scalar(7)['tau']))
    reject('floating_repair',lambda:make_entries(7,0.001))
    reject('singular_kernel_gram',lambda:inverse([[1,1],[1,1]]))
    reject('nonexact_polynomial_division',lambda:exact_divide((F(1),F(0),F(1)),(F(1),F(1))))
    reject('negative_unbounded_constant',lambda:R((-1,1)).coefficients_positive())
    reject('zero_pivot_nonzero_row',lambda:schur_psd([[0,1],[1,0]]))
    reject('negative_characteristic_form',lambda:polynomial_psd([[-1,0],[0,1]]))
    damaged=copy.deepcopy(base_record);damaged['lower_floor_determinants'][0]['coefficients'][0]='-1'
    reject('damaged_frozen_coefficient',lambda:compare(damaged,base_record))
    weights=formula(F(4));weights[((0,1),(0,1))]+=1
    reject('damaged_base_constant_action',lambda:literal_base(4,weights=weights))
    _,_,wrong_chi,_=cap_parameters(F(7),F(1,2))
    reject('old_kappa_wrong_cap_premise',lambda:require(wrong_chi>0,'old sufficient condition fails atq7'))
    info,X,core,star,L=prepare(7);N=len(X);idx={A:i for i,A in enumerate(X)}
    altered=copy.deepcopy(L);altered[0][0]+=1
    reject('changed_actual_empty_loop',lambda:check_whole(7,X,altered))
    altered=copy.deepcopy(L);i,j=idx[1],idx[2];altered[i][j]=altered[j][i]=L[i][j]+1
    reject('allowed_weight_wrong_row_sum',lambda:check_whole(7,X,altered))
    altered=copy.deepcopy(L)
    # A symmetric four-cycle preserves every row and diagonal, but changes
    # two intersecting entries: this genuinely tests support after row checks.
    for A,B,v in [(1,3,1),(3,4,-1),(4,6,1),(6,1,-1)]:
        i,j=idx[A],idx[B];altered[i][j]+=v;altered[j][i]+=v
    require(all(sum(row)==N for row in altered),'support control did not preserve rows')
    reject('row_balanced_intersection_damage',lambda:check_whole(7,X,altered))
    altered=copy.deepcopy(L);altered[1][2]+=1
    reject('asymmetric_whole_entry',lambda:check_whole(7,X,altered))
    reject('missing_empty_vertex',lambda:check_whole(7,X[1:],L))
    with TemporaryDirectory(prefix='two-deletion-helper-') as dirname:
        target=Path(dirname)
        for name in bootstrap.PINS:shutil.copyfile(bootstrap.BASE/name,target/name)
        path=target/'poly.py';path.write_bytes(path.read_bytes()+b'\n# damaged pinned helper\n')
        reject('changed_helper_pin',lambda:bootstrap.setup(target))
    # An actual large-order entry needs no large literal allocation. This is
    # formula validation, not finite evidence for the unbounded PSD theorem.
    huge=10**6;info,scaled,normalized=make_entries(huge)
    require(scaled(1,1)==info['s'] and normalized(1,1)==0,'large-order diagonal formula')
    require(scaled(1,3)==0 and normalized(1,3)==0,'large-order support formula')
    expected_loop=(info['s']-3+KAPPA*(F(huge*(huge+1),2)+F(3*huge-1,3*huge+5)))/(info['N']-info['s'])
    require(normalized(0,0)==expected_loop,'large-order allowed loop formula')
    return {'rejections':rejected,'rejection_count':len(rejected),'large_entry_parameter':huge,'row_balanced_support_control':True}
