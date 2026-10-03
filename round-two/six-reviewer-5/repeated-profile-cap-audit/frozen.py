"""Independent frozen sign-certificate checking with Fraction Gaussian determinants.

The producer uses integer Bareiss plus finite differences. This checker
does neither reconstruction nor polynomial division, and validates every
original row binding in QQ(q) before degree-bounded determinant identities.
"""
import copy,json,pathlib,sys
from fractions import Fraction as F
from frame import build,forms
from uniform import K,q

def polynomial(values,base=q):
    if type(values) is not list or not 1<=len(values)<=200:raise ValueError('bounded polynomial')
    a=[]
    for x in values:
        if type(x) is not str or str(F(x))!=x:raise ValueError('canonical exact coefficient')
        a.append(F(x))
    if len(a)>1 and not a[-1]:raise ValueError('canonical polynomial degree')
    return sum((x*base**i for i,x in enumerate(a)),K.zero),a
def value(p,x):
    y=F(0)
    for a in reversed(p):y=y*x+a
    return y
def determinant(a):
    a=[[F(x) for x in row] for row in a];d=F(1)
    for k in range(len(a)):
        pivot=next((i for i in range(k,len(a)) if a[i][k]),None)
        if pivot is None:return F(0)
        if pivot!=k:a[k],a[pivot]=a[pivot],a[k];d=-d
        v=a[k][k];d*=v
        for i in range(k+1,len(a)):
            c=a[i][k]/v
            for j in range(k+1,len(a)):a[i][j]-=c*a[k][j]
    return d
MODEL=build(q)
FORM_CACHE={str(extra):forms(MODEL,F(extra))[0] for extra in (0,1)}
NAMES=['alphaH','betaH','alphaL','betaL','nu','muL','heavy anti','light anti','heavy standard','fixed']
def check(data,expected_margin):
    if data['extra_margin']!=str(expected_margin) or data['dimension']!=20 or data['multiplicities']!=[2,1,1,1]:raise ValueError('whole domain/dimension/multiplicity')
    if data['untouched_dimensions']!=['q-2','q-3'] or data['untouched_margins']!=[str(17-expected_margin),str(2*q+5-expected_margin)]:raise ValueError('whole untouched spaces')
    if data['off_sector_positions']!=544 or data['original_field_identities']!=MODEL['identities']:raise ValueError('whole original field identities')
    if [t['label'] for t in data['tables']]!=NAMES:raise ValueError('whole obligation catalogue')
    matrices=[[[x]] for x in MODEL['scalars']]+FORM_CACHE[str(expected_margin)]
    positions=points=coefficients=0
    for table,original in zip(data['tables'],matrices):
        n=len(original)
        if len(table['original_cleared_entries'])!=n or len(table['row_domains'])!=n or len(table['minors'])!=n:raise ValueError('complete form size')
        a=[];bounds=[]
        for i,row in enumerate(table['original_cleared_entries']):
            if len(row)!=n:raise ValueError('complete row size')
            domain=table['row_domains'][i];d,dc=polynomial(domain['coefficients']);scale=domain['positive_scale']
            if type(scale) is not int or scale<=0:raise ValueError('positive row multiplier')
            # Exact domain shift positivity, independently using binomial coefficients.
            import math
            shifted=[sum(dc[j]*math.comb(j,k)*4**(j-k) for j in range(k,len(dc))) for k in range(len(dc))]
            if shifted[0]<=0 or any(x<0 for x in shifted):raise ValueError('whole positive denominator domain')
            decoded=[]
            for j,entry in enumerate(row):
                p,co=polynomial(entry)
                if p!=original[i][j]*d*scale:raise ValueError('every original rational entry binding')
                decoded.append(co);positions+=1
            a.append(decoded);bounds.append(max(len(co)-1 for co in decoded))
        if table['row_degree_bounds']!=bounds:raise ValueError('derived entry degree bounds')
        for i,minor in enumerate(table['minors']):
            _,co=polynomial(minor['shifted_coefficients'],q-4)
            bound=sum(max(len(a[r][c])-1 for c in range(i+1)) for r in range(i+1))
            declared=minor['degree_bound']
            # Producer uses full-row degree maxima, a possibly larger valid bound.
            if type(declared) is not int or declared!=sum(bounds[:i+1]) or declared<bound or len(co)-1>declared:raise ValueError('honest complete determinant degree bound')
            if minor['degree']!=len(co)-1 or co[0]<=0 or any(x<0 for x in co):raise ValueError('whole strict shifted sign')
            for v in range(declared+1):
                exact=determinant([[value(a[r][c],4+v) for c in range(i+1)] for r in range(i+1)])
                if exact!=value(co,v):raise ValueError('full degree-bounded Gaussian determinant identity')
                points+=1
            coefficients+=sum(x>0 for x in co)
    return dict(original_QQ_positions=positions,obligations=24,
                full_gaussian_identity_points=points,positive_coefficients=coefficients)
def run(primary):
    results={str(m):check(primary['uniform'+str(m)],m) for m in (0,1)}
    labels=[]
    def reject(label,mutate):
        bad=copy.deepcopy(primary['uniform1']);mutate(bad)
        try:check(bad,1)
        except ValueError:labels.append(label);return
        raise ValueError('semantic damage accepted '+label)
    reject('missing final fixed minor',lambda d:d['tables'][-1]['minors'].pop())
    reject('missing heavy multiplicity',lambda d:d['multiplicities'].__setitem__(0,1))
    reject('wrong full-domain margin',lambda d:d.__setitem__('extra_margin','0'))
    reject('wrong untouched dimension',lambda d:d['untouched_dimensions'].__setitem__(0,'q-3'))
    reject('wrong untouched margin',lambda d:d['untouched_margins'].__setitem__(0,'17'))
    reject('negative shifted constant',lambda d:d['tables'][0]['minors'][0]['shifted_coefficients'].__setitem__(0,'-1'))
    reject('changed entire original entry',lambda d:d['tables'][0]['original_cleared_entries'][0][0].__setitem__(0,'0'))
    reject('negative row multiplier',lambda d:d['tables'][0]['row_domains'][0].__setitem__('positive_scale',-1))
    reject('negative row domain',lambda d:d['tables'][0]['row_domains'][0]['coefficients'].__setitem__(0,'-1000000'))
    reject('false entry degree',lambda d:d['tables'][0]['row_degree_bounds'].__setitem__(0,0))
    reject('false determinant bound',lambda d:d['tables'][-1]['minors'][-1].__setitem__('degree_bound',0))
    reject('noncanonical exact coefficient',lambda d:d['tables'][0]['minors'][0]['shifted_coefficients'].__setitem__(0,'01'))
    reject('wrong original dimension',lambda d:d.__setitem__('dimension',19))
    reject('missing original intersection identity',lambda d:d['original_field_identities'].pop())
    return dict(valid_complete_certificates=results,rejected_semantic_damages=labels,
        float_inputs=False,generator_determinants_or_interpolation_used=False)
if __name__=='__main__':
    P=pathlib.Path(__file__).resolve().parent
    record=run(json.loads((P/'PRIMARY.json').read_text()))
    (P/'CONTROLS.json').write_text(json.dumps(record,sort_keys=True,indent=2)+'\n')
    print(json.dumps(record,sort_keys=True))
