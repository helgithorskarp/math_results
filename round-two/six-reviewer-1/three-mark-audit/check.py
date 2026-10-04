"""Full independent arithmetic record: author data plus fresh original controls."""
from pathlib import Path
import hashlib,json,signal,sys
from fractions import Fraction as Q

HERE=Path(__file__).resolve().parent
seal=json.loads((HERE/'PRIMARY_SEAL.json').read_text())
for name,digest in seal['files'].items():
    if hashlib.sha256((HERE/name).read_bytes()).hexdigest()!=digest:
        raise ValueError('preimport primary source binding')
sys.path.insert(0,str(HERE))
from certificate import verify
from geometry import construct


def arithmetic():
    # Every comparison is rational; square-root bounds are paid by squares.
    a=Q(3,13);c=Q(9,26)
    row_bounds=[1+2*a*a+a*c*Q(3,2)/3+a*Q(3,2),
      1+c*c+a*c*Q(3,2)/3+c/3+c*2*Q(7,4)/3,
      1+a*Q(3,2)+c/3,3*Q(29,57)+c*2*Q(7,4)/3]
    if row_bounds!=[Q(1009,676),Q(1135,676),Q(19,13),Q(1907,988)]or 1+c*c+c!=Q(991,676):raise ValueError('independent complete row bound reconstruction')
    checks={
      'sqrt2_below_three_halves':Q(9,4)-2,
      'sqrt58over19_below_seven_fourths':Q(49,16)-Q(58,19),
      'heavy_large_mu_slope_minus_one_fifth':Q(421,1536)-Q(1,5),
      'heavy_large_mu_margin_at_s16':16*(Q(421,1536)-Q(1,5))-Q(5,6),
      'small_mu_margin_at_s13':13*(Q(1,3)-Q(1,22)-Q(9,338)-Q(1,5))+Q(9,22)-1-Q(1,242),
      'nu_bound_below_half':Q(1,2)-Q(31,63),
      'nu_bound_below_old_row_bound':Q(29,57)-Q(31,63),
      'standard_row_1_slack':2-Q(1009,676),
      'standard_row_2_slack':2-Q(1135,676),
      'standard_row_3_slack':2-Q(19,13),
      'standard_row_4_slack':2-Q(1907,988),
      'leaf_trace_row_slack':2-Q(991,676),
      'rank_two_bound_squared_slack':(Q(105,16)-3)**2-Q(25,2),
      'new_endpoint_inside_lower_interval':6-Q(3,20)*Q(59,156),
    }
    if any(v<=0 for v in checks.values()):raise ValueError('all rational universal bound gates')
    if 1-Q(3,20)*Q(105,16)!=Q(1,64)or 1-Q(1,32)*Q(105,16)!=Q(407,512):raise ValueError('new whole interval margins')
    if Q(5,39)+Q(1,4)!=Q(59,156):raise ValueError('uniform kappa arithmetic')
    return {'strict_positive_slacks':{k:str(v)for k,v in checks.items()},
            'standard_normalized_row_bounds':[str(v)for v in row_bounds],
            'new_closed_positive_endpoint':'3/20','new_uniform_cap_floor':'1/64',
            'delta_one_thirty_second_floor':'407/512',
            'exact_rank_two_eigenvalues':'delta*(3 +/- sqrt((9+3/h)*(1+1/(2*l))))',
            'optimal_upper_interval_claimed':False}


def record():
    return {'agent':'six-reviewer-1','role':'independent mathematical reviewer',
            'all_count_coefficient_certificate':verify(),
            'literal_original_controls':[construct(*a)for a in [(3,3,2),(4,3,2),(4,4,3)]],
            'universal_arithmetic':arithmetic()}


if __name__=='__main__':
    signal.alarm(45)
    data=record();raw=(json.dumps(data,sort_keys=True,separators=(',',':'))+'\n').encode()
    Path(sys.argv[1]).write_bytes(raw)
    print(json.dumps({'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),
       'whole_original_N':[c['N']for c in data['literal_original_controls']],
       'full_physical_dimensions':[c['full_physical_dimension']for c in data['literal_original_controls']],
       'all_coefficient_and_geometry_and_interval_gates_passed':True}))
