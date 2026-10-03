"""LATE supplemental comparison only; never import the producer program.

The independent nine-file primary seal predates this script. Native tuples
are credited producer input data, not independent discovery. Complete maps
are compared, not hashes alone or selected nonzero coefficients.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations
from math import comb
import json,sys,hashlib
import core
import arithmetic as A
def compare(native):
    d=core.build();count=0
    def equal(a,b,name):
        nonlocal count
        core.need(a==b,name);count+=1
    for ours,theirs in [('phase','mean'),('balanced','modulus'),('variance','variance')]:
        r=d['polar']['streams'][ours];s=native['polar_certificates'][theirs]
        equal(r['coefficients'],s['whole_polynomial'],'all scalar polar coefficients '+ours)
        equal(r['lower_coefficient'],s['complete_tail_lower'],'entire polar absolute-tail budget '+ours)
    equal(d['polar']['whole_B'],native['whole_polar']['whole_balanced_integral'],'whole balanced integral')
    equal(d['polar']['whole_T'],native['whole_polar']['whole_tail'],'whole polar higher tail')
    for r,s in zip(d['faces'],native['whole_faces']):
        equal(r['m'],s['m'],'all8 face indices')
        equal(r['whole_coefficients'],s['whole_residual'],'all8 whole residual maps')
        equal(r['positive_lower'],s['full_tail_lower'],'all8 complete face tails')
        equal(r['dm'],s['defect_coefficient'],'all8 defects')
    equal(len(native['whole_faces']),8,'entire face census')
    def coeffs(p):
        q={(i,j):Q(v)for i,j,v in p};return list(map(str,A.uni(q)))
    for stage,key in [(0,'first_whole_Newton_stream'),(1,'second_whole_Newton_stream')]:
        for values in native[key].values():core.need(all(type(v)in [str,int]for v in values),'native polynomial rational token types')
        equal({k:coeffs(p)for k,p in d['Newton'][stage]['polynomials'].items()},{k:list(map(lambda v:str(Q(v)),p))for k,p in native[key].items()},'whole all8 Newton orders')
    s=native['complete_constants'];r=d['budgets']['normalization']
    for ours,theirs in [('beta_prime','beta_prime'),('S_prime','phase_prime'),('C0','global_cost'),('K1','first_cost'),('K2','second_cost'),('c1','first_gap'),('c2','second_gap'),('Av','Av'),('Ar','Ar')]:equal(r[ours],s[theirs],'entire receiving constant '+theirs)
    r=d['budgets']['centered']
    for ours,theirs in [('A','Aj'),('higher_B','Bj'),('Cd','Cd'),('Bd','Bd'),('Nc','Nc'),('Be','Be'),('beta','mean_absorption'),('kappa','kappa')]:equal(r[ours],s[theirs],'entire centered constant '+theirs)
    equal(d['cube_square']['whole_original_square'],native['whole_mean_square']['lhs'],'whole original square')
    equal(d['cube_square']['whole_completed_square'],native['whole_mean_square']['expanded_rhs'],'whole completed square')
    for row,n in zip(d['cube_square']['all7_coefficients'],native['whole_cube_field']):
        equal(row['j'],n['j'],'all7 cube indices')
        for key,nkey in [('full_individual','full_individual_coefficient'),('full_pair','full_pair_coefficient')]:
            vals=[Q(0),Q(0)]
            for ph,tokens,c in row[key]:vals[ph]+=Q(c)
            equal(list(map(str,vals)),n[nkey],'whole cube field '+key)
    equal(len(native['whole_cube_field']),7,'all7 cube coefficient census')
    for row,n in zip(d['definition_level']['all7_twolevel_controls'],native['all_seven_real_skew_controls']):equal(row['cubic_ratio_squared'],n['squared_skew_ratio'],'all7 skew ratios')
    equal(len(native['all_seven_real_skew_controls']),7,'all7 skew census')
    # Reconstruct every author's literal tuple independently from its credited
    # Gaussian input data, including ALL8 centered Newton orders.
    g=A.ga;scale=A.gsc;times=A.gmul;total=A.gsum
    def prod(xs):
        out=g(1)
        for x in xs:out=times(out,x)
        return out
    def el(xs,k):return total(prod(c)for c in combinations(xs,k))
    def polynomial(xs,a):
        return [scale(el(xs,k),(-a)**k)for k in range(len(xs)+1)]
    def integral(p,shift,factor):return total(scale(c,Q(factor,k+shift+1))for k,c in enumerate(p))
    enc=lambda x:list(map(str,x))
    for n in native['whole_literal_controls']:
        qs=[g(Q(x),Q(y))for x,y in n['whole_q']];a=Q(n['a'])
        p=polynomial(qs,a);equal(list(map(enc,p)),n['whole_origin_product_coefficients'],'whole credited tuple product')
        equal(enc(integral(p,0,9)),n['origin'],'whole credited tuple origin')
        mean=scale(total(qs),Q(1,8));xs=[A.gadd(z,scale(mean,-1))for z in qs]
        equal(list(map(enc,xs)),n['whole_centered_tuple'],'whole credited centered tuple')
        equal([enc(el(xs,k))for k in range(9)],n['all_centered_elementary_coefficients'],'all9 credited centered elementary')
        equal([enc(total(A.gp(z,k)for z in xs))for k in range(9)],n['all_centered_traces'],'all9 credited centered traces')
        grads=[];hess=[]
        for i in range(8):
            rest=[z for j,z in enumerate(qs)if j!=i];grads.append(enc(scale(integral(polynomial(rest,a),1,9),-a)))
            hr=[]
            for j in range(8):
                v=g(0)
                if i!=j:v=scale(integral(polynomial([z for k,z in enumerate(qs)if k not in [i,j]],a),2,9),a*a)
                hr.append(enc(v))
            hess.append(hr)
        equal(grads,n['all_eight_gradients'],'all8 credited tuple gradients')
        equal(hess,n['whole_ordered_hessian'],'all64 credited tuple Hessians')
    equal(len(native['whole_literal_controls']),3,'entire native tuple census')
    return {'whole_comparisons':count,'all99_polar_coefficients':True,'all8_complete_face_residuals':True,'both_whole_Newton_streams':True,'all7_cube_pairs':True,'all7_skew_ratios':True,'all3_credited_native_tuples_whole_maps':True,'producer_program_imported':False,'primary_record_sha256':core.digest(d)}
if __name__=='__main__':
    n=core.load(Path(sys.argv[1]));r=compare(n)
    bad=json.loads(json.dumps(n));bad['second_whole_Newton_stream']['7'][-1]='0'
    try:compare(bad)
    except ValueError:r['native_last_Newton_damage_rejected']=True
    else:raise ValueError('accepted whole native damage')
    r.update(status='PASS',native_record_sha256=hashlib.sha256(json.dumps(n,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest())
    print(json.dumps(r,sort_keys=True))
