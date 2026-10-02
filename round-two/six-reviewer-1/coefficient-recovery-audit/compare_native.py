"""Post-seal data-only whole native coefficient alignment.

No producer executable is imported. Takes its separately verified JSON
export, and the owned independent full record; new refinements have no
producer counterpart. The late257 unit is corroboration, not a premise
of the sealed263 proof.
"""
from pathlib import Path
from fractions import Fraction as Q
import argparse
import hashlib
import json
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from algebra import P, bezout


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('native_export',type=Path)
    parser.add_argument('--owned',type=Path,default=Path(__file__).with_name('EXPECTED.json'))
    args=parser.parse_args();own=json.loads(args.owned.read_text())
    raw=json.loads(args.native_export.read_text());native=raw['record'];checks=[]
    def op(row):return P({tuple(k):Q(n,d) for k,n,d in row})
    def np(row):
        result={}
        for k,value in row:
            if len(k)!=10 or any(k[8:]):raise ValueError('native monomial dimension/tail')
            key=tuple(k[:8])
            if key in result:raise ValueError('duplicate native monomial')
            result[key]=Q(value)
        return P(result)
    def same(label,left,right):
        if left!=right:raise ValueError('full native comparison: '+label)
        checks.append(label)
    for i in range(5):same('full-chart-R'+str(i),op(own['chart_residual'][i]),np(raw['entire_transformed_R'][i]))
    for i in range(4):
        a,b=op(own['alpha'][i]),op(own['beta'][i])
        same('alpha'+str(i),a,np(native['complete_Elinear_coefficients_alpha'][i]))
        same('beta'+str(i),b,np(native['complete_Elinear_constants_beta'][i]))
        same('primitive-A'+str(i),op(own['primitive_A'][i]),np(native['primitive_E_leading_polynomials_A'][i]))
        same('whole-affine'+str(i),a*P({(0,1,0,0,0,0,0,0):1})+b,np(raw['entire_Elinear_rows'][i]))
    r0=op(own['chart_residual'][0])
    for i,j in enumerate([2,1,0]):
        same('R0-E'+str(j),r0.coeff(1,j),np(native['complete_remaining_R0_E_coefficients'][i]))
    for name in ['F','G','J','N','P','R','L']:
        same('entire-necessary-'+name,op(own[name]),np(native['complete_necessary_polynomials'][name]))
    for i,item in enumerate(native['fixed_resultants']):
        p=op(own['determinants'][i]);coeff=[p.coeff(3,j).d.get((0,)*8,Q(0))for j in range(p.degree(3)+1)]
        same('whole-determinant-'+str(i),coeff,[Q(v)for v in item['whole_determinant_coefficients']])
        same('primitive-determinant-'+str(i),own['primitive_determinants'][i],item['primitive_coefficients'])
        same('determinant-content-'+str(i),Q(own['determinant_contents'][i]),Q(item['content']))
        # Align every full coefficient series used to construct fixed matrices.
        for key,polyname in [('left_entire_coefficient_arrays','P'),('right_entire_coefficient_arrays','R' if i==0 else 'L')]:
            poly=op(own[polyname]);series=[]
            for degree in range(poly.degree(2)+1):
                part=poly.coeff(2,degree)
                series.append([int(part.coeff(3,j).d.get((0,)*8,0))for j in range(max(0,part.degree(3))+1)])
            same('entire-fixed-matrix-series-'+str(i)+'-'+polyname,series,item[key])
        for x,value in enumerate(item['every_integer_value']):
            same('determinant-at-native-node-'+str(i)+'-'+str(x),
                 sum(v*x**j for j,v in enumerate(coeff)),Q(value))
    unit=native['whole_univariate_finite_unit']
    prime=257;left,right=[[v%prime for v in row]for row in own['primitive_determinants']]
    u,v=bezout(left,right,prime)
    for name,value in [('left',left),('right',right),('left_multiplier',u),('right_multiplier',v)]:
        same('entire-late257-unit-'+name,value,unit[name])
    record={'agent':'six-reviewer-1','role':'independent mathematical reviewer',
            'whole_comparisons':checks,'whole_comparison_count':len(checks),
            'producer_imports':False,'ordering':'data-only adapter written AFTER independent core/proof/fixture seal',
            'native_export_sha256':hashlib.sha256(args.native_export.read_bytes()).hexdigest(),
            'owned_canonical_sha256':hashlib.sha256(json.dumps(own,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
            'native_refinements_not_present':['four complex recovery charts','sharper directional E bound']}
    print(json.dumps(record,sort_keys=True))


if __name__=='__main__':
    main()
