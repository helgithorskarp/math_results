"""Exact finite hypotheses for a two-dimensional conditional J74 patch.

Python3.11+ standard library; the real-parameter proof is in PROOF.md.
The four exact stress corrections are consistency checks, not a sampled
substitute for the uniform Neumann and weight-repair estimates.
"""
from pathlib import Path
from fractions import Fraction as F
import copy,hashlib,json,sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from q5 import Q,add,sub,scale,dot,cross
from model import VERTICES as V
from nonlocal_arc_wrench import check as parent

def require(ok,message):
    if not ok:raise ValueError(message)

def exact_solve(matrix,rhs):
    n=len(rhs);a=[list(row)+[b] for row,b in zip(matrix,rhs)]
    for j in range(n):
        p=next((i for i in range(j,n) if a[i][j]!=0),None)
        require(p is not None,'exact stress-repair matrix is nonsingular')
        a[j],a[p]=a[p],a[j];pivot=a[j][j];a[j]=[x/pivot for x in a[j]]
        for i in range(n):
            if i!=j:
                v=a[i][j];a[i]=[x-v*y for x,y in zip(a[i],a[j])]
    result=[row[-1] for row in a]
    require(all(sum((x*y for x,y in zip(row,result)),Q())==b for row,b in zip(matrix,rhs)),
            'entrywise exact stress-repair equations')
    return result

def replay_parent(dependencies):
    for name,expected in dependencies['pinned_input_sha256'].items():
        observed=hashlib.sha256((HERE.parent/name).read_bytes()).hexdigest()
        require(observed==expected,'pinned input '+name+': expected '+expected+', observed '+observed)
    raw=(HERE.parent/'nonlocal_arc_wrench/certificate.json').read_bytes()
    cert=json.loads(raw);record=parent.evaluate(cert)
    record['certificate_sha256']=hashlib.sha256(raw).hexdigest()
    record['negative_controls']=parent.damaged_controls(cert)
    frozen=json.loads((HERE.parent/'nonlocal_arc_wrench/expected.json').read_text())
    require(record==frozen,'complete published parent finite record')
    return cert,record

