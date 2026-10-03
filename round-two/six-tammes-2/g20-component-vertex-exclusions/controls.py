"""Actual damaged inputs, boundary/root guards and an exact credited core."""
from pathlib import Path
from fractions import Fraction as Q
from copy import deepcopy
import argparse,hashlib,json,signal
from scope import validate,require,CUTS,CORE,CONTACTS
from frame import make
from polynomials import P,dot
from check import produce as primary,bernstein
from audit import produce as alternate,taylor
HERE=Path(__file__).resolve().parent
def rejected(call,name):
    try:call()
    except (ValueError,TypeError):return name
    raise ValueError('damaged actual input accepted: '+name)
def signed(A,B,R,w):
    require(w>0 and w*w==R,'positive actual radical branch')
    require(B>0 and (B*B*R>A*A or A>0),'actual strict signed-radical guard')
    require(A+B*w>0,'actual positive excess')
    return True
def exact_core():
    t,z,w=Q(29,50),Q(5400,3973),Q(454484658996081,225033203125000)
    m=make(t,z,w);O=m['Omega'];p={i:[v/O for v in m['points'][i]] for i in CORE}
    require(w>0 and w*w==m['root_squared'] and 2*m['G']>m['a']**4*m['C']**2,'credited core positive root/regularity')
    units=[dot(p[i],p[i],t)-1 for i in CORE]
    contacts=[dot(p[i],p[j],t)-t for i,j in CONTACTS]
    packs=[t-dot(p[i],p[j],t) for q,i in enumerate(CORE) for j in CORE[q+1:]]
    require(all(v==0 for v in units+contacts) and all(v>=0 for v in packs),'all12 units/20contacts/66packing of credited core')
    a,b,c=1+t,1-t,1+2*t;L=7*t*t+2*t-1;vertices=[]
    capnormals={98:(-8,12,-5),99:(-5,-14,20)}
    for triple,central,left,right,label,rhs in [((0,6,7),0,6,7,99,15),((1,4,12),1,4,12,99,15),((2,8,10),2,8,10,98,9),((5,7,9),5,7,9,10,t),((6,9,11),11,6,9,98,9)]:
        x=[t*(a*a*(p[left][v]+p[right][v])-L*p[central][v])/(b*b*c) for v in range(3)]
        require(all(dot(x,p[i],t)==t for i in triple),'exact three active equations')
        norm=dot(x,x,t);require(norm==t*t*(5*t+3)/(b*c) and norm>1,'exact common long-vertex norm')
        excess=dot(x,p[label] if label==10 else capnormals[label],t)-rhs
        require(excess>0,'exact excluded comparison at credited core')
        vertices.append({'triple':list(triple),'vertex_coefficients':list(map(str,x)),'norm_squared':str(norm),'violated_comparison':label,'strict_excess':str(excess)})
    require(dot(p[5],p[12],t)==t,'credited5-12 equality is CONTROL ONLY')
    return {'credited_core':[str(t),str(z),str(w)],'all12_unit_zero_residuals':list(map(str,units)),'all20_contact_zero_residuals':list(map(str,contacts)),
            'all66_packing_margins':list(map(str,packs)),'all5_exact_excluded_vertices':vertices,'new_construction':False,'extra5_12_is_not_a_hypothesis':True}
