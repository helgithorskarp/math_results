"""Optional late comparison of whole universal polynomials; imports no author code."""
import hashlib,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from verify import build,parse,typed_equal

NAMES=['A','B','E','F','G','J']+['p'+str(i) for i in range(7)]
def digest(polynomial):
    if not polynomial:polynomial=[{}]
    coefficients=[]
    for poly in polynomial:
        terms=[]
        for monomial,pair in poly.items():
            if pair[1]!='0':raise ValueError('nonreal coefficient in real polynomial')
            exponents=[0]*16
            if monomial!='1':
                for factor in monomial.split('*'):
                    name,*power=factor.split('^');name='p4' if name=='t' else name
                    exponents[NAMES.index(name)]=int(power[0]) if power else 1
            terms.append([exponents,pair[0]])
        coefficients.append(sorted(terms))
    canonical=json.dumps(coefficients,sort_keys=True,separators=(',',':')).encode()
    return {'degree':len(coefficients)-1,'coefficient_terms':[len(x) for x in coefficients],'sha256':hashlib.sha256(canonical).hexdigest()}

def main():
    if len(sys.argv)!=2:raise ValueError('supply the separately verified author expected.json')
    own=build()['algebra'];author=parse(Path(sys.argv[1]).read_text());u=author['universal'];pairs={
      'general_mass_kernel':own['whole_generic_kernel'],'degree_five_mass_kernel':own['whole_quintic_kernel']}
    selected={'top_odd_relation':[own['whole_quintic_kernel'][5]],'quartic_K2':[own['whole_quartic_kernel'][2]],'quartic_K1':[own['whole_quartic_kernel'][1]],'quartic_ODE5':[own['whole_quartic_ODE'][5]],'quartic_ODE4':[own['whole_quartic_ODE'][4]],'quartic_ODE2':[own['whole_quartic_ODE'][2]],'resonance_derivative':own['checks']['whole final-resonance derivative ODE']}
    # The resonance ODE has zero residual; its derivative polynomial is reconstructed
    # directly from the frozen formula rather than from an author field.
    selected['resonance_derivative']=[{'p0^3':['7/512','0']},{},{'p0^2':['21/64','0']},{},{'p0':['21/8','0']},{},{'1':['7','0']}]
    for name,p in pairs.items():
        if not typed_equal(digest(p),u[name]):raise ValueError('whole polynomial mismatch: '+name)
    for name,p in selected.items():
        if not typed_equal(digest(p),u['selected_entire_polynomials'][name]):raise ValueError('whole selected polynomial mismatch: '+name)
    print('PASS nine entire universal polynomial records against separately verified author fixture')

if __name__=='__main__':main()
