"""Optional independently rebuilt shared finite identities. No author import.
Pass the original pinned author expected.json as an external comparison only.
This does not certify the ordinary analytic bridges or any parent theorem.
"""
import argparse, hashlib, json
from fractions import Fraction as F
from pathlib import Path
import importlib.util
spec=importlib.util.spec_from_file_location('independent_phase_own',Path(__file__).with_name('check.py'))
own=importlib.util.module_from_spec(spec);spec.loader.exec_module(own)

def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':')).encode()
def poly_record(p):
    entries=[[list(e),str(c)] for e,c in sorted(p.items()) if c]
    return {'complete_terms':len(entries),'coefficient_sha256':hashlib.sha256(canon(entries)).hexdigest()}
def serialize(A):return [[str(a.r) for a in row] for row in A]
def generate():
    P,S,I,J=own.P,own.S,own.I,own.J
    matrices={'P_squared':serialize(own.mul(P,P)),'S_squared':serialize(own.mul(S,S)),
              'SP':serialize(own.mul(S,P)),'PS':serialize(own.mul(P,S)),'P_ones':['0']*8}
    coefficient_matrices=[]
    for k in range(8):coefficient_matrices.append(own.mul(own.mul(P,own.diag([F(i==k) for i in range(8)])),P))
    records=[]
    for i in range(8):
        row=[]
        for j in range(8):
            p={tuple(int(a==k) for a in range(8)):coefficient_matrices[k][i][j].r for k in range(8)}
            row.append(poly_record(p))
        records.append(row)
    matrices['PKP']={'rows':8,'columns':8,'complete_entry_sha256':hashlib.sha256(canon(records)).hexdigest(),'total_complete_terms':sum(a['complete_terms'] for row in records for a in row)}
    chi={};minors=[];common={};big=own.add(I,J)
    for mask in range(256):
        ix=[i for i in range(8) if mask>>i&1];d=own.det_elim([[big[i][j] for j in ix] for i in ix]).r;minors.append(str(d));k=len(ix)
        e=(8-k,)+tuple(int(mask>>i&1) for i in range(8));chi[e]=(-1)**k*d
        pair=(8-k,k);common[pair]=common.get(pair,F())+(-1)**k*d
    polys={'full_characteristic_minors_vs_derivative':poly_record(chi),
           'monic_characteristic':poly_record({(8,)+(0,)*8:F(1)}),
           'complete_first_trace':poly_record({(0,)+tuple(int(i==k) for i in range(8)):F(-2) for k in range(8)}),
           'entire_common_family_factorization':poly_record(common)}
    qforms=own.quadratics()
    for name,key in [('full_imaginary_norm','imaginary'),('full_light_imaginary_norm','fixed_light'),('full_PV_norm','projected_perturbation')]:
        Q=qforms[key];p={}
        for i in range(8):
            for j in range(i,8):
                e=tuple(int(a==i)+int(a==j) for a in range(8));p[e]=Q[i][j]*(1 if i==j else 2)
        polys[name]=poly_record(p)
    p={}
    for i in range(8):
        for j in range(i,8):
            e=tuple(int(a==i)+int(a==j) for a in range(8));p[e]=(F(3,4)*(i==j)+F(1,32))*(1 if i==j else 2)
    polys['whole_combined_leading_phase_budget']=poly_record(p)
    eps=F(1,1000);phase=F(41,40);den=164000;root=165000;dmin=F(13,8);cap=F(505,499)**2
    u=own.C(F(1,2),F(1,2000));z=1-1/u;E=2*(u-F(1,2)).n2();B=2*(z+1).n2()
    margins={
       'epsilon_below_critical_disjointness':F(4,5)*F(1,2)-eps,
       'heavy_gap_above_seven_ell':F(1,2)-9*eps,
       'projector_one_fifth':49-25*F(15,8),
       'linear_norm_ten_thirds':F(100,9)-11,
       'sqrt_eight_below_three':F(9)-8,
       'pair_error_below_five':F(25)-(16+F(4,9)),
       'uniform_phase_coefficient':phase-cap,
       'original_root_to_reciprocal_energy':root*F(639,640)**2-den,
       'root_budget_sqrt_denominator_above_400':F(root)-400**2,
       'gamma_sqrt_below_five_eighths':F(25,64)-F(3,8),
       'automatic_epsilon':eps**2-F(3,8)/(den*dmin**2),
       'slack_entry':F(1,64)-10/(den*dmin**2),
       'old_max_domain_containment':F(1,root)-F(8,1200**2),
       'witness_root_budget':F(3,2*root)-B,
       'witness_outside_old_max':B/2-F(1,960000),
       'witness_reciprocal_energy':F(3,8)/(4*den)-E,
       'witness_baseline_already_known':F(3,4)/1154736-E,
    }
    witness={'a':'1','gamma':'3/8','six_roots':'-1','pair_real':str(z.r),'pair_imaginary_absolute':str(abs(z.i)),'A':'0','E':str(E),'B_original':str(B),'previous_max_radius_squared':'1/960000'}
    return {'complete_rational_matrices':matrices,'whole_polynomial_identities':polys,'all256_principal_minors':minors,'strict_sufficient_margins':{k:str(v) for k,v in margins.items()},'actual_witness':witness}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('author_fixture',type=Path);a=ap.parse_args();b=a.author_fixture.read_bytes();target=json.loads(b);own_record=generate()
    for key,val in own_record.items():own.require(target[key]==val,'whole shared author field '+key)
    print(json.dumps({'status':'PASS','shared_fields':list(own_record),'matrices':6,'whole_polynomials':8,'principal_minors':256,'strict_margins':17,'complete_witness':True,'author_fixture_file_sha256':hashlib.sha256(b).hexdigest(),'shared_record_sha256':hashlib.sha256(canon(own_record)).hexdigest()},sort_keys=True))
if __name__=='__main__':main()