def evaluate(cert,old):
    m,d,e=[parent.vector(cert[k]) for k in ('m','d','transverse_vector')]
    require(m==parent.vector(old['receiving_ray']['m']) and d==parent.vector(old['receiving_ray']['d']),
            'same literal parent receiving arc')
    require(dot(m,m)==1 and dot(m,d)==0 and dot(d,d)>0,'unit base and nonzero tangent')
    require(e==cross(m,d) and dot(e,m)==dot(e,d)==0 and Q()<dot(e,e)<1,
            'independent orthogonal transverse vector of norm less than one')
    lo,hi=Q(F(cert['t_interval'][0])),Q(F(cert['t_interval'][1]))
    require((lo,hi)==(Q(F(3,5)),Q(F(7,10))),'parent closed parameter interval')
    eps=Q(F(cert['transverse_radius']));require(eps>0,'positive transverse radius')
    J=cert['inverse_infinity_bound'];weight_denominator=cert['positive_weight_denominator']
    require(J==12 and isinstance(J,int),'literal inverse bound12')
    require(isinstance(weight_denominator,int) and weight_denominator>0,'positive weight denominator')
    # A row has three torque entries bounded by R<9/4 and two force
    # entries bounded by one when its normal uses the unit-length edge and e.
    row_l1=Q(9);require(row_l1>3*Q(F(9,4))+2,'physical perturbation row bound')
    neumann=6*row_l1*eps
    require(neumann<Q(F(1,2)) and (1-neumann)*J>=6,'uniform Neumann inverse budget')
    residual_bound=Q(F(9,4));repair=5*J*residual_bound*eps
    require(repair==135*eps,'five corrected-weight entry budget')
    normalized_lower=(Q(F(1,50))-repair)/(1+5*repair)
    require(normalized_lower>Q(F(1,weight_denominator)),'strict normalized positive-weight budget')
    span=3*J*weight_denominator
    radius=F(cert['relative_cayley_radius'])
    contraction=span*F(81,32)*radius
    require(radius>0 and contraction<1,'exact nonlinear Cayley contraction')
    # Require the advertised values only after testing their mathematical gates.
    require(eps==Q(F(1,50000)) and weight_denominator==60 and radius==F(1,14400),
            'literal theorem constants')

    cycle=cert['receiver_cycle']
    require(len(cycle)==len(set(cycle))==18 and all(isinstance(i,int) and 0<=i<60 for i in cycle),
            'complete18-corner candidate on actual original indices')
    require(len(V)==len(set(V))==60 and all(dot(v,v)==Q(11,4)/4 for v in V),
            'complete original60-vertex sphere')
    edges=list(zip(cycle,cycle[1:]+cycle[:1]))
    supports=[];gaps=[];corners=[];norms=[];zvalues=[]
    for t in (lo,hi):
        for s in (-eps,eps):
            u=add(add(m,scale(t,d)),scale(s,e));norms.append(dot(u,u));zvalues.append(u[2])
            require(dot(u,u)<Q(F(81,64)) and u[2]<0,'physical normal bound and translation chart')
            for a,b in edges:
                delta=sub(V[b],V[a]);require(dot(delta,delta)==1,'unit physical edge')
                normal=cross(delta,u);h=dot(normal,V[a]);supports.append(h)
                require(h>0 and dot(normal,u)==0,'positive outward physical support')
                for i,v in enumerate(V):
                    gap=dot(normal,sub(V[a],v));gaps.append(gap)
                    require(gap>=0,'all60 original receiving supports at every box corner')
                    if i not in (a,b):require(gap>0,'strict nonincident original support')
                    if i in cycle and i not in (a,b):corners.append(gap)
    require(cycle==old['receiver_cycle'],'literal full parent horizon preserved')

    # Norm convexity and affine signs extend the preceding gates over the
    # entire real rectangle.  Parent separation polynomials lose at most
    # (9/4)*eps+eps^2 under the orthogonal transverse perturbation.
    phi=Q(1,1)/2
    axes=[(Q(1),Q(),Q()),(Q(),Q(1),Q())]+[
        scale(1/(2*phi),(Q(1),a*phi,b*phi*phi)) for a,b in ((-1,-1),(-1,1),(1,-1),(1,1))]
    U0,U1=add(m,scale(lo,d)),scale(hi-lo,d)
    loss=Q(F(9,4))*eps+eps*eps;separations=[]
    for axis in axes:
        require(dot(axis,axis)==1,'unit minimum axis')
        norm=[dot(U0,U0),2*dot(U0,U1),dot(U1,U1)]
        a,b=dot(axis,U0),dot(axis,U1)
        power=[Q(F(17,18)**2)*x-y for x,y in zip(norm,(a*a,2*a*b,b*b))]
        lower=min(parent.bernstein(power));require(lower>loss,'entire patch separated from every projective minimum by chord>1/3')
        separations.append(lower-loss)

    matches=0
    for diagonal in ((1,1,1),(-1,-1,1),(-1,1,1),(1,-1,1)):
        transformed={tuple(Q(s)*x for s,x in zip(diagonal,v)) for v in V}
        require(transformed==set(V),'actual full-body symmetry, not prototype symmetry');matches+=60

    # Check the actual correction formula at four exact box corners, including
    # full spatial force.  Uniform existence and positivity use the estimates
    # above, never these four point evaluations.
    alpha=[parent.field(x) for x in old['alpha']];gamma=[parent.field(x) for x in old['gamma']]
    selected=old['minor_contact_rows'];contacts=old['contact_rows'];balance_checks=0
    for t in (lo,hi):
        for s in (-eps,eps):
            u=add(add(m,scale(t,d)),scale(s,e));z=20*t-13
            beta=[a+z*g for a,g in zip(alpha,gamma)]
            normals=[cross(sub(V[b],V[a]),u) for a,b,k in contacts]
            torques=[cross(V[k],a) for (i,j,k),a in zip(contacts,normals)]
            A=[list(torque)+list(a[:2]) for torque,a in zip(torques,normals)]
            residual=[sum((w*row[j] for w,row in zip(beta,A)),Q()) for j in range(5)]
            B=[A[i] for i in selected]
            correction=exact_solve(list(map(list,zip(*B))),[-r for r in residual])
            require(all(parent.absolute(x)<=repair for x in correction),'actual correction satisfies uniform entry bound')
            for i,x in zip(selected,correction):beta[i]+=x
            total=sum(beta,Q());require(total>0,'positive normalization after repair')
            beta=[x/total for x in beta]
            require(min(beta)>Q(F(1,60)) and sum(beta,Q())==1,'actual repaired normalized positive stress')
            for j in range(3):
                require(sum((w*a[j] for w,a in zip(beta,normals)),Q())==0,'actual full spatial force balance')
                require(sum((w*q[j] for w,q in zip(beta,torques)),Q())==0,'actual spatial torque balance')
                balance_checks+=2

    U=add(m,scale(Q(F(13,20)),d));example=add(U,scale(eps,e))
    cos2=dot(U,U)/dot(example,example);r=Q(F(cert['off_arc_chord_lower']))
    require(dot(example,e)==eps*dot(e,e)>0,'explicit noncoplanar off-arc receiver')
    require(r>0 and cos2<(1-r*r/2)*(1-r*r/2),'exact distance from the entire projective parent arc')
    require(r==Q(F(1,200000)),'literal off-arc distance comparison')
    return {'agent':'six-rupert-2','role':'researcher',
      'finite_hypotheses':'PASS; real-parameter Neumann/repair/Cayley proof in PROOF.md; unformalized',
      'receiving_domain':'u(t,s)=m+t*d+s*(m cross d),3/5<=t<=7/10,|s|<=1/50000; genuinely two-dimensional',
      'source_domain':'four conditional relative Cayley neighborhoods; not all sources',
      'relative_cayley_radius':str(radius),'receiver_corners':len(cycle),
      'receiving_box_corner_count':4,'all_original_receiving_support_comparisons':len(gaps),
      'strict_nonincident_original_comparisons':4*18*58,'strict_nonincident_corner_comparisons':len(corners),
      'minimum_physical_support':parent.encoded(min(supports)),
      'minimum_nonincident_corner_gap':parent.encoded(min(corners)),
      'maximum_corner_normal_norm_squared':parent.encoded(max(norms)),
      'maximum_corner_z_coordinate':parent.encoded(max(zvalues)),
      'transverse_norm_squared':parent.encoded(dot(e,e)),
      'uniform_neumann_product_upper':parent.encoded(neumann),'inverse_infinity_upper':J,
      'five_weight_correction_entry_upper':parent.encoded(repair),
      'normalized_stress_lower':parent.encoded(normalized_lower),
      'normalized_weights':'>1/60','weighted_span_coefficient':span,
      'nonlinear_contraction':str(contraction),
      'all_six_projective_minimum_separation':'>1/3',
      'separation_polynomial_lower_bounds_after_loss':[parent.encoded(x) for x in separations],
      'full_body_symmetry_vertex_matches':matches,
      'four_exact_point_stress_repair_consistency_checks':4,
      'exact_point_full_spatial_balance_checks':balance_checks,
      'off_arc_example_parameters':['13/20','1/50000'],
      'off_arc_example_squared_cosine':parent.encoded(cos2),
      'off_arc_example_chord_from_entire_parent_arc':'>1/200000'}

