"""Late corroboration only: compare all coefficients without author imports."""
import argparse, hashlib, json, sys
from fractions import Fraction
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from verify import build, parse, typed_equal

NAMES=['B','E','r','s','t','F','G','J','p0','p1']
def encode(poly,n=10):
    result=[]
    for monomial,(real,imaginary) in poly.items():
        if Fraction(imaginary):raise ValueError('nonreal independent coefficient')
        powers=[0]*n
        if monomial!='1':
            for factor in monomial.split('*'):
                name,_,power=factor.partition('^');powers[NAMES.index(name)]=int(power) if power else 1
        result.append([powers,str(Fraction(real))])
    return sorted(result)
def digest(polys):
    polys=list(polys)
    while len(polys)>1 and not polys[-1]:polys.pop()
    encoded=[encode(p) for p in polys]
    return {'degree':len(polys)-1,'coefficient_terms':[len(p) for p in polys],
            'sha256':hashlib.sha256(json.dumps(encoded,sort_keys=True,separators=(',',':')).encode()).hexdigest()}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--export',type=Path,required=True);ap.add_argument('--expected',type=Path,required=True);args=ap.parse_args()
    own=build()['algebra'];export=parse(args.export.read_text());native=parse(args.expected.read_text())
    pairs=[('whole_h','h_ascending'),('whole_p','p_ascending'),('whole_residuals','residuals_ascending')]
    checks=0
    for ours,theirs in pairs:
        values=[encode(p,5) for p in own[ours]]
        if not typed_equal(values,export[theirs]):raise ValueError('entire exported coefficients differ: '+ours)
        checks+=len(values)
    if not typed_equal(encode(own['whole_gamma'],5),export['C']):raise ValueError('entire gamma differs')
    checks+=1
    if not typed_equal([[encode(p,5) for p in row] for row in own['whole_matrix']],export['matrix_rows_ABC']):raise ValueError('entire matrix differs')
    checks+=15
    solved={'F':own['whole_h'][2],'G':own['whole_h'][1],'J':own['whole_h'][0],
            'p0':own['whole_p'][0],'p1':own['whole_p'][1],'p2':own['whole_p'][2],'C':own['whole_gamma']}
    for name,p in solved.items():
        if not typed_equal(digest([p]),native['solved_polynomials'][name]):raise ValueError('whole solved digest differs '+name)
    for name,p in zip(['tODE2','tODE1','tODE0','K1','K0plus4'],own['whole_residuals']):
        if not typed_equal(digest([p]),native['entire_residual_polynomials'][name]):raise ValueError('whole residual digest differs '+name)
    if not typed_equal([digest(row) for row in own['whole_matrix']],native['whole_matrix_rows']):raise ValueError('whole matrix digests differ')
    if [str(x) for x in own['obstruction']['whole_P']]!=native['slice_cubic'] or [str(x) for x in own['obstruction']['whole_S']]!=native['slice_degree_six']:raise ValueError('whole integer obstruction differs')
    print(json.dumps({'status':'PASS','entire_exported_scalar_polynomials_compared':checks,'entire_native_polynomial_digests_compared':17,'native_code_imported':False,'post_seal_corroboration_only':True}))
if __name__=='__main__':main()
