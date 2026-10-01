"""Exact finite hypotheses for a conditional nonlocal J74 motion exclusion.

Python3.11+, standard library. Written continuum proof is in PROOF.md.
No numerical solver or author discovery program is a checker dependency.
"""
from pathlib import Path
from fractions import Fraction as F
import copy,hashlib,itertools,json,math,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from q5 import Q,add,sub,scale,dot,cross
from model import VERTICES as V

def require(ok,message):
    if not ok:raise ValueError(message)

def field(x):return Q(F(x[0]),F(x[1]))
def vector(xs):return tuple(field(x) for x in xs)
def encoded(x):return [str(x.a),str(x.b)]
def absolute(x):return x if x>=0 else -x

def addpoly(a,b):
    out=[Q()]*max(len(a),len(b))
    for i,x in enumerate(a):out[i]+=x
    for i,x in enumerate(b):out[i]+=x
    return out

def multiply(a,b):
    out=[Q()]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return out

def determinant(matrix):
    size=len(matrix);out=[Q()]*(size+1)
    for perm in itertools.permutations(range(size)):
        sign=(-1)**sum(perm[i]>perm[j] for i in range(size) for j in range(i+1,size))
        term=[Q(sign)]
        for i,j in enumerate(perm):term=multiply(term,matrix[i][j])
        out=addpoly(out,term)
    return out

def bernstein(power):
    degree=len(power)-1
    return [sum((power[j]*F(math.comb(k,j),math.comb(degree,j)) for j in range(k+1)),Q()) for k in range(degree+1)]

def evaluate(cert):
    ray=cert['receiving_ray'];m,d=vector(ray['m']),vector(ray['d'])
    phi=Q(1,1)/2
    require(m==scale(1/(2*phi),(Q(1),-phi,-phi*phi)),'literal minimum axis')
    require(d==(Q(-5,3)/8,Q(11,-3)/8,Q(-1)/4),'literal physical tangent')
    require(dot(m,m)==1 and dot(m,d)==0,'unit base and tangent')
    require(ray['parameter_midpoint']=='13/20' and ray['parameter_radius']=='1/20'
            and ray['closed_parameter_interval']==['3/5','7/10'],'literal closed arc')
    midpoint,radius=Q(F(13,20)),Q(F(1,20))
    endpoints=[add(m,scale(midpoint+s*radius,d)) for s in (-1,1)]
    require(len(V)==len(set(V))==60,'all60 originals')
    require(all(dot(v,v)==Q(11,4)/4 for v in V),'original circumradius')
    cycle=cert['receiver_cycle'];require(len(cycle)==len(set(cycle))==18,'complete18-corner certificate')
    require(all(isinstance(i,int) and 0<=i<60 for i in cycle),'original indices')
    edges=list(zip(cycle,cycle[1:]+cycle[:1]));support_checks=corner_checks=0;minimum_support=None
    for u in endpoints:
        require(dot(u,u)<Q(F(81,64)) and u[2]<0,'normal norm and nonzero translation chart throughout arc')
        for a,b in edges:
            delta=sub(V[b],V[a]);require(dot(delta,delta)==1,'actual unit edges')
            normal=cross(delta,u);h=dot(normal,V[a]);require(h>0,'physical original outward support')
            minimum_support=h if minimum_support is None else min(minimum_support,h)
            require(dot(normal,u)==0,'physical projected normal')
            for i,v in enumerate(V):
                gap=dot(normal,sub(V[a],v));require(gap>=0,'all-original receiver support')
                support_checks+=1
                if i in cycle and i not in (a,b):
                    require(gap>0,'strict complete polygon boundary');corner_checks+=1
    contacts=cert['contact_rows'];require(len(contacts)==36,'36 selected actual contacts')
    require(set(map(tuple,contacts))=={(a,b,k) for a,b in edges for k in (a,b)},'exact endpoint contacts')
    alpha=[field(x) for x in cert['alpha']];gamma=[field(x) for x in cert['gamma']]
    require(len(alpha)==len(gamma)==36,'weight dimensions')
    require(sum(alpha,Q())==1 and sum(gamma,Q())==0,'stress normalization')
    lower=min(a+s*g for a,g in zip(alpha,gamma) for s in (-1,1));require(lower>Q(F(1,50)),'uniform positive stress')
    A0=[];A1=[]
    for a,b,k in contacts:
        delta=sub(V[b],V[a]);a0=cross(delta,add(m,scale(midpoint,d)));a1=cross(delta,scale(radius,d))
        require(dot(a0,sub(V[a],V[k]))==dot(a1,sub(V[a],V[k]))==0,'literal original contact identities')
        A0.append(tuple(cross(V[k],a0))+a0[:2]);A1.append(tuple(cross(V[k],a1))+a1[:2])
    coefficients=[]
    for j in range(5):
        coeff=[sum((alpha[i]*A0[i][j] for i in range(36)),Q()),
               sum((alpha[i]*A1[i][j]+gamma[i]*A0[i][j] for i in range(36)),Q()),
               sum((gamma[i]*A1[i][j] for i in range(36)),Q())]
        require(coeff==[Q()]*3,'exact balanced force/torque polynomial');coefficients+=coeff
    selected=cert['minor_contact_rows'];require(len(selected)==len(set(selected))==5 and all(0<=i<36 for i in selected),'five independent selected rows')
    B=[[[A0[i][j]-A1[i][j],2*A1[i][j]] for j in range(5)] for i in selected]
    power=determinant(B);db=bernstein(power)
    sign=1 if sum((c*Q(F(1,2)**j) for j,c in enumerate(power)),Q())>0 else -1
    D=min(sign*c for c in db);require(D>0,'uniform nonsingular minor by Bernstein coefficients')
    cofactor=[]
    for i in range(5):
        row=[]
        for j in range(5):
            minor=[[B[a][b] for b in range(5) if b!=j] for a in range(5) if a!=i]
            row.append(max(absolute(x) for x in bernstein(determinant(minor))))
        cofactor.append(row)
    inverse_rows=[sum((cofactor[j][i] for j in range(5)),Q())/D for i in range(5)]
    J=cert['inverse_infinity_bound'];require(isinstance(J,int) and J==6 and all(q<=J for q in inverse_rows),'uniform inverse infinity bound6')
    kappa=F(cert['relative_cayley_radius']);require(kappa>0,'positive Cayley radius')
    contraction=3*J*50*F(81,32)*kappa
    require(contraction<1,'nonlinear Cayley contraction gate')
    require(kappa==F(1,6000),'literal theorem radius')
    # The four centers use actual full-body symmetries, never a silhouette-only symmetry.
    diagonals=cert['known_body_symmetry_diagonals']
    require(diagonals==[[1,1,1],[-1,-1,1],[-1,1,1],[1,-1,1]],'literal four symmetry matrices')
    symmetry_matches=source_checks=shared_corners=0
    for diagonal in diagonals:
        transformed=[tuple(Q(s)*x for s,x in zip(diagonal,v)) for v in V]
        require(set(transformed)==set(V),'actual full-body symmetry')
        symmetry_matches+=60;shared_corners+=18
        for u in endpoints:
            for a,b in edges:
                normal=cross(sub(V[b],V[a]),u);h=dot(normal,V[a])
                for p in transformed:require(dot(normal,p)<=h,'all-original reference source support');source_checks+=1
    # Receiving arc is separated from every projective minimum by chord>1/3.
    axes=[(Q(1),Q(),Q()),(Q(),Q(1),Q())]+[scale(1/(2*phi),(Q(1),e*phi,s*phi*phi)) for e,s in ((-1,-1),(-1,1),(1,-1),(1,1))]
    U0,U1=endpoints[0],sub(endpoints[1],endpoints[0]);separations=[]
    for axis in axes:
        require(dot(axis,axis)==1,'unit catalogue minimum')
        normpoly=[dot(U0,U0),2*dot(U0,U1),dot(U1,U1)]
        a,b=dot(axis,U0),dot(axis,U1)
        polynomial=[Q(F(17,18)**2)*c-q for c,q in zip(normpoly,(a*a,2*a*b,b*b))]
        lower_sep=min(bernstein(polynomial));require(lower_sep>0,'entire closed arc is nonlocal to all minima');separations.append(encoded(lower_sep))
    return {'agent':'six-rupert-2','role':'researcher','finite_hypotheses':'PASS; continuum argument in PROOF.md, unformalized',
      'closed_receiving_parameter_interval':['3/5','7/10'],'minimum_projective_chord_separation':'>1/3',
      'receiver_corners':18,'contact_rows':36,'receiver_all_original_comparisons':support_checks,
      'strict_receiver_corner_comparisons':corner_checks,'reference_source_original_comparisons':source_checks,
      'full_body_symmetry_vertex_matches':symmetry_matches,'literal_reference_corner_matches':shared_corners,
      'positive_weight_lower':'>1/50','actual_minimum_endpoint_weight':encoded(lower),
      'balanced_polynomial_coefficients':len(coefficients),'selected_minor_rows':selected,
      'determinant_bernstein_coefficients':[encoded(x) for x in db],'absolute_minor_lower':encoded(D),
      'inverse_infinity_upper':J,'relative_cayley_radius':str(kappa),'nonlinear_contraction':str(contraction),
      'four_reference_families':['I','diag(-1,-1,1)','M_u diag(-1,1,1)','M_u diag(1,-1,1)'],
      'minimum_separation_polynomial_bounds':separations}