def damaged_controls(cert,old):
    results=[]
    for name in ('collapsed_transverse_direction','widened_patch','cropped_receiver','false_weight_lower','unsafe_motion_radius'):
        bad=copy.deepcopy(cert)
        if name=='collapsed_transverse_direction':bad['transverse_vector']=copy.deepcopy(bad['d'])
        elif name=='widened_patch':bad['transverse_radius']='1/1000'
        elif name=='cropped_receiver':bad['receiver_cycle'][bad['receiver_cycle'].index(23)]=58
        elif name=='false_weight_lower':bad['positive_weight_denominator']=50
        else:bad['relative_cayley_radius']='1/4000'
        try:evaluate(bad,old)
        except (ValueError,IndexError,KeyError,ZeroDivisionError) as error:
            results.append({'control':name,'rejected':True,'reason':str(error)})
        else:raise ValueError('unsafe control accepted: '+name)
    return results

def main():
    dependencies=json.loads((HERE/'DEPENDENCIES.json').read_text())
    old,old_record=replay_parent(dependencies)
    raw=(HERE/'certificate.json').read_bytes();cert=json.loads(raw)
    result=evaluate(cert,old)
    result['parent_full_record_replayed']=True
    result['parent_certificate_sha256']=old_record['certificate_sha256']
    result['parent_expected_sha256']=hashlib.sha256((HERE.parent/'nonlocal_arc_wrench/expected.json').read_bytes()).hexdigest()
    result['certificate_sha256']=hashlib.sha256(raw).hexdigest()
    result['negative_controls']=damaged_controls(cert,old)
    if '--write-expected' in sys.argv:(HERE/'expected.json').write_text(json.dumps(result,indent=2)+'\n')
    else:require(result==json.loads((HERE/'expected.json').read_text()),'complete frozen expected entrywise record')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
