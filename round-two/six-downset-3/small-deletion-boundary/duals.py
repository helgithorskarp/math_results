"""Independently replay compact original rank-one/two PSD separators.

This checker uses only the standard library and literal.py. No search,
solver, matrix elimination, imported author engine, or floating point.
"""
from pathlib import Path
import json,sys,hashlib
from fractions import Fraction as F
from literal import require,core_data,domain,quadratic,action

PATH=Path(__file__).resolve().with_name('DUALS.json')


def negative_kappa(q):
    X,N,s,C0,delta,R,U0=core_data(q,3,scan=True)
    z=[F(1)-bool(A&2)-bool(A&4)+int(A.bit_count()==3 or A.bit_count()==2 and A&7==A) for A in X[1:]]
    require(not any(action(C0,z)) and not any(action(R,z)), 'lower separator kernel actions')
    alpha=F(q*(q+1),2)+F(3*(q+1),3*q+5)
    require(quadratic(z,delta)==alpha>0,'exact negative-kappa lower separator')
    return {'q':q,'N':N,'alpha':str(alpha),'C0_z':'0','R_z':'0'}


def check(q,fixture):
    require(q in (5,6,7),'three explicit rank-two upper duals only')
    X,N,s,C0,delta,R,U0=core_data(q,3,scan=True)
    require(X==domain(q,3),'literal full scan / combinations order')
    vs=fixture['vectors'];weight=F(fixture['weight'])
    require(len(vs)==2 and all(len(v)==N-1 and all(type(x) is int for x in v) for v in vs), 'literal integer vector dimensions')
    require(weight>0,'positive rank-two PSD weight')
    pairs=[{'a':quadratic(w,U0),'d':quadratic(w,delta),'r':quadratic(w,R)} for w in vs]
    combined={key:pairs[0][key]+weight*pairs[1][key] for key in ('a','d','r')}
    require(combined['r']==0 and combined['a']<0 and combined['d']>=0,'all-real-t/all-nonnegative-kappa dual signs')
    require([{key:str(value) for key,value in row.items()} for row in pairs]==fixture['pairings'],'all original pairings differ from frozen scalars')
    require({key:str(value) for key,value in combined.items()}==fixture['combined'],'combined frozen scalars')
    return {'q':q,'N':N,'weight':str(weight),'pairings':fixture['pairings'],'combined':fixture['combined'],
            'lower_negative_kappa':negative_kappa(q)}


def all_checks(fixtures=None):
    fixtures=json.loads(PATH.read_text()) if fixtures is None else fixtures
    require(set(fixtures)=={'5','6','7'},'complete exceptional dual census')
    X,N,s,C0,delta,R,U0=core_data(4,3,scan=True)
    ones=[F(1)]*(N-1)
    alpha=F(4*5,2)+F(3*5,17)
    coefficient=alpha-F(6,17)
    require(quadratic(ones,U0)==-1 and quadratic(ones,delta)==coefficient>0 and quadratic(ones,R)==0,
            'q4 original empty-cap rank-one separator')
    return {'q4':{'q':4,'N':N,'zero_upper':'-1','delta':str(coefficient),'repair':'0',
                   'lower_negative_kappa':negative_kappa(4)},
            'rank_two':[check(q,fixtures[str(q)]) for q in (5,6,7)],
            'fixture_sha256':hashlib.sha256(PATH.read_bytes()).hexdigest(),
            'scope':'all real kappa,t infeasible only in the specified affine-table/four-edge ansatz'}


if __name__=='__main__':print(json.dumps(all_checks(),sort_keys=True,indent=2))