def produce(s,d,pbytes):
    validate(s,pbytes);scope_controls=[]
    changes=[('t-closed-endpoint','t_interval',['561/1000','593/1000']),('z-closed-endpoint','z_interval',['1201/1000','7/5']),
             ('import-hidden1399-cut','z_interval',['6/5','1399/1000']),('open-domain','intervals_closed',False),
             ('unsigned-root','root','w*w=R'),('weak-selected-rank','selected_Gram_rank','nonnegative'),
             ('point13-premise','additional_hypotheses',['point13']),('global-claim','global_Tammes15_bound_claimed',True),
             ('capacity-claim','capacity_claimed',True),('extra5-12-contact','original_contacts',s['original_contacts']+[[5,12]]),
             ('extra1-7-contact','original_contacts',s['original_contacts']+[[1,7]]),('incomplete255','remaining_regular_triples',s['remaining_regular_triples'][:-1]),
             ('return-excluded-case','remaining_regular_triples',sorted(s['remaining_regular_triples']+[[0,6,7]])),
             ('wrong-pure-target','new_excluded_triples',[[0,5,6],*s['new_excluded_triples'][1:]])]
    for name,key,value in changes:
        bad=deepcopy(s);bad[key]=value
        for reverse in (False,True):scope_controls.append(rejected(lambda bad=bad,reverse=reverse:validate(bad,pbytes,reverse),name+('-reverse' if reverse else '-forward')))
    bad=deepcopy(s);bad['square_integer_multipliers']['excess579_square']=-4
    scope_controls.append(rejected(lambda:validate(bad,pbytes),'negative-square-multiplier'))
    altered_parent=json.loads(pbytes);altered_parent['schema_version']=2
    altered=(json.dumps(altered_parent,separators=(',',':'))+'\n').encode()
    require(altered!=pbytes,'actual parent damage fixture')
    scope_controls.append(rejected(lambda:validate(s,altered),'actual-unpinned-parent'))
    polynomial_controls=[]
    for name in sorted(d['rows']):
        bad=deepcopy(d);bad['rows'][name][0][3]=str(-int(bad['rows'][name][0][3]))
        for label,check in [('primary',primary),('alternate',alternate)]:
            polynomial_controls.append(rejected(lambda bad=bad,check=check:check(s,bad,pbytes),'actual-coefficient-'+name+'-'+label))
    box=tuple(map(Q,s['t_interval']+s['z_interval']));boundary=[]
    for label,p in [('zero-at-t-lower',25*P.var(0)-14),('zero-at-t-upper',593-1000*P.var(0)),('zero-at-z-lower',5*P.var(1)-6),('zero-at-z-upper',7-5*P.var(1))]:
        vals=[v for row in bernstein(p,box) for v in row]
        require(min(vals)==0 and not all(v>0 for v in vals),'closed Bernstein zero sign control')
        rows=[(i,j,k,v) for (i,j,k),v in p.c.items()]
        boundary.append(rejected(lambda rows=rows:taylor(rows,0,box),label+'-Taylor'))
    positive=[signed(*x) for x in [(Q(-2),Q(1),Q(9),Q(3)),(Q(2),Q(1),Q(9),Q(3)),(Q(2),Q(1),Q(1),Q(1))]]
    roots=[rejected(lambda:signed(Q(-2),Q(1),Q(9),Q(-3)),'negative-root'),rejected(lambda:signed(Q(0),Q(1),Q(0),Q(0)),'zero-root'),rejected(lambda:signed(Q(-3),Q(1),Q(9),Q(3)),'zero-square-excess')]
    require(len(scope_controls)==30 and len(polynomial_controls)==12,'all semantic and actual coefficient damages')
    return {'actual_agent':'six-tammes-2','role':'researcher','status':'COMPLETE_COMPONENT_EXCLUSION_CONTROLS','rejected_scope_and_parent_inputs':scope_controls,
            'rejected_actual_polynomial_inputs_both_algorithms':polynomial_controls,'closed_zero_sign_controls':boundary,
            'valid_signed_root_controls':positive,'rejected_root_and_zero_square_controls':roots,'exact_credited_positive_core':exact_core(),
            'same_author_controls':True,'independent_review':False,'new_packing_bound':False}
if __name__=='__main__':
    signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('fixed20s controls guard')));signal.alarm(20)
    parser=argparse.ArgumentParser();parser.add_argument('--emit');args=parser.parse_args()
    out=produce(json.loads((HERE/'SYSTEM.json').read_text()),json.loads((HERE/'FACTORS.json').read_text()),(HERE/'PARENT_SYSTEM.json').read_bytes())
    data=(json.dumps(out,separators=(',',':'))+'\n').encode()
    if args.emit:Path(args.emit).write_bytes(data)
    else:require(out==json.loads((HERE/'CONTROLS.json').read_text()),'entire controls expected artifact')
    print(json.dumps({'status':out['status'],'scope_damages':30,'polynomial_damages':12,'closed_zero_controls':4,'exact_excluded_vertices':5,'whole_controls_sha256':hashlib.sha256(data).hexdigest()},indent=2))
