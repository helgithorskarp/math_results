"""LATE data-only comparison. Import only the already sealed owned checker.

Arguments: own EXPECTED.json; producer expected.json. No producer code import.
The author's new source was first intentionally inspected after both seals.
"""
import importlib.util
import json
from pathlib import Path
import sys

spec=importlib.util.spec_from_file_location('owned_portable',Path(__file__).with_name('portable.py'))
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
own=json.loads(Path(sys.argv[1]).read_text());native=json.loads(Path(sys.argv[2]).read_text())
p.check(own);checked=[];entries=0


def decode(row,rename=None):
    global entries
    if type(row)!=dict or set(row)!={'variables','whole_QQ_Laurent_terms'}:raise ValueError('native polynomial schema')
    names=row['variables'];out={};seen=set()
    if type(names)!=list or len(names)!=len(set(names)):raise ValueError('native variables')
    aliases={'v'+str(i):'a'+str(i+1)for i in range(4)}| (rename or {})
    names=[aliases.get(n,n)for n in names]
    if any(n not in p.V for n in names):raise ValueError('native domain')
    for item in row['whole_QQ_Laurent_terms']:
        if type(item)!=list or len(item)!=2:raise ValueError('native term')
        ex,c=item
        if type(ex)!=list or len(ex)!=len(names) or any(type(i)!=int for i in ex):raise ValueError('native exponents')
        if type(c)!=str or str(p.F(c))!=c or not p.F(c):raise ValueError('native exact rational')
        ex=tuple(ex)
        if ex in seen:raise ValueError('duplicate native monomial')
        seen.add(ex);e=list(p.ZERO)
        for n,i in zip(names,ex):e[p.V.index(n)]=i
        out[tuple(e)]=p.F(c)
    entries+=len(out)
    return out


def compare(name,nat,identity,factor=1,rename=None):
    row=own['identities'][identity]
    p.require(p.mul(p.mul(decode(nat,rename),p.number(factor)),p.decode(row['clearing_denominator'])),
              p.decode(row['left']),name);checked.append(name)


def direct(name,nat,expected,rename=None):
    p.require(decode(nat,rename),expected,name);checked.append(name)


g=native['pencil'];b=native['fiber_interval_bridges'];z,S,T,U,A,d=map(p.var,['z','S','T','U','A','d'])
q=p.sub(p.sub(p.power(z,2),p.mul(S,z)),p.monodiv(T,S));R=p.sub(p.neg(p.power(T,2)),p.mul(p.power(S,2),U))
direct('complete q',g['quadratic'],q)
for key,identity in [('quartic','pencil factor decomposition'),('quotient_decomposition','pencil factor decomposition'),
                     ('third_power','pencil odd moment 3'),('fifth_power','pencil odd moment 5'),
                     ('Hurwitz_invariant','pencil invariant R')]:compare(key,g[key],identity)
direct('whole six-pair product',g['full_Hurwitz_pair_product'],p.decode(own['identities']['whole Orlando six-pair product']['left']))
direct('Abar',g['normalized_Abar'],p.sub(p.mul(p.number(p.F(1,2)),p.power(S,2)),p.number(p.F(1,4))))
direct('whole odd cross term',g['whole_odd_cross_part'],p.monodiv(p.mul(p.number(2),p.mul(R,z)),S))
compare('J',g['J'],'original octic coefficient 1',8)
if len(g['all_nine_normalized_octic_coefficients_ascending'])!=9:raise ValueError('all nine native coefficients')
for i,v in enumerate(g['all_nine_normalized_octic_coefficients_ascending']):compare('octic '+str(i),v,'original octic coefficient '+str(i))
for key,identity in [('critical_cubic_N','critical cubic zero'),('critical_cubic_derivative','three-branch cubic derivative'),
                     ('N_at_zero','critical cubic zero'),('N_at_quarter_sum','critical cubic quarter'),
                     ('N_at_half_sum','critical cubic half'),('direction_discriminant','direction discriminant')]:
    if key=='critical_cubic_N':direct(key,b[key],p.decode(own['polynomials']['critical_cubic']))
    else:compare(key,b[key],identity)
N=p.decode(own['polynomials']['critical_cubic'])
direct('H numerator',b['H_numerator'],p.mul(z,p.power(q,2)))
direct('H denominator',b['H_denominator'],p.sub(S,p.mul(p.number(2),z)))
direct('whole H derivative numerator',b['H_derivative_numerator'],p.mul(q,N))
direct('entire double-root equation',b['entire_double_root_equation'],
       p.sub(p.mul(R,p.sub(S,p.mul(p.number(2),z))),p.mul(p.number(2),p.mul(p.power(S,2),p.mul(z,p.power(q,2))))))
for key,identity in [('cube_max_gap','triple upper gap'),('cube_min_gap','triple Jensen gap'),
                     ('support3_cube_gap','triple lower-branch boundary gap'),
                     ('multiplier','multiplier factor'),('lower_Hessian','lower Hessian'),('upper_Hessian','upper Hessian')]:
    rename={'b':'s'}if key in ('cube_max_gap','cube_min_gap','support3_cube_gap')else {'t':'a','z':'x'}
    compare(key,native['universal_quartet_maps'][key],identity,rename=rename)
direct('regular zero-opening derivative',native['universal_quartet_maps']['regular_zero_opening_fifth_derivative'],
       p.mul(p.number(5),p.mul(p.power(p.var('a'),2),p.power(p.var('b'),2))),rename={'t':'a','z':'x'})
print(json.dumps({'complete_shared_polynomial_fields':len(checked),'all_native_nonzero_coefficient_entries':entries,
                  'fields':checked,'late_data_only_comparison':True,'producer_code_imported':False},sort_keys=True))
