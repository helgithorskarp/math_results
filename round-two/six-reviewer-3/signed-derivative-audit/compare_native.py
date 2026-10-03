"""POST-SEAL adapter; independently rebuild every mathematical native field.

The native directory must be a byte-pinned copy of the defining source.
No native module is imported. EXPECTED is a diagnostic comparison input.
"""
from pathlib import Path
from fractions import Fraction as Q
from math import comb
import ast, hashlib, importlib.util,json,sys

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('owned_sealed_audit',HERE/'audit.py')
own=importlib.util.module_from_spec(spec);spec.loader.exec_module(own)

def unique(xs):
    d={}
    for k,v in xs:
        if k in d:raise ValueError('duplicate JSON key')
        d[k]=v
    return d
def load(path):return json.loads(Path(path).read_text(),object_pairs_hook=unique,
    parse_constant=lambda x: (_ for _ in ()).throw(ValueError('nonfinite JSON')))
def sparse(power):return [[i,j,str(v)] for (i,j),v in sorted(power.items())]
def literal(a,q):
    enc=lambda z:[str(x) for x in own.ga(z)]
    return {'a':str(a),'q':[enc(z) for z in q],'origin':enc(own.derivative(a,q,set())),
      'gradient':[enc(own.derivative(a,q,{j})) for j in range(8)],
      'ordered_hessian':[[enc(own.derivative(a,q,{j,k})) if j!=k else ['0','0'] for k in range(8)] for j in range(8)],
      'successive_distinct_partials':[enc(own.derivative(a,q,set(range(p)))) for p in range(1,9)]}

def expected_native():
    r=own.build();faces=[]
    for f in r['faces']:
        # Invert v=100a-99 with an independent exact coefficient transform.
        au={}
        for (x,y),c in f['power'].items():
            for i in range(x+1):
                au[i,y]=au.get((i,y),Q(0))+c*comb(x,i)*100**i*(-99)**(x-i)
        au={k:v for k,v in au.items() if v};b=f['bernstein'];flat=[c for row in b for c in row]
        faces.append({'order':f['p'],'free':f['k'],'tensor_degrees':[8,f['k']],
          'power_a_u':sparse(au),'power_v_u':sparse(f['power']),
          'bernstein':[[str(c) for c in row] for row in b],'min':str(min(flat)),'max':str(max(flat))})
    budgetmap={'complex_gradient':'complex_gradient','complex_hessian':'complex_hessian',
      'product_gradient':'product_gradient','seed_parameter_box':'a_domain',
      'whole_phase_box':'phase_path','global_cost_rounding':'original_global',
      'initial_E2':'initial_E2','coarse_v1':'first_bootstrap','coarse_E2_25':'second_E2',
      'coarse_v2':'second_bootstrap','coarse_E2_27':'third_E2','coarse_v3':'third_bootstrap'}
    margins={k:str(r['budgets'][v]) for k,v in budgetmap.items()}
    real=[Q(9,2)]+[Q(1,2)]*7;q=list(map(own.ga,real));q[1]=(Q(63,130),Q(8,65))
    controls=[literal(Q(1),[Q(1)]*8),literal(Q(99,100),[Q(1,2)]*8),literal(Q(1),real),literal(Q(1),q)]
    maxima=[own.M[p]-r['signed_margins'][p-1] for p in range(1,8)]+[Q(1)]
    bad={'real_gradient_half':Q(1,2)-maxima[0],'real_hessian_half':Q(1,2)-maxima[1],
      'seventh_order_three':Q(3)-maxima[6],'eighth_order_zero':-maxima[7],
      'complex_gradient_budget_three_fifths':Q(3,5)-r['complex_endpoint'][0],
      'complex_hessian_budget_two_thirds':Q(2,3)-r['complex_endpoint'][1],
      'global_nonpositive_gradient':-Q(1971,3584),'zero_phase_loss_on_all_envelopes':-r['positive_loss']}
    result={'agent':'six-sendov-1','role':'researcher','a_interval':['99/100','1'],
      'real_floor':'1/2','real_total_cap':'803/100','excess':'403/100',
      'real_bounds':[str(x) for x in own.M[1:]],'whole_faces':faces,
      'real_strict_margins':[str(x) for x in r['signed_margins']],'closed_order8_maximum':'1',
      'complete_complex_taylor_coefficients':[[str(x) for x in row] for row in r['N']],
      'complex_eps_cap':'1/8','complex_endpoint_values':[str(x) for x in r['complex_endpoint']],
      'strict_margins':margins,'phase_coefficients':{'deficit':'9/16','l1_square':'3/8',
        'normalized_phase':'525/8','normalization':'16','whole_cost':'653/8','rounded':'82'},
      'coarse_d0':str(Q(104960,39)),'coarse_proportional_v':str(Q(1469440,1053)),
      'whole_literal_controls':controls,'positive_gradient':str(Q(1971,3584)),
      'phase_loss':str(r['positive_loss']),'literal_eps_squared':'1/65','literal_deficit':'1/65',
      'rejected_mathematical_budgets':{k:str(v) for k,v in bad.items()}}
    return result

def main():
    if len(sys.argv)!=2:raise ValueError('usage: compare_native.py PINNED_NATIVE_DIRECTORY')
    native=Path(sys.argv[1]);pins=load(HERE/'NATIVE_PINS.json')
    for name,x in pins['files'].items():
        if hashlib.sha256((native/name).read_bytes()).hexdigest()!=x['sha256']:raise ValueError('external source pin '+name)
    seal=load(HERE/'SEAL.json')
    for name,x in seal['files'].items():
        if hashlib.sha256((HERE/name).read_bytes()).hexdigest()!=x['sha256']:raise ValueError('independent seal changed '+name)
    expected=expected_native();actual=load(native/'EXPECTED.json')
    if own.canonical(expected)!=own.canonical(actual):raise ValueError('ENTIRE native record differs')
    digest=hashlib.sha256(own.canonical(expected)).hexdigest()
    if digest!='53e74e5b1a6f342dd5777b9c8d30b34aed65843eac89bd5b89d6178ac98b18ed':raise ValueError('native whole-record digest')
    print(json.dumps({'entire_native_record_equal':True,'native_sha256':digest,
      'native_record_bytes':len(own.canonical(expected)),'faces':36,'bernstein_entries':1080,
      'four_whole_control_records_equal':True,'all_native_source_pins_and_seal_preserved':True},sort_keys=True))
if __name__=='__main__':main()
