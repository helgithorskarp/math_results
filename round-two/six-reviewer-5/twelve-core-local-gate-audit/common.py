"""Late correspondence; producer computation never supplies primary truth."""
import pathlib,json,sys,hashlib
from fractions import Fraction as F
P=pathlib.Path(__file__).resolve().parent
from normals import references
from algebra import solve
sys.path.insert(0,str(P/'author'))
import check as native

def main():
    original=json.loads((P/'PRIMARY.json').read_text());seal=json.loads((P/'PRIMARY-SEAL.json').read_text())
    for row in seal['files']:
        if hashlib.sha256((P/row['path']).read_bytes()).hexdigest()!=row['sha256']:raise ValueError('primary seal changed after target access')
    data=json.loads((P/'author'/'INPUT.json').read_text());plan=json.loads((P/'author'/'PLAN.json').read_text())
    native.layout(data,plan);H,V,B,z0,jets,units=native.calibrate(data,plan)
    d,root,p,alt,q=references();count=0;groups={}
    def eq(a,b):
        nonlocal count
        if tuple(F(x) for x in a)!=tuple(F(x) for x in b):raise ValueError('entire algebraic polynomial mismatch')
        count+=5
    for i,v in enumerate(V):
        for j in range(3):eq(p[i][j].encode(),v[j])
    groups['all_original_reference_coefficients']=count
    before=count
    M=[[p[j][i] for j in (1,2,4)] for i in range(3)]
    for i,v in enumerate(p):
        coeff=solve(M,v)
        for j in range(3):eq(coeff[j].encode(),B[i][j])
    groups['all_original_anchor_coefficients']=count-before
    before=count;eq(original['moving_chart']['chart_inverse_z0'],z0)
    for row in original['moving_chart']['exact_jet_values']:
        out=jets[row['label']][row['coordinate']]
        for key,attr in [('value','v'),('dt','dt'),('dz','dz')]:eq(row[key],getattr(out,attr))
    groups['all_jet_and_inverse_chart_coefficients']=count-before
    before=count
    for row in original['positive_normals']['normal_systems']:
        new=native.normal_case(H,V,units[row['name']],row['normal_labels'])
        for a,b in zip(row['weights'],new['positive_weights']):eq(a,b)
        for old,newcorner in zip(row['cube_vertices'],new['corner_norms']):
            if old['signs']!=newcorner[0]:raise ValueError('entire inverse cube corner order')
            eq(old['norm_squared'],newcorner[1])
    groups['all_weight_and_cube_polynomial_coefficients']=count-before
    expected=json.loads((P/'author'/'EXPECTED.json').read_text());actual=json.loads((P/'native-normal.json').read_text())
    if actual!=expected:raise ValueError('whole native normal record differs from published expected')
    normal=actual;optimized=json.loads((P/'native-optimized.json').read_text())
    if normal!=optimized:raise ValueError('whole native normal/O differs')
    if normal['derivative_certificate']['coordinate_derivatives_enclosed_over_entire_rectangle']!=72:raise ValueError('native derivative coverage')
    return dict(actual_reviewer='six-reviewer-5',role='independent mathematical reviewer',primary_program_and_data_seal_unchanged_after_native_access=True,post_access_document_only_boundary_correction=True,all_rational_field_coefficients_compared=count,groups=groups,whole_native_expected_record_matches=True,whole_native_normal_optimized_matches=True,independent_interval_bits=128,native_interval_bits=80,interval_endpoints_not_expected_identical=True,producer_only_geometry_premises_not_reaudited=[7123,8704],primary_external_premises_explicit=True)
if __name__=='__main__':print(json.dumps(main(),sort_keys=True,separators=(',',':')))
