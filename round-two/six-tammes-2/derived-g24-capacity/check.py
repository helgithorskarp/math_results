"""Replay the whole cap certificate using exact rational Bernstein signs.

The alternate audit uses rational centered Taylor enclosures instead.
Both share the stated coordinate/Cramer reduction and integer polynomial
kernel; they do not constitute independent mathematical peer review.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations
import argparse,hashlib,json,signal
from polynomials import P,dot
from model import LABELS,CONTACTS,NORMAL,CUT,make,positive_factors
from algebra import LO,HI,require,primitive,row_planes,vertex,cramer,parameter_box
from schema import system,validate
from signs import rational_bernstein,taylor_positive

HERE=Path(__file__).resolve().parent
FROZEN=('SYSTEM.json','polynomials.py','model.py','algebra.py','signs.py',
        'schema.py','generate.py','check.py','audit.py','controls.py')

def pins():
    data=json.loads((HERE/'RUNTIME_PINS.json').read_text());require(set(data)==set(FROZEN),'complete ten-file runtime pins')
    for name in FROZEN:require(hashlib.sha256((HERE/name).read_bytes()).hexdigest()==data[name],name+' runtime source pin')
    require(json.loads((HERE/'SYSTEM.json').read_text())==system(),'literal source system agreement')
    return data

def identities():
    t=P.var(0);Y,O,m=make(t);a=1+t;names=[]
    def zero(name,p):
        require(not p.c,'nonzero generic identity '+name);names.append(name)
    for i in LABELS:zero('unit-'+str(i),dot(Y[i],Y[i],t)-O*O)
    for i,j in CONTACTS:zero('contact-'+str(i)+'-'+str(j),dot(Y[i],Y[j],t)-t*O*O)
    reflections=((8,2,4,1),(10,1,2,4),(12,1,10,2),(13,2,10,1),
                 (9,10,13,2),(0,5,7,12),(11,0,5,7),(6,0,11,5))
    for n,i,j,o in reflections:
        for k in range(3):zero('reflection-'+str(n)+'-'+str(k),a*(Y[n][k]+Y[o][k])-2*t*(Y[i][k]+Y[j][k]))
    dnum=dot(Y[9],Y[12],t)
    for k in range(3):
        zero('generalized-reflection-5-'+str(k),(O*O+dnum)*(Y[5][k]+Y[10][k])-2*t*O*O*(Y[9][k]+Y[12][k]))
        zero('A-chain-7-'+str(k),a**3*Y[9][k]-4*t*t*(a+2*t)*Y[5][k]-a*(a*a-4*t*t)*Y[12][k]+4*t*m['L']*Y[7][k])
    zero('noncontact-9-12-formula',a**3*dnum-(2*m['Q4']-a**3)*O*O)
    n=[t*0+x for x in NORMAL];zero('cap-normal-squared',dot(n,n,t)-(621-620*t))
    require(len(names)==69,'complete generic identity census')
    return {'generic_unit_identities':13,'literal_contact_identities':24,
            'reflection_scalar_identities':30,'other_scalar_identities':2,
            'all_generic_identities_actually_checked':69,'names':names}

def scalar_bounds():
    require(0<LO<HI<1 and 3*LO-1>0,'strictly positive known factors on closed band')
    low,high=621-620*HI,621-620*LO
    require(low==Q(12667,50) and high==Q(1369,5) and low>CUT*CUT,'nonempty proper cap threshold throughout band')
    pair=2*CUT*CUT/high-1
    require(pair==Q(881,1369)>HI,'uniform one-cap packing capacity1')
    return {'normal_squared_closed_bounds':[str(low),str(high)],
            'open_cap_pair_product_strict_lower':str(pair),'maximum_code_parameter':str(HI),
            'cap_at_most_one_code_point':True,'short_vertex_squared_bound':'49/50',
            'positive_denominators':'(1+t)^5 Q4 L, Q4=(1-t^2)(1+3t)+8t^4>0, L=1+t(2-t)>0'}

def obligations(c):
    t=P.var(0);known=positive_factors(t);planes,Y,O=row_planes(t)
    labels=(0,4,9,11);M=[[Y[labels[j]][i] for j in range(3)] for i in range(3)]
    D,C=cramer(M,[-x for x in Y[11]],t);sgn=c['boundedness_determinant_sign']
    require(bool(D.c) and len(C)==3,'spanning boundedness normals')
    for j,p in enumerate([D]+C):yield 'positive-dependence-'+str(j),primitive(sgn*p,known),LO,HI
    for record in c['records']:
        inds=tuple(record['triple']);D,W=vertex(planes,inds,t)
        if record['type']=='S':require(not D.c,'singular triple is not identically singular');continue
        require(bool(D.c),'covered triple cannot be identically singular')
        N=primitive(49*D*D-50*dot(W,W,t),known);H={}
        for leaf in record['leaves']:
            a,b=parameter_box(leaf['path']);name='-'.join(map(str,inds))+':'+''.join(map(str,leaf['path']))
            if leaf['type']=='N':yield name+':short',N,a,b
            else:
                for role,sign in (('positive_residual',1),('negative_residual',-1)):
                    j=leaf[role]
                    if j not in H:
                        row,rhs=planes[j]
                        H[j]=primitive(sum((x*y for x,y in zip(row,W)),t*0)-rhs*D,known)
                    yield name+':'+role+':'+str(j),sign*H[j],a,b

def positive_control():
    """A feasible thirteen-core and one radial addition at t=29/50."""
    t=Q(29,50);Y,O,_=make(t);Pnt={i:[x/O for x in row] for i,row in Y.items()}
    require(all(dot(x,x,t)==1 for x in Pnt.values()),'rational control13 unit norms')
    allpairs=list(combinations(LABELS,2));require(all(dot(Pnt[i],Pnt[j],t)<=t for i,j in allpairs),'all78 rational control packing pairs')
    pts=(0,4,6);rows=[[(1-t)*x+t*sum(Pnt[i],Q()) for x in Pnt[i]] for i in pts]
    # Definition-level rational Cramer, rather than a symbolic specialization.
    def det(M):
        return M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])-M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])+M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0])
    D=det(rows);require(D!=0,'control active-plane independence')
    v=[det([[t if j==k else rows[i][j] for j in range(3)] for i in range(3)])/D for k in range(3)]
    require(all(dot(v,x,t)<=t for x in Pnt.values()),'all13 control avoidance inequalities')
    norm=dot(v,v,t);require(norm>1,'radial projection provides an actual unit addition')
    # Scaling v by1/sqrt(norm)<1 preserves every inequality with positive RHS.
    return {'t':str(t),'prefix_unit_points':13,'prefix_packing_pairs':78,
            'radial_vertex_active_labels':list(pts),'radial_vertex_squared_norm':str(norm),
            'radial_vertex_avoidance_tests':13,'one_unit_addition_exists':True,
            'known_record_bound_or_new_fifteen_configuration_claimed':False}

def run(c,method='bernstein'):
    validate(c);source=pins();generic=identities();bounds=scalar_bounds();control=positive_control()
    checks=0;maximum=0;taylor_cells=0;taylor_depth=0;digest=hashlib.sha256()
    for name,p,a,b in obligations(c):
        checks+=1;maximum=max(maximum,max((k[0] for k in p.c),default=0));digest.update((name+'\n').encode())
        if method=='bernstein':require(min(rational_bernstein(p,a,b))>0,'nonpositive full-cell Bernstein obligation '+name)
        elif method=='taylor':
            cells,depth=taylor_positive(p,a,b);taylor_cells+=cells;taylor_depth=max(taylor_depth,depth)
        else:raise ValueError('explicit exact positivity method')
    require(checks==706,'all4 boundedness and702 cap sign obligations')
    leafs=[l for r in c['records'] for l in r.get('leaves',[])]
    return {'format':'derived-g24-cap-replay-v1','actual_agent':'six-tammes-2','role':'researcher',
            'claim':'13-label derived G24 has at most one arbitrary additional code point on closed I; no15-code',
            'method':method,'source_pins':source,'generic_identities':generic,'scalar_bounds':bounds,
            'positive_control':control,'triples_actually_checked':len(c['records']),
            'identically_singular_triples':sum(r['type']=='S' for r in c['records']),
            'complete_parameter_cover_leaves':len(leafs),'short_leaves':sum(l['type']=='N' for l in leafs),
            'opposite_residual_leaves':sum(l['type']=='I2' for l in leafs),
            'all_strict_sign_obligations_actually_checked':checks,'maximum_deflated_sign_degree':maximum,
            'ordered_obligation_names_sha256':digest.hexdigest(),'Taylor_subcells_actually_enclosed':taylor_cells,
            'Taylor_max_extra_depth':taylor_depth,'no_unresolved_cases':True,
            'formalized':False,'independent_mathematical_review':'pending'}

def main():
    signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('50-second exact replay guard')));signal.alarm(50)
    p=argparse.ArgumentParser();p.add_argument('--certificate',type=Path,default=HERE/'CERTIFICATE.json');p.add_argument('--output',type=Path);args=p.parse_args()
    out=run(json.loads(args.certificate.read_text()));raw=json.dumps(out,sort_keys=True,indent=2)+'\n'
    if args.output:args.output.write_text(raw)
    print(raw,end='')
if __name__=='__main__':main()
