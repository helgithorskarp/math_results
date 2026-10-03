"""Damaged-input, signed-root and exact old-core controls."""
from pathlib import Path
from fractions import Fraction as Q
from copy import deepcopy
import json,signal,argparse,hashlib
import check,audit
from coverage import validate,census
from exact import derive,require,load
from frame import make,CORE,CONTACTS
from polynomials import dot
from branches import branch
HERE=Path(__file__).resolve().parent

def rejects(fn,label):
    try:fn()
    except (ValueError,TypeError):return label
    raise ValueError('damaged control accepted: '+label)

def run(s,f):
    bad=[]
    for name,edit in [
        ('missing closed lower endpoint',lambda x:x['t_interval'].__setitem__(0,'561/1000')),
        ('open endpoints',lambda x:x.__setitem__('intervals_closed',False)),
        ('discarded upper inner seam',lambda x:x['z_interval'].__setitem__(1,'1399/1000')),
        ('missing original contact',lambda x:x['original_contacts'].pop()),
        ('extra5-12 premise',lambda x:x['original_contacts'].append([5,12])),
        ('extra1-7 equality premise',lambda x:x['original_contacts'].append([1,7])),
        ('point13 premise',lambda x:x['required_labels'].append(13)),
        ('hidden face assumption',lambda x:x['additional_hypotheses'].append('actual_face')),
        ('restricted additions',lambda x:x.__setitem__('other_points','chosen_centers')),
        ('unsigned root',lambda x:x.__setitem__('root','w*w=R')),
        ('different sheet',lambda x:x.__setitem__('sheet',[1,1])),
        ('weak regularity',lambda x:x.__setitem__('regularity','2G-a^4 C^2>=0')),
        ('wrong cap rhs',lambda x:x['cap_planes'][0].__setitem__('rhs',8)),
        ('missing pair exclusion',lambda x:x['incompatible_pairs'].pop()),
        ('deleted alternate closed cell',lambda x:x['alternate_bound2_closed_cover'].pop()),
        ('claimed global bound',lambda x:x.__setitem__('global_bound_claimed',True)),
        ('wrong clique count',lambda x:x['equilateral_short_triples'].append([1,7,12]))]:
        x=deepcopy(s);edit(x);bad.append(rejects(lambda:validate(x),name))
        rejects(lambda:audit.run(x,f),'alternate scope '+name)
    x=deepcopy(s);x['residual_triples'].pop();bad.append(rejects(lambda:census(x),'missing residual branch'));rejects(lambda:census(x,reverse=True),'alternate missing branch')
    x=deepcopy(s);x['residual_triples'].append(x['residual_triples'][0]);bad.append(rejects(lambda:census(x),'duplicate residual branch'));rejects(lambda:census(x,reverse=True),'alternate duplicate branch')
    polynomial_damage=[]
    for name in ['bound0','delta','critical_norm99','bound2_square_factor']:
        x=deepcopy(f);x['rows'][name][0][3]=str(int(x['rows'][name][0][3])+1)
        polynomial_damage.append(rejects(lambda:derive(x,s),'whole primary damaged '+name))
        if name=='bound2_square_factor':rejects(lambda:audit.sign_audit(audit.literals(x),s),'alternate damaged square factor')
        else:rejects(lambda:audit.identity_audit(audit.literals(x),s),'alternate damaged '+name)
    x=deepcopy(f);x['rows']['bound1'].append(x['rows']['bound1'][0]);polynomial_damage.append(rejects(lambda:load(x),'duplicate monomial'));rejects(lambda:audit.literals(x),'alternate duplicate monomial')
    # A+B*w positivity cases require the sign of w; squaring alone is insufficient.
    radical=[]
    for mode,A,B,w in [('B-and-H',Q(-1),Q(1),Q(2)),('A-and-B',Q(1),Q(2),Q(3)),('A-and-negative-H',Q(5),Q(-2),Q(2))]:
        H=B*B*w*w-A*A;guard=w>0 and (B>0 and H>0 if mode=='B-and-H' else A>0 and B>0 if mode=='A-and-B' else A>0 and H<0)
        require(guard and A+B*w>0,'valid signed radical control');radical.append(mode)
    require(Q(-1)+Q(1)*Q(-2)<0,'negative root defeats unsigned square inference')
    zero=__import__('polynomials').P.cv(0)
    endpoint_rejections=[rejects(lambda:require(all(v>0 for row in check.bernstein(zero,(Q(0),Q(1),Q(0),Q(1))) for v in row),'zero sign'),'primary zero sign')]
    endpoint_rejections.append(rejects(lambda:audit.taylor({(0,0):0},('0','1','0','1'),1),'alternate zero sign'))
    p=__import__('polynomials').P.var(0)
    endpoint_rejections.append(rejects(lambda:require(all(v>0 for row in check.bernstein(p,(Q(0),Q(1),Q(0),Q(1))) for v in row),'endpoint zero'),'primary closed endpoint zero'))
    endpoint_rejections.append(rejects(lambda:audit.taylor({(1,0):1},('0','1','0','1'),1),'alternate closed endpoint zero'))
    # Known rational family is a control only, credited to10012/9984.
    t,z,w=Q(29,50),Q(5400,3973),Q(454484658996081,225033203125000);m=make(t,z,w);O=m['Omega'];Y=m['points']
    require(w*w==m['root_squared'] and w>0 and O>0,'old exact signed core')
    require(all(dot(Y[i],Y[i],t)==O*O for i in CORE),'all12 old core units')
    pairs=[(i,j) for n,i in enumerate(CORE) for j in CORE[n+1:]]
    require(all(dot(Y[i],Y[j],t)<=t*O*O for i,j in pairs),'all66 old core products')
    require(all(dot(Y[i],Y[j],t)==t*O*O for i,j in CONTACTS),'all20 original contacts')
    s0=branch(t,z,w,(1,2,4));require(all(v==0 for n,v in s0['equalities']) and all(v>0 for n,v in s0['strict_positive']) and all(v>=0 for n,v in s0['closed_domain']),'exact branch base/rank control')
    require(s0['nonnegative'][-1][1]<0,'short regular vertex correctly fails long norm predicate')
    require(audit.Pair(3,2,0).__mul__(audit.Pair(4,1,0)).a==12,'root-zero arithmetic retained without inverse')
    return {'actual_agent':'six-tammes-2','role':'researcher','status':'ALL_SCOPE_POLYNOMIAL_AND_ROOT_CONTROLS_PASSED','scope_and_census_damages_rejected_by_both':bad,'polynomial_damages_rejected_by_both':polynomial_damage,'valid_signed_radical_cases':radical,'negative_root_counterexample_retained':True,'zero_sign_rejections':endpoint_rejections,'old_exact_core_control':{'t':str(t),'z':str(z),'w':str(w),'units':12,'packing_pairs':66,'original_contacts':20,'credit':'prior10012 and9984; not a new construction'},'regular_short_branch_rejected_by_norm':True,'root_zero_never_inverted':True,'independent_review':'pending'}

if __name__=='__main__':
    signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('25s fixed controls guard')));signal.alarm(25)
    parser=argparse.ArgumentParser();parser.add_argument('--emit');args=parser.parse_args()
    out=run(json.loads((HERE/'SYSTEM.json').read_text()),json.loads((HERE/'FACTORS.json').read_text()));data=(json.dumps(out,separators=(',',':'))+'\n').encode()
    if args.emit:Path(args.emit).write_bytes(data)
    else:require(out==json.loads((HERE/'CONTROLS.json').read_text()),'whole control output equality')
    print(json.dumps({'status':out['status'],'scope_and_census_damage_count':len(out['scope_and_census_damages_rejected_by_both']),'polynomial_damage_count':len(out['polynomial_damages_rejected_by_both']),'whole_controls_sha256':hashlib.sha256(data).hexdigest()},indent=2))
