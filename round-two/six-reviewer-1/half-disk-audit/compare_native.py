"""Late DATA-ONLY comparison; optional corroboration, not a primary premise.

Argument is the complete freshly regenerated native JSON certificate. This
imports only the unchanged sealed reviewer implementation, never author code.
"""
from pathlib import Path
from fractions import Fraction as Q
from exact import require,power,encode
import check,literal,json,sys

def compare(native):
    own=check.build()['original'];notes=[]
    target=sorted(native['polar_cells'],key=lambda c:(Q(c['a'][0]),Q(c['T'][0])))
    fresh=sorted(own['polar'],key=lambda c:(Q(c['a'][0]),Q(c['T'][0])))
    require(len(target)==len(fresh)==14,'all polar cells')
    for n,f in zip(target,fresh):
        for key in ('a','T','d','k1','k2','coefficients','integral'):
            require(n[key]==f[key],'whole polar physical field '+key)
        require(n['P']==f['phase_floor'],'complete phase floor')
        notes.append({'a':f['a'],'T':f['T'],'coefficients':f['coefficients'],
                      'integral':f['integral'],'all_eight_fields_equal':True})
    require(len(native['origin_terms'])==len(own['origin']['seven_terms'])==7,'all centered orders')
    for n,f in zip(native['origin_terms'],own['origin']['seven_terms']):
        require(n['l']==f['order'] and n['c']==f['constant'] and
                n['coefficients']==f['coefficients'] and n['integral']==f['integral'],
                'whole centered origin polynomial and integral')
    require(native['origin_sum']==own['origin']['remainder'],'entire seven-order sum')
    require(native['monotonicity']==own['origin']['derivative_coefficients'],'whole monotonicity polynomial')
    for n,(identifier,a,b,expected) in zip(native['scalar_integrals'],[
            ('small-a',Q(2,5),Q(21,25),own['scalar_small_a']),
            ('radius-mass',Q(1,2),Q(117,160),own['scalar_mass_floor'])]):
        require(n['id']==identifier and n['integral']==expected and
                n['coefficients']==encode(power([a,b],8)),'entire scalar integral polynomial')
    fresh_newton=literal.generic_newton()
    require(len(native['newton'])==len(fresh_newton)==8,'all generic Newton identities')
    for n,f in zip(native['newton'],fresh_newton):
        degree=f['degree']
        lhs=[ [list(exp),str(Q(coefficient,degree))] for exp,coefficient in f['lhs']]
        require(n['l']==degree and n['e']==lhs and n['complete_residual']==[],
                'whole generic Newton elementary map and zero residual')
        ps=[[list(tuple(degree if j==i else 0 for j in range(8))),'1'] for i in range(8)]
        require(sorted(n['power_sum'])==sorted(ps),'whole eight-variable power-sum map')
    gaussian=[]
    require(len(native['gaussian_controls'])==4,'four complete author-defined late controls')
    for n in native['gaussian_controls']:
        a=Q(n['a']);q=[tuple(Q(z) for z in pair) for pair in n['q']]
        f=encode(literal.one_control(a,q))
        for nk,fk in [('all_nine_origin_coefficients','origin_coefficients'),
                      ('all_nine_polar_coefficients','polar_coefficients'),('O','O'),('J','J')]:
            require(n[nk]==f[fk],'all nine Gaussian coefficients/integrals '+nk)
        radii=[Q(x) for x in n['r']]
        require(sum(radii)==8 and len(radii)==8,'late first-power and multiplicities')
        norm=lambda z:z[0]**2+z[1]**2
        require(all(norm(z)==r*r for z,r in zip(q,radii)),'all exact Gaussian norms')
        require(sum(norm(z) for z in q)>8,'late controls outside quadratic sublevel')
        require(all((1-a*a)*norm(z)+2*a*z[0]>=1 for z in q),'all critical-disk predicates')
        require(norm(tuple(Q(z) for z in f['J']))>1,'late polar predicate')
        require(norm(tuple(Q(z) for z in f['O']))>Q(129,128)**2,'late origin predicate')
        require(n['outside_second_moment'] is True and
                n['original_disk_feasibility_asserted'] is False,'no original witness assertion')
        gaussian.append(f)
    return {'agent':'six-reviewer-1','role':'independent mathematical reviewer',
            'late_data_only_native_corroboration_NOT_primary':True,
            'all14_whole_polar_fields':notes,'all7_origin_fields':own['origin']['seven_terms'],
            'all8_generic_Newton_maps':fresh_newton,'all4_late_Gaussian_full_polynomials':gaussian,
            'all2_scalar_full_polynomials_compared':True,'no_author_code_imported':True}

if __name__=='__main__':
    result=compare(json.loads(Path(sys.argv[1]).read_text()))
    print(json.dumps(result,sort_keys=True,separators=(',',':')))
