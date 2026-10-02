"""Late corroboration adapter; never imports or supplies the author's proof.

Inputs are the entire native emitted record and the previously sealed own
record. Every coefficient of each compared polynomial contributes to its
canonical digest, not just an aggregate count or evaluation.
"""
import argparse,hashlib,json
from fractions import Fraction as F
from pathlib import Path

def convert(p,mapping,part):
    out=[]
    for key,pair in p.items():
        value=F(pair[part])
        if not value:continue
        mon=[0]*18
        if key!='1':
            for factor in key.split('*'):
                bits=factor.split('^');name=bits[0];degree=int(bits[1]) if len(bits)>1 else 1
                if name not in mapping:raise ValueError('unmapped whole polynomial variable')
                mon[mapping[name]]+=degree
        out.append([mon,[value.numerator,value.denominator]])
    out.sort(key=lambda x:x[0])
    raw=json.dumps(out,separators=(',',':')).encode()
    return {'terms':len(out),'entire_coefficients_sha256':hashlib.sha256(raw).hexdigest()}

def compare(own,native):
    rows=own['audit']['rows'];checks={x['name']:x for x in native['complete_controls']}
    axes={('d'+str(k)+part):2*k+offset for k in range(9) for part,offset in [('R',0),('I',1)]}
    matches=[]
    candidates=[('full cyclic weight frequency '+str(k),k) for k in range(9)]
    candidates += [('full cyclic mean including negative constant norm',0),
                   ('full first Fourier row with wrap',1),
                   ('full second Fourier row with zero extra wrap',2)]
    candidates += [('whole real weight conjugacy '+str(k),k) for k in range(1,5)]
    positions=0
    for name,k in candidates:
        for part,label in [(0,'real'),(1,'imag')]:
            got=convert(rows[k],axes,part)
            if got!=checks[name][label]:raise ValueError('whole native coefficient digest differs: '+name+'/'+label)
            positions+=got['terms'];matches.append(name+'/'+label)
    norm_axes={name:i for i,name in enumerate(['eta','x','y','L','v1','v2'])}
    got=convert(own['audit']['norm_bounds'][0],norm_axes,0)
    actual=checks['whole first Fourier majorant']
    if got!={k:actual[k] for k in ['terms','entire_coefficients_sha256']}:raise ValueError('entire first norm majorant differs')
    positions+=got['terms'];matches.append('whole first Fourier majorant')
    def ratio(value):return F(*value)
    b=own['audit']['budgets']['30']
    pairs=[('refined_lower_sum','lower_tail'),('first_mean_lambda','lambda'),('final_coefficient_cap','cap')]
    scalar_matches=[]
    for field,our in pairs:
        if ratio(native[field])!=F(b[our]):raise ValueError('whole scalar differs '+field)
        scalar_matches.append(field)
    if [ratio(x) for x in native['initial_lower_coefficient_bounds']]!=[F(x) for x in b['initial_lower']]:raise ValueError('all six initial lower coefficients differ')
    if [ratio(x) for x in native['final_majorant_costs']]!=[F(b['Kx']),F(b['Ky'])]:raise ValueError('both full original quadratic costs differ')
    return {'coefficient_digest_matches':matches,'compared_coefficient_positions_with_repeated_rows':positions,
            'scalar_matches':scalar_matches,'initial_lower_entries':6,'final_cost_entries':2,
            'scope':'late corroboration only; no author imports or theorem input'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('own',type=Path);ap.add_argument('native',type=Path);a=ap.parse_args()
    print(json.dumps(compare(json.loads(a.own.read_text()),json.loads(a.native.read_text())),indent=2))

if __name__=='__main__':main()
