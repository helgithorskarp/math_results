"""Scope and algebra controls for losslessness, not exclusion certificates."""
from pathlib import Path
from copy import deepcopy
from fractions import Fraction as Q
import argparse,json,signal
from schema import layout,require
from polynomials import P,dot
from model import make,stereographic
from check import pins

HERE=Path(__file__).resolve().parent
def run():
    source=pins();s=json.loads((HERE/'SYSTEM.json').read_text());d=json.loads((HERE/'INPUT.json').read_text());damages=[]
    def reject(name,change):
        a,b=deepcopy(s),deepcopy(d);change(a,b)
        try:layout(a,b)
        except (ValueError,KeyError,TypeError):damages.append({'name':name,'rejected':True})
        else:raise ValueError('accepted unsound scope damage '+name)
    def setkey(k,v):return lambda a,b:a.__setitem__(k,v)
    reject('silently-fix-point13',setkey('all_three_actual_additions_arbitrary',False))
    reject('require-added-proximity',setkey('initial_added_point_proximity_required',True))
    reject('quotient-added-points-without-proof',setkey('symmetry_quotient_applied',True))
    reject('identify-two-added-variables',setkey('variables',['t','z','w','u0','v0','u0','v1','u2','v2']))
    reject('wrong-coefficient-ring',setkey('coefficient_ring','Q[t,z,w]'))
    reject('wrong-frame-branch',setkey('sole_frame_branch',[1,1]))
    reject('lose-positive-radical-sign',setkey('strict_radical_branch','w>=0'))
    reject('incorrect-radical-clearing',setkey('radical_equalities',['w^2=G']))
    reject('omit-strict-regularization',setkey('strict_core_regularization_predicate','G>=0'))
    reject('incorrect-chart-clearing',setkey('core_chart_predicate','(1+t)^2*z^2<=1'))
    reject('discard-critical-strip',setkey('t_closed',['14/25','5926/10000']))
    reject('too-small-added-chart-box',setkey('added_chart_coordinates_closed',['-3','3']))
    reject('restrict-core-z',setkey('z_closed',['0','5/2']))
    reject('restrict-positive-root',setkey('w_closed',['0','1']))
    reject('make-local-gate-a-model-constraint',setkey('local_gate9866_is_optional_future_stopping_lemma_and_not_model_constraint',False))
    reject('replace-exact-incumbent-by-endpoint',setkey('strict_improvement_additional_predicate','t<0.59260590292507377809642492233275'))
    reject('omit-integral-strict-improvement',setkey('strict_improvement_integral_polynomial','t<0.5926'))
    reject('incorrect-exact-root',setkey('root_quintic_for_controls',[-1,-3,2,6,-1,12]))
    reject('incorrect-incumbent-chart',setkey('exact_z0_coefficients',['0']*5))
    reject('add-core-label13',setkey('original_core_labels',s['original_core_labels']+[13]))
    reject('omit-contact',setkey('original_twenty_contacts',s['original_twenty_contacts'][:-1]))
    reject('omit-core-six-eight-comparison',setkey('core_packing_pairs',[p for p in s['core_packing_pairs'] if p!=[6,8]]))
    reject('omit-added-anchor-comparison',setkey('arbitrary_addition_core_pairs',[p for p in s['arbitrary_addition_core_pairs'] if p!=[0,1]]))
    reject('omit-added-mutual-comparison',setkey('arbitrary_addition_mutual_pairs',[[0,1],[1,2]]))
    reject('duplicate-core-comparison',setkey('core_packing_pairs',s['core_packing_pairs'][:-1]+[s['core_packing_pairs'][0]]))
    reject('truncate-root-isolator',lambda a,b:b.__setitem__('root_bracket',[b['root_bracket'][0]]))
    reject('truncate-exact-vector',lambda a,b:b['vectors'][0].pop())
    good=[]
    for name,change in (
        ('harmless-metadata',lambda a,b:(a.__setitem__('comment','not a premise'),b.__setitem__('candidate_gram_permutations',None))),
        ('logical-pair-ordering',lambda a,b:[a[k].reverse() for k in ('original_twenty_contacts','core_packing_pairs','arbitrary_addition_core_pairs','arbitrary_addition_mutual_pairs')]),
        ('JSON-key-ordering',lambda a,b:None)):
        a,b=deepcopy(s),deepcopy(d);change(a,b);layout(a,b);good.append({'name':name,'accepted':True})
    algebra=[]
    for name,call in (('float-polynomial-coefficient',lambda:P({(0,0,0):0.1})),('rational-polynomial-coefficient',lambda:P.cv(Q(1,2))),('invalid-local-slot',lambda:P.var(3)),('negative-exponent',lambda:P.var(0)**-1),('root-dependent-modulus',lambda:P.var(2).reduced(P.var(2)))):
        try:call()
        except (ValueError,TypeError):algebra.append({'name':name,'rejected':True})
        else:raise ValueError('accepted inexact/invalid polynomial input '+name)
    t,z,w=(P.var(i) for i in range(3));m=make(t,z,w);Y=m['points'];R=m['root_squared'];bad=list(Y[7]);bad[0]+=1
    require(bool((dot(bad,bad,t)-m['Omega']**2).reduced(R).c),'one corrupted frame coordinate detected by generic unit identity')
    u,v=P.var(1),P.var(2);T,A,_=stereographic(t,u,v);bad=list(T);bad[1]+=1
    require(bool((dot(bad,bad,t)-A*A).c),'one corrupted stereographic coordinate detected generically')
    # Finite antipode and both mixed-sign local slots are present, including
    # the origin where an inverse dividing by u or v would lose a valid point.
    for uv in ((Q(0),Q(0)),(Q(1,3),Q(-2,5)),(Q(-1,4),Q(1,2))):
        tt=Q(14,25);T,A,Rc=stereographic(tt,*uv);x=[h/A for h in T];an=dot(x,[Q(1),Q(0),Q(0)],tt)
        require(dot(x,x,tt)==1 and (1-an)>0 and (x[1]/(1-an),x[2]/(1-an))==uv,'finite chart boundary/inverse control')
    return {'format':'bounded-polynomial-model-controls-v1','actual_agent':'six-tammes-2','role':'researcher','source_pins':source,'scope_damages_actually_rejected':len(damages),'valid_scope_controls_actually_accepted':len(good),'invalid_polynomial_inputs_actually_rejected':len(algebra),'corrupted_coordinate_identities_actually_detected':2,'finite_chart_controls_actually_checked':3,'damages':damages,'valid_controls':good,'algebra_controls':algebra}

def main():
    signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('50-second controls guard')));signal.alarm(50)
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path);args=p.parse_args();out=run();raw=json.dumps(out,sort_keys=True,indent=2)+'\n'
    if args.output:args.output.write_text(raw)
    print(raw,end='')
if __name__=='__main__':main()