def damaged_controls(cert):
    controls=[]
    for name in ('wrong_stress','cropped_receiver','repeated_minor','unsafe_motion_radius'):
        bad=copy.deepcopy(cert)
        if name=='wrong_stress':
            bad['alpha'][0][0]=str(F(bad['alpha'][0][0])+F(1,100000))
            bad['alpha'][1][0]=str(F(bad['alpha'][1][0])-F(1,100000))
        elif name=='cropped_receiver':bad['receiver_cycle'][bad['receiver_cycle'].index(23)]=58
        elif name=='repeated_minor':bad['minor_contact_rows'][0]=bad['minor_contact_rows'][1]
        else:bad['relative_cayley_radius']='1/500'
        try:evaluate(bad)
        except (ValueError,IndexError,KeyError,ZeroDivisionError) as error:controls.append({'control':name,'rejected':True,'reason':str(error)})
        else:raise ValueError('unsafe control accepted:'+name)
    return controls

def main():
    dependencies=json.loads((HERE/'DEPENDENCIES.json').read_text())
    for name,expected in dependencies['pinned_input_sha256'].items():
        require(hashlib.sha256((HERE.parent/name).read_bytes()).hexdigest()==expected,'pinned named-solid input:'+name)
    raw=(HERE/'certificate.json').read_bytes();cert=json.loads(raw);result=evaluate(cert)
    result['certificate_sha256']=hashlib.sha256(raw).hexdigest();result['negative_controls']=damaged_controls(cert)
    if '--write-expected' in sys.argv:(HERE/'expected.json').write_text(json.dumps(result,indent=2)+'\n')
    else:require(result==json.loads((HERE/'expected.json').read_text()),'complete expected entrywise record')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
